// Estilo estático da casa (tokens do design-guide). Nada de animação CSS aqui:
// no Remotion todo movimento vem do quadro atual (src/base/motion.tsx).
export const TOKENS = {
  bg: '#0A0A0A', surface: '#141414', raised: '#1C1C1C', sunk: '#101010',
  ink: '#F4F4F4', mute: '#A6A6A6', faint: '#8C8C8C',
  line: 'rgba(255,255,255,.10)', line2: 'rgba(255,255,255,.16)',
  dot: '#A6A6A6', dotOff: '#3A3A3A', skel: '#262626', sinal: '#48A0C7',
};

export const FONTES_URL =
  'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=Inter+Tight:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=block';

export const CSS = `
*{box-sizing:border-box; margin:0; padding:0}
.eze{color:${TOKENS.ink}; font-family:"Inter Tight", system-ui, sans-serif; -webkit-font-smoothing:antialiased; text-rendering:geometricPrecision}
.slide{position:absolute; inset:0; padding:84px 88px 76px; display:flex; flex-direction:column; overflow:hidden;
  background:radial-gradient(70% 55% at 50% 12%, rgba(210,210,210,.08), transparent 72%) no-repeat, ${TOKENS.bg}}
.topo{display:flex; justify-content:space-between; align-items:center; height:40px; flex:none}
.topo img{height:36px; width:auto; display:block}
.miolo{flex:1; display:flex; flex-direction:column; justify-content:center; min-height:0}
.base{display:flex; justify-content:space-between; align-items:center; flex:none; height:24px}
.prog{display:flex; gap:10px}
.prog i{width:9px; height:9px; border-radius:50%; background:${TOKENS.dotOff}}
.prog i.on{background:${TOKENS.dot}}
.handle{font:400 22px/1 "JetBrains Mono", monospace; letter-spacing:.02em; color:${TOKENS.faint}}
.rotulo{font:500 21px/1 "JetBrains Mono", monospace; letter-spacing:.14em; text-transform:uppercase; color:${TOKENS.faint}}
.hero{font:700 168px/.92 "Archivo", sans-serif; font-stretch:106%; letter-spacing:-.04em}
.frase{font:600 92px/1 "Archivo", sans-serif; font-stretch:106%; letter-spacing:-.04em; text-wrap:balance}
.titulo{font:600 64px/1.06 "Archivo", sans-serif; font-stretch:106%; letter-spacing:-.035em; text-wrap:balance}
.sub{font:600 46px/1.12 "Archivo", sans-serif; font-stretch:106%; letter-spacing:-.03em; text-wrap:balance}
.lead{font:400 40px/1.32 "Inter Tight", sans-serif; letter-spacing:-.015em; color:${TOKENS.mute}; text-wrap:pretty}
.corpo{font:400 34px/1.45 "Inter Tight", sans-serif; letter-spacing:-.01em; color:${TOKENS.mute}; text-wrap:pretty}
.ink{color:${TOKENS.ink}}
.pt{color:${TOKENS.sinal}}
.linha{height:1px; background:${TOKENS.line}; transform-origin:left center}
.card{position:relative; isolation:isolate; background:${TOKENS.surface}; border:1px solid ${TOKENS.line2}; border-radius:20px; overflow:hidden}
.lista{list-style:none; display:grid; gap:20px}
.lista li{display:grid; grid-template-columns:14px 1fr; gap:20px; align-items:baseline; font:400 36px/1.3 "Inter Tight", sans-serif; color:${TOKENS.ink}; letter-spacing:-.01em}
.lista li::before{content:""; width:12px; height:12px; border-radius:50%; background:${TOKENS.dot}; transform:translateY(-4px)}
.pilula{display:inline-flex; align-items:center; gap:22px; border-radius:999px; background:${TOKENS.ink}; color:${TOKENS.bg}; padding:14px 14px 14px 40px; font:500 44px/1 "Inter Tight", sans-serif; letter-spacing:-.015em}
.pilula .chip{width:76px; height:76px; border-radius:50%; background:${TOKENS.bg}; display:grid; place-items:center}
.pilula .chip svg{width:30px; height:30px; fill:none; stroke:${TOKENS.ink}; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round}
.w{display:inline-block}
`;
