/**
 * FUIEU · Vandal School: abertura animada do carrossel (4:5) e Reel (9:16).
 *
 * Título VANDAL SCHOOL escorrendo tinta → íris de desenho antigo → sala de aula:
 * o Ze aponta pro quadro, a equação monta (balaclava + luva + lata =) e o FUIEU
 * vai sendo pintado → íris fecha no Ze → volta pro título (loop fechado).
 *
 * As camadas saem de clientes/Fuieu/estampas/Vandal School/fuieu-school.png
 * (recorte das camadas: src/fuieu/prep_vandal.py, gera public/fuieu-vandal/).
 */
import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import meta from '../../public/fuieu-vandal/meta.json';

const A = (n: string) => staticFile(`fuieu-vandal/${n}`);
const EASE = Easing.bezier(0.16, 1, 0.3, 1);
const IO = Easing.inOut(Easing.cubic);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// ---------------------------------------------------------------- linha do tempo (quadros, 30 fps)
export const VS_DUR = 360;
const T = {
  irisFecha1: [76, 94], // título → preto
  irisAbre1: [98, 118], // preto → sala
  eq: [124, 133, 142, 151, 160, 170], // balaclava, +, luva, +, lata, =
  pinta: [182, 262], // FUIEU sendo pintado
  irisFecha2: [300, 326], // fecha no rosto do Ze
  irisAbre2: [332, 350], // abre no título de novo
};
const JABS = [122, 131, 140, 149, 158, 168, 182, 206, 230, 262, 284]; // cutucadas do braço
const NODS = [196, 236, 272]; // aluno balançando a cabeça

// ---------------------------------------------------------------- utilidades
const pulse = (f: number, at: number, up = 3, down = 9) =>
  f < at ? 0 : f < at + up ? (f - at) / up : Math.max(0, 1 - (f - at - up) / down);

/** tremidinha de desenho animado antigo: o traço "ferve" trocando de semente a cada 3 quadros */
const Boil: React.FC<{id: string; scale: number; freq: number}> = ({id, scale, freq}) => {
  const f = useCurrentFrame();
  const seed = Math.floor(f / 3) % 4;
  return (
    <svg width="0" height="0" style={{position: 'absolute'}}>
      <filter id={id} x="-2%" y="-2%" width="104%" height="104%">
        <feTurbulence type="fractalNoise" baseFrequency={freq} numOctaves={2} seed={seed * 7 + 3} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={scale} xChannelSelector="R" yChannelSelector="G" />
      </filter>
    </svg>
  );
};

/** grão de papel por cima de tudo */
const Grao: React.FC = () => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  return (
    <svg width={width} height={height} style={{position: 'absolute', inset: 0, mixBlendMode: 'multiply', opacity: 0.09, pointerEvents: 'none'}}>
      <filter id="grao">
        <feTurbulence type="fractalNoise" baseFrequency={0.85} numOctaves={2} seed={f % 8} />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#grao)" />
    </svg>
  );
};

/** vinheta suave de cinema velho */
const Vinheta: React.FC = () => (
  <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 70%, rgba(0,0,0,.07) 100%)', pointerEvents: 'none'}} />
);

// ---------------------------------------------------------------- título
const DRIPS = [
  {x: 124, w: 22, len: 170, at: 6},
  {x: 486, w: 18, len: 95, at: 14},
  {x: 1119, w: 20, len: 210, at: 4},
  {x: 1624, w: 24, len: 120, at: 18},
  {x: 2189, w: 18, len: 185, at: 10},
  {x: 2631, w: 22, len: 80, at: 22},
  {x: 2939, w: 20, len: 140, at: 12},
];

const Titulo: React.FC<{largura: number; f: number; comTag?: boolean}> = ({largura, f, comTag = true}) => {
  const {title} = meta;
  const s = largura / title.w;
  const BOTTOM = 620;
  return (
    <div style={{position: 'relative', width: largura, height: (title.h + (comTag ? 900 : 0)) * s}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: title.w, height: title.h, transform: `scale(${s})`, transformOrigin: '0 0'}}>
        {/* escorrido: cresce devagar, como tinta de spray carregada */}
        <svg width={title.w} height={title.h + 400} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
          {DRIPS.map((d, i) => {
            const p = interpolate(f, [d.at, d.at + 60], [0, 1], {...clamp, easing: Easing.out(Easing.quad)});
            const L = d.len * p;
            if (L < 2) return null;
            return (
              <g key={i}>
                <rect x={d.x - d.w / 2} y={BOTTOM - 10} width={d.w} height={L + 10} rx={d.w / 2} fill="#000" />
                <circle cx={d.x} cy={BOTTOM + L} r={d.w * 0.68} fill="#000" />
              </g>
            );
          })}
        </svg>
        {title.letters.map((b, i) => {
          // onda: cada letra dá um pulinho, da esquerda pra direita
          const hop = pulse(f, 8 + i * 2.2, 4, 10);
          const rot = Math.sin(i * 1.7) * 3 * hop;
          return (
            <Img
              key={i}
              src={A(`t-${i}.png`)}
              style={{position: 'absolute', left: b.x, top: b.y, width: b.w, height: b.h, transform: `translateY(${-hop * 46}px) rotate(${rot}deg)`, transformOrigin: '50% 100%'}}
            />
          );
        })}
      </div>
      {comTag ? (
        <Img
          src={A('fuieu-tag.png')}
          style={{
            position: 'absolute', left: '50%', top: (title.h + 170) * s, width: largura * 0.3,
            transform: `translateX(-50%) rotate(${-4 + Math.sin(f / 9) * 0.6}deg)`,
          }}
        />
      ) : null}
    </div>
  );
};

// ---------------------------------------------------------------- sala de aula
type Cam = {s: number; x: number; y: number};
const mix = (a: Cam, b: Cam, t: number): Cam => ({s: a.s + (b.s - a.s) * t, x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t});

/** câmera: keyframes [quadro, câmera] interpolados com easing */
const camAt = (f: number, keys: [number, Cam][]): Cam => {
  if (f <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [f0, c0] = keys[i];
    const [f1, c1] = keys[i + 1];
    if (f <= f1) return mix(c0, c1, IO((f - f0) / (f1 - f0)));
  }
  return keys[keys.length - 1][1];
};

const ZE_ROSTO = {x: 490, y: 640};

const Sala: React.FC<{f: number}> = ({f}) => {
  const {arm, head, eq, scene} = meta;

  // braço: cutucadas + acompanha a pintura subindo um pouco
  const jab = JABS.reduce((acc, j) => Math.max(acc, pulse(f, j, 3, 8)), 0);
  const segue = interpolate(f, [T.pinta[0], (T.pinta[0] + T.pinta[1]) / 2, T.pinta[1]], [0, -5, 0], clamp);
  const armRot = -4.5 * jab + segue;
  const armPush = 9 * jab;

  // cabeça do aluno
  const nod = NODS.reduce((acc, n) => Math.max(acc, pulse(f, n, 5, 10)), 0);

  // graffiti: revela da esquerda pra direita e dá um "boing" no final
  const px = interpolate(f, T.pinta, [700, 1720], {...clamp, easing: Easing.inOut(Easing.sin)});
  const boing = spring({frame: f - T.pinta[1], fps: 30, config: {damping: 8, stiffness: 200, mass: 0.6}});
  const grScale = f < T.pinta[1] ? 1 : 1 + (1 - boing) * 0.06;
  const mask = `linear-gradient(to right, #000 ${px - 60}px, transparent ${px + 30}px)`;

  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: scene.w, height: scene.h, background: '#fff'}}>
      <Img src={A('base.png')} style={{position: 'absolute', left: 0, top: 0, width: scene.w, height: scene.h}} />

      {/* equação */}
      {eq.map((b, i) => {
        const sp = spring({frame: f - T.eq[i], fps: 30, config: {damping: 9, stiffness: 190, mass: 0.7}});
        if (f < T.eq[i]) return null;
        return (
          <Img
            key={i}
            src={A(`eq-${i}.png`)}
            style={{position: 'absolute', left: b.x, top: b.y, width: b.w, height: b.h, transform: `scale(${sp}) rotate(${(1 - sp) * -18}deg)`, transformOrigin: '50% 60%'}}
          />
        );
      })}

      {/* FUIEU no quadro */}
      <div style={{position: 'absolute', left: 0, top: 0, width: scene.w, height: scene.h, transform: `scale(${grScale})`, transformOrigin: '1200px 720px', WebkitMaskImage: mask, maskImage: mask}}>
        <Img src={A('graffiti.png')} style={{width: scene.w, height: scene.h}} />
      </div>

      {/* aluno */}
      <Img
        src={A('head.png')}
        style={{position: 'absolute', left: head.x, top: head.y, width: head.w, height: head.h, transform: `rotate(${nod * 6}deg) translateY(${nod * 4}px)`, transformOrigin: '45% 100%'}}
      />

      {/* braço do Ze apontando (pivô no ombro) */}
      <Img
        src={A('arm.png')}
        style={{
          position: 'absolute', left: arm.x, top: arm.y, width: arm.w, height: arm.h,
          transform: `translate(${armPush * 0.85}px, ${-armPush * 0.3}px) rotate(${armRot}deg)`,
          transformOrigin: `${650 - arm.x}px ${860 - arm.y}px`,
        }}
      />
    </div>
  );
};

// ---------------------------------------------------------------- íris
const Iris: React.FC<{r: number; x: number; y: number; children: React.ReactNode}> = ({r, x, y, children}) => (
  <AbsoluteFill style={{background: '#000'}}>
    <AbsoluteFill style={{clipPath: `circle(${Math.max(0, r)}px at ${x}px ${y}px)`}}>{children}</AbsoluteFill>
  </AbsoluteFill>
);

// ---------------------------------------------------------------- composição
export const VandalSchool: React.FC<{formato: '4x5' | '9x16'}> = ({formato}) => {
  const f = useCurrentFrame();
  const {width: W, height: H} = useVideoConfig();
  const vertical = formato === '9x16';
  const R = Math.hypot(W, H) + 40; // cobre a tela mesmo com a íris fora do centro

  // câmera da sala (escala em relação aos 2048 px da arte)
  const base = vertical ? 0.6 : 0.66;
  // no vertical o zoom é mais contido, pra não cortar o Ze nem bater no título/tag
  const z = (k: number) => base * (vertical ? 1 + (k - 1) * 0.3 : k);
  const KEYS: [number, Cam][] = [
    [T.irisAbre1[0], {s: z(1.18), x: 760, y: 760}],
    [128, {s: z(1.0), x: 1000, y: 1010}],
    [170, {s: z(1.28), x: 830, y: 660}],
    [215, {s: z(1.22), x: 1000, y: 720}],
    [262, {s: z(1.2), x: 1100, y: 740}],
    [292, {s: z(1.05), x: 1000, y: 920}],
    [T.irisFecha2[1], {s: z(1.35), x: 640, y: 760}],
  ];
  const cam0 = camAt(f, KEYS);
  // vertical: câmera quase não sobe/desce, a sala fica entre o título e a tag
  const cam = vertical ? {...cam0, y: cam0.y * 0.3 + 1000 * 0.7} : cam0;
  const salaY = vertical ? H * 0.5 : H * 0.5;
  const tx = W / 2 - cam.x * cam.s;
  const ty = salaY - cam.y * cam.s;

  const naSala = f >= T.irisAbre1[0] && f < T.irisAbre2[0];

  // íris
  let irisR = R;
  let irisX = W / 2;
  let irisY = H / 2;
  if (f >= T.irisFecha1[0] && f < T.irisAbre1[0]) {
    irisR = interpolate(f, T.irisFecha1, [R, 0], {...clamp, easing: Easing.in(Easing.cubic)});
  } else if (naSala && f < T.irisFecha2[0]) {
    irisR = interpolate(f, T.irisAbre1, [0, R], {...clamp, easing: Easing.out(Easing.cubic)});
    irisX = ZE_ROSTO.x * cam.s + tx;
    irisY = ZE_ROSTO.y * cam.s + ty;
  } else if (naSala) {
    // fecha no rosto do Ze, segura um instante num círculo pequeno, some
    irisX = ZE_ROSTO.x * cam.s + tx;
    irisY = ZE_ROSTO.y * cam.s + ty;
    const hold = 150 * (cam.s / base);
    irisR = interpolate(f, [T.irisFecha2[0], T.irisFecha2[0] + 14, T.irisFecha2[1] - 4, T.irisFecha2[1] + 4], [R, hold, hold, 0], {...clamp, easing: IO});
  } else if (f >= T.irisAbre2[0]) {
    irisR = interpolate(f, T.irisAbre2, [0, R], {...clamp, easing: Easing.out(Easing.cubic)});
  }

  // título: no começo e na volta (quadro final igual ao primeiro)
  const fTitulo = f >= T.irisAbre2[0] ? 0 : f;
  const largTitulo = vertical ? W * 0.86 : W * 0.86;

  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Boil id="boil" scale={vertical ? 5 : 5} freq={0.012} />
      <Boil id="boil-t" scale={7} freq={0.008} />
      <Iris r={irisR} x={irisX} y={irisY}>
        <AbsoluteFill style={{background: '#fff'}}>
          {naSala ? (
            <>
              <div style={{position: 'absolute', left: 0, top: 0, transform: `translate(${tx}px, ${ty}px) scale(${cam.s})`, transformOrigin: '0 0', filter: 'url(#boil)'}}>
                <Sala f={f} />
              </div>
              {vertical ? (
                <>
                  <div style={{position: 'absolute', left: 0, right: 0, top: 120, display: 'flex', justifyContent: 'center', filter: 'url(#boil-t)'}}>
                    <Titulo largura={W * 0.78} f={-100} comTag={false} />
                  </div>
                  <div style={{position: 'absolute', left: 0, right: 0, bottom: 110, display: 'flex', justifyContent: 'center'}}>
                    <Img src={A('fuieu-tag.png')} style={{width: W * 0.26, transform: `rotate(${-4 + Math.sin(f / 9) * 0.6}deg)`}} />
                  </div>
                </>
              ) : null}
            </>
          ) : (
            <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', filter: 'url(#boil-t)'}}>
              <div style={{transform: `translateY(${vertical ? -40 : 10}px)`}}>
                <Titulo largura={largTitulo} f={fTitulo} />
              </div>
            </AbsoluteFill>
          )}
          <Vinheta />
        </AbsoluteFill>
      </Iris>
      <Grao />
    </AbsoluteFill>
  );
};
