---
name: site-do-instagram
description: >
  Monta o site de apresentação de uma profissional de estética/saúde (prospect do Ponto Digital)
  a partir do Instagram dela: lê bio, legendas e destaques, captura fotos e antes e depois, pesquisa
  no Google, clona a estrutura do site da Dra. Renata Oliveira trocando paleta, textos e fotos, monta
  a pasta da cliente com briefing e publica no Cloudflare. Use quando o Ezequiel disser "faz um site
  pra [pessoa] a partir do Instagram", "/site-do-instagram", "mesmo site da Renata pra [pessoa]",
  "vou oferecer site pra [pessoa], olha o Instagram dela", ou mandar um @ ou link de Instagram
  pedindo site de apresentação.
---

# /site-do-instagram: site de apresentação a partir do Instagram

Entrada: @ ou link do Instagram + pasta da cliente em `clientes/` (criar do `_modelo-cliente` se não existir).
Saída: `clientes/<pasta>/site/index.html` + `assets/ig/`, `briefing.md`, `CLAUDE.md`, link publicado.

Base visual e de estrutura (não reescrever do zero, clonar):
- `clientes/Dra. Renata Oliveira  Harmonização Facial/site/index.html` (original)
- `clientes/Dra Vivian Stevam/site/index.html` (já adaptado: A/D com arquivos separados, mosaico enxuto, card do Instagram)
Apoio nesta pasta: `captura.js` (visualizador de imagem no Instagram) e `costura.py` (junta tiles e limpa a costura).

## Regras que não se negociam

- Nada inventado. Texto sai das legendas dela, reescrito no tom dela. Depoimento só de print real (anônimo vira "Paciente de toxina", sem nome). Número de seguidores, credencial, formação: só o que ela publicou.
- Endereço, horário, conselho e grafia do nome sem confirmação viram **pendência** no briefing e na resposta final. Se usar um palpite no site (ex: clínica parceira), dizer qual é e por quê.
- Tom ezeOS na escrita: sem travessão, sem contraste "não é X, é Y", nada de cara de IA.
- Publicar só com ok do Ezequiel.

## 1. Pesquisa

Claude in Chrome (o Chrome dele está logado no Instagram). Carregar as ferramentas num ToolSearch só, incluindo `browser_batch`, `find`, `javascript_tool`, `get_page_text`, `tabs_close_mcp`.

1. **Perfil:** `get_page_text` em `instagram.com/<user>/` traz nome, bio, link (WhatsApp) e nomes dos destaques.
2. **Legendas de todos os posts:** rolar o grid via JS juntando `href` + `img.alt` (o alt é a legenda). A saída do `javascript_tool` corta em ~1.000 caracteres e bloqueia URL com query string, então escrever o texto dentro do `<main>` da página e ler com `get_page_text`.
3. **Não tentar** a API interna do Instagram (`/api/v1/...`): o classificador bloqueia. O embed público (`/embed/`) pede login. Curl não serve.
4. **Destaques:** abrir "Feedbacks"/"Depoimentos" e ir com `space` (pausa) + `ArrowRight`, capturando com `zoom` na faixa central. É de onde saem os depoimentos. Destaques costumam ser antigos, conferir as semanas.
5. **Google:** WebSearch com o nome (com e sem "Dra") e Google Maps no Chrome. Procurar ficha própria e clínica onde atende (collabs no Instagram dão a pista). Sem ficha = argumento do Ponto Digital.
6. Mapear: procedimentos, carro-chefe, credenciais, formação, eventos (Botox Day etc.), frases fortes, cores das artes, quais posts têm antes e depois.

## 2. Fotos

Usar o grid do perfil: as imagens do grid já vêm em 1080px ou mais. Fluxo em `captura.js`:

- Coletar `window._g` (href + src) rolando o grid. Navegar pra outra página apaga a variável, coletar de novo.
- `_showW(i, largura, deslocamento)` põe a imagem num overlay preto em tela cheia.
- Antes de capturar: `hover` no canto (1530,730), senão o cursor sai na foto.
- `zoom` com `save_to_disk:true` e `scale:1`. O arquivo salvo tem o mesmo tamanho da imagem devolvida (scale 0.5 salva pequeno). Fator real ~1.18 a 1.25 px por px de CSS.
- Imagem alta (retrato 9:16, antes e depois empilhado): mostrar com largura 700 e capturar em 2 ou 3 tiles (deslocamento 0, 506...), depois juntar com `costura.py`. A última linha de cada tile vem escura; o script já troca.
- Foto com texto por cima da arte serve só pra card pequeno; pra hero e "sobre" usar retrato limpo.
- O `img` de "foto do perfil" no cabeçalho pega o avatar de quem está logado (o Ezequiel). Avatar dela: recortar o rosto de um retrato.
- Nomear em `site/assets/ig/`: `retrato-*`, `ad-<procedimento>.jpg` (lado a lado), `ad-<proc>-antes.jpg` / `-depois.jpg`, `atendimento-*`, `cafe.jpg` etc. `og-compartilhar.jpg` 1200x630 em `assets/`.

## 3. Site

Copiar o `index.html` base pra `site/` e trocar por script (Python, como em `clientes/Dra Vivian Stevam` foi feito):

1. **Paleta:** trocar os tokens de `:root` (`--grafite`, `--marrom`, `--marrom-escuro`, `--areia`, `--off`, `--marrom-texto`, `--marrom-fundo`, `--texto-suave`, `--papel`, `--areia-funda`) e os rgba fixos do marrom. Cor tirada das artes/jaleco dela. Fontes podem ficar (Playfair + Manrope).
2. **Monograma:** letra do intro, `hero-r`, `.sobre-texto::before`, `.pilula-end i`, favicon.
3. **Head:** title, description, canonical e og apontando pra `https://ezeos-publicacoes.pages.dev/<slug>/`, JSON-LD com dados dela.
4. **Corpo** (entre `<script type="application/ld+json">` e `<script>\n(function(){`): reescrever seção por seção mantendo as classes. Hero, faixa, bento (4 cards), manifesto, fichário (abas = procedimentos dela), resultados, conversa guiada (queixas sem artigo: "lábios", "flacidez"), sobre, passos, depoimentos, dúvidas (tiradas dos posts de dúvida dela), visita com mapa (`https://www.google.com/maps?q=<endereço>&output=embed`).
5. **JS:** número do WhatsApp, mensagem padrão, chave do sessionStorage, mapa `MARCA` (chaves = `data-marca` das abas, valores = `data-q` das queixas), textos "Olá, Dra. <Nome>".
6. `assert 'Renata' not in s` no fim.
7. Otimizar: `python .claude/skills/site-do-instagram/otimizar.py clientes/<pasta>/site`. Reduz as fotos (lado maior 1200, JPG 78 progressivo), põe `width`/`height` em toda `<img>` e troca o Google Fonts por woff2 em `assets/fontes/`. Pode rodar de novo depois de trocar foto.

Armadilhas já resolvidas:
- **Slider de antes e depois (card-a3):** o original espera imagem empilhada com proporção exata. Usar `-antes.jpg` e `-depois.jpg` separados + CSS `.card-a3 .ad-camada img,.card-a3 .ad-depois img{top:0;height:100%;object-fit:cover}`.
- **Poucos antes e depois:** mosaico com `.foto.grande.inteira` (aspect 9/8) e um card `.foto-ig` levando pro Instagram. O card do Instagram **não** pode ter a classe `foto` (o zoom quebra procurando `img`).
- Card "Quem já passou por aqui": sem nota do Google, trocar o bloco `.nota` por uma credencial dela ("1ª credenciada...").

## 4. Conferir

- `python -m http.server` em segundo plano dentro de `site/` e abrir `localhost` no Chrome. O Chrome segura cache: recarregar com `?v=N`.
- Olhar: hero, bento (slider), fichário, resultados, sobre, mapa. Conferir que todo `assets/...` citado existe.
- Checagem técnica da /jury (rápida, sem crítico): com o servidor no ar, rodar de dentro de `~/.cache/jury` `node ~/.claude/skills/jury/scripts/audit.mjs http://localhost:<porta>/ --max 10`. Meta: 0 FAIL; WARN de título longo e 404 sem H1 vão como observação.
- Parar o servidor e fechar a aba no fim.

## 5. Entregar

1. `briefing.md` com dados levantados, procedimentos, tom, material disponível e **pendências**. `CLAUDE.md` copiado de `clientes/_modelo-cliente/`.
2. Perguntar se publica. Com ok: copiar `site/*` inteiro (com `assets/`) pra `_publicado/<slug>/` e seguir `/publicar-site`. Conferir com curl que página e uma imagem dão 200.
3. Resposta final: o que achou (curto), como ficou, link, e as pendências pra confirmar com ela antes de mostrar.
