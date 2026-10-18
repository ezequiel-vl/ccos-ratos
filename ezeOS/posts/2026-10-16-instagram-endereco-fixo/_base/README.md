# Base dos carrosséis do lançamento

CSS, JS e logo compartilhados pelos carrosséis desta pasta (`metodo/`, `isca/`, `vida-depois/`, `solucoes/`, `vendas/`). O Manifesto tem a cópia própria dele em `manifesto/instagram/`, de antes desta base existir.

- `slides.css`: tokens da casa (preto, cinzas, ponto azul `--sinal` só no ponto final dos títulos), tipografia, fundo com grão, lanterna, animações de entrada e os componentes de cada carrossel (portas, linha do tempo, antes/depois, prédio, recibo, barra dos 10 dias)
- `slides.js`: quebra títulos em palavras e textos em letras pra animar
- `assets/logo-branco.png`: logo com ponto azul

Cada slide é um HTML de 1080x1350 em `<carrossel>/instagram/slide-XX.html`, com a duração do vídeo em `<body data-duracao="...">`. Mudou o texto ou o visual? Edita o HTML (ou o CSS daqui, que muda todos) e renderiza de novo:

```
node .claude/skills/carrossel/scripts/render-motion.js <pasta>/instagram all both
```

Saem `slide-XX.png` (último quadro) e `slide-XX.mp4` (com motion; fora do git). Depois, `calendario/gerar.py` leva os novos pro calendário publicado.
