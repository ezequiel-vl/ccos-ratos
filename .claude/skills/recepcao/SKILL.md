---
name: recepcao
description: >
  Monta a recepção de um evento da ThaminyIlha.Cerimonial: pega a planilha de convidados
  com mesas e devolve um link pra fazer o check-in de chegada no iPad (busca por nome,
  mostra a mesa, funciona sem internet). Use quando mencionar "recepção", "check-in dos
  convidados", "lista de convidados no iPad", "lista de mesas pro evento", "marcar quem chegou",
  "/recepcao", ou mandar uma planilha de convidados com mesas pra usar no dia do evento.
---

# /recepcao: lista de convidados no iPad

Entrada: planilha (xlsx ou csv) com nome e mesa de cada convidado + nome do evento.
Saída: link curto que abre a Recepção já com a lista carregada no iPad.

Ferramenta: `clientes/ThaminyIlha.Cerimonial/recepcao/` (index.html + sw.js + gerar-link.js),
publicada em `https://ezeos-publicacoes.pages.dev/recepcao-thaminy/`.

## Regras de privacidade (não negociar)

- A lista tem nome de convidado. **Nunca** salvar TSV/CSV da lista dentro do repositório
  (ele sincroniza com o GitHub). Arquivos intermediários vão no scratchpad.
- A lista só é publicada **criptografada** (o `gerar-link.js` faz isso). A chave fica só no link.
- Não imprimir a lista inteira na conversa sem necessidade; mostrar resumo.

## Workflow

### 1. Achar a planilha
Se o usuário der só o nome ("tá em Downloads, chama Lista"), procurar em `~/Downloads`.
Se tiver mais de um arquivo parecido, perguntar qual. Se o arquivo for xlsx com várias abas,
rodar sem `--aba` primeiro (pega a primeira aba com NOME/CONVIDADO + MESA) e conferir no
resumo se é a aba certa. Na dúvida, perguntar.

Perguntar o **nome do evento** se não veio (ex: "Casamento Fernando & Vanessa").

### 2. Converter
```bash
python .claude/skills/recepcao/converter-lista.py "<planilha>" "<scratchpad>/lista.tsv" [--aba "Nome da aba"]
```
O script já trata:
- seção "NÃO CONFIRMADOS": entra sem mesa, com obs "Não confirmado"
- mesa "não vem": pula e avisa
- coluna ACOMPANHANTE: vira outra linha na mesma mesa
- colunas de observação/restrição: vão pra Obs
- NOME EM MAIÚSCULA: vira "Nome Normal"; "Mesa 02"/"4.0": vira "2"/"4"

### 3. Conferir com o usuário antes de gerar
Mostrar o resumo que o script imprime: total, **quantos por mesa**, sem mesa, pulados,
nomes repetidos. Se a planilha tiver capacidade por mesa no cabeçalho (ex: "MESA 1 (16)"),
comparar. Apontar inconsistências (ex: confirmado numa aba e ausente na lista de mesas).

### 4. Gerar o link e publicar
```bash
node clientes/ThaminyIlha.Cerimonial/recepcao/gerar-link.js "<scratchpad>/lista.tsv" "Nome do evento"
```
Grava `_publicado/recepcao-thaminy/listas/<id>.json` (criptografado) e imprime o link
`...recepcao-thaminy/#k=<id>.<chave>`. Depois publicar com a skill `/publicar-site`
(deploy da pasta `_publicado` inteira; não precisa copiar nada, o arquivo já tá lá).

Se o `index.html` ou `sw.js` da ferramenta mudou, copiar pra `_publicado/recepcao-thaminy/` antes do deploy.

### 5. Testar antes de entregar
Abrir o link publicado num navegador headless (Playwright) e conferir que `#evento` mostra
o nome do evento e `#sTotal` bate com o total. Só entregar depois de ver isso.

### 6. Entregar
Link + checklist do iPad:
1. Abrir o link numa aba nova (não anônima). Precisa de internet na primeira vez.
2. Conferir nome do evento e total.
3. Teste offline: modo avião, fechar o navegador de vez e abrir de novo. Se não abrir no
   Chrome, usar o Safari no dia (o Safari guarda a página pra abrir sem internet).
4. Se testou marcando chegadas: ⋯ → Zerar check-ins.
5. No dia: Bloqueio automático em Nunca, carregador, aba aberta sem recarregar.

## Como a ferramenta funciona (pra responder dúvidas)

- Toque no nome marca a chegada e mostra "Chegou · Mesa X" com **Desfazer** por 6s.
  Tocar num nome já marcado pergunta se quer desmarcar.
- Busca pelo começo das palavras do nome; digitar só o número lista a mesa inteira.
- Abas: Buscar, Mesas ("5 de 8" por mesa), Faltam (por mesa).
- ⋯: adicionar convidado na hora, exportar CSV (com horário de chegada), trocar lista, zerar.
- **Cada aparelho guarda a própria lista** (localStorage). Não sincroniza entre iPad e notebook.
  Se um dia precisar de 2+ aparelhos sincronizados, isso é outra construção (precisa de
  internet no salão; ver `sistema-rsvp/`).

## Histórico
- 2026-09-18: criada pro Casamento Fernando & Vanessa (19/09, 64 convidados, 6 mesas).
  Aprendizado: link com a lista inteira no `#` (uns 2.200 caracteres) chegou cortado no iPad.
  Por isso o link curto criptografado.
