# Guia de Design — ezeOS

> As skills de carrossel, proposta e slide leem este arquivo antes de criar qualquer visual.
> Definido em 2026-10-15. Referências: `mosaik-iota.vercel.app` e `lastro-demo-alpha.vercel.app`.

**Regra de ouro da arquitetura:** a casa é neutra, a vertical tem cor. O sistema visual é um só. A ezeOS roda em preto, cinza e branco puros. A eze.clinicas usa o mesmo sistema e troca só a cor de sinal pelo carmim. Vertical nova ganha a cor dela e nada mais muda.

---

## Cores

O sistema nasce escuro. A versão clara existe pra documento, proposta e PDF.

### Escuro (padrão: site, carrossel, slide)

- **Fundo principal:** `#0A0A0B`
- **Fundo alternativo / cards:** `#141416` (superfície), `#1C1C1F` (superfície elevada)
- **Texto principal:** `#F4F4F2`
- **Texto secundário:** `#9A9A9E`
- **Texto apagado / legenda:** `#6E6E72`
- **Linha / divisor:** `rgba(255,255,255,0.10)`, sempre 1px
- **Cor de destaque / CTA:** branco `#F4F4F2` sólido. O contraste é o destaque.

### Claro (proposta, documento, impresso)

- **Fundo principal:** `#FAFAF9`
- **Fundo alternativo / cards:** `#FFFFFF`
- **Texto principal:** `#0A0A0B`
- **Texto secundário:** `#6E6E72`
- **Linha / divisor:** `rgba(0,0,0,0.10)`
- **Cor de destaque / CTA:** preto `#0A0A0B` sólido

### Cor de sinal por marca

| Marca | Sinal | Onde entra |
| --- | --- | --- |
| **ezeOS** | nenhuma | o destaque é o próprio contraste |
| **eze.clinicas** | carmim `#EF064A` | no máximo um elemento por tela |

### Cor proibida

Gradiente colorido, roxo de SaaS, azul corporativo, dourado, e qualquer cor fora dos neutros no material da casa. Verde e vermelho só aparecem como estado de interface (sucesso, erro), nunca em peça de marketing.

---

## Tipografia

Três famílias, todas no Google Fonts e licenciadas pra uso comercial (OFL).

- **Títulos e destaques:** **Archivo**, peso 600 ou 700, tracking negativo de `-0.03em` a `-0.045em`. Quanto maior o título, mais fechado o tracking.
- **Corpo, subtítulos e botões:** **Inter Tight**, peso 400 e 500, `line-height: 1.5`, tracking `-0.01em`.
- **Rótulos, números e marcadores de seção:** **JetBrains Mono**, peso 400 ou 500, caixa alta, tamanho 11 a 13px, tracking **positivo** de `+0.12em` a `+0.16em`.

**Peso do título:** 600 como padrão. 700 só no hero.

O contraste do sistema é esse: título enorme com tracking apertado ao lado de um rótulo minúsculo em mono, caixa alta e bem espaçado. É o que dá a cara editorial das duas referências.

**Tamanhos fluidos**, sempre com `clamp()`:

```css
--fs-hero:  clamp(40px, 7vw,   104px);
--fs-h2:    clamp(28px, 3.6vw,  56px);
--fs-lead:  clamp(20px, 2.4vw,  34px);
--fs-body:  clamp(15px, 1.05vw, 17px);
--fs-mono:  clamp(11px, 0.9vw,  13px);
```

**Marcador de seção:** numeração em mono, no padrão `01 / PONTO`, `02 / MOVIMENTO`. Conversa direto com os três andares do serviço e com a ideia de sistema operacional.

---

## Estilo geral

Editorial, técnico e silencioso. A página respira muito, o texto é curto e declarativo, e a hierarquia vem do tamanho e do espaço, não de caixa colorida. Parece relatório bem feito, não parece panfleto.

Ritmo de seção: rótulo em mono, título grande, uma linha de 1px atravessando, conteúdo. Repete.

Fundo escuro com um leve gradiente radial no topo da página dá profundidade sem sujar:

```css
background: radial-gradient(120% 90% at 50% 40%, #16161A 0%, #0A0A0B 55%);
```

---

## Elementos-chave

- **Bordas:** hairline de 1px em 10% de opacidade. Nunca borda grossa, nunca borda colorida.
- **Border-radius dos cards:** 12px. Botão 8px. Pílula 999px. Nada acima de 12px em card.
- **Botões:** pílula sólida. No escuro, fundo claro com texto escuro. No claro, fundo preto com texto branco. Botão secundário é só contorno hairline com fundo transparente. Sem ícone decorativo, no máximo uma seta.
- **Sombras:** não. Elevação se resolve trocando a cor da superfície (`#141416` → `#1C1C1F`).
- **Grid:** base 8. Gutter `clamp(16px, 3.3vw, 56px)`.
- **Movimento:** `cubic-bezier(.16, 1, .3, 1)`, entre 200 e 400ms. Entrada por fade com 12 a 20px de deslocamento. Respeitar `prefers-reduced-motion`.

---

## O que NUNCA fazer

- Cor fora dos neutros em peça da casa
- Sombra, bisel, brilho ou gradiente colorido
- Mais de uma cor de sinal na mesma tela
- Ícone genérico de banco de imagem (foguete, alvo, engrenagem, aperto de mão)
- Caixa alta no corpo do texto. Caixa alta só em rótulo mono
- Tracking positivo em título. Título é sempre fechado
- Travessão (`—`) em qualquer texto
- Construção "não é X. É Y."
- Emoji

---

## Logo

- **Arquivo:** ainda não existe. Pendente.
- **Versão pra fundo escuro:** pendente
- **Onde usar:** slide final do carrossel (CTA), header de propostas, slides de apresentação
- **Tamanho sugerido:** largura entre 120 e 200px nos HTMLs

Enquanto não existe logo, usar o nome em Archivo 600, caixa baixa (`ezeOS`), tracking `-0.03em`, com o "OS" no mesmo peso. A skill `logo-design` está instalada em `~/.claude/skills/logo-design` pra quando for desenhar.

---

## Perfil do autor

> Usado no estilo "tweet" do carrossel.

- **Nome:** Ezequiel
- **Handle:** @ezeos (atualizar se diferente)
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
