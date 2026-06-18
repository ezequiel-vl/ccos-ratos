---
name: carrossel
description: >
  Cria carrosseis completos para Instagram e TikTok para clientes da ezeOS.
  Pergunta qual cliente, lê o briefing dele, e salva o resultado em
  clientes/[cliente]/carrossel/[data]-[tema]/.
  Gera texto editorial, HTMLs estilizados, renderiza em PNG via Playwright.
  Use quando mencionar "carrossel", "carousel", "slides instagram",
  "faz um carrossel", "carrossel pra [cliente]", ou pedir pra transformar um tema em carrossel.
---

# /carrossel — Criação de Carrossel para Clientes

## Passo 0 — Qual cliente?

Antes de qualquer coisa, perguntar:

> "Pra qual cliente é esse carrossel?"

Listar as pastas dentro de `clientes/` (excluindo `_modelo-cliente`) como opções.
Com a resposta, definir `[cliente]` = nome da pasta correspondente.

Ler o briefing: `clientes/[cliente]/briefing.md`

Se o briefing não existir ou estiver vazio, avisar:
> "Não encontrei o briefing de [cliente]. Quer criar agora ou me passa as informações básicas (segmento, cliente ideal, tom de voz, identidade visual)?"

---

## Setup (primeira vez por cliente)

Antes de criar o carrossel, checar 4 coisas. Se tudo estiver OK, pular direto pro workflow.

### 1. Identidade visual do cliente

Ler a seção `## Identidade visual` do `clientes/[cliente]/briefing.md`.

Se estiver vazia ou não definida, perguntar:
> "Qual é a identidade visual de [cliente]?
> 1. Cor principal da marca (ex: #FF5C35 ou "azul escuro")
> 2. Estilo: clean/minimalista, bold/impactante, editorial/elegante?
> 3. Tem logo? Se sim, joga em `clientes/[cliente]/marca/` e me diz o nome."

Salvar no briefing do cliente e continuar.

Se o cliente não tiver identidade definida, usar padrão limpo (fundo escuro #0D0D0D, destaque #FFD600, Bricolage Grotesque + Instrument Serif).

### 2. Estilo de design dos slides

Ler `references/design-carrossel.md`. Se contiver `<!-- estilo: pendente -->`, perguntar:

> "Como quer o visual dos slides de [cliente]?
> 1. **Minimalista** — limpo, muito espaço em branco, elegante
> 2. **Elaborado** — texturas, composições ousadas, impactante
> 3. **Tweet** — simula tweet do Twitter, fundo branco, ultra-limpo"

Substituir o conteúdo de `references/design-carrossel.md` pelo arquivo do estilo escolhido:
- Minimalista → conteúdo de `references/design-minimalista.md`
- Elaborado → conteúdo de `references/design-elaborado.md`
- Tweet → conteúdo de `references/design-tweet.md`

Se escolher **tweet**, perguntar também:
> "Pra o estilo tweet, preciso do handle do Instagram de [cliente] e de uma foto de perfil (joga em `clientes/[cliente]/marca/foto-perfil.jpg`). Se não tiver foto, uso as iniciais."

Salvar handle e foto no briefing.

Se o arquivo NÃO contiver `<!-- estilo: pendente -->`, o estilo já foi escolhido. Não perguntar.

O estilo é global pra todos os clientes. Se precisar de estilo diferente por cliente, mencionar e ajustar.

### 3. Tom de voz do cliente

Ler a seção `## Tom de voz da marca` do briefing.

Se estiver vazio, perguntar:
> "Como [cliente] prefere que o conteúdo seja escrito? Informal, profissional, técnico? Tem algo que ele odeia em textos de IA?"

Salvar no briefing.

### 4. Playwright

Verificar se Playwright está instalado:

```bash
npx playwright screenshot --help 2>/dev/null && echo "OK" || echo "INSTALAR"
```

Se precisar instalar:
```bash
npx playwright install chromium
```

---

## Dependências

- **Briefing do cliente:** `clientes/[cliente]/briefing.md`
- **Regras de design:** `references/design-carrossel.md` (dentro desta skill)
- **Tom de voz geral:** `_contexto/preferencias.md`
- **Playwright CLI:** `npx playwright screenshot`

---

## Input

O usuário fornece:
- Tema, ideia, texto livre, link ou referência
- Imagens (opcional): se anexar fotos, usar nos slides
- Número de slides desejado (padrão: 8-10)

---

## Workflow em 3 Fases

### Fase 1 — Texto

1. Ler `clientes/[cliente]/briefing.md` pra calibrar tom, cliente ideal e contexto
2. Ler `_contexto/preferencias.md` pra restrições gerais de escrita
3. Se o input for um link, buscar o conteúdo:
   - **Links normais:** WebFetch. Se falhar, usar Jina Reader (`https://r.jina.ai/[URL]`)
   - **X/Twitter:** substituir domínio por `api.fxtwitter.com`
   - **Instagram:** WebFetch não funciona. Pedir pro usuário colar o texto
   - **YouTube:** usar `/yt-transcript` se disponível
4. Se mencionar algo desconhecido (produto, ferramenta, pessoa), pesquisar antes de escrever. Nunca chutar
5. Definir ângulo: educacional, oportunidade, contrário, provocativo ou inspiracional

6. **Briefing rápido** — perguntar numa mensagem só:
   > "Antes de escrever, me confirma:
   > - Quantos slides? (padrão: 8-10)
   > - Vai querer imagem na capa ou nos slides? Se sim, quantas tens?
   >   - Se tiver: joga em `clientes/[cliente]/carrossel/[data]-[tema]/imagens/` e me diz os nomes
   >   - Se não tiver: crio design visual sem foto
   > - CTA do último slide? (ex: 'siga pra mais', 'comenta X pra receber o link')
   > - Tipo: dica prática, tendência, opinião forte, bastidores?"

7. **Planejar a espinha dorsal e mostrar:**

   > **Espinha dorsal do carrossel:**
   >
   > **Ângulo:** [a opinião/tese sobre o assunto]
   >
   > **Tensão central:** [a fricção ou dado surpreendente]
   >
   > **Mecanismo:** [por que isso acontece]
   >
   > **Provas:** [2-3 evidências concretas]
   >
   > **Virada:** [o que muda pra quem lê]
   >
   > **5 opções de capa:**
   > A: [título] / [subtítulo]
   > B: [título] / [subtítulo]
   > C: [título] / [subtítulo]
   > D: [título] / [subtítulo]
   > E: [título] / [subtítulo]
   >
   > Qual capa preferes? A narrativa tá no caminho certo ou quer ajustar?

   **CHECKPOINT 1:** Aguardar aprovação da capa e direção narrativa. Ajustar se necessário. Só escrever os slides com a narrativa confirmada.

   Cada capa: título (max 8 palavras) + subtítulo próprio. Criar tensão ou curiosidade. Nunca descritivo ("5 dicas de X"), sempre com ângulo.

8. **Escrever os slides** com base na espinha dorsal e capa aprovadas:

   **Slide 1 (Capa):** capa escolhida no checkpoint 1.

   **Slide 2 (Hook):** fato, dado ou situação que cria tensão. Termina preparando o próximo slide pela tensão narrativa, não por aviso.

   **Slides 3-4 (Mecanismo):** explica POR QUE isso acontece. Dados concretos: número + fonte + ano. Se não tiver dado, exemplo real e específico.

   **Slides 5-7 (Provas):** um ponto por slide, cada um aprofundando aspecto diferente. Cada slide adiciona camada nova.

   **Slides 8-9 (Virada):** não é resumo. É o que isso significa pra quem lê. Conexão prática e específica.

   **Slide final (CTA):** chamada pra ação + marca do cliente. Curto. Frase-ponte que conecta o conteúdo com a ação.

**Regras de construção do texto:**
- Cada slide é um parágrafo de reportagem, não uma lista disfarçada. 2-4 frases com conectivos naturais (porque, só que, por isso, enquanto, mas, então)
- Artigos sempre presentes: "um mercado", "a marca", "os dados"
- Cada frase funciona lida em voz alta
- Cada slide termina preparando o próximo pela tensão narrativa
- Toda afirmação factual: dado + fonte + ano. Se não tiver dado verificável, não inventar

**Padrões proibidos:**
- Sem "não é X, é Y" ou variações de contraste em duas frases curtas
- Sem travessão (—)
- Sem cacoetes: "e isso muda tudo", "no fim das contas", "de forma X", "cada vez mais", "simplesmente", "basicamente"
- Sem jargão: "ecossistema", "mindset", "sinergia", "disruptivo"
- Sem aberturas genéricas: "hoje vamos falar sobre", "neste carrossel tu vai"
- Sem CTA cordial: "espero que tenha gostado", "se esse conteúdo te ajudou"
- Sem "continue no próximo", "swipe pra ver mais"

9. Gerar legenda Instagram:
   - Gancho nos primeiros 125 caracteres
   - 2-3 parágrafos curtos
   - CTA no final
   - 5-10 hashtags relevantes

10. Mostrar texto completo de todos os slides + legenda no chat

11. Salvar em `clientes/[cliente]/carrossel/[data]-[tema]/carousel-text.md`

**CHECKPOINT 2:** Mostrar texto + legenda. Aguardar aprovação antes de seguir pra Fase 2.

---

### Fase 2 — Visual (HTMLs + PNGs)

1. Ler identidade visual do cliente em `clientes/[cliente]/briefing.md`
2. Ler `references/design-carrossel.md` pra regras de design
3. Criar HTMLs seguindo as regras
4. Salvar HTMLs em `clientes/[cliente]/carrossel/[data]-[tema]/instagram/`
5. Renderizar slide 1 primeiro:
   ```bash
   npx playwright screenshot --viewport-size=1080,1350 --full-page "file:///[caminho-absoluto]/slide-01.html" "slide-01.png"
   ```

**CHECKPOINT:** Mostrar slide 1. Se aprovado, renderizar os demais. Se pedir ajuste, editar HTML e re-renderizar só aquele.

Salvar PNGs em `clientes/[cliente]/carrossel/[data]-[tema]/instagram/`.

---

### Fase 3 — Versão TikTok (opcional)

Após finalizar Instagram, perguntar:
> "Quer a versão TikTok também? (1080x1920, formato vertical)"

Se sim:
- Adaptar HTMLs: height 1920px, padding maior, bottom safe zone de 230px
- Renderizar:
  ```bash
  npx playwright screenshot --viewport-size=1080,1920 --full-page "file:///[caminho]/slide-01.html" "slide-01.png"
  ```
- Salvar em `clientes/[cliente]/carrossel/[data]-[tema]/tiktok/`

---

## Output final

```
clientes/[cliente]/carrossel/[data]-[tema]/
  carousel-text.md          ← texto aprovado + legenda
  imagens/                  ← fotos do usuário (se houver)
  instagram/
    slide-01.html → slide-01.png
    slide-02.html → slide-02.png
    ...
  tiktok/ (se solicitado)
    slide-01.html → slide-01.png
    ...
```

## Geração de imagens (opcional)

Se o usuário não tiver imagens, oferecer gerar via Pollinations.ai (gratuito, sem cadastro):

```bash
curl -L "https://image.pollinations.ai/prompt/[descricao]?width=1080&height=720&nologo=true" -o imagens/foto-01.jpg
```

Mostrar pro usuário aprovar antes de usar no slide.
Se qualidade não servir: "Se quiser imagem melhor, gera no Canva ou Midjourney e joga na pasta imagens/."

---

## Regras

- Texto aprovado na Fase 1 não muda na Fase 2
- Sempre mostrar slide 1 antes de renderizar os demais
- Se pedir ajuste no visual, editar o HTML e re-renderizar apenas o slide alterado
- Se o setup já foi feito antes (briefing preenchido, estilo escolhido), não repetir perguntas
- Regras de design vivem em `references/design-carrossel.md`. Se quiser mudar algo visual, editar lá ou pedir: "muda a regra X no design do carrossel"
