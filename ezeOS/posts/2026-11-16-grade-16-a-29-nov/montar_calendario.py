"""Monta o calendário visual da grade 16-29/11 (perfil simulado no celular), no mesmo formato
da apresentação da 8Sec, e grava em _publicado/ezeos-grade-nov/index.html.

  python montar_calendario.py
As mídias (media/) já ficam em _publicado/ezeos-grade-nov/media. Depois: deploy do _publicado no Cloudflare.
"""
import json
import os
import re

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))
BASE = os.path.join(RAIZ, "clientes/FernandoMorinelli/conteudo/2026-10-27-8sec-instagram/apresentacao/index.html")
SAIDA = os.path.join(RAIZ, "_publicado/ezeos-grade-nov/index.html")
AQUI = os.path.dirname(os.path.abspath(__file__))


def leg(pasta):
    p = os.path.join(AQUI, pasta, "legenda.txt")
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else ""


POSTS = [
    {"id": "botao", "tipo": "Carrossel", "titulo": "Pra onde vai o botão \"Site\" da sua ficha", "quando": "seg 16/11 · 07h30", "n": 8, "st": "ag",
     "obj": "Mostrar os três destinos do botão \"Site\" (nada, Instagram, página própria) e fazer a pessoa testar a própria ficha.", "legenda": leg("01-botao-site")},
    {"id": "reel6", "tipo": "Reel", "titulo": "Reel · A clínica que só tinha Instagram", "quando": "ter 17/11 · 19h30", "reel": "06", "st": "ag",
     "obj": "Case real em 15s: a ficha sem site, o site da Dra. Renata rolando no celular, a ficha com o botão \"Site\" ligado.", "legenda": leg("02-reel-renata")},
    {"id": "cinco", "tipo": "Carrossel", "titulo": "As 5 respostas que o paciente procura", "quando": "qui 19/11 · 07h30", "n": 7, "st": "ag",
     "obj": "Conteúdo de valor pra clínica: procedimento, quem atende, onde fica, como funciona e como agendar.", "legenda": leg("03-cinco-respostas")},
    {"id": "reel-busca", "tipo": "Reel", "titulo": "Reel · Busquei \"harmonização\" na sua cidade", "quando": "sáb 21/11 · 10h", "st": "prod",
     "obj": "Gravação de uma busca real: quem aparece primeiro, quem tem site, quem leva pro Instagram. Nomes borrados.", "legenda": "Comente: PONTO"},
    {"id": "carrossel2", "tipo": "Carrossel", "titulo": "Case · A clínica que só tinha Instagram", "quando": "seg 23/11 · 07h30", "n": 9, "st": "ag", "video1": True,
     "obj": "Case da Dra. Renata Oliveira (autorizado em 13/11). O 1º slide é um vídeo: as seções do site entram como abas e revelam a capa. Depois, o site no celular, seção por seção, e a ficha do Google com o botão Site.", "legenda": leg("02b-carrossel-renata")},
    {"id": "reel7", "tipo": "Reel", "titulo": "Reel · Seu Instagram é alugado", "quando": "ter 24/11 · 19h30", "reel": "07", "st": "ag",
     "obj": "Adaptado da referência \"Instagram não é site\": 4 motivos (a conta pode cair, o algoritmo escolhe quem vê, o Google não acha perfil, o feed perde a informação) e o fecho dos três andares.", "legenda": leg("06-reel-alugado")},
    {"id": "entra", "tipo": "Carrossel", "titulo": "O que entra num site de clínica", "quando": "qui 26/11 · 07h30", "n": 8, "st": "ag",
     "obj": "Escopo honesto do site: o que traz paciente e o que é enfeite. Fecha com tudo no nome da cliente.", "legenda": leg("07-o-que-entra")},
    {"id": "reel8", "tipo": "Reel", "titulo": "Reel · Quando o paciente pede o seu site", "quando": "sáb 28/11 · 10h", "reel": "08", "st": "ag",
     "obj": "Adaptado da referência \"Quando pedem o seu site, o que você manda?\": conversa no WhatsApp, o link do Instagram riscado e o site real da Renata no lugar.", "legenda": leg("08-reel-pediu-site")},
]
ANTIGOS = [  # feed já publicado, do mais novo pro mais antigo (só capa)
    {"img": "media/reels/05.jpg", "reel": True}, {"img": "media/antigo-vendas.jpg"}, {"img": "media/reels/04.jpg", "reel": True},
    {"img": "media/antigo-solucoes.jpg"}, {"img": "media/reels/03.jpg", "reel": True}, {"img": "media/antigo-vida-depois.jpg"},
    {"img": "media/antigo-isca.jpg"}, {"img": "media/reels/02.jpg", "reel": True}, {"img": "media/antigo-metodo.jpg"},
    {"img": "media/reels/01.jpg", "reel": True}, {"img": "media/antigo-manifesto.jpg"},
]


def montar():
    html = open(BASE, encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    # marca: tokens da ezeOS (preto, cinza e ponto azul no lugar do ouro)
    css = re.sub(r":root \{.*?\n\}", """:root {
  --coal: #0A0A0A; --coal-2: #141414; --stone: #ECECEA; --stone-2: #F6F6F4; --stone-3: #D6D6D2;
  --gold: #48A0C7; --gold-deep: #2B6F8E; --ink: #0A0A0A; --ink-mut: #555;
  --line: rgba(10,10,10,.12);
  --ig-text: #000; --ig-mut: #737373; --ig-line: #DBDBDB; --ig-blue: #0095F6;
  --display: "Archivo", system-ui, sans-serif; --sans: "Inter Tight", "Segoe UI", Arial, sans-serif;
  --ig: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --ease: cubic-bezier(.16,1,.3,1);
}""", css, count=1, flags=re.S)
    css = css.replace(".lista h1 { font-family: var(--display); font-weight: 400;", ".lista h1 { font-family: var(--display); font-weight: 700; letter-spacing: -.02em;")
    css = css.replace(".notas h2 { font-family: var(--display); font-weight: 400;", ".notas h2 { font-family: var(--display); font-weight: 700; letter-spacing: -.02em;")
    css += """
.lista__marca img { height: 26px; filter: none; }
.avatar img, .post__cab .mini img, .reel__info .quem img, .navbar .eu img { filter: none; }
.avatar img { width: 66px; } .post__cab .mini img { width: 24px; } .reel__info .quem img { width: 22px; } .navbar .eu img { width: 18px; }
.item__st.ag { background: #4CAF7A; } .item__st.alt { background: #48A0C7; } .item__st.prod { background: #E0952E; }
.item__q { font-variant-numeric: tabular-nums; }
.tile__prod { position: absolute; inset: 0; display: grid; place-items: center; text-align: center; padding: 10px; background: #1C1C1C; color: #A6A6A6; font: 600 11px/1.3 var(--sans); letter-spacing: .04em; }
.tile__novo { position: absolute; left: 6px; bottom: 6px; background: var(--gold); color: #fff; font: 700 10px/1 var(--sans); padding: 4px 6px; border-radius: 6px; letter-spacing: .03em; }
.tile--antigo { opacity: .55; }
.item.is-on { background: rgba(72,160,199,.16); }
.emprod { position: absolute; inset: 0; display: grid; place-items: center; text-align: center; padding: 40px; background: #111; color: #A6A6A6; font: 500 15px/1.5 var(--sans); }
.emprod b { display: block; color: #fff; font: 700 20px/1.2 var(--display); margin-bottom: 10px; }
.semana { font: 600 11px/1 var(--sans); letter-spacing: .2em; text-transform: uppercase; color: #8C8C8C; margin: 16px 8px 6px; }
"""
    dados = json.dumps(POSTS, ensure_ascii=False)
    antigos = json.dumps(ANTIGOS, ensure_ascii=False)
    pagina = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ezeOS · Calendário 16 a 29/11</title>
<meta name="robots" content="noindex">
<link rel="icon" href="media/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="app">
  <aside class="lista" aria-label="Calendário de publicação">
    <div class="lista__marca"><img src="media/logo-branco.png" alt="ezeOS"><span>Instagram</span></div>
    <h1>Calendário de 16 a 29/11</h1>
    <p class="lista__sub">8 publicações em 2 semanas, na ordem em que vão pro ar. Verde: agendado. Laranja: em produção. Azul: versão pra escolher.</p>
    <div class="lista__itens" id="lista"></div>
    <p class="lista__nota">Foco das duas semanas: clínica e consultório. Toda peça termina com <b>Comente PONTO</b>. Nenhuma mostra preço.</p>
  </aside>
  <main class="palco">
    <div class="celular"><div class="tela" id="tela"><span class="ilha" aria-hidden="true"></span></div></div>
    <a class="voltar-feed" id="voltarFeed" href="#/" hidden><svg class="ic" viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>Voltar ao feed</a>
    <p class="palco__dica" id="dica">Clique numa imagem do feed pra abrir o post.</p>
  </main>
  <section class="notas" id="notas" aria-live="polite"></section>
</div>
<script>
const PERFIL = {{
  user: 'agenciaezeos', nome: 'ezeOS | A gente instala sua empresa no digital', cat: 'Agência de marketing',
  bio: 'Site, ficha do Google, e-mail no domínio e WhatsApp configurados de verdade.\\nPra negócio local que atende presencialmente.',
  link: 'ezeos.com.br', destaques: ['Ponto', 'Cases', 'Como funciona', 'Teste'],
}};
const POSTS = {dados};
const ANTIGOS = {antigos};
const LOGO = 'media/logo-branco.png';
const capa = p => p.reel ? `media/reels/${{p.reel}}.jpg` : (p.n ? `media/${{p.id}}/01.jpg` : '');
const ST = {{ ag: 'Agendado', prod: 'Em produção', alt: 'Versão pra escolher' }};
"""
    # reaproveita ícones e utilitários do script original
    script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    icones = re.search(r"(/\* ---------- ícones.*?)/\* ---------- lista ---------- \*/", script, re.S).group(1)
    icones = icones.replace("media/8sec-mark.png", "${LOGO}").replace("<span class=\"eu\"><img src=\"${LOGO}\" alt=\"\"></span>", "<span class=\"eu\"><img src=\"${LOGO}\" alt=\"\"></span>")
    carrossel = re.search(r"(/\* ---------- carrossel ---------- \*/.*?)/\* ---------- rotas ---------- \*/", script, re.S).group(1)
    pagina += icones + r"""
/* ---------- lista ---------- */
const lista = document.getElementById('lista');
lista.innerHTML = `<a class="item item--feed" href="#/" data-id=""><span>${I.feed}</span><span class="item__t">Ver o feed completo</span></a>` +
  POSTS.map((p, i) => (i === 0 ? '<p class="semana">Semana 1</p>' : i === 4 ? '<p class="semana">Semana 2</p>' : '') +
  `<a class="item" href="#/post/${p.id}" data-id="${p.id}">
<span class="item__n">${i + 1}</span><span class="item__thumb">${capa(p) ? `<img src="${capa(p)}" alt="" loading="lazy">` : ''}</span>
<span><span class="item__t">${esc(p.titulo)}</span><span class="item__m"><b class="item__q">${p.quando}</b><span>${p.tipo}${p.n ? ` · ${p.n} slides` : ''}</span></span></span><span class="item__st ${p.st}" aria-hidden="true"></span></a>`).join('');

/* ---------- vistas ---------- */
const tela = document.getElementById('tela');
const notas = document.getElementById('notas');
const voltarFeed = document.getElementById('voltarFeed');
const dica = document.getElementById('dica');
let posFeed = 0;

function tileNovo(p) {
  const img = capa(p);
  return `<a class="tile" href="#/post/${p.id}" aria-label="${esc(p.titulo)}">${img ? `<img src="${img}" alt="" loading="lazy">` : `<span class="tile__prod">EM PRODUÇÃO<br>${p.quando}</span>`}
<span class="tile__ic">${p.reel || p.tipo === 'Reel' ? I.reelTile : I.pilha}</span><span class="tile__novo">${p.quando.split(' · ')[0]}</span></a>`;
}
function vistaFeed() {
  const novos = [...POSTS].filter(p => p.st !== 'alt').reverse();
  tela.innerHTML = `<span class="ilha" aria-hidden="true"></span><div class="vista">${status()}
<div class="topo"><strong>${PERFIL.user}${I.seta}</strong><span class="acoes">${I.mais}${I.menu}</span></div>
<div class="rolagem" id="rol">
<div class="perfil">
<div class="perfil__linha"><span class="avatar"><img src="${LOGO}" alt="ezeOS"></span>
<div class="stats"><span><b>${POSTS.length + ANTIGOS.length + 4}</b>posts</span><span><b>·</b>seguidores</span><span><b>·</b>seguindo</span></div></div>
<p class="perfil__nome">${esc(PERFIL.nome)}</p><p class="perfil__cat">${PERFIL.cat}</p>
<p class="perfil__bio">${esc(PERFIL.bio)}</p>
<p class="perfil__link">${I.link}${PERFIL.link}</p>
<div class="botoes"><span class="seguir">Seguir</span><span>Mensagem</span><span>${I.seta}</span></div></div>
<div class="destaques">${PERFIL.destaques.map(d => `<span class="destaque"><i><img src="${LOGO}" alt="" style="width:40px"></i>${d}</span>`).join('')}</div>
<div class="abas"><span class="is-on">${I.grade}</span><span>${I.reels}</span><span>${I.marcado}</span></div>
<div class="grade">${novos.map(tileNovo).join('')}${ANTIGOS.map(a => `<span class="tile tile--antigo"><img src="${a.img}" alt="" loading="lazy"><span class="tile__ic">${a.reel ? I.reelTile : I.pilha}</span></span>`).join('')}</div>
</div>${navbar()}</div>`;
  const rol = document.getElementById('rol'); rol.scrollTop = posFeed;
  rol.addEventListener('scroll', () => { posFeed = rol.scrollTop; }, { passive: true });
  voltarFeed.hidden = true;
  dica.textContent = 'Clique numa imagem do feed pra abrir o post.';
  const ag = POSTS.filter(p => p.st === 'ag').length;
  notas.innerHTML = `<p class="notas__tipo">Visão geral</p><h2>O feed da ezeOS no fim de novembro</h2>
<div class="notas__bloco"><h3>Situação</h3><ul class="resumo"><li><span>Agendados na Zernio</span><b>${ag}</b></li><li><span>Em produção</span><b>${POSTS.length - ag}</b></li><li><span>Ritmo</span><b>4 por semana</b></li></ul></div>
<div class="notas__bloco notas__geral"><h3>Como ler</h3><p>Os 8 posts novos aparecem no topo com a data de publicação. Os mais apagados, embaixo, são os do lançamento, que já estão no ar.</p><p>Foco em clínica e consultório, que é a frente da prospecção. Toda peça leva pro PONTO: o diagnóstico das quatro portas no direct.</p></div>
<div class="notas__bloco"><h3>Prova real</h3><p>O Reel de 17/11 e o carrossel de 23/11 usam o site da Dra. Renata Oliveira, com autorização.</p></div>`;
}

function vistaPost(p) {
  pararVideos();
  if (p.tipo === 'Reel') return vistaReel(p);
  const slides = Array.from({ length: p.n }, (_, i) => String(i + 1).padStart(2, '0'));
  tela.innerHTML = `<span class="ilha" aria-hidden="true"></span><div class="vista">${status()}
<a class="voltar-ig" href="#/">${I.voltar}<span>Publicações</span></a>
<div class="rolagem">
<div class="post__cab"><span class="mini"><img src="${LOGO}" alt=""></span><span><b>${PERFIL.user}</b><small>Canoas, Rio Grande do Sul</small></span><span class="mais">${I.pontos}</span></div>
<div class="midia" id="midia" aria-roledescription="carrossel" aria-label="${esc(p.titulo)}">
<div class="trilho" id="trilho">${slides.map(n => (p.video1 && n === '01' ? `<div class="slide"><video src="media/${p.id}/01.mp4" poster="media/${p.id}/01.jpg" muted playsinline loop autoplay></video></div>` : `<div class="slide"><img src="media/${p.id}/${n}.jpg" alt="Slide ${+n} de ${p.n}" ${n === '01' ? '' : 'loading="lazy"'} draggable="false"></div>`)).join('')}</div>
<span class="contador" id="cont">1/${p.n}</span>
<button class="seta seta--ant" id="ant" aria-label="Slide anterior" hidden>${I.ant}</button>
<button class="seta seta--prox" id="prox" aria-label="Próximo slide">${I.prox}</button></div>
<div class="post__acoes">${I.coracao}${I.comentario}${I.enviar}<span class="pontos" id="pontos">${slides.map((_, i) => `<i${i ? '' : ' class="is-on"'}></i>`).join('')}</span><span class="salvar">${I.salvar}</span></div>
<p class="post__texto"><b>${PERFIL.user}</b> ${esc(p.legenda).replace(/\n/g, '<br>').replace('PONTO', '<span class="pc">PONTO</span>')}<small>${p.quando} · ${ST[p.st]}</small></p>
</div>${navbar()}</div>`;
  carrossel(p.n);
  depoisDeAbrir(p);
}

function vistaReel(p) {
  const corpo = p.reel
    ? `<video id="reelVid" src="media/reels/${p.reel}.mp4" poster="media/reels/${p.reel}.jpg" muted playsinline loop autoplay></video>`
    : `<div class="emprod"><div><b>Em produção</b>${esc(p.obj)}<br><br>Sai ${p.quando}.</div></div>`;
  tela.innerHTML = `<span class="ilha" aria-hidden="true"></span><div class="reel">${corpo}
${status('#fff')}<div class="reel__topo"><a href="#/" aria-label="Voltar ao feed" style="display:flex;gap:10px;align-items:center;text-decoration:none">${I.voltar}Reels</a>${I.busca}</div>
<div class="reel__lado" aria-hidden="true"><span>${I.coracao}</span><span>${I.comentario}</span><span>${I.enviar}</span><span>${I.pontos}</span></div>
<div class="reel__info"><div class="quem"><i><img src="${LOGO}" alt=""></i>${PERFIL.user}<span>Seguir</span></div>${esc(p.legenda.split('\n')[0])}</div>
${navbar()}</div>`;
  const v = document.getElementById('reelVid'); if (v) { const r = v.play(); if (r && r.catch) r.catch(() => {}); }
  depoisDeAbrir(p);
}

function depoisDeAbrir(p) {
  voltarFeed.hidden = false;
  dica.textContent = p.tipo === 'Reel' ? (p.reel ? 'O Reel toca em loop, sem som.' : 'Esse Reel ainda está em produção.') : 'Use as setas, as teclas ← → ou arraste pra passar os slides.';
  const i = POSTS.indexOf(p), ant = POSTS[i - 1], prox = POSTS[i + 1];
  notas.innerHTML = `<p class="notas__tipo"><span>Post ${i + 1} de ${POSTS.length}</span><span>·</span><span>${p.tipo}</span></p>
<h2>${esc(p.titulo)}</h2><span class="selo ${p.st === 'ag' ? 'ok' : 'aj'}">${ST[p.st]} · ${p.quando}</span><p class="notas__obj">${esc(p.obj)}</p>
<div class="navpost"><a href="${ant ? `#/post/${ant.id}` : '#/'}" aria-disabled="${!ant}">← Anterior</a><a href="${prox ? `#/post/${prox.id}` : '#/'}" aria-disabled="${!prox}">Próximo →</a></div>
<div class="notas__bloco"><h3>Legenda</h3><p>${esc(p.legenda)}</p></div>
<div class="notas__bloco"><h3>Palavra-chave</h3><span class="notas__pc">PONTO</span></div>`;
}

""" + carrossel + r"""
/* ---------- rotas ---------- */
function rota() {
  const m = location.hash.match(/^#\/post\/([\w-]+)/);
  const p = m && POSTS.find(x => x.id === m[1]);
  document.querySelectorAll('.item').forEach(a => a.classList.toggle('is-on', a.dataset.id === (p ? p.id : '')));
  if (p) vistaPost(p); else { pararVideos(); vistaFeed(); }
  notas.scrollTop = 0;
  const ativo = document.querySelector('.item.is-on');
  if (ativo && window.matchMedia('(max-width: 820px)').matches) ativo.scrollIntoView({ inline: 'center', block: 'nearest' });
}
window.addEventListener('hashchange', rota);
rota();
</script>
</body>
</html>
"""
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(pagina)
    print("ok", SAIDA, len(pagina))


if __name__ == "__main__":
    montar()
