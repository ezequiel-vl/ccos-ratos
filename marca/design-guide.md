# Guia de Design da ezeOS

> As skills de carrossel, proposta e slide leem este arquivo antes de criar qualquer visual.
> Definido em 2026-10-15. Referências: `mosaik-iota.vercel.app` e `lastro-demo-alpha.vercel.app`.

**Regra de ouro da arquitetura:** a casa é neutra, a vertical tem cor. O sistema visual é um só. A ezeOS roda em preto, cinza e branco puros, com um único acento: o ponto em azul `#48A0C7`. A eze.clinicas usa o mesmo sistema e troca só a cor de sinal, do azul pro carmim. Vertical nova ganha a cor dela e nada mais muda.

---

## Cores

O sistema nasce escuro. A versão clara existe pra documento, proposta e PDF.

### Escuro (padrão: site, carrossel, slide)

- **Fundo principal:** `#0A0A0A`
- **Fundo alternativo / cards:** `#141414` (superfície), `#1C1C1C` (superfície elevada)
- **Texto principal:** `#F4F4F4`
- **Texto secundário:** `#A6A6A6` (o cinza da casa; o ponto do logo era desse cinza antes de virar azul)
- **Texto apagado / legenda:** `#8C8C8C`. O antigo `#6E6E6E` reprovava contraste em texto pequeno sobre o preto (3,6:1); ele continua valendo pra borda e ponto apagado, nunca pra texto
- **Superfície afundada:** `#101010` (barra do navegador, seletor, caixas dentro de card)
- **Esqueleto e ponto apagado:** `#262626` e `#3A3A3A`
- **Linha / divisor:** `rgba(255,255,255,0.10)`, sempre 1px
- **Cor de destaque / CTA:** branco `#F4F4F4` sólido. O contraste é o destaque.

### Claro (proposta, documento, impresso)

- **Fundo principal:** `#FAFAFA`
- **Fundo alternativo / cards:** `#FFFFFF`
- **Texto principal:** `#0A0A0A`
- **Texto secundário:** `#6E6E6E`
- **Linha / divisor:** `rgba(0,0,0,0.10)`
- **Cor de destaque / CTA:** preto `#0A0A0A` sólido

Os cinzas são neutros puros, sem viés de azul. O único azul do sistema é o do ponto, e ele aparece pequeno justamente porque todo o resto é neutro.

### Cor de sinal por marca

| Marca | Sinal | Onde entra |
| --- | --- | --- |
| **ezeOS** | azul `#48A0C7` | só no ponto: o ponto do logo, o ponto final dos títulos, o status "no ar" e o pino do mapa. Bullet de lista e placar continuam cinza `#A6A6A6` |
| **eze.clinicas** | carmim `#EF064A` | no máximo um elemento por tela |

**Azul do ponto `#48A0C7`.** Tirado do azul do terminal onde a ezeOS é construída. Contraste: 6,7:1 sobre `#0A0A0A` e 6,3:1 sobre `#141414`, então serve até pra texto no escuro, mas a regra é usar só no ponto. No claro dá 2,8:1 sobre `#FAFAFA`: vale como marca (ponto do logo, ponto do título) e nunca como texto. Se um dia precisar de texto azul no claro, usar `#2A7699` (4,9:1).

O azul nunca vira fundo, botão, borda, card, ícone ou texto corrido. Se ele aparecer em mais que o ponto, deixa de ser foco e vira tema.

### Cor proibida

Gradiente colorido, roxo de SaaS, azul corporativo, dourado, e qualquer cor fora dos neutros e do azul do ponto no material da casa. Verde e vermelho só aparecem como estado de interface (sucesso, erro), nunca em peça de marketing.

---

## Tipografia

Três famílias, todas no Google Fonts e licenciadas pra uso comercial (OFL).

- **Títulos e destaques:** **Archivo**, peso 600 ou 700, tracking negativo de `-0.03em` a `-0.04em`. Quanto maior o título, mais fechado o tracking, e `-0.04em` é o piso: mais fechado que isso as letras encostam.
- **Corpo, subtítulos e botões:** **Inter Tight**, peso 400 e 500, `line-height: 1.5`, tracking `-0.01em`.
- **Rótulos de dado e números:** **JetBrains Mono**, peso 400 ou 500, caixa alta, tamanho 11 a 13px, tracking **positivo** de `+0.12em` a `+0.16em`.

**Peso do título:** 600 como padrão. 700 só no hero.

O contraste do sistema é esse: título enorme com tracking apertado ao lado de um rótulo minúsculo em mono, caixa alta e bem espaçado. É o que dá a cara editorial das duas referências.

**Tamanhos fluidos**, sempre com `clamp()`:

```css
--fs-hero:  clamp(40px, 7vw,    96px);
--fs-h2:    clamp(28px, 3.6vw,  56px);
--fs-lead:  clamp(20px, 2.4vw,  34px);
--fs-body:  clamp(15px, 1.05vw, 17px);
--fs-mono:  clamp(11px, 0.9vw,  13px);
```

**Sequência do método:** numeração em mono só no método, no padrão `01 / Ponto`, `02 / Movimento`, `03 / Atendimento`, porque ali a ordem é real (a etapa 2 depende da 1). Nenhuma outra seção leva número.

---

## Estilo geral

Editorial, técnico e silencioso. A página respira muito, o texto é curto e declarativo, e a hierarquia vem do tamanho e do espaço, não de caixa colorida. Parece relatório bem feito, não parece panfleto.

Ritmo de seção: o título grande abre a seção, sem rótulo em cima, depois uma linha de 1px atravessando e o conteúdo. Rótulo mono em caixa alta só onde ele rotula um dado (prazo, formato, status, etapa) e uma vez no hero. Posto em cima de toda seção, ele vira o andaime típico de página feita por IA.

### Fundo: grão e brilho

O fundo da casa é cinza com grão, no clima do mosaik-iota.vercel.app. A base continua `#0A0A0A`; o cinza que aparece vem de duas camadas por cima dela. Medido no hero do site, o resultado dá `#1B1B1B` com grão visível, contra `#1A1A1C` na referência (a nossa fica neutra, sem o azul dela, pra casar com o ponto do logo).

**1. Brilho no topo:** luz cinza suave no alto da página.

```css
background: radial-gradient(70% 55% at 50% 12%, rgba(210,210,210,.08), transparent 72%) no-repeat, #0A0A0A;
```

**2. Grão:** ruído fractal em SVG, 15% de opacidade, numa camada fixa por cima de tudo que não recebe clique.

```css
body::after{
  content:""; position:fixed; inset:0; z-index:25; pointer-events:none; opacity:.15;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E");
  background-size:140px 140px;
}
```

Vale pra tudo que sai escuro: site, carrossel, slide, capa de proposta. Nos PNGs do carrossel o grão aparece normalmente, porque o render é de navegador. Na versão clara (proposta, documento) não leva grão nem brilho.

---

## Elementos-chave

- **Bordas:** hairline de 1px em 10% de opacidade. Nunca borda grossa, nunca borda colorida.
- **Border-radius dos cards:** 12px. Botão 8px. Pílula 999px. Nada acima de 12px em card.
- **Botões:** pílula sólida. No escuro, fundo claro com texto escuro. No claro, fundo preto com texto branco. Botão secundário é só contorno hairline com fundo transparente. Sem ícone decorativo, no máximo uma seta.
- **Sombras:** não. Elevação se resolve trocando a cor da superfície (`#141414` → `#1C1C1C`).
- **Grid:** base 8. Gutter `clamp(16px, 3.3vw, 56px)`.
- **Movimento:** `cubic-bezier(.16, 1, .3, 1)`, entre 200 e 400ms. Entrada por fade com 12 a 20px de deslocamento. Respeitar `prefers-reduced-motion`.
- **Lanterna:** card com superfície ganha uma luz circular de 420px que segue o cursor e acende ao passar o mouse, também do mosaik. Cinza neutro a 10%. Fica **atrás do texto** (o card ilumina, a leitura não lava); em ilustração, como o painel do navegador no hero, fica **por cima**, como reflexo no vidro. Só em aparelho com mouse. Vai em painel, card de pergunta, card de preço e card de lista; não vai em botão, que já tem o próprio brilho, nem em bloco sem borda.

```css
.luz{position:relative; isolation:isolate}
.luz::before{
  content:""; position:absolute; inset:0; z-index:-1; border-radius:inherit; pointer-events:none;
  background:radial-gradient(420px circle at var(--lx,50%) var(--ly,0%), rgba(220,220,220,.10), transparent 60%);
  opacity:0; transition:opacity .35s cubic-bezier(.16,1,.3,1);
}
.luz--sobre::before{z-index:5}  /* ilustracao: luz por cima */
@media (hover:hover) and (pointer:fine){ .luz:hover::before{opacity:1} }
```

O JavaScript só grava `--lx` e `--ly` (posição do cursor dentro do card) num `pointermove` delegado no documento. Em peça estática (carrossel, slide) não há cursor: se quiser o efeito, fixar a luz num ponto, de preferência sobre o número ou a frase principal do card.

---

## O que NUNCA fazer

- Cor fora dos neutros e do azul do ponto em peça da casa
- Azul em área grande: fundo, botão, card, borda ou texto corrido
- Sombra, bisel, brilho ou gradiente colorido
- Mais de uma cor de sinal na mesma tela
- Ícone genérico de banco de imagem (foguete, alvo, engrenagem, aperto de mão)
- Caixa alta no corpo do texto. Caixa alta só em rótulo mono
- Tracking positivo em título. Título é sempre fechado
- Travessão (`—`) em qualquer texto
- Construção "não é X. É Y."
- Emoji
- Rótulo em caixa alta em cima de toda seção
- Conteúdo que só aparece se o JavaScript rodar a animação. A animação enfeita o que já está visível, nunca esconde
- Texto pequeno em `#6E6E6E` sobre o preto

---

## Logo

O logotipo é a palavra **eze.OS** em minúscula, grotesca pesada, com o ponto em azul `#48A0C7`. O ponto é o único elemento de cor do sistema e é o detalhe que dá nome ao arquivo de marca.

### Arquivos

```
marca/logo/
  ezeos-horizontal-preto.png    1597x400, letras #000000, ponto #48A0C7, transparente
  ezeos-horizontal-branco.png   1597x400, letras #FFFFFF, ponto #48A0C7, transparente
  ezeos-simbolo.svg             o ponto sozinho, 256x256, #48A0C7
  _originais/                   os 2000x2000 como vieram, antes do corte
  favicon/                      17 arquivos: .ico, PNGs, manifest e snippet de <head>
```

- **Fundo claro:** usar a versão preta
- **Fundo escuro:** usar a versão branca
- **Proporção:** 4:1. Definir sempre a **altura** no CSS e deixar a largura automática
- **Altura sugerida:** 28 a 40px em header, 48 a 64px em capa de carrossel
- **Área de respiro:** a altura do "e" minúsculo de cada lado
- **Onde usar:** slide final do carrossel (CTA), header de propostas, slides de apresentação

### Símbolo

O símbolo é **o ponto sozinho**: círculo em `#48A0C7`. A proporção veio do logotipo, onde o ponto mede 0,28 da altura total. No canvas quadrado de 256 ele ocupa 62,5% (raio 80), que é a proporção padrão de ícone de app.

Onde usa: favicon, foto de perfil, ícone de app, marcador de lista, bullet de slide.

App icon e favicon saem como ponto azul sobre quadrado `#0A0A0A`.

**Limite assumido:** círculo liso é a forma mais genérica que existe. Sozinho ele não identifica a marca e não dá pra registrar como forma. Funciona porque o ponto aparece sempre junto do logotipo no resto do sistema, então o favicon vira lembrete, não apresentação. Se um dia a ezeOS precisar de reconhecimento isolado, o caminho é o "e" com o ponto.

### O que falta

- **Logotipo em SVG.** Só o símbolo é vetor. O logotipo ainda é PNG, então não escala pra impresso grande nem recolore por código. Adiado por decisão, não por esquecimento.

---

## Perfil do autor

> Usado no estilo "tweet" do carrossel.

- **Nome:** Ezequiel
- **Handle:** @agenciaezeos (instagram.com/agenciaezeos)
- **Foto:** *(colocar em `marca/foto-perfil.jpg` e atualizar aqui)*
- **Badge verificado:** não

---

## Observações adicionais

### De onde veio o sistema

Lido direto do CSS das duas referências que o Ezequiel mandou:

- **mosaik-iota.vercel.app:** Sora + JetBrains Mono, preto `#0a0a0a` com brancos e cinzas (`#ededed`, `#8a8a8e`, `#6e6e72`), radius 10px em superfície e 8px em botão, easing `cubic-bezier(.16,1,.3,1)`. Usa a dobradinha de título com tracking negativo e rótulo em caixa alta com tracking até `+0.16em`.
- **lastro-demo-alpha.vercel.app:** Archivo + Inter Tight + IBM Plex Mono, fundo `#121314`, texto `#ecebe6`, apagado `#8d8e8a`, linha em 22% de opacidade, tipografia inteira em `clamp()`, seções numeradas e um acento terracota `#d9733f` usado com muita parcimônia.

O `minimalista.braboacademy.com.br` bloqueou leitura automática, então entrou só como referência de nome e tom.

### Componentes da Profitize mapeados pro site

Os quatro links são componentes prontos pra colar no Claude Code. Os prompts ficam atrás de login, então aqui fica só o uso recomendado:

| Componente | O que faz | Onde usar no site da ezeOS |
| --- | --- | --- |
| **Cristal** (grátis) | par de botões em pílula, um claro com chip de seta e um de vidro que acende no hover | CTA principal do hero e do rodapé |
| **Âncora** | preço num card só, três ofertas num seletor deslizante, dígitos que rolam, adicionais que somam | a escada de ofertas, com Ponto Digital, Movimento e Demanda Contínua no seletor |
| **Esteira** | duas fileiras de cartões correndo em sentidos opostos conforme a página rola | prova social: clínicas atendidas, prints de ficha do Google, antes e depois |
| **Relevo** | painel em perspectiva que inclina com o cursor e se monta ao entrar na tela | hero, mostrando o site de um cliente dentro do navegador |

Cristal é o único marcado como grátis. Os outros três parecem estar no plano Pro.
