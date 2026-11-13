import React from 'react';
import {Easing, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {CSS, TOKENS} from '../base/estilo';
import {Grao, useFontes} from '../base/motion';

// Slide 1 (vídeo 4:5) do carrossel "A clínica que só tinha Instagram", estilo referência:
// seções do site da Dra. Renata entram como abas pela direita, empilham e saem revelando a capa.
// O primeiro e o último quadro são a capa, então o loop do Instagram fica contínuo.
export const ABAS_DUR = 330;
const ABAS = ['1-hero', '2-naturalidade', '3-sobre', '4-avaliacao', '5-procedimentos', '6-resultados'];
const ENTRA = 24; // quadro em que a primeira aba entra
const PASSO = 30; // intervalo entre abas
const SAI = ENTRA + PASSO * ABAS.length + 30; // começo da saída
const W_ABA = 640;
const H_ABA = 960;
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

const Aba: React.FC<{i: number}> = ({i}) => {
  const f = useCurrentFrame();
  const t0 = ENTRA + i * PASSO;
  const entra = interpolate(f, [t0, t0 + 22], [0, 1], {...cl, easing: ease});
  // quantas abas entraram depois desta: cada uma empurra esta pra trás
  const depois = ABAS.reduce((n, _, k) => n + (k > i ? interpolate(f, [ENTRA + k * PASSO, ENTRA + k * PASSO + 22], [0, 1], {...cl, easing: ease}) : 0), 0);
  const sai = interpolate(f, [SAI + (ABAS.length - 1 - i) * 4, SAI + (ABAS.length - 1 - i) * 4 + 20], [0, 1], {...cl, easing: Easing.in(Easing.cubic)});
  const x = 1120 - (1120 - 330) * entra - depois * 64 + sai * 1300;
  const escala = 1 - depois * 0.035;
  const sombra = Math.min(depois, 3) * 0.12;
  if (entra <= 0 || sai >= 1) return null;
  return (
    <div style={{position: 'absolute', left: x, top: 190, width: W_ABA, height: H_ABA, zIndex: 10 + i, transformOrigin: '0% 50%',
      transform: `perspective(1800px) rotateY(${-10 + 10 * entra - 4 * Math.min(depois, 2)}deg) scale(${escala})`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 34, overflow: 'hidden', background: '#F4F1EC',
        boxShadow: '-30px 0 60px -10px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.12)'}}>
        <Img src={staticFile(`renata-abas/${ABAS[i]}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top'}} />
        <div style={{position: 'absolute', inset: 0, background: `rgba(0,0,0,${sombra})`}} />
      </div>
    </div>
  );
};

export const AbasRenata: React.FC = () => {
  useFontes();
  const f = useCurrentFrame();
  // a capa recua um pouco enquanto as abas estão na frente
  const naFrente = interpolate(f, [ENTRA, ENTRA + 20, SAI + 10, SAI + 40], [0, 1, 1, 0], cl);
  return (
    <div className="eze" style={{position: 'absolute', inset: 0, overflow: 'hidden', background: TOKENS.bg}}>
      <style>{CSS}</style>
      <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(70% 45% at 50% 30%, rgba(210,210,210,.10), transparent 70%)'}} />
      <div style={{position: 'absolute', inset: 0, transform: `scale(${1 - 0.04 * naFrente})`, filter: `brightness(${1 - 0.45 * naFrente})`}}>
        <div style={{position: 'absolute', top: 72, left: 88, right: 88, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <Img src={staticFile('logo-branco.png')} style={{height: 36}} />
          <span style={{font: '400 22px/1 "JetBrains Mono"', color: TOKENS.mute}}>@agenciaezeos</span>
        </div>
        {/* o site no monitor */}
        <div style={{position: 'absolute', left: 88, right: 88, top: 170, borderRadius: 22, overflow: 'hidden', border: `1px solid ${TOKENS.line2}`, background: '#1C1C1C',
          boxShadow: '0 50px 90px -30px rgba(0,0,0,.8)', transform: 'perspective(2000px) rotateX(6deg)', transformOrigin: '50% 0%'}}>
          <div style={{height: 46, display: 'flex', alignItems: 'center', gap: 9, padding: '0 18px'}}>
            {[0, 1, 2].map((k) => <i key={k} style={{width: 12, height: 12, borderRadius: '50%', background: '#3A3A3A'}} />)}
            <span style={{marginLeft: 14, flex: 1, height: 28, borderRadius: 999, background: '#111', color: TOKENS.mute, font: '500 17px/28px "JetBrains Mono"', padding: '0 16px'}}>drarenataoliveira.com.br</span>
          </div>
          <Img src={staticFile('renata-abas/d-hero.jpg')} style={{display: 'block', width: '100%'}} />
        </div>
        <div style={{position: 'absolute', left: 88, right: 88, bottom: 120, display: 'grid', gap: 26}}>
          <span style={{font: '500 22px/1 "JetBrains Mono"', letterSpacing: '.22em', textTransform: 'uppercase', color: TOKENS.faint}}>Case real · Dra. Renata Oliveira</span>
          <h1 style={{margin: 0, font: '700 104px/.95 "Archivo"', fontStretch: '106%', letterSpacing: '-.04em', color: TOKENS.ink}}>
            A clínica que só tinha Instagram<span style={{color: TOKENS.sinal}}>.</span>
          </h1>
          <span style={{justifySelf: 'start', display: 'inline-flex', alignItems: 'center', gap: 16, height: 64, padding: '0 14px 0 30px', borderRadius: 999, background: TOKENS.ink, color: TOKENS.bg, font: '500 28px/1 "Inter Tight"'}}>
            Arraste pro lado
            <span style={{width: 40, height: 40, borderRadius: '50%', background: TOKENS.bg, display: 'grid', placeItems: 'center'}}>
              <svg viewBox="0 0 16 16" style={{width: 20, height: 20, fill: 'none', stroke: TOKENS.ink, strokeWidth: 1.8}}><path d="M3 8h10M9 4l4 4-4 4" /></svg>
            </span>
          </span>
        </div>
      </div>
      {ABAS.map((_, i) => <Aba key={i} i={i} />)}
      <Grao opacidade={0.08} porSegundo={4} />
    </div>
  );
};
