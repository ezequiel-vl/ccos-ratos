---
name: operacao-instagram
description: >
  Monta a operação de Instagram de um mês inteiro para um cliente da ezeOS:
  persona, funil com quiz, 10 roteiros de Reels, calendário de 4 semanas e um
  calendário visual em HTML com cronograma interativo.
  Lê o briefing, a voz e o design system do cliente antes de escrever qualquer coisa,
  e aplica as substituições obrigatórias que impedem o material de sair genérico.
  Use quando o usuário disser "operação de instagram", "calendário de conteúdo",
  "calendário visual", "monta o mês", "cronograma de posts", "funil de instagram",
  "10 reels", "quiz de captura", ou pedir isso pra um cliente específico.
---

# /operacao-instagram

Transforma briefing de cliente em operação de Instagram de 4 semanas, pronta pra executar.

Serve pra qualquer cliente da ezeOS. O que muda de um pra outro são as travas da conta, e é exatamente isso que a Fase 1 extrai.

## O que entrega

1. **Persona**: quem assina, @ recomendado, campo Nome indexado pela busca, bio, material visual
2. **Produto e funil**: caminho do comentário até a venda, com o que a automação manda no direct
3. **Quiz de 5 perguntas** com diagnóstico escrito e roteamento condicional
4. **10 roteiros de Reels** com gancho, desenvolvimento, CTA e legenda
5. **Calendário de 4 semanas** dia a dia, com horário e justificativa por peça
6. **Calendário visual em HTML** no design system do cliente, com cronograma interativo

Arquivos gerados:

```
clientes/[cliente]/conteudo/
  AAAA-MM-DD-operacao-instagram.md      documento de trabalho
  AAAA-MM-DD-calendario-visual.html     calendário navegável e marcável
```

---

## Passo 0: qual cliente?

Se o usuário não disse, pergunte. Liste as pastas de `clientes/`, ignorando as que começam com `_`.

Se ele estiver com a pasta do cliente aberta, o `CLAUDE.md` de lá já carregou sozinho. Se não, leia explicitamente.

---

## Fase 1: ler o cliente e extrair as travas

**Não escreva uma linha antes de terminar esta fase.** É ela que separa material sob medida de template preenchido.

Leia, na ordem, o que existir:

| Arquivo | O que extrair |
|---|---|
| `briefing.md` | produto, público, preço, dor, diferencial, pendências |
| `voz.md` ou bloco de voz no `CLAUDE.md` | quem fala, palavras proibidas, o teste antes de publicar |
| `CLAUDE.md` do cliente | regras inegociáveis, compliance, CTA padrão |
| `DESIGN.md` | paleta, tipografia, componentes, para gerar o HTML |
| `conteudo/` | o que já existe, pra não repetir argumento |
| `../../_contexto/preferencias.md` | estilo de escrita da casa |

Depois escreva, para si mesmo, a **tabela de travas** deste cliente:

- O que a conta **não pode prometer** (resultado, dinheiro, cura, prazo)
- Que **prova existe de verdade** hoje, e qual não existe
- **Vocabulário proibido**
- Restrição de **compliance** (conselho profissional, registro obrigatório na peça, CFM/CFO/COFEN)
- **Quem assina**: pessoa, clínica ou marca
- **Onde o lead vai parar**: WhatsApp, checkout, agendamento
- Conta **nova ou já existente**
- **Uma campanha ou várias** no mesmo perfil

Essa tabela governa tudo que vem depois. Quando o template genérico brigar com ela, **a trava ganha sempre**.

### Duas perguntas que você precisa fazer se o briefing não responder

1. **Conta nova ou já existente?** Conta nova abre com Story de Reposicionamento e a semana 1 muda inteira. Conta existente entra direto no conteúdo.
2. **Uma campanha ou mais no mesmo perfil?** Se for mais de uma, cada semana carrega uma campanha, alternando, e o calendário precisa dizer isso na abertura de cada semana. Feed que mistura dois assuntos no mesmo dia parece bipolar.

---

## As substituições obrigatórias

Esta é a parte que dá valor à skill. Todo template de funil de infoproduto pede as mesmas coisas, e quase todas quebram uma conta séria. Substitua sempre:

| O template pede | Se o cliente não tem | Use no lugar |
|---|---|---|
| Card de PROVAS com cases e números | depoimento real | declarar em voz alta que ainda não existe, e explicar por quê. Numa conta que ataca prova forjada, admitir a ausência é a prova |
| Prova social | qualquer prova própria | caso público verificável e atribuído, ou a própria história de quem lê ("quantos anos você já tentou assim?") |
| "Vagas limitadas", contagem regressiva | escassez real | urgência de calendário próprio: o mês vai passar de qualquer jeito. Produto digital com entrega imediata não tem vaga, e inventar isso é a primeira mentira da conta |
| Promessa de resultado | controle sobre o resultado | prometer só o que o cliente controla: a rotina, o procedimento, o registro, a avaliação |
| Gancho de dano ("isso está te matando") | tom agressivo compatível | abrir tensão sem gritar. Ganchos calmos convertem melhor em público adulto |
| Ficha técnica de entregável ("você recebe 2 fichas") | nada | reconhecimento: mostre a frase que a pessoa fala, o sintoma que ela tem. Ninguém deseja ficha, todo mundo se reconhece |
| Ticket de R$5.000 e etapas de serviço | ticket alto | ajustar ao preço real. Se for produto barato, cards de etapa viram cards de entregável |
| Objeção de preço | preço alto | a objeção real quase nunca é preço. Costuma ser "vai virar mais uma coisa que eu compro e não uso". Responda com o entregável que resolve isso |
| Persona inventada | pessoa real disponível | se a persona for sintética, registre isso no briefing e ajuste o meio de produção dos Reels. Nunca simule documento, print financeiro ou depoimento |

### Estilo da casa

De `_contexto/preferencias.md`, vale para toda copy gerada:

- **Sem travessão.** Em nenhum contexto. Use vírgula, dois-pontos ou parênteses
- **Sem "não é X. É Y."** e variações de contraste em duas frases curtas
- Prosa quando cabe prosa. Lista só quando a lista faz sentido de verdade

---

## Fase 2: persona

- Quem assina, com nome e função
- **@ recomendado**, com duas alternativas e o porquê da escolha
- **Campo Nome do perfil**, que é o indexado pela busca do Instagram e o @ não é. Máximo 30 caracteres. Coloque ali o termo que o público procura, nunca repita o @
- História de origem em 3 linhas
- Tom, palavras que usa e palavras que não usa
- Bio de até 150 caracteres, 3 opções, com a recomendada justificada
- Material visual: o que existe na pasta serve? Se não, brief do que falta

---

## Fase 3: produto, funil e quiz

**Funil**, em diagrama, do comentário até a conversão. Mapeie onde o lead cai: WhatsApp, checkout ou agendamento.

**O que a automação manda no direct.** Três mensagens, não uma:

1. Resposta imediata ao comentário. **Não mande link de venda aqui.** A pessoa comentou uma palavra num vídeo, ela não pediu pra comprar
2. Disparo curto pra quem não abriu, algumas horas depois
3. Follow-up de 24h pra quem abriu e não converteu

**Quiz de 5 perguntas.** Regras que fazem ele funcionar:

- A pergunta 5 é a dor central do briefing, escrita literalmente. Quem trava nela é exatamente o público
- Uma das perguntas serve pra **rotear**: o resultado decide qual página ou qual oferta a pessoa vê
- Uma das perguntas é uma **lista de tentativas fracassadas** pra pessoa marcar. Ela se vê sozinha, sem ninguém acusar
- Resultado **sem cadastro**. Pedir e-mail antes derruba a conclusão em cerca de metade. Peça depois, como opção
- Dois diagnósticos escritos, um por perfil, cada um terminando no destino certo

---

## Fase 4: dez roteiros de Reels

Distribuição por semana: 3, 3, 2, 2.

Cada roteiro tem **gancho (0 a 3s)**, **desenvolvimento** e **CTA (últimos 5s)**, com marcação de tempo, mais a **legenda** e uma nota de produção.

- Semana 1: identificação com o problema
- Semana 2: solução prática, um Reels por etapa do método
- Semana 3: história e prova
- Semana 4: o que muda de verdade, e a decisão

Regras: fala da pessoa, sem trilha épica, sem corte a cada 2 segundos, sem legenda saltitante. Cenário repetido vira assinatura visual em três semanas. CTA falado e escrito na tela.

---

## Fase 5: calendário de 4 semanas

### A regra que organiza tudo

**Cada semana tem um assunto só, e o Reels puxa o carrossel da mesma semana.** Quem vê o vídeo e depois o post recebe reforço, não assunto novo. Se o cliente tem mais de uma campanha, cada semana carrega uma.

Arco de temperatura, com o que a pessoa deve sentir ao fim de cada uma:

1. **Reconhecimento**: "isso sou eu"
2. **Método**: "existe um jeito, e eu quero"
3. **Prova e vínculo**: "eu confio nessa gente"
4. **Decisão**: "eu quero, e sei quanto custa"

**A venda só aparece na semana 4.** Três semanas entregando de graça é o que compra o direito de vender, principalmente em conta nova.

### Horários

Não use horário genérico de meio-dia. Derive do público do briefing e escreva o porquê. Duas janelas costumam funcionar em público adulto:

- **Manhã cedo**, antes da casa acordar: conteúdo de método e prática, porque é pra fazer no mesmo dia
- **Noite, depois das 20h30**: conteúdo de dor e história, porque é quando a dor aparece

Escolha o dia mais forte da semana pro público e ponha nele a peça que decide a semana. Reserve pelo menos um dia sem post: o feed respirar faz parte do posicionamento.

### Stories

Um story de aquecimento por semana, sempre na véspera da peça principal, criando compromisso antes da tarefa. Mais stories de resposta e bastidor nos outros dias.

---

## Fase 6: calendário visual em HTML

Um arquivo só, autocontido, no design system do cliente lido na Fase 1.

**Conteúdo:**

- Cabeçalho com totais e a palavra-chave de CTA
- Bloco de estratégia: o arco das 4 semanas e as regras de horário
- Tabela do mês inteiro numa tela
- Cada semana com objetivo e o que a pessoa deve sentir
- Cada peça com quando, tipo, roteiro completo ou capa, legenda e **por que está nesse dia e nesse horário**
- Rodapé com o que medir e o que ainda trava

**Cronograma interativo**, que é o que faz o arquivo virar ferramenta:

- Botão "marcar publicado" em cada peça, com `data-id` estável por semana e posição
- Peça publicada fica com fundo acinzentado, dessaturada, título riscado, e clareia no hover
- A próxima peça não publicada ganha destaque e selo
- Barra fixa com progresso, botão que rola até a próxima, e zerar com confirmação
- Estado em `localStorage`. Se o navegador bloquear em `file://`, avise na barra em vez de fingir que salvou
- `@media print` esconde os controles e marca as publicadas com um check

**Três armadilhas que já custaram retrabalho:**

1. `[hidden]` perde pra qualquer classe que defina `display`. Use `[hidden]{display:none!important}`
2. Barra de navegação que quebra em várias linhas empilha altura no celular. Use `flex-wrap:nowrap` com `overflow-x:auto`
3. `scroll-padding-top` fixo quebra quando existe mais de uma barra fixa. Meça as alturas em JS e atualize no resize. E use `block:'start'` no `scrollIntoView`, porque `'center'` ignora o scroll-padding

---

## Verificação antes de entregar

Não diga que está pronto sem rodar:

```bash
# contraste de todo par de texto do design system, calculado
# tags balanceadas
for t in section article div; do
  echo "$t: $(grep -o "<$t[ >]" $F|wc -l) / $(grep -o "</$t>" $F|wc -l)"
done
# vocabulário proibido do cliente
grep -niE "palavra1|palavra2" $F
# travessão na copy
grep -c '—' $F
```

Se Playwright estiver disponível, abra o arquivo e teste de verdade: overflow horizontal em 1440, 820 e 390, alvos de toque abaixo de 44px, erros de JS, e o ciclo de marcar, recarregar e desmarcar.

Playwright costuma estar no cache do npx, não instalado no projeto. Procure em `~/AppData/Local/npm-cache/_npx/*/node_modules/playwright` e importe pelo caminho absoluto.

---

## Regras

- **Leia antes de escrever.** Material que ignora o briefing sai genérico, e genérico não converte
- **A trava do cliente ganha do template.** Sempre
- **Nunca invente prova.** Nem número, nem depoimento, nem print
- **Nunca prometa resultado** que o cliente não controla
- Ao terminar, liste o que ficou **pendente com o cliente** e diga o que cada pendência trava
- Se o briefing não responder o que você precisa, **pergunte antes de inventar**

## Depois

Ofereça, nesta ordem:

1. Renderizar os carrosséis em PNG com `/carrossel`
2. Publicar o calendário visual com `/publicar-site`, pra ele marcar do celular
3. Atualizar o `briefing.md` do cliente com as decisões tomadas
