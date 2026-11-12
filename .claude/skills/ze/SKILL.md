---
name: ze
description: Cria artes com o Ze, o mascote da FUIEU (pichador de balaclava preta com ponta, olhos ovais com pupila ondulada, sorrisão, moletom branco com hachura). Gera a cena no Kittl com o GPT Image 2.5 Sunburst-Max usando as referências oficiais, amplia para 4096 px, converte para preto e branco puro, cola o lettering FUIEU original e, se pedido, prepara para DTF. Use quando o Ezequiel disser "/ze", "arte com o Ze", "coloca o Ze", "cria uma cena do Ze", "o nosso personagem de balaclava", ou mandar uma imagem de referência pedindo para recriar com o personagem dele.
---

# Ze, o mascote da FUIEU

Antes de qualquer coisa, ler a ficha completa: `clientes/Fuieu/personagem-ze/ZE.md`.
Ela tem a identidade que não pode mudar, as referências aprovadas, o placar das IAs e as regras aprendidas.

Referências: `clientes/Fuieu/personagem-ze/referencias/`.

## Entrada

O Ezequiel manda uma ou mais destas coisas:
- a descrição da cena ("o Ze pintando um trem", "o Ze fugindo da polícia");
- uma imagem de referência de outro artista para recriar com o Ze (vale só pose e composição);
- uma cena anterior do Ze para continuar ("agora ele correndo depois de pintar").

Se a imagem anexada não aparecer como arquivo em `images/` da sessão, pedir para ele salvar numa pasta ou descrever a cena a partir do que dá para ver. Não travar.

## Passo a passo

### 1. Pasta
Criar `clientes/Fuieu/estampas/AAAA-MM-DD-ze-<tema>/`. Copiar a referência que ele mandou para lá como `_ref-<nome>.<ext>`.

### 2. Referências no Kittl
Workspace: `cmtlys1l12ao90jdg00ptdv3h`.

IDs que já funcionam como referência em `kittl-generate-media` (não precisa subir):
- cabeça oficial do Ze: `cmw9xb1v728eg0j9yhqnqh49u` (**mandar sempre**)
- fuieu-school (corpo inteiro, frente e costas): `cmw9vu7w722ca0j9tcatm8x6p`
- policial oficial: `cmw9zr3nm2hzc0j9y3bgt4n7f`

Referência nova (a imagem que ele mandou): `kittl-upload-image` sem `imageUrl`, depois `curl -X PUT --data-binary @arquivo -H "Content-Type: image/..." "<signedUrl>"`. Se o curl falhar com código 000, repetir com `--retry 2`.

Se um ID antigo der "not found", subir de novo o arquivo correspondente da pasta `referencias/`.

### 3. Gerar com o modelo certo
**Sempre GPT Image 2.5 Sunburst-Max**: `modelId: cmu0vtzk92sus0j83ysu7bh7v` (50 tokens, sai em 2048 px). Não testar outros modelos.

Usar o prompt base da ficha (`ZE.md`, seção "Prompt base") e preencher a cena. Pontos que sempre entram no prompt:
- balaclava SOLID BLACK com pointed tip, olhos ovais com wavy squiggly pupils, grin com vertical lines between the teeth;
- white hoodie + white sweatpants com diagonal hatching, black gloves, black sneakers com white zigzag;
- `No white outline or halo around the character`;
- `No text, no letters, no logos` (o lettering entra depois);
- com policial: `SAME SIZE as Ze` e para onde ele está olhando;
- com referência de outro artista: usar só pose e composição, sem copiar assinatura, logo, texto ou emblema.

Acompanhar com `kittl-get-media-generation-status` (leva uns 80 s; esperar com `timeout 90 sh -c 'while true; do :; done'`).

**Nano Banana 2.1 4K** (`cmuy7jlcj1b9k0j3kdq3htfxb`) só para: ajuste pequeno com máscara (só o braço, só a cabeça), montagem em foto real, recolorir. Nunca para cena nova do Ze nem para tirar contorno.

### 4. Conferir antes de mostrar
Baixar o resultado, gerar uma prévia de 1000 px e um zoom no rosto do Ze. Conferir:
- ponta na balaclava (não pode ser cabeça redonda);
- pupila ondulada (não bolinha), sorriso com dentes em linhas;
- balaclava toda preta, sem listra;
- sem borda branca em volta do Ze;
- tamanho e direção dos personagens como pedido.

Se errou algo, gerar de novo no GPT 2.5 passando a imagem errada como primeira referência e dizendo só o que mudar ("Edit the first image. Keep everything identical. Only change: ..."). Não remendar com colagem suavizada (deixa marca) nem engrossar o preto para esconder borda (tira o movimento do traço).

### 5. Ampliar (grátis)
`kittl-upscale-image` com a `url` do resultado, depois `kittl-get-image-upscale-status`. Sai em 4096 px (.jpeg).

### 6. Finalizar
```bash
python .claude/skills/ze/ze_final.py <upscale.jpeg> <pasta>/ze-<tema>.png [--fuieu x y largura rot cor]
```
- converte para preto e branco puro (as IAs puxam o preto para o roxo);
- `--fuieu` cola o lettering original. `x y` é o centro e `largura` o tamanho em px na imagem de 4096. `rot` em graus. `cor` é `preto` ou `branco`. Usar para tag em muro, costas do moletom, sacola.

Guardar versões anteriores com sufixo (`-v1-<motivo>.png`) e apagar os temporários `_*.jpg`.

### 7. DTF (só se ele pedir)
```bash
python .claude/skills/ze/ze_dtf.py <arte.png> <saida.png> <altura_cm> [--sem-branco] [--sem-fundo]
```
- `--sem-fundo`: tira o fundo cinza/papel (o que for claro e ligado à borda da imagem);
- `--sem-branco`: tira todo o branco (camiseta branca: o tecido faz o branco);
- sai em 300 dpi, sem transparência parcial e sem pontinhos soltos.

## Saída para o Ezequiel
Curta: link do arquivo, tamanho em px, o que tem na cena, o que conferi no rosto do Ze, e o que ficou de fora (ex.: "deixei o muro limpo, se quiser coloco o FUIEU"). Se precisou gerar mais de uma vez, dizer por quê.

## Coadjuvante: o policial
Sempre o mesmo rosto (`referencias/coadjuvante-policial.png`): quepe preto com distintivo e faixa branca, óculos escuros redondos, nariz grande branco, orelha redonda, cigarro, farda preta, luvas brancas. Mesmo tamanho do Ze.

## Cor oficial
Azul usado nas artes da FUIEU (listras do Renato, número 7): `#2484CC` (RGB 36, 132, 204).
