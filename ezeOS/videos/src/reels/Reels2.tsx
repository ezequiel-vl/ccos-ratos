import React from 'react';
import {Img, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {TOKENS} from '../base/estilo';
import {Acende, Digita} from '../base/motion';
import {Celular, Esk, Fade, In, q, Reel, useP} from './comum';
import {BUSCA, Perfil} from './Reels';

// Reels 7 e 8 da grade 16-29/11 (ezeOS/posts/2026-11-16-grade-16-a-29-nov), adaptados das referências
// "Instagram não é site" e "Quando pedem o seu site, o que você manda?".
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

/* ------------------------------------------------------------ Reel 7: seu Instagram é alugado (24/11) */
const Cena7: React.FC<{de: number; ate: number; rotulo: string; children: React.ReactNode}> = ({de, ate, rotulo, children}) => (
  <Sequence from={q(de)} durationInFrames={q(ate - de)} layout="none">
    <div style={{position: 'absolute', left: 0, right: 0, top: 600, textAlign: 'center', zIndex: 5}}>
      <In d={100} className="rotulo" style={{fontSize: 28, color: TOKENS.ink}}>{rotulo}</In>
    </div>
    <Celular d={0}>
      <div style={{position: 'absolute', inset: 0, padding: '110px 26px 0', display: 'grid', alignContent: 'start', gap: 22}}>{children}</div>
    </Celular>
  </Sequence>
);

const Barra: React.FC<{d: number; pct: number}> = ({d, pct}) => {
  const p = useP(d, 40);
  return (
    <div style={{height: 22, borderRadius: 11, background: TOKENS.raised, overflow: 'hidden', border: `1px solid ${TOKENS.line}`}}>
      <div style={{height: '100%', width: `${pct * p}%`, background: TOKENS.sinal}} />
    </div>
  );
};

const Resultado: React.FC<{d: number; dominio: string}> = ({d, dominio}) => (
  <In d={d} style={{display: 'grid', gap: 10, padding: '20px 0', borderBottom: `1px solid ${TOKENS.line}`}}>
    <span style={{font: '400 22px/1 "JetBrains Mono"', color: TOKENS.mute}}>{dominio}</span>
    <Esk w="78%" h={22} cor="#2e2e2e" />
    <Esk w="92%" h={13} />
  </In>
);

const ANDARES: [string, string][] = [['Instagram', 'atrai.'], ['Site', 'convence.'], ['WhatsApp', 'fecha.']];

export const DUR7 = 680;
export const Reel7: React.FC = () => (
  <Reel hook="Seu Instagram é alugado. O site é seu" pt fimEm={DUR7 - 55}>
    <Cena7 de={0} ate={4300} rotulo="1 · A conta pode cair">
      <In d={900} style={{marginTop: 120, padding: 34, borderRadius: 26, background: TOKENS.surface, border: `1px solid ${TOKENS.line2}`, display: 'grid', gap: 18, justifyItems: 'center', textAlign: 'center'}}>
        <svg viewBox="0 0 24 24" style={{width: 64, height: 64, fill: 'none', stroke: TOKENS.ink, strokeWidth: 1.6}}><circle cx="12" cy="12" r="9" /><path d="M12 7v6M12 16.5v.5" /></svg>
        <b style={{font: '600 40px/1.15 "Archivo"', letterSpacing: '-.02em'}}>Sua conta foi suspensa</b>
        <span style={{font: '400 26px/1.4 "Inter Tight"', color: TOKENS.mute}}>Seus posts, seus seguidores e o link da bio saem do ar até a análise terminar.</span>
      </In>
      <Fade d={2300} style={{textAlign: 'center', font: '400 28px/1.4 "Inter Tight"', color: TOKENS.faint, marginTop: 20}}>Bloqueio, invasão ou regra nova. Sem aviso.</Fade>
    </Cena7>
    <Cena7 de={4300} ate={8400} rotulo="2 · O algoritmo escolhe quem vê">
      <In d={600} style={{marginTop: 80, padding: 30, borderRadius: 26, background: TOKENS.surface, border: `1px solid ${TOKENS.line2}`, display: 'grid', gap: 22}}>
        <div style={{height: 340, borderRadius: 18, background: 'linear-gradient(160deg,#1c1c1c,#111)'}} />
        <span style={{font: '500 28px/1.3 "Inter Tight"'}}>Este post alcançou</span>
        <Barra d={1200} pct={8} />
        <b style={{font: '700 64px/1 "Archivo"', letterSpacing: '-.03em'}}>
          8%<span style={{font: '400 26px/1 "Inter Tight"', color: TOKENS.mute, marginLeft: 14}}>dos seus seguidores</span>
        </b>
      </In>
    </Cena7>
    <Cena7 de={8400} ate={12800} rotulo="3 · No Google, perfil não aparece">
      <In d={400} style={{display: 'flex', alignItems: 'center', gap: 14, height: 86, padding: '0 26px', borderRadius: 999, border: `1px solid ${TOKENS.line2}`, background: TOKENS.surface, font: '400 28px/1 "Inter Tight"'}}>
        {BUSCA}
        <Digita texto="harmonização perto de mim" d={700} passo={55} />
      </In>
      <Resultado d={2300} dominio="clinicadaana.com.br" />
      <Resultado d={2600} dominio="espacobeleza.com.br" />
      <Resultado d={2900} dominio="drajulia.com.br" />
      <Fade d={3400} style={{textAlign: 'center', font: '400 28px/1.4 "Inter Tight"', color: TOKENS.faint, marginTop: 10}}>Quem busca serviço com cidade encontra site e ficha do Google.</Fade>
    </Cena7>
    <Cena7 de={12800} ate={16600} rotulo="4 · No feed, tudo se perde">
      <Perfil />
      <Fade d={2200} style={{position: 'absolute', left: 30, right: 30, bottom: 300, zIndex: 3, textAlign: 'center', padding: '22px 26px', borderRadius: 20, background: 'rgba(10,10,10,.88)', font: '400 28px/1.4 "Inter Tight"', color: TOKENS.ink}}>
        Procedimento, horário e endereço no meio de centenas de posts.
      </Fade>
    </Cena7>
    <Sequence from={q(16600)} layout="none">
      <Celular d={0}>
        <div style={{position: 'absolute', inset: 0, display: 'grid', alignContent: 'center', gap: 46, padding: '0 56px'}}>
          {ANDARES.map(([a, b], i) => (
            <In key={a} d={400 + i * 700} style={{display: 'flex', alignItems: 'center', gap: 22, font: '700 62px/1 "Archivo"', letterSpacing: '-.03em'}}>
              <Acende d={600 + i * 700} size={24} cor={i === 1 ? 'sinal' : 'dot'} />
              {a}
              <span style={{fontWeight: 400, color: TOKENS.mute}}>{b}</span>
            </In>
          ))}
        </div>
      </Celular>
    </Sequence>
  </Reel>
);

/* ------------------------------------------------------------ Reel 8: o paciente pediu o site (28/11) */
const Balao: React.FC<{d: number; meu?: boolean; children: React.ReactNode; style?: React.CSSProperties}> = ({d, meu, children, style}) => (
  <In d={d} style={{
    alignSelf: meu ? 'flex-end' : 'flex-start', maxWidth: '84%', padding: '22px 26px', font: '400 30px/1.38 "Inter Tight"',
    borderRadius: meu ? '28px 28px 6px 28px' : '28px 28px 28px 6px', background: meu ? '#1D3329' : '#1F1F1F', border: `1px solid ${TOKENS.line2}`, ...style,
  }}>
    {children}
  </In>
);

const Legenda8: React.FC<{de: number; ate?: number; cor: string; children: React.ReactNode}> = ({de, ate, cor, children}) => (
  <Sequence from={q(de)} durationInFrames={ate ? q(ate - de) : undefined} layout="none">
    <div style={{position: 'absolute', left: 0, right: 0, top: 600, textAlign: 'center'}}>
      <In d={0} className="rotulo" style={{fontSize: 28, color: cor}}>{children}</In>
    </div>
  </Sequence>
);

export const DUR8 = 450;
export const Reel8: React.FC = () => {
  const f = useCurrentFrame();
  const risca = interpolate(f, [q(4300), q(4900)], [0, 1], clamp);
  const some = interpolate(f, [q(5600), q(6100)], [1, 0.35], clamp);
  return (
    <Reel hook="Quando o paciente pede o seu site, o que você manda?" fimEm={DUR8 - 55}>
      <Celular>
        <div style={{position: 'absolute', inset: 0, background: '#0d0d0d', display: 'flex', flexDirection: 'column'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 18, padding: '84px 26px 20px', borderBottom: `1px solid ${TOKENS.line}`}}>
            <i style={{width: 58, height: 58, borderRadius: '50%', background: TOKENS.raised, border: `1px solid ${TOKENS.line2}`}} />
            <div style={{display: 'grid', gap: 8}}>
              <b style={{font: '600 28px/1 "Inter Tight"'}}>Paciente nova</b>
              <span style={{font: '400 20px/1 "Inter Tight"', color: TOKENS.faint}}>online</span>
            </div>
          </div>
          <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', gap: 18, padding: '0 22px 280px'}}>
            <Balao d={900}>Oi! Vocês têm site? Queria ver os procedimentos antes de marcar.</Balao>
            <Balao d={2600} meu style={{opacity: some}}>
              <span style={{position: 'relative', color: '#7FB8E0'}}>
                instagram.com/suaclinica
                <span style={{position: 'absolute', left: 0, top: '52%', height: 3, width: `${risca * 100}%`, background: TOKENS.ink}} />
              </span>
            </Balao>
            <Sequence from={q(6300)} layout="none">
              <Balao d={0} meu style={{padding: 12, maxWidth: '90%'}}>
                <div style={{borderRadius: 18, overflow: 'hidden', background: '#16261F'}}>
                  <Img src={staticFile('renata-abas/d-hero.jpg')} style={{display: 'block', width: '100%'}} />
                  <div style={{padding: '18px 18px 20px', display: 'grid', gap: 8}}>
                    <b style={{font: '600 26px/1.2 "Inter Tight"'}}>Dra. Renata Oliveira · Harmonização facial</b>
                    <span style={{font: '400 22px/1 "JetBrains Mono"', color: TOKENS.mute}}>drarenataoliveira.com.br</span>
                  </div>
                </div>
              </Balao>
            </Sequence>
          </div>
        </div>
      </Celular>
      <Legenda8 de={4600} ate={6300} cor={TOKENS.mute}>Parece menor do que é</Legenda8>
      <Legenda8 de={7600} cor={TOKENS.ink}>Um site no seu nome</Legenda8>
    </Reel>
  );
};
