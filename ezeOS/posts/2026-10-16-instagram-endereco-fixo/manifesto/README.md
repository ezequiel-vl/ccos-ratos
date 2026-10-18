# Manifesto: carrossel pronto

Texto aprovado em `../02-manifesto.md` (10 cards, sem o 4b de prova). Visual no sistema escuro da casa: Archivo, Inter Tight e JetBrains Mono, fundo com brilho e grão, ponto cinza no fim de cada título, lanterna nos cards.

## Arquivos

Em `instagram/`, cada slide tem três versões:

- `slide-XX.mp4`: com motion, 6 a 7 segundos, 1080x1350, H.264. Fica só na máquina (`*.mp4` está no `.gitignore`); se sumir, renderiza de novo a partir do HTML
- `slide-XX.png`: estático, o último quadro da animação
- `slide-XX.html`: a fonte. Muda aqui e renderiza de novo

## Como postar

O Instagram aceita vídeo dentro do carrossel. Duas formas:

1. **Tudo em vídeo:** sobe os 10 MP4 na ordem. Cada slide anima quando a pessoa chega nele. É a versão recomendada.
2. **Misto:** capa (slide 1) em MP4, porque é ela que para a rolagem do feed, e o resto em PNG. Fica mais leve se a internet estiver ruim na hora de subir.

Sem música. Se o Instagram pedir, escolhe uma faixa instrumental e deixa o volume em zero.

Legenda: está em `../02-manifesto.md`, seção Legenda.

## O que cada slide anima

| Slide | Motion |
| --- | --- |
| 01 Capa | título surge palavra por palavra, painel do navegador monta em perspectiva, endereço digitado letra por letra, "NO AR" acende |
| 02 Aparição | visualização, post, story e anúncio são riscados um por um |
| 03 A prova | a busca é digitada na barra e os resultados aparecem |
| 04 O outro lado | os cinco itens da ficha acendem em sequência |
| 05 Conexão | a frase do dono surge palavra por palavra, a sequência de tentativas entra linha a linha |
| 06 O que morreu | cada prática é riscada e apaga |
| 07 O princípio | um holofote varre a frase do aluguel enquanto ela surge |
| 08 O método | as etapas acendem em ordem e a linha desce de uma pra outra |
| 09 Garantia | o contador rola até 10 dias |
| 10 CTA | a lista entra item por item e a seta do "Comente PONTO" pulsa |

Em todos: o grão do fundo se mexe, como filme, e a luz dos cards anda devagar.

## Renderizar de novo

Script: `.claude/skills/carrossel/scripts/render-motion.js`. Ele pausa as animações CSS e fotografa quadro a quadro, então o vídeo sai idêntico ao HTML. Dependências e uso estão no topo do arquivo.
