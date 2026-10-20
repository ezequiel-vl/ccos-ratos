import React, {useEffect, useState} from 'react';
import {
  continueRender, delayRender, Easing, Img, interpolate, interpolateColors, staticFile, useCurrentFrame,
} from 'remotion';
import {CSS, FONTES_URL, TOKENS} from './estilo';

export const FPS = 30;
/** milissegundos -> quadros (os atrasos foram pensados em ms, como no HTML) */
export const q = (ms: number) => Math.round((ms * FPS) / 1000);
const EASE = Easing.bezier(0.16, 1, 0.3, 1);

/** progresso 0..1 de uma entrada que começa em `ms` e dura `dur` quadros, com o easing da casa */
export const useP = (ms: number, dur = 30) => {
  const f = useCurrentFrame();
  return interpolate(f, [q(ms), q(ms) + dur], [0, 1], {easing: EASE, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
};

type Base = {d: number; className?: string; style?: React.CSSProperties; children?: React.ReactNode};

/** entra com fade e 22px de deslocamento */
export const In: React.FC<Base & {as?: keyof React.JSX.IntrinsicElements; y?: number}> = ({d, as = 'div', className, style, children, y = 22}) => {
  const p = useP(d);
  const T = as as any;
  return <T className={className} style={{...style, opacity: p, transform: `translateY(${(1 - p) * y}px)`}}>{children}</T>;
};

export const Fade: React.FC<Base> = ({d, className, style, children}) => {
  const p = useP(d, 27);
  return <div className={className} style={{...style, opacity: p}}>{children}</div>;
};

/** título que surge palavra por palavra, com desfoque saindo; `pt` põe o ponto azul no fim */
export const Palavras: React.FC<{texto: string; d: number; passo: number; pt?: boolean; depois?: string; className?: string; style?: React.CSSProperties; as?: keyof React.JSX.IntrinsicElements}> = ({texto, d, passo, pt, depois, className, style, as = 'p'}) => {
  const f = useCurrentFrame();
  const palavras = texto.split(' ');
  const w = (i: number) => {
    const p = interpolate(f, [q(d + i * passo), q(d + i * passo) + 27], [0, 1], {easing: EASE, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return {opacity: p, transform: `translateY(${(1 - p) * 0.35}em)`, filter: `blur(${(1 - p) * 6}px)`};
  };
  const T = as as any;
  return (
    <T className={className} style={style}>
      {palavras.map((p, i) => (
        <React.Fragment key={i}>
          <span className="w" style={w(i)}>{p}</span>
          {i < palavras.length - 1 ? ' ' : null}
        </React.Fragment>
      ))}
      {pt ? <span className="w pt" style={w(palavras.length)}>.</span> : null}
      {depois ? <span className="w" style={w(palavras.length + 1)}>{depois}</span> : null}
    </T>
  );
};

/** texto digitado letra por letra, com cursor piscando */
export const Digita: React.FC<{texto: string; d: number; passo: number}> = ({texto, d, passo}) => {
  const f = useCurrentFrame();
  const n = Math.max(0, Math.min(texto.length, Math.floor((f - q(d)) / ((passo * FPS) / 1000)) + 1));
  const visivel = f >= q(d) ? texto.slice(0, n) : '';
  const cursor = Math.floor(f / 15) % 2 === 0;
  return (
    <span>
      {visivel}
      <i style={{display: 'inline-block', width: 3, height: '1.05em', background: TOKENS.ink, verticalAlign: '-.15em', marginLeft: 3, opacity: cursor ? 1 : 0}} />
    </span>
  );
};

/** risco que atravessa o texto (várias linhas) e apaga a cor */
export const Riscado: React.FC<{d: number; children: React.ReactNode}> = ({d, children}) => {
  const p = useP(d, 24);
  return (
    <span style={{
      backgroundImage: `linear-gradient(${TOKENS.mute}, ${TOKENS.mute})`, backgroundRepeat: 'no-repeat',
      backgroundPosition: '0 58%', backgroundSize: `${p * 100}% 3px`, WebkitBoxDecorationBreak: 'clone', boxDecorationBreak: 'clone',
      color: interpolateColors(p, [0, 1], [TOKENS.ink, TOKENS.faint]),
    }}>{children}</span>
  );
};

/** hairline que se desenha da esquerda pra direita */
export const Risca: React.FC<{d: number; style?: React.CSSProperties}> = ({d, style}) => {
  const p = useP(d, 24);
  return <div className="linha" style={{...style, transform: `scaleX(${p})`}} />;
};

/** ponto que acende (cinza = marcador; azul = sinal, só no ponto) com halo pulsando depois */
export const Acende: React.FC<{d: number; size: number; cor?: 'dot' | 'sinal'; halo?: boolean; style?: React.CSSProperties}> = ({d, size, cor = 'dot', halo, style}) => {
  const f = useCurrentFrame();
  const p = useP(d, 18);
  const c = cor === 'sinal' ? TOKENS.sinal : TOKENS.dot;
  const rgb = cor === 'sinal' ? '72,160,199' : '166,166,166';
  const t = f - q(d) - 18;
  const h = halo && t > 0 ? (t % 72) / 72 : -1;
  const sombra = h >= 0 && h <= 0.7 ? `0 0 0 ${(h / 0.7) * 14}px rgba(${rgb},${0.45 * (1 - h / 0.7)})` : 'none';
  return (
    <i style={{
      ...style, display: 'block', width: size, height: size, borderRadius: '50%', flex: 'none',
      background: interpolateColors(p, [0, 1], ['rgba(0,0,0,0)', c]),
      border: `1.5px solid ${interpolateColors(p, [0, 1], [TOKENS.dotOff, c])}`,
      transform: `scale(${0.6 + 0.4 * p})`, boxShadow: sombra,
    }} />
  );
};

/** posição da lanterna indo e voltando devagar (7s cada sentido) */
export const useLanterna = () => {
  const f = useCurrentFrame();
  const t = (f % 420) / 420;
  const ida = t < 0.5 ? t * 2 : 2 - t * 2;
  const e = EASE(ida);
  return {lx: 12 + 76 * e, ly: 10 + 60 * e};
};

export const Luz: React.FC<{sobre?: boolean}> = ({sobre}) => {
  const {lx, ly} = useLanterna();
  return (
    <div style={{
      position: 'absolute', inset: 0, zIndex: sobre ? 5 : -1, borderRadius: 'inherit', pointerEvents: 'none',
      background: `radial-gradient(520px circle at ${lx}% ${ly}%, rgba(220,220,220,.10), transparent 60%)`,
    }} />
  );
};

const GRAO = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E")`;
const SALTOS = [[0, 0], [-37, 21], [19, -44], [-12, -9], [28, 33]];

/** grão de filme: troca de posição 8 vezes por segundo */
export const Grao: React.FC<{opacidade?: number; porSegundo?: number}> = ({opacidade = 0.15, porSegundo = 8}) => {
  const f = useCurrentFrame();
  const [x, y] = SALTOS[Math.floor(f / (FPS / porSegundo)) % SALTOS.length];
  return <div style={{position: 'absolute', inset: -140, zIndex: 25, pointerEvents: 'none', opacity: opacidade, backgroundImage: GRAO, backgroundSize: '140px 140px', transform: `translate(${x}px, ${y}px)`}} />;
};

/** segura o render até as fontes do Google carregarem */
export const useFontes = () => {
  const [h] = useState(() => delayRender('fontes'));
  useEffect(() => {
    let link = document.querySelector<HTMLLinkElement>('link[data-eze-fontes]');
    const pronto = () =>
      Promise.all([
        document.fonts.load('700 168px "Archivo"'), document.fonts.load('600 64px "Archivo"'),
        document.fonts.load('400 34px "Inter Tight"'), document.fonts.load('500 44px "Inter Tight"'),
        document.fonts.load('500 21px "JetBrains Mono"'), document.fonts.load('400 22px "JetBrains Mono"'),
      ]).then(() => document.fonts.ready).then(() => continueRender(h));
    if (!link) {
      link = document.createElement('link');
      link.rel = 'stylesheet'; link.href = FONTES_URL; link.dataset.ezeFontes = '1';
      link.onload = () => { pronto(); };
      document.head.appendChild(link);
    } else {
      pronto();
    }
  }, [h]);
};

export const SETA = <svg viewBox="0 0 16 16"><path d="M3 8h10M9 4l4 4-4 4" /></svg>;

/** moldura de todo slide: fundo, grão, logo, @ e pontinhos de progresso */
export const Slide: React.FC<{n: number; total: number; capa?: boolean; children: React.ReactNode; extra?: React.ReactNode; mioloStyle?: React.CSSProperties}> = ({n, total, capa, children, extra, mioloStyle}) => {
  useFontes();
  return (
    <div className="eze" style={{position: 'absolute', inset: 0}}>
      <style>{CSS}</style>
      <div className="slide">
        <div className="topo">
          <Fade d={0}><Img src={staticFile('logo-branco.png')} style={{height: 36}} /></Fade>
          {capa ? <Fade d={100} className="handle">@agenciaezeos</Fade> : null}
        </div>
        <div className="miolo" style={mioloStyle}>{children}</div>
        {capa ? null : (
          <div className="base">
            <Fade d={100} className="handle">@agenciaezeos</Fade>
            <Fade d={100} className="prog">{Array.from({length: total}, (_, i) => <i key={i} className={i + 1 === n ? 'on' : ''} />)}</Fade>
          </div>
        )}
        {extra}
        <Grao />
      </div>
    </div>
  );
};
