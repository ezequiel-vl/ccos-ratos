import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {TOKENS} from '../base/estilo';
import {Acende, Digita, Fade, In, Luz, Palavras, q, Riscado, Risca, SETA, Slide, useP} from '../base/motion';

// Manifesto do Endereço Fixo, refeito em Remotion. Texto igual a posts/.../02-manifesto.md.
const T = 10;

const Navegador: React.FC = () => {
  const p = useP(900, 48);
  const esk = (d: number, w: string, h = 14, bg = TOKENS.skel) => (
    <In d={d} style={{height: h, width: w, borderRadius: h / 2, background: bg}} />
  );
  return (
    <div style={{position: 'absolute', left: 64, right: 64, bottom: -150, perspective: 1600, zIndex: 2}}>
      <div className="card" style={{transformOrigin: '50% 100%', opacity: p, transform: `rotateX(${28 - 19 * p}deg) translateY(${160 * (1 - p)}px)`}}>
        <Luz sobre />
        <div style={{display: 'flex', alignItems: 'center', gap: 22, padding: '20px 24px', borderBottom: `1px solid ${TOKENS.line}`, background: TOKENS.sunk}}>
          <div style={{display: 'flex', gap: 10}}>{[0, 1, 2].map((i) => <i key={i} style={{width: 14, height: 14, borderRadius: '50%', background: TOKENS.skel}} />)}</div>
          <div style={{flex: 1, display: 'flex', alignItems: 'center', gap: 14, height: 52, padding: '0 22px', borderRadius: 999, background: TOKENS.raised, border: `1px solid ${TOKENS.line}`, font: '400 24px/1 "JetBrains Mono"'}}>
            <svg viewBox="0 0 16 16" style={{width: 18, height: 18, fill: 'none', stroke: TOKENS.mute, strokeWidth: 1.6}}><rect x="3.5" y="7" width="9" height="6.5" rx="1.5" /><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" /></svg>
            <Digita texto="suaempresa.com.br" d={1900} passo={60} />
          </div>
          <Fade d={2950} style={{display: 'flex', alignItems: 'center', gap: 12, font: '500 19px/1 "JetBrains Mono"', letterSpacing: '.14em'}}>
            <Acende d={2950} size={12} cor="sinal" halo />NO AR
          </Fade>
        </div>
        <div style={{display: 'grid', gridTemplateColumns: '1.25fr 1fr', minHeight: 560}}>
          <div style={{padding: '40px 36px', borderRight: `1px solid ${TOKENS.line}`, display: 'grid', alignContent: 'start', gap: 22}}>
            <In d={3150} style={{font: '600 26px/1 "Archivo"', letterSpacing: '-.02em'}}>Sua Empresa</In>
            {esk(3250, '88%', 34, '#2e2e2e')}{esk(3300, '64%', 34, '#2e2e2e')}{esk(3400, '80%')}{esk(3450, '58%')}
            <In d={3600} style={{justifySelf: 'start', marginTop: 10, padding: '16px 26px', borderRadius: 999, background: TOKENS.ink, color: TOKENS.bg, font: '500 22px/1 "Inter Tight"'}}>Agendar pelo WhatsApp</In>
          </div>
          <div style={{padding: '34px 30px', display: 'grid', alignContent: 'start', gap: 20}}>
            <In d={3300} style={{display: 'flex', alignItems: 'center', gap: 12, height: 52, padding: '0 20px', borderRadius: 999, border: `1px solid ${TOKENS.line2}`, font: '400 21px/1 "Inter Tight"', color: TOKENS.mute}}>sua empresa perto de mim</In>
            <In d={3500} style={{border: `1px solid ${TOKENS.line2}`, borderRadius: 14, padding: 22, display: 'grid', gap: 14, background: TOKENS.raised}}>
              <b style={{font: '600 24px/1 "Archivo"'}}>Sua Empresa</b>
              <small style={{font: '400 17px/1 "Inter Tight"', color: TOKENS.faint}}>Aberto agora · Rua do seu endereço</small>
              <div style={{display: 'flex', gap: 8}}>
                {['Site', 'Rotas', 'Ligar'].map((b, i) => (
                  <span key={b} style={{padding: '9px 14px', borderRadius: 999, border: `1px solid ${i ? TOKENS.line2 : TOKENS.ink}`, font: '500 16px/1 "Inter Tight"', background: i ? 'transparent' : TOKENS.ink, color: i ? TOKENS.mute : TOKENS.bg}}>{b}</span>
                ))}
              </div>
              <div style={{height: 150, borderRadius: 10, border: `1px solid ${TOKENS.line}`, position: 'relative', backgroundImage: `linear-gradient(${TOKENS.line} 1px, transparent 1px), linear-gradient(90deg, ${TOKENS.line} 1px, transparent 1px)`, backgroundSize: '28px 28px'}}>
                <Acende d={3900} size={16} cor="sinal" halo style={{position: 'absolute', left: '62%', top: '46%'}} />
              </div>
            </In>
          </div>
        </div>
      </div>
    </div>
  );
};

export const M01: React.FC = () => (
  <Slide n={1} total={T} capa extra={<Navegador />} mioloStyle={{justifyContent: 'flex-start', paddingTop: 96}}>
    <div>
      <In d={150} className="rotulo" style={{marginBottom: 34}}>Manifesto</In>
      <Palavras as="h1" className="hero" texto="Endereço Fixo" d={250} passo={140} pt style={{marginBottom: 40}} />
      <In d={700} className="lead" style={{maxWidth: 860}}>Sua empresa encontrada em qualquer lugar onde o cliente procurar.</In>
      <In d={850} className="lead ink" style={{marginTop: 18}}>Mesmo nas semanas em que você não posta nada.</In>
    </div>
  </Slide>
);

export const M02: React.FC = () => (
  <Slide n={2} total={T}>
    <div style={{display: 'grid', gap: 44}}>
      <In d={200} className="sub">Eu também já vendi aparição: <Riscado d={1300}>visualização</Riscado>, <Riscado d={1500}>post pro feed</Riscado>, <Riscado d={1700}>story</Riscado>, <Riscado d={1900}>anúncio apontando pro perfil</Riscado>.</In>
      <In d={2400} className="corpo">Funcionava enquanto o cliente pagava. No mês em que ele parava, a empresa sumia junto, e a gente começava do zero no mês seguinte.</In>
      <Risca d={3000} />
      <In d={3300} className="corpo ink">Hoje eu instalo outra coisa: site, ficha do Google, e-mail no domínio e WhatsApp configurado, tudo no nome da empresa e tudo ligado.</In>
      <Palavras className="titulo" texto="Uma coisa que fica de pé depois que eu vou embora" d={4000} passo={80} pt />
    </div>
  </Slide>
);

export const M03: React.FC = () => (
  <Slide n={3} total={T}>
    <div style={{display: 'grid', gap: 34}}>
      <Palavras as="h2" className="frase" texto="Não precisa acreditar em mim" d={200} passo={110} pt style={{fontSize: 84}} />
      <In d={900} className="corpo">Pega o celular e busca o seu serviço mais caro junto com o nome do seu bairro.</In>
      <In d={1200} style={{font: '400 27px/1.4 "Inter Tight"', color: TOKENS.faint}}>Ex.: “harmonização facial centro”, “advogado trabalhista moinhos”, “pet shop zona sul”.</In>
      <In d={1500} className="card" style={{display: 'flex', alignItems: 'center', gap: 20, height: 100, padding: '0 34px', borderRadius: 999, font: '400 36px/1 "Inter Tight"'}}>
        <Luz />
        <svg viewBox="0 0 16 16" style={{width: 30, height: 30, fill: 'none', stroke: TOKENS.mute, strokeWidth: 1.7, flex: 'none'}}><circle cx="7" cy="7" r="4.5" /><path d="M10.5 10.5 14 14" /></svg>
        <Digita texto="harmonização facial centro" d={1900} passo={60} />
      </In>
      <div style={{display: 'grid', gap: 12}}>
        {[[3700, '62%'], [3850, '48%'], [4000, '70%']].map(([d, w]) => (
          <In key={d as number} d={d as number} style={{display: 'grid', gridTemplateColumns: '14px 1fr 120px', gap: 22, alignItems: 'center', padding: '18px 26px', border: `1px solid ${TOKENS.line}`, borderRadius: 14, background: TOKENS.sunk}}>
            <i style={{width: 12, height: 12, borderRadius: '50%', background: TOKENS.dotOff}} />
            <b style={{height: 16, width: w as string, borderRadius: 8, background: TOKENS.skel}} />
            <s style={{height: 30, borderRadius: 999, border: `1px solid ${TOKENS.line2}`}} />
          </In>
        ))}
      </div>
      <Palavras className="titulo ink" texto="Agora olha quem apareceu" d={4500} passo={90} pt />
    </div>
  </Slide>
);

export const M04: React.FC = () => {
  const itens = ['site ligado no botão,', 'foto real do lugar,', 'serviço descrito,', 'horário certo,', 'avaliação respondida.'];
  return (
    <Slide n={4} total={T}>
      <div style={{display: 'grid', gap: 38}}>
        <In d={200} className="titulo">Quem apareceu na sua frente provavelmente não posta mais do que você.</In>
        <In d={800} className="corpo">Abre a ficha dele e repara:</In>
        <In d={1100} className="card" style={{padding: '40px 44px', display: 'grid', gap: 26}}>
          <Luz />
          <div style={{display: 'grid', gap: 14, paddingBottom: 26, borderBottom: `1px solid ${TOKENS.line}`}}>
            <b style={{height: 26, width: '46%', borderRadius: 9, background: '#2e2e2e'}} />
            <s style={{height: 14, width: '30%', borderRadius: 7, background: TOKENS.skel}} />
          </div>
          <div style={{display: 'grid', gap: 22}}>
            {itens.map((t, i) => (
              <In key={t} d={1500 + i * 300} style={{display: 'flex', alignItems: 'center', gap: 24, font: '400 36px/1.2 "Inter Tight"'}}>
                <Acende d={1700 + i * 300} size={26} />{t}
              </In>
            ))}
          </div>
        </In>
        <Palavras className="titulo" texto="O que ele tem a mais que você é endereço" d={3600} passo={90} pt />
      </div>
    </Slide>
  );
};

export const M05: React.FC = () => (
  <Slide n={5} total={T}>
    <div style={{display: 'grid', gap: 38}}>
      <Palavras as="h2" className="frase" texto="“Acho que eu precisava aparecer mais" d={200} passo={120} pt depois="”" style={{fontSize: 96}} />
      <In d={1300} className="corpo">É a frase que eu mais escuto de dono de negócio.</In>
      <Risca d={1700} />
      <div style={{display: 'grid', gap: 6}}>
        <In d={2000} className="corpo ink">Aí ele contrata alguém pra postar.</In>
        <In d={2400} className="corpo ink">Depois alguém pra impulsionar.</In>
        <In d={2800} className="corpo ink">Depois troca os dois.</In>
      </div>
      <In d={3400} className="corpo">E a agenda continua enchendo do mesmo jeito: <span className="ink">indicação.</span></In>
      <Palavras className="titulo" texto="O que falta é um lugar pra onde a pessoa vá depois que te vê" d={4200} passo={70} pt />
    </div>
  </Slide>
);

export const M06: React.FC = () => {
  const mortos = ['Perfil de Instagram como único endereço.', 'Anúncio que leva pro feed em vez de levar pro serviço.', 'Orçamento mandado de um e-mail @gmail.', 'WhatsApp pessoal, sem horário e sem catálogo.', 'Site de 2019 que ninguém sabe quem tem a senha.'];
  return (
    <Slide n={6} total={T}>
      <div style={{display: 'grid', gap: 30}}>
        <In d={200} as="h2" className="titulo">O que já não segura empresa nenhuma:</In>
        <div style={{marginTop: 10}}>
          {mortos.map((m, i) => (
            <In key={m} d={600 + i * 150} style={{padding: '28px 0', borderTop: `1px solid ${TOKENS.line}`, borderBottom: i === 4 ? `1px solid ${TOKENS.line}` : undefined, font: '400 38px/1.3 "Inter Tight"', letterSpacing: '-.01em'}}>
              <Riscado d={1700 + i * 350}>{m}</Riscado>
            </In>
          ))}
        </div>
        <Palavras className="titulo ink" texto="O cliente mudou o jeito de procurar" d={3900} passo={90} pt />
      </div>
    </Slide>
  );
};

const Holofote: React.FC = () => {
  const f = useCurrentFrame();
  const x = interpolate(f, [q(1600), q(1600) + 135], [-200, 520], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const o = interpolate(f, [q(1600), q(1600) + 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{position: 'absolute', zIndex: 0, width: 900, height: 700, left: -110, top: 600, opacity: o, transform: `translateX(${x}px)`, background: 'radial-gradient(closest-side, rgba(220,220,220,.09), transparent)'}} />;
};

export const M07: React.FC = () => (
  <Slide n={7} total={T} extra={<Holofote />}>
    <div style={{display: 'grid', gap: 40, position: 'relative', zIndex: 1}}>
      <In d={200} className="lead">Você investiu no ponto, na fachada, na vitrine e no móvel pra ser encontrado na rua.</In>
      <In d={800} className="corpo">Aparição cobra de novo toda vez que acontece, enquanto um endereço continua trabalhando no mês em que você não pagou nada.</In>
      <Risca d={1300} />
      <Palavras as="h2" className="frase" texto="Você está pagando aluguel na rua e morando de favor na internet" d={1700} passo={140} pt style={{fontSize: 100, lineHeight: 0.98}} />
    </div>
  </Slide>
);

export const M08: React.FC = () => {
  const etapas = [['01 / Ponto', 'A empresa ganha endereço próprio e passa a ser encontrada.'], ['02 / Movimento', 'O endereço passa a receber gente, com conteúdo e anúncio que levam pra dentro.'], ['03 / Atendimento', 'Quem chega é recebido na hora, até fora do seu horário.']];
  const f = useCurrentFrame();
  return (
    <Slide n={8} total={T}>
      <div style={{display: 'grid', gap: 46}}>
        <In d={200} as="h2" className="titulo">O Endereço Fixo tem três etapas, nessa ordem:</In>
        <div>
          {etapas.map(([r, t], i) => {
            const d = 900 + i * 1100;
            const desce = interpolate(f, [q(d + 500), q(d + 500) + 27], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
            return (
              <div key={r} style={{display: 'grid', gridTemplateColumns: '44px 1fr', gap: 34}}>
                <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                  <Acende d={d} size={26} halo style={{marginTop: 4}} />
                  {i < 2 ? <b style={{width: 1, flex: 1, background: 'rgba(255,255,255,.26)', marginTop: 14, transformOrigin: 'top', transform: `scaleY(${desce})`}} /> : null}
                </div>
                <In d={d} style={{paddingBottom: i < 2 ? 52 : 0, display: 'grid', gap: 16}}>
                  <span className="rotulo" style={{fontSize: 24, color: TOKENS.mute}}>{r}</span>
                  <p style={{font: '400 38px/1.3 "Inter Tight"', letterSpacing: '-.01em'}}>{t}</p>
                </In>
              </div>
            );
          })}
        </div>
        <Palavras className="sub" texto="Três peças. Cada uma só funciona porque a anterior existe" d={4100} passo={80} pt />
      </div>
    </Slide>
  );
};

const Odo: React.FC<{d: number; digitos: number[]}> = ({d, digitos}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [q(d), q(d) + 54], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (t) => 1 - Math.pow(1 - t, 4)});
  return (
    <span style={{display: 'inline-flex', height: '1em', overflow: 'hidden', lineHeight: '1em'}}>
      <span style={{display: 'flex', flexDirection: 'column', transform: `translateY(${-(digitos.length - 1) * p}em)`}}>
        {digitos.map((n, i) => <span key={i} style={{height: '1em', lineHeight: '1em', display: 'block'}}>{n}</span>)}
      </span>
    </span>
  );
};

export const M09: React.FC = () => (
  <Slide n={9} total={T}>
    <div style={{display: 'grid', gap: 30}}>
      <In d={200} className="lead">A primeira etapa fica pronta em</In>
      <In d={400} style={{font: '700 260px/1 "Archivo"', fontStretch: '106%', letterSpacing: '-.045em', display: 'flex', alignItems: 'baseline', marginTop: 10}}>
        <Odo d={600} digitos={[0, 1]} /><Odo d={600} digitos={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]} />
        <Fade d={1700} style={{marginLeft: '.22em'}}>dias</Fade>
      </In>
      <In d={1900} className="lead ink">corridos.</In>
      <Risca d={2400} style={{marginTop: 20}} />
      <In d={2700} className="corpo">Se eu passar disso por atraso meu, você paga só metade da segunda parcela.</In>
      <Palavras className="titulo" texto="O risco do prazo é meu" d={3400} passo={110} pt />
    </div>
  </Slide>
);

export const M10: React.FC = () => {
  const f = useCurrentFrame();
  const ciclo = (f % 48) / 48;
  const empurra = ciclo < 0.3 ? (ciclo / 0.3) * 7 : ciclo < 0.55 ? 7 * (1 - (ciclo - 0.3) / 0.25) : 0;
  const itens = ['domínio registrado no seu nome', 'site com SEO local, ligado na ficha do Google', 'ficha do Google completa', 'e-mail profissional no seu domínio', 'WhatsApp Business e redes sociais padronizados'];
  return (
    <Slide n={10} total={T}>
      <div style={{display: 'grid', gap: 36}}>
        <In d={200} className="lead">O Ponto Digital instala na sua empresa:</In>
        <In d={450} className="card" style={{padding: '44px 48px'}}>
          <Luz />
          <ul className="lista">{itens.map((t, i) => <In key={t} as="li" d={700 + i * 180}>{t}</In>)}</ul>
        </In>
        <Palavras className="sub" texto="Quer saber quais portas estão fechadas na sua?" d={1900} passo={80} />
        <div style={{display: 'grid', gap: 24, justifyItems: 'start', marginTop: 8}}>
          <In d={2800} className="pilula">Comente PONTO<span className="chip" style={{transform: `translateX(${empurra}px)`}}>{SETA}</span></In>
          <In d={3100} className="corpo">que eu faço o teste na sua empresa e te mando o resultado no direct.</In>
        </div>
      </div>
    </Slide>
  );
};

export const SLIDES = [M01, M02, M03, M04, M05, M06, M07, M08, M09, M10];
/** duração de cada slide em quadros (30 fps), igual à versão HTML */
export const DURACAO = [195, 180, 210, 195, 195, 195, 210, 195, 180, 195];
