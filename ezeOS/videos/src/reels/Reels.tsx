import React from 'react';
import {Img, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {TOKENS} from '../base/estilo';
import {Acende, Digita} from '../base/motion';
import {Botao, Celular, Esk, Estrelas, Fade, In, q, Reel, Rotulo, Toque, useP} from './comum';

// Os 5 Reels ADS de posts/2026-10-16-instagram-endereco-fixo/08-reels-ads.md.
// Texto de tela exatamente como no roteiro. Telas recriadas em motion, com nomes genéricos;
// os reels 2 e 4 usam a captura real do site da ezeOS (public/ezeos-site-mobile.png).

const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const BUSCA = (
  <svg viewBox="0 0 16 16" style={{width: 30, height: 30, fill: 'none', stroke: TOKENS.mute, strokeWidth: 1.7, flex: 'none'}}><circle cx="7" cy="7" r="4.5" /><path d="M10.5 10.5 14 14" /></svg>
);

/** ficha de empresa no resultado de busca (genérica, sem marca) */
const Ficha: React.FC<{nome?: string; site?: boolean; destaque?: number; style?: React.CSSProperties; botoes?: string[]}> = ({nome, site, destaque = 0, style, botoes}) => {
  const lista = botoes ?? (site ? ['Site', 'Rotas', 'Ligar'] : ['Rotas', 'Ligar', 'Salvar']);
  return (
    <div style={{border: `1px solid ${TOKENS.line2}`, borderRadius: 22, padding: 28, background: TOKENS.surface, display: 'grid', gap: 16, ...style}}>
      {nome ? <b style={{font: '600 34px/1 "Archivo"', letterSpacing: '-.02em'}}>{nome}</b> : <Esk w="58%" h={26} cor="#2e2e2e" />}
      <div style={{display: 'flex', gap: 14, alignItems: 'center'}}><Estrelas /><Esk w={170} h={14} /></div>
      <Esk w="72%" h={14} />
      <div style={{display: 'flex', gap: 10}}>
        {lista.map((b) => (
          <Botao key={b} aceso={b === 'Site'} style={b === 'Site' && destaque ? {boxShadow: `0 0 0 ${6 * destaque}px rgba(244,244,244,${0.35 * destaque})`} : undefined}>{b}</Botao>
        ))}
      </div>
    </div>
  );
};

/** linhas genéricas de fundo, pra tela não parecer vazia */
const Fundo: React.FC<{d: number; n?: number; alto?: number}> = ({d, n = 3, alto = 120}) => (
  <div style={{display: 'grid', gap: 14, opacity: 0.55}}>
    {Array.from({length: n}, (_, i) => (
      <In key={i} d={d + i * 120} style={{height: alto, borderRadius: 20, border: `1px solid ${TOKENS.line}`, background: TOKENS.sunk, padding: 24, display: 'grid', alignContent: 'center', gap: 12}}>
        <Esk w={`${55 + ((i * 17) % 30)}%`} h={16} cor="#232323" /><Esk w={`${35 + ((i * 23) % 40)}%`} h={12} />
      </In>
    ))}
  </div>
);

/** página do site dentro do celular (captura real do ezeos.com.br) */
const SiteReal: React.FC<{d: number}> = ({d}) => {
  const p = useP(d, 22);
  return (
    <div style={{position: 'absolute', inset: 0, zIndex: 6, transform: `translateY(${(1 - p) * 100}%)`}}>
      <Img src={staticFile('ezeos-site-mobile.png')} style={{width: '100%', display: 'block'}} />
    </div>
  );
};

/* ------------------------------------------------------------ Reel 1: a busca */
export const DUR1 = 330;
const Reel1Tela: React.FC = () => {
  const f = useCurrentFrame();
  const rola = interpolate(f, [q(4200), q(7400)], [0, -560], {...clamp, easing: (t) => t * t * (3 - 2 * t)});
  const brilho = interpolate(f, [q(7600), q(8200)], [0, 1], clamp);
  return (
    <div style={{position: 'absolute', inset: 0, padding: '0 30px'}}>
      <div style={{position: 'relative', zIndex: 3, background: TOKENS.bg, paddingTop: 96, paddingBottom: 18, marginLeft: -30, marginRight: -30, paddingLeft: 30, paddingRight: 30}}>
      <In d={900} style={{display: 'flex', alignItems: 'center', gap: 18, height: 92, padding: '0 30px', borderRadius: 999, border: `1px solid ${TOKENS.line2}`, background: TOKENS.surface, font: '400 32px/1 "Inter Tight"'}}>
        {BUSCA}<Digita texto="harmonização facial centro" d={1300} passo={65} />
      </In>
      </div>
      <div style={{position: 'relative', zIndex: 1, marginTop: 8, transform: `translateY(${rola}px)`, display: 'grid', gap: 18}}>
        <In d={3200} style={{height: 250, borderRadius: 22, border: `1px solid ${TOKENS.line}`, position: 'relative', backgroundImage: `linear-gradient(${TOKENS.line} 1px, transparent 1px), linear-gradient(90deg, ${TOKENS.line} 1px, transparent 1px)`, backgroundSize: '34px 34px'}}>
          {[[18, 30], [52, 58], [74, 24], [38, 70]].map(([x, y], i) => <Acende key={i} d={3500 + i * 120} size={20} style={{position: 'absolute', left: `${x}%`, top: `${y}%`}} />)}
        </In>
        <In d={3500}><Ficha site destaque={brilho} /></In>
        <In d={3650}><Ficha /></In>
        <In d={3800}><Ficha site destaque={brilho} /></In>
        <In d={3950}><Ficha /></In>
      </div>
    </div>
  );
};
export const Reel1: React.FC = () => (
  <Reel hook="Busque seu serviço com o nome do seu bairro. Quem apareceu?" fimEm={DUR1 - 50}>
    <Celular><Reel1Tela /></Celular>
  </Reel>
);

/* ------------------------------------------------------------ Reel 2: o botão vazio */
export const DUR2 = 300;
export const Reel2: React.FC = () => (
  <Reel hook="Toque no botão Site da sua ficha agora" pt fimEm={DUR2 - 50}>
    <Rotulo d={900} ate={4000}>Sem site: o botão nem aparece</Rotulo>
    <Sequence from={q(4100)}><Rotulo d={0}>Com site: abre a página da empresa</Rotulo></Sequence>
    <Celular>
      <div style={{position: 'absolute', inset: 0, padding: '110px 30px 0', display: 'grid', alignContent: 'start', gap: 22}}>
        <Sequence durationInFrames={q(4100)} layout="none">
          <In d={800} style={{display: 'flex', alignItems: 'center', gap: 18, height: 84, padding: '0 28px', borderRadius: 999, border: `1px solid ${TOKENS.line2}`, background: TOKENS.surface, font: '400 30px/1 "Inter Tight"', color: TOKENS.mute}}>{BUSCA}sua empresa</In>
          <In d={1000}><Ficha nome="Sua Empresa" /></In>
          <Fade d={2600} style={{textAlign: 'center', font: '400 26px/1.4 "Inter Tight"', color: TOKENS.faint}}>quem procura, desiste aqui</Fade>
          <Fundo d={1300} n={3} />
        </Sequence>
        <Sequence from={q(4100)} layout="none">
          <In d={0} style={{display: 'flex', alignItems: 'center', gap: 18, height: 84, padding: '0 28px', borderRadius: 999, border: `1px solid ${TOKENS.line2}`, background: TOKENS.surface, font: '400 30px/1 "Inter Tight"', color: TOKENS.mute}}>{BUSCA}ezeos</In>
          <In d={0}><Ficha nome="ezeOS" site /></In>
          <Fundo d={200} n={3} />
        </Sequence>
      </div>
      <Sequence from={q(5600)}><SiteReal d={0} /></Sequence>
    </Celular>
    <Toque x={283} y={1106} em={q(5300)} />
  </Reel>
);

/* ------------------------------------------------------------ Reel 3: o anúncio sem destino */
export const DUR3 = 420;
const Anuncio: React.FC = () => (
  <div style={{border: `1px solid ${TOKENS.line2}`, borderRadius: 22, overflow: 'hidden', background: TOKENS.surface}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 16, padding: 22}}>
      <i style={{width: 54, height: 54, borderRadius: '50%', background: TOKENS.raised, border: `1px solid ${TOKENS.line2}`}} />
      <div style={{display: 'grid', gap: 8}}><Esk w={200} h={16} cor="#2e2e2e" /><span style={{font: '400 20px/1 "Inter Tight"', color: TOKENS.faint}}>Patrocinado</span></div>
    </div>
    <div style={{height: 520, background: `linear-gradient(160deg, #1c1c1c, #111)`}} />
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '22px 24px'}}>
      <span style={{font: '500 26px/1 "Inter Tight"'}}>Saiba mais</span><span style={{font: '500 26px/1 "Inter Tight"', color: TOKENS.mute}}>›</span>
    </div>
  </div>
);
const Perfil: React.FC = () => {
  const f = useCurrentFrame();
  const rola = interpolate(f, [q(600), q(2200)], [0, -380], clamp);
  return (
    <div style={{position: 'absolute', inset: 0, padding: '100px 30px 0', background: TOKENS.bg, transform: `translateY(${rola}px)`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 26}}>
        <i style={{width: 130, height: 130, borderRadius: '50%', background: TOKENS.raised, border: `1px solid ${TOKENS.line2}`}} />
        <div style={{display: 'grid', gap: 12, flex: 1}}><Esk w="70%" h={22} cor="#2e2e2e" /><Esk w="90%" h={14} /><Esk w="60%" h={14} /></div>
      </div>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 6, marginTop: 40}}>
        {Array.from({length: 15}, (_, i) => <div key={i} style={{aspectRatio: '1', background: i % 3 === 1 ? '#1d1d1d' : '#171717'}} />)}
      </div>
    </div>
  );
};
const PaginaServico: React.FC = () => (
  <div style={{position: 'absolute', inset: 0, padding: '100px 34px 0', background: TOKENS.bg, display: 'grid', alignContent: 'start', gap: 24}}>
    <span style={{font: '600 28px/1 "Archivo"'}}>Sua Empresa</span>
    <div style={{height: 300, borderRadius: 22, background: 'linear-gradient(160deg,#1c1c1c,#111)', border: `1px solid ${TOKENS.line}`}} />
    <span style={{font: '600 52px/1.04 "Archivo"', letterSpacing: '-.03em'}}>O serviço que você faz, no bairro onde você está.</span>
    <Esk w="90%" h={16} /><Esk w="70%" h={16} />
    <span style={{justifySelf: 'start', marginTop: 10, padding: '22px 34px', borderRadius: 999, background: TOKENS.ink, color: TOKENS.bg, font: '500 30px/1 "Inter Tight"'}}>Chamar no WhatsApp</span>
  </div>
);
const Conversa: React.FC = () => (
  <div style={{position: 'absolute', inset: 0, background: '#0d0d0d', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', padding: '0 26px 260px'}}>
    <In d={200} style={{alignSelf: 'flex-end', maxWidth: '82%', padding: '24px 28px', borderRadius: '28px 28px 6px 28px', background: '#232323', border: `1px solid ${TOKENS.line2}`, font: '400 30px/1.35 "Inter Tight"'}}>
      Oi! Vi o anúncio e quero saber os horários pra avaliação.
    </In>
  </div>
);
export const Reel3: React.FC = () => {
  const f = useCurrentFrame();
  const saida = interpolate(f, [q(5600), q(6200)], [0, 1], clamp);
  return (
    <Reel hook="Pare de pagar anúncio pra levar cliente pro seu perfil" pt fimEm={DUR3 - 50}>
      <Rotulo d={900} ate={6300}>Anúncio levando pro perfil</Rotulo>
      <Sequence from={q(6500)}><Rotulo d={0}>Anúncio levando pra página do serviço</Rotulo></Sequence>
      <Celular>
        <Sequence durationInFrames={q(6500)} layout="none">
          <div style={{position: 'absolute', inset: 0, padding: '100px 26px 0'}}><In d={1000}><Anuncio /></In></div>
          <Sequence from={q(2900)} durationInFrames={q(3600)}>
            <div style={{position: 'absolute', inset: 0, opacity: 1 - saida, transform: `translateY(${saida * 50}%)`}}><Perfil /></div>
          </Sequence>
          <Fade d={6000} style={{position: 'absolute', left: 0, right: 0, top: 560, textAlign: 'center', font: '400 30px/1.4 "Inter Tight"', color: TOKENS.faint}}>e saiu sem falar com ninguém</Fade>
        </Sequence>
        <Sequence from={q(6500)} layout="none">
          <div style={{position: 'absolute', inset: 0, padding: '100px 26px 0'}}><In d={0}><Anuncio /></In></div>
          <Sequence from={q(1500)}><PaginaServico /></Sequence>
          <Sequence from={q(3600)}><Conversa /></Sequence>
        </Sequence>
      </Celular>
      <Toque x={300} y={1473} em={q(2700)} />
      <Toque x={300} y={1473} em={q(7700)} />
      <Toque x={404} y={1509} em={q(9800)} />
    </Reel>
  );
};

/* ------------------------------------------------------------ Reel 4: a instalação em 10 dias */
export const DUR4 = 480;
const PASSOS: [number, string][] = [[0, 'Dia 1'], [2600, 'Dia 1'], [4600, 'Dia 2'], [6600, 'Dias 3 a 7'], [9200, 'Dia 7'], [11400, 'Dia 10']];
const Contador: React.FC = () => {
  const f = useCurrentFrame();
  const i = PASSOS.reduce((acc, [ms], k) => (f >= q(ms + 900) ? k : acc), 0);
  const barra = interpolate(f, [q(900), q(12600)], [0.1, 1], clamp);
  return (
    <div style={{position: 'absolute', left: 160, right: 160, top: 610, display: 'grid', gap: 16, justifyItems: 'center'}}>
      <Fade d={900} className="rotulo" style={{fontSize: 30, color: TOKENS.ink}}>{PASSOS[i][1]}</Fade>
      <Fade d={900} style={{width: '100%', height: 6, borderRadius: 3, background: TOKENS.skel, overflow: 'hidden'}}>
        <div style={{height: '100%', width: `${barra * 100}%`, background: TOKENS.ink}} />
      </Fade>
    </div>
  );
};
const Cena: React.FC<{de: number; ate: number; children: React.ReactNode}> = ({de, ate, children}) => (
  <Sequence from={q(de)} durationInFrames={q(ate - de)}>
    <div style={{position: 'absolute', inset: 0, padding: '120px 34px 0', display: 'grid', alignContent: 'start', gap: 24}}>{children}</div>
  </Sequence>
);
const Linha: React.FC<{d: number; children: React.ReactNode; ok?: boolean}> = ({d, children, ok}) => (
  <In d={d} style={{display: 'flex', alignItems: 'center', gap: 18, padding: '26px 28px', borderRadius: 20, border: `1px solid ${TOKENS.line2}`, background: TOKENS.surface, font: '400 30px/1.3 "Inter Tight"'}}>
    {ok ? <Acende d={d + 400} size={22} /> : null}{children}
  </In>
);
export const Reel4: React.FC = () => (
  <Reel hook="Instale sua empresa no digital em 10 dias, no seu nome" pt fimEm={DUR4 - 50}>
    <Contador />
    <Celular>
      <Cena de={900} ate={3500}>
        <span className="rotulo">Domínio</span>
        <In d={200} style={{display: 'flex', alignItems: 'center', gap: 16, height: 90, padding: '0 28px', borderRadius: 999, border: `1px solid ${TOKENS.line2}`, font: '400 32px/1 "JetBrains Mono"'}}><Digita texto="suaempresa.com.br" d={400} passo={55} /></In>
        <Linha d={1500} ok>disponível</Linha>
        <Linha d={2000} ok>registrado no seu CPF ou CNPJ</Linha>
      </Cena>
      <Cena de={3500} ate={5500}>
        <span className="rotulo">E-mail</span>
        <In d={200} style={{padding: 28, borderRadius: 24, background: TOKENS.raised, border: `1px solid ${TOKENS.line2}`, display: 'grid', gap: 12}}>
          <span style={{font: '500 24px/1 "JetBrains Mono"', color: TOKENS.mute}}>contato@suaempresa.com.br</span>
          <b style={{font: '600 34px/1.1 "Archivo"'}}>Seu e-mail está funcionando</b>
          <Esk w="80%" h={14} />
        </In>
        <Fundo d={500} n={4} alto={100} />
      </Cena>
      <Cena de={5500} ate={7500}>
        <span className="rotulo">WhatsApp Business</span>
        <Linha d={200} ok>horário de atendimento</Linha>
        <Linha d={500} ok>catálogo de serviços</Linha>
        <Linha d={800} ok>mensagem de ausência</Linha>
      </Cena>
      <Sequence from={q(7500)} durationInFrames={q(10100 - 7500)}><Img src={staticFile('ezeos-site-mobile.png')} style={{width: '100%', display: 'block', opacity: 1}} /></Sequence>
      <Cena de={10100} ate={12300}>
        <span className="rotulo">Ficha do Google</span>
        <In d={200}><Ficha nome="Sua Empresa" site destaque={1} /></In>
      </Cena>
      <Cena de={12300} ate={16000}>
        <In d={0} style={{display: 'flex', alignItems: 'center', gap: 18, justifyContent: 'center', marginTop: 260, font: '500 44px/1 "JetBrains Mono"', letterSpacing: '.14em'}}>
          <Acende d={200} size={28} cor="sinal" halo />NO AR
        </In>
      </Cena>
    </Celular>
  </Reel>
);

/* ------------------------------------------------------------ Reel 5: o @gmail */
export const DUR5 = 240;
const Email: React.FC<{de: string; d: number; destaque?: number}> = ({de, d, destaque = 0}) => (
  <In d={d} style={{display: 'grid', gridTemplateColumns: '64px 1fr', gap: 20, alignItems: 'center', padding: '26px 24px', borderRadius: 22, border: `1px solid ${destaque ? `rgba(244,244,244,${0.2 + 0.5 * destaque})` : TOKENS.line}`, background: destaque ? TOKENS.raised : TOKENS.surface}}>
    <i style={{width: 64, height: 64, borderRadius: '50%', background: TOKENS.raised, border: `1px solid ${TOKENS.line2}`}} />
    <div style={{display: 'grid', gap: 10, minWidth: 0}}>
      <span style={{font: '500 24px/1.2 "JetBrains Mono"', color: TOKENS.ink, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}}>{de}</span>
      <b style={{font: '600 30px/1 "Archivo"'}}>Orçamento</b>
      <Esk w="85%" h={13} />
    </div>
  </In>
);
export const Reel5: React.FC = () => {
  const f = useCurrentFrame();
  const destaque = interpolate(f, [q(4300), q(4800)], [0, 1], clamp);
  return (
    <Reel hook="Troque o @gmail do orçamento por um e-mail com seu nome" pt fimEm={DUR5 - 50}>
      <Celular>
        <div style={{position: 'absolute', inset: 0, padding: '110px 26px 0', display: 'grid', alignContent: 'start', gap: 18}}>
          <In d={900} style={{font: '600 40px/1 "Archivo"', letterSpacing: '-.02em', marginBottom: 10}}>Caixa de entrada</In>
          <Email d={1600} de="clinica.exemplo2019@gmail.com" />
          <Email d={2600} de="contato@clinicaexemplo.com.br" destaque={destaque} />
          <Fundo d={1000} n={4} alto={130} />
        </div>
      </Celular>
      <Toque x={540} y={1132} em={q(4300)} />
    </Reel>
  );
};
