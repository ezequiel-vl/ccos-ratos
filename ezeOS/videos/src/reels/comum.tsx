import React from 'react';
import {Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {CSS, TOKENS} from '../base/estilo';
import {Fade, Grao, In, Palavras, q, SETA, useFontes, useP} from '../base/motion';

// Peças comuns dos Reels ADS (1080x1920). Zona segura do Instagram: nada importante
// nos 220px de cima nem nos 420px de baixo, onde ficam nome, legenda e botões.

export const W = 1080;
export const H = 1920;

/** fundo da casa, hook no terço de cima, celular embaixo e cartão final */
export const Reel: React.FC<{hook: string; pt?: boolean; children: React.ReactNode; fimEm: number}> = ({hook, pt, children, fimEm}) => {
  useFontes();
  return (
    <div className="eze" style={{position: 'absolute', inset: 0, overflow: 'hidden', background: `radial-gradient(80% 40% at 50% 8%, rgba(210,210,210,.09), transparent 72%) no-repeat, ${TOKENS.bg}`}}>
      <style>{CSS}</style>
      <div style={{position: 'absolute', left: 80, right: 80, top: 250}}>
        <Palavras className="frase" texto={hook} d={150} passo={110} pt={pt} style={{fontSize: 84, lineHeight: 1.02}} />
      </div>
      {children}
      <Fim em={fimEm} />
      <Grao opacidade={0.1} porSegundo={4} />
    </div>
  );
};

/** cartão final: logo, Comente PONTO e o @ */
const Fim: React.FC<{em: number}> = ({em}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [em, em + 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (p === 0) return null;
  return (
    <div style={{position: 'absolute', inset: 0, zIndex: 20, background: `rgba(10,10,10,${0.94 * p})`, display: 'grid', placeItems: 'center'}}>
      <div style={{display: 'grid', justifyItems: 'center', gap: 46, opacity: p, transform: `translateY(${(1 - p) * 24}px)`}}>
        <Img src={staticFile('logo-branco.png')} style={{height: 92}} />
        <span className="pilula" style={{fontSize: 52, padding: '16px 16px 16px 46px'}}>Comente PONTO<span className="chip" style={{width: 88, height: 88}}>{SETA}</span></span>
        <span className="handle" style={{fontSize: 30}}>@agenciaezeos</span>
      </div>
    </div>
  );
};

/** celular: entra em perspectiva e sangra pra fora da borda de baixo */
export const Celular: React.FC<{d?: number; children: React.ReactNode}> = ({d = 600, children}) => {
  const p = useP(d, 42);
  return (
    <div style={{position: 'absolute', left: (W - 760) / 2, top: 700, width: 760, perspective: 1800}}>
      <div style={{
        height: 1420, borderRadius: 72, padding: 18, background: '#050505', border: `2px solid ${TOKENS.line2}`,
        boxShadow: '0 0 0 1px rgba(255,255,255,.04) inset', transformOrigin: '50% 0%',
        opacity: p, transform: `rotateX(${14 * (1 - p)}deg) translateY(${140 * (1 - p)}px)`,
      }}>
        <div style={{position: 'relative', height: '100%', borderRadius: 56, overflow: 'hidden', background: TOKENS.bg}}>
          <div style={{position: 'absolute', top: 18, left: '50%', width: 150, height: 40, marginLeft: -75, borderRadius: 999, background: '#000', zIndex: 10}} />
          {children}
        </div>
      </div>
    </div>
  );
};

/** dedo tocando a tela: círculo que aparece, aperta e some */
export const Toque: React.FC<{x: number; y: number; em: number}> = ({x, y, em}) => {
  const f = useCurrentFrame();
  const t = f - em;
  if (t < -8 || t > 22) return null;
  const chega = interpolate(t, [-8, 0], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const onda = interpolate(t, [0, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: x - 45, top: y - 45, width: 90, height: 90, zIndex: 15, pointerEvents: 'none'}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: 'rgba(244,244,244,.28)', border: '2px solid rgba(244,244,244,.6)', opacity: chega * (1 - onda), transform: `scale(${t < 0 ? 1.2 - 0.2 * chega : 0.85})`}} />
      <div style={{position: 'absolute', inset: 0, borderRadius: '50%', border: '2px solid rgba(244,244,244,.5)', opacity: t >= 0 ? 1 - onda : 0, transform: `scale(${1 + onda * 1.4})`}} />
    </div>
  );
};

/** rótulo de cena, em mono, acima do celular */
export const Rotulo: React.FC<{d: number; ate?: number; children: React.ReactNode}> = ({d, ate, children}) => {
  const f = useCurrentFrame();
  const sai = ate ? interpolate(f, [q(ate), q(ate) + 8], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 612, textAlign: 'center', opacity: sai}}>
      <In d={d} className="rotulo" style={{fontSize: 26, color: TOKENS.mute}}>{children}</In>
    </div>
  );
};

/** peças de tela */
export const Esk: React.FC<{w: number | string; h?: number; cor?: string; style?: React.CSSProperties}> = ({w, h = 16, cor = TOKENS.skel, style}) => (
  <div style={{width: w, height: h, borderRadius: h / 2, background: cor, ...style}} />
);

export const Estrelas: React.FC<{size?: number}> = ({size = 20}) => (
  <span style={{display: 'flex', gap: 4}}>
    {[0, 1, 2, 3, 4].map((i) => <i key={i} style={{width: size, height: size, background: TOKENS.mute, clipPath: 'polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)'}} />)}
  </span>
);

export const Botao: React.FC<{children: React.ReactNode; aceso?: boolean; style?: React.CSSProperties}> = ({children, aceso, style}) => (
  <span style={{padding: '14px 24px', borderRadius: 999, border: `1px solid ${aceso ? TOKENS.ink : TOKENS.line2}`, background: aceso ? TOKENS.ink : 'transparent', color: aceso ? TOKENS.bg : TOKENS.mute, font: '500 24px/1 "Inter Tight"', ...style}}>{children}</span>
);

/** usado pra saber a duração total dentro de um componente */
export const useDur = () => useVideoConfig().durationInFrames;
export {Fade, In, q, useP};
