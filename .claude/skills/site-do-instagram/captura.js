// Rodar com javascript_tool na página do perfil (instagram.com/<user>/).
// 1) Coleta o grid inteiro: window._g = [[href, {src}], ...] na ordem do feed.
await new Promise(r => setTimeout(r, 2500));
const seen = new Map();
for (let i = 0; i < 14; i++) {
  document.querySelectorAll('a[href*="/p/"],a[href*="/reel/"]').forEach(a => {
    const img = a.querySelector('img'); const href = a.getAttribute('href');
    if (img && !seen.has(href)) seen.set(href, { src: img.src, alt: img.alt });
  });
  window.scrollBy(0, 1400); await new Promise(r => setTimeout(r, 1300));
}
window._g = [...seen.entries()];

// 2) Overlay preto em tela cheia pra capturar uma imagem.
let o = document.getElementById('_ov');
if (!o) { o = document.createElement('div'); o.id = '_ov'; o.style.cssText = 'position:fixed;inset:0;background:#000;z-index:999999;overflow:hidden'; document.body.appendChild(o); }

// _showW(i, largura_css, deslocamento_css) -> "i:LxA hAltura_exibida"
// Retrato: largura = 738 * L / A (cabe na altura da tela, 1 tile).
// Alta (9:16, empilhado): largura 700, tiles em deslocamento 0 e altura-738.
window._showW = function (i, w, off) {
  const o = document.getElementById('_ov'); o.innerHTML = '';
  const im = new Image(); im.src = window._g[i][1].src;
  im.style.cssText = 'position:absolute;left:0;top:' + (-off) + 'px;width:' + w + 'px;height:auto;max-width:none';
  o.appendChild(im);
  return new Promise(r => { const f = () => r(i + ':' + im.naturalWidth + 'x' + im.naturalHeight + ' h' + Math.round(w * im.naturalHeight / im.naturalWidth)); im.onload = f; if (im.complete) f(); });
};

// Legendas pra ler com get_page_text (a saída do javascript_tool corta):
// const m=document.querySelector('main');m.innerHTML='';const a=document.createElement('article');a.style.whiteSpace='pre-wrap';
// a.textContent=window._g.map(([h,o],i)=>'#'+i+' '+h+' | '+(o.alt||'').replace(/\s+/g,' ').slice(0,400)).join('\n');m.appendChild(a);
window._g.length;
