# Fundo
O chão escuro da casa: brilho suave no topo e grão a 15% por cima de tudo.

Aplique `eze-chao` no elemento que é a página (no site, o `body`). O cinza que se vê não é a cor do fundo: `bg` continua `#0a0a0a`, e o cinza vem das duas camadas.

- **Brilho:** radial de 70% × 55% em `50% 12%`, cor `brilho`. Só aparece no tema escuro.
- **Grão:** ruído fractal em SVG, opacidade `opacidade-grao`, z-index `z-grao`, sem receber clique. No site é uma camada `position: fixed` no `body::after`; dentro de um bloco, `absolute`.

**O consumidor fornece** o conteúdo da página dentro do chão.

**Faça**: use em toda peça escura (site, carrossel, slide, capa de proposta). Nos PNGs do carrossel o grão sai normal, porque o render é de navegador.

**Não faça**: grão no tema claro (proposta, documento); gradiente colorido no lugar do brilho; grão acima de 15%, que suja o texto.
