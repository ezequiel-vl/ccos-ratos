A ezeOS instala a empresa do cliente no digital por inteiro: site, ficha do Google, e-mail no domínio, redes sociais e WhatsApp configurados de verdade. O público é dono de negócio local, que lê no celular, entre um atendimento e outro. O sistema é preto, cinza e branco, com o ponto cinza do logo como única cor. Ele tem que passar a sensação de algo instalado e de pé, e nunca de agência que posta por você.

A casa é neutra e a vertical tem cor. A ezeOS usa só os neutros e o `dot`. A vertical eze.clinicas usa o mesmo sistema inteiro e troca só a cor de sinal por `sinal-clinicas`. Vertical nova ganha a cor dela e nada mais muda.

## Conteúdo

**Voz.** Informal, direta, em primeira pessoa quando é o Ezequiel falando ("Me chama. Eu olho a sua empresa do jeito que o seu cliente olha"). No site, trate o leitor por "você". Diagnóstico concreto antes de qualquer promessa: mostre o buraco, depois o método.

**Frases da marca**, escreva exatamente assim:

- Institucional: "A gente instala a sua empresa no digital."
- Abertura falada: "Onde o seu cliente procurar, você vai estar lá."
- Fecho do diagnóstico: "Você está pagando aluguel na rua e morando de favor na internet."
- Método: **Endereço Fixo**, em três etapas, Ponto, Movimento e Atendimento.

**Regras de escrita:**

- Sem travessão em nenhum texto. Use vírgula, dois-pontos ou ponto.
- Sem a construção "não é X. É Y." nem contraste em duas frases curtas.
- Sem emoji, sem "transforme seu negócio", sem "propósito".
- Caixa de frase em título e botão. Caixa alta só no `rotulo`.
- Botão diz o que acontece: "Fazer o teste de 1 minuto", "Chamar no WhatsApp", "Quero o Ponto Digital". Se a ação muda, o rótulo muda junto.
- Nenhum número de resultado, depoimento ou case que não seja real. Sem prova, a peça fica sem prova.

## Fundamentos visuais

**Cor.** Toda peça escura começa no componente Fundo: `bg` com `brilho` no topo e grão a `opacidade-grao` por cima. Texto principal em `ink`, secundário em `mute`, apagado em `faint`. Nunca use `#6e6e6e` em texto sobre o escuro, porque reprova contraste. Superfícies sobem em degraus de cor (`sunk` < `bg` < `surface` < `raised`) e nunca por sombra. Bordas são hairline de 1px em `line`, ou `line-2` quando o card precisa se separar mais. O tema `claro` serve só pra proposta, documento e PDF, e vai sem grão e sem brilho.

**O ponto.** `dot` é a assinatura. Todo título termina com o ponto final pintado em `dot` (`<span class="eze-pt">.</span>`), igual ao "eze.OS" do logo. O mesmo ponto é bullet de lista, pino de mapa, status "no ar" e placar do teste. Não use outro acento na casa.

**Tipo.** Três famílias, todas do Google Fonts com licença OFL:

- `display` (Archivo) nos títulos: `hero`, `frase`, `titulo`, `etapa`, `preco`, `placar`, `card-titulo`. Peso 600 ou 700, tracking negativo com piso em -0,04em e `font-stretch: 106%`. Quanto maior o título, mais fechado o tracking, mas nunca abaixo do piso.
- `ui` (Inter Tight) no texto: `lead`, `body`, `body-sm`, `botao`. Entrelinha de 1,6 no `body`, porque texto claro em fundo escuro precisa de ar. Linhas de até 65 caracteres.
- `mono` (JetBrains Mono) só pra dado de sistema: `rotulo` em caixa alta com +0,14em (prazo, formato, status, etapa) e `endereco` em caixa baixa.

No site os tamanhos são fluidos com `clamp()`. O valor do token é o máximo, e a nota de cada estilo traz o clamp.

**Ritmo de seção.** O título grande abre a seção sozinho, sem rótulo em cima. Depois vêm uma hairline em `line` e o conteúdo. O respiro vertical vai até `secao` e a margem lateral até `gutter`. Rótulo mono em caixa alta só onde ele rotula um dado, mais uma vez no hero. Numeração só no método (`01 / Ponto`), porque ali a ordem é real.

**Espaço e raio.** Grid de base 8 (`space-2` a `space-8`). Raio `radius-card` em card comum, `radius-painel` em painel grande, `radius-preco` só no card de preço, e `radius-pilula` em botão, seletor, escolha, chave e barra de endereço.

**Movimento.** Easing `cubic-bezier(.16, 1, .3, 1)`, de 200 a 400ms. Entrada por fade com 12 a 24px de deslocamento, ligada à rolagem e nunca escondendo conteúdo: a animação enfeita o que já está visível. Os destaques são a Lanterna nos cards, a montagem do Navegador no hero e o Preço que rola. Respeite `prefers-reduced-motion` em tudo.

**Acessibilidade.** Texto com contraste de 4,5:1 ou mais, alvos de toque de 44px, foco visível em anel de 2px `ink`, link de pular pro conteúdo e o conteúdo inteiro de pé sem JavaScript.

## Iconografia

A casa quase não usa ícone. Os únicos são traço fino de 1,5 a 1,8 desenhado na hora, sem preenchimento:

- a seta do chip do botão principal
- o check da lista do preço
- o cadeado da barra de endereço
- a lupa da busca no mockup

Não use ícone de banco de imagem (foguete, alvo, engrenagem, aperto de mão), ícone grande em cima de título, nem emoji.

## Logo

O logo está no grupo **Logos**. É o logotipo **eze.OS** em minúscula, grotesca pesada, com o ponto em `dot`.

- `ezeos-horizontal-branco.png` em fundo escuro, `ezeos-horizontal-preto.png` em fundo claro. Proporção 4:1: defina sempre a **altura** (28 a 40px em menu, 48 a 64px em capa de carrossel) e deixe a largura livre.
- Respiro de uma altura do "e" minúsculo em volta.
- `ezeos-simbolo.svg` é o símbolo: o ponto sozinho, em `dot`. Use em favicon, foto de perfil e ícone de app, e em app icon sobre quadrado `bg`. Sozinho ele não identifica a marca, então funciona como lembrete do logotipo, não como apresentação.
- Ainda não existe logotipo em vetor (SVG). Use o PNG.
