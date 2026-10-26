---
name: recepcao
description: >
  Monta a recepção de um evento (Ilha Eventos, ou casamento da ThaminyIlha.Cerimonial): pega a
  planilha de convidados e devolve um link pra fazer o check-in de chegada nos tablets, sincronizado
  entre vários aparelhos, funcionando sem internet, com lista final exportável pelo computador.
  Use quando mencionar "recepção", "check-in dos convidados", "lista de convidados no tablet/iPad",
  "lista de mesas pro evento", "marcar quem chegou", "lista final do evento", "/recepcao", ou mandar
  uma planilha de convidados pra usar no dia do evento.
---

# /recepcao: lista de convidados sincronizada nos tablets

Produto da **Ilha Eventos**. Código em `clientes/Ilha Eventos/recepcao/` (ler o `README.md` de lá).
No ar em `https://recepcao.ilhaeventos.com.br/<evento>/` (Cloudflare Pages `ilhaeventos-recepcao` + banco D1 `recepcao`).

Entrada: planilha (xlsx ou csv) + nome do evento.
- Evento com mesa (casamento, jantar): Nome + Mesa.
- Evento sem mesa (corporativo, médico): Nome + CRM + Especialidade; a tela troca mesa por CRM e agrupa por especialidade.

Saída: um link `#k=<id>.<chave>` que vai igual pra todos os tablets do evento.

## Regras de privacidade (não negociar)

- A lista tem nome de convidado. **Nunca** salvar TSV/CSV da lista no workspace; intermediários no scratchpad.
- A lista e cada registro do diário vão **criptografados** com a chave do link. O servidor não lê nada.
- Não imprimir a lista inteira na conversa sem necessidade; mostrar resumo.
- Testar com dado real só no evento real. Pra testar fluxo, usar a lista fictícia `demo-lista.csv` (evento `/demo/`).

## Workflow

### 1. Achar a planilha
Se o usuário der só o nome ("tá em Downloads, chama Lista"), procurar em `~/Downloads`.
Mais de um arquivo parecido: perguntar qual. xlsx com várias abas: rodar sem `--aba` e conferir no resumo.
Perguntar o **nome do evento** e o **endereço** (slug) se não vieram.

### 2. Converter
```bash
python .claude/skills/recepcao/converter-lista.py "<planilha>" "<scratchpad>/lista.tsv" [--aba "Nome da aba"]
```
O script trata: seção "NÃO CONFIRMADOS" (sem mesa, obs "Não confirmado"), mesa "não vem" (pula),
ACOMPANHANTE (vira linha na mesma mesa), observação/restrição (vai pra Obs), NOME EM MAIÚSCULA,
"Mesa 02"/"4.0". No modo CRM, junta inscrições duplicadas e mantém os dois CRMs se divergirem.

### 3. Conferir com o usuário antes de gerar
Mostrar o resumo do script: total, por mesa ou por especialidade, sem CRM/sem especialidade,
duplicados juntados, pulados. Apontar inconsistências.

### 4. Criar o evento
O Ezequiel e a Thaminy também criam sozinhos pelo **painel** (`recepcao.ilhaeventos.com.br`, com senha). Pelo computador:
```bash
cd "clientes/Ilha Eventos/recepcao"
node gerar-evento.js "<scratchpad>/lista.tsv" "Nome do evento" --slug nome-do-evento --data AAAA-MM-DD
```
(credenciais `CLOUDFLARE_*` do `.env` da raiz exportadas antes.) Grava lista e metadados cifrados no D1 de produção;
o evento aparece no painel e não precisa publicar nada. Exige o painel já configurado (usa a chave pública dele).

### 5. Testar antes de entregar
Abrir o link publicado no Playwright e conferir que `#evento` e `#sTotal` batem e que o status
no topo diz "Sincronizado". Não marcar ninguém em evento real; se precisar testar, ⋯ → Zerar depois.

### 6. Entregar
Link + checklist dos tablets:
1. Abrir o link em cada tablet, numa aba normal (não anônima), com internet na primeira vez.
2. Conferir nome do evento, total e "Sincronizado · N aparelhos" no topo.
3. Bloqueio automático em Nunca, carregador, aba aberta.
4. Sem internet no salão funciona: o topo mostra "N registros aguardando internet" e sobe quando o sinal volta.

### 7. Lista final
```bash
node "clientes/Ilha Eventos/recepcao/exportar.js" "<link do evento>" "<scratchpad>/lista-final.csv"
```
Sai do banco, sem precisar de nenhum tablet ligado. Mesmo formato do botão Exportar do app.

## Como funciona (pra responder dúvidas)

- Toque no nome marca a chegada ("Chegou · Mesa X" ou CRM) com **Desfazer** por 6s.
- Modo sem mesa: dado faltante abre "Completar dados"; tocar em quem chegou abre "Editar dados / Desmarcar".
- Busca pelo começo das palavras do nome; número busca mesa (ou CRM).
- Abas: Buscar, Mesas/Especialidades, Faltam. ⋯: adicionar convidado, exportar, trocar lista, zerar (zera em todos os aparelhos).
- Dois tablets marcando a mesma pessoa: vale a chegada mais cedo, conta uma vez.
- Tablet mínimo: navegador atual (iPadOS 15.4+ ou Android com Chrome atualizado). iPad 3 não roda.

## Versão antiga (sem sincronização)
`clientes/ThaminyIlha.Cerimonial/recepcao/` + `gerar-link.js`, publicada em `ezeos-publicacoes.pages.dev/<slug>/`.
Cada aparelho guarda a própria lista; se o tablet morrer, as presenças vão junto. Não usar pra evento novo.

## Histórico
- 2026-09-18: criada pro Casamento Fernando & Vanessa (19/09, 64 convidados, 6 mesas). Link com a lista inteira no `#` chegou cortado no iPad: daí o link curto criptografado.
- 2026-10-22: modo sem mesa (CRM + especialidade) pro Hospital Nora Teixeira (63 convidados). O tablet desligou no dia 23 e a lista final ficou presa no aparelho.
- 2026-10-24: versão sincronizada (D1 + diário de ações criptografado, vários tablets, exportação pelo servidor) vira produto da Ilha Eventos em `recepcao.ilhaeventos.com.br`.
