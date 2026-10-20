# Vídeos da ezeOS (Remotion)

Vídeo feito com código: cada slide ou cena é um componente React, e o Remotion renderiza em MP4. Versão fixada: **remotion 4.0.532** com React 19.3.0, instalada só nesta pasta (nada global).

## Estrutura

```
videos/
  src/
    base/estilo.ts      tokens da casa (preto, cinzas, ponto azul #48A0C7 só no ponto) e CSS estático
    base/motion.tsx     peças de movimento: In, Palavras, Digita, Riscado, Risca, Acende, Luz, Grao, Slide
    manifesto/Slides.tsx o Manifesto do Endereço Fixo (10 slides), texto igual a posts/.../02-manifesto.md
    reels/comum.tsx     peças dos reels 9:16: Reel (hook + cartão final), Celular, Toque, Rotulo
    reels/Reels.tsx     os 5 Reels ADS de posts/.../08-reels-ads.md (Reel-01 a Reel-05)
    Root.tsx            lista das composições (Manifesto-01 a 10 e Manifesto-Completo)
  public/logo-branco.png, ezeos-site-mobile.png (captura real do site, usada nos reels 2 e 4)
  remotion.config.ts    usa o Chrome headless que o Playwright já baixou; H.264, CRF 21
  out/                  vídeos renderizados (fora do git)
```

## Comandos (rodar dentro de `ezeOS/videos/`)

```
npm run studio                                   # abre o editor no navegador, com linha do tempo
npx remotion render src/index.ts Manifesto-01 out/manifesto/slide-01.mp4
npx remotion render src/index.ts Manifesto-Completo out/manifesto/manifesto-completo.mp4
npx remotion render src/index.ts Reel-01 out/reels/reel-01.mp4
npx remotion still src/index.ts Manifesto-01 out/m01.png --frame=185
```

Se a pasta `node_modules/` sumir: `npm install`.

## Regra do movimento

Nada de animação CSS: todo movimento sai do quadro atual (`useCurrentFrame`), senão o vídeo sai tremido. Os atrasos estão em milissegundos, como no HTML, e `q(ms)` converte pra quadros a 30 fps. Easing da casa: `cubic-bezier(.16, 1, .3, 1)`.

## Licença

Remotion é gratuito pra pessoa física e empresa com até 3 funcionários. Conferir em remotion.dev/license se a ezeOS crescer.
