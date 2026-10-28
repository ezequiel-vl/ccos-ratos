# Zernio API — referência condensada (automações comentário → DM)

Base: `https://zernio.com/api/v1` · Auth: `Authorization: Bearer sk_...` · Doc: https://docs.zernio.com

## Criar — `POST /v1/comment-automations`

| Campo | Tipo | Notas |
|---|---|---|
| `profileId`, `accountId` | string | obrigatórios (o script resolve sozinho da config) |
| `trigger` | `comment` \| `story_reply` | comment = padrão. story_reply = resposta a story |
| `platformPostId` | string | omitir = vale pra TODOS os posts (account-wide, recomendado). Account-wide empilha automações ilimitadas, cada uma com suas keywords |
| `keywords` | array | vazio = qualquer comentário dispara (evitar) |
| `matchMode` | `exact` \| `word` \| `contains` | **word** = palavra isolada (recomendado). exact = comentário inteiro igual. contains = substring (evitar: "app" dispara em "happy") |
| `excludeKeywords` | array | comentário com uma dessas nunca dispara |
| `typoTolerance` | bool | só com word; tolera 1-2 erros de digitação (keywords 4+ chars) |
| `dmMessage` | string | obrigatório. Máx 640 chars com botões, ~1000 sem |
| `buttons` | array | 1-3 de `{"type":"url","title":"...","url":"..."}` |
| `dmMessageVariations` | array | até 5 textos alternados aleatoriamente (anti-padrão de spam) |
| `commentReply` | string | resposta pública opcional ao comentário |
| `alsoMatchInDms` | bool | keyword mandada no direct também dispara (dedupe separado por porta) |
| `linkTracking` | bool | default true: links dos botões viram redirect rastreado (conta cliques) |
| `clickTag` | string | etiqueta aplicada ao contato que clica (segmentação p/ broadcast futuro) |
| `dmDelaySeconds` | int | espera antes do DM (máx 86400). Dedupe acontece na hora do comentário |
| `commentReplyDelaySeconds` | int | espera da resposta pública (nunca sai antes do DM) |
| `audience` | obj | `{"followerStatus":"follower"\|"non_follower"\|"any", "minFollowerCount":N, "whenUnknown":"send"\|"skip"\|"verify"}` |
| `followGate` | obj | com whenUnknown=verify: `{"message","buttonLabel","notFollowingMessage"}` — convite de 1 toque; o toque dá o consent da Meta e resolve o follow. Quem já segue E já conversou com a conta pula o gate |
| `template` | obj | card de produto (imagem+título+botões, até 10 em carrossel) NO LUGAR do dmMessage simples |

## Gerenciar

- `GET /v1/comment-automations?profileId=...` — lista com stats (totalTriggered/totalSent/totalFailed)
- `GET /v1/comment-automations/{id}` — detalhe
- `PATCH /v1/comment-automations/{id}` — editar qualquer campo; `{"isActive": false}` pausa; `buttons: []` limpa botões
- `DELETE /v1/comment-automations/{id}` — apaga automação e logs
- `GET /v1/comment-automations/{id}/logs` — cada disparo

## Ler os logs

| Campo | Significado |
|---|---|
| `status` | `sent` (DM entregue) · `gated` (convite da trava enviado) · `skipped` (dedupe/trava pendente) · `failed` |
| `audienceOutcome` | `gate_sent` → `gate_passed` (tocou e recebeu) · `blocked` |
| `commenterIsFollower` | true/false/null (null = Meta não revelou; vira true/false quando a pessoa toca no gate) |
| `gateResolvedAt` | quando tocou no botão da trava |
| `clickedAt`, `clickCount` | clique no link do DM |
| `misses` | comentários que não bateram em nenhuma keyword (amostra, 14 dias) |

## Limites da Meta (qualquer ferramenta)

- **1 private reply por comentário, pra sempre** (a Meta bloqueia a 2ª)
- Comentário precisa ter **menos de 7 dias**
- **~750 private replies/hora** por conta
- Relação de seguidor: a Meta só revela pra quem **já mandou mensagem** pra conta. Por isso `whenUnknown` importa: `verify` manda o convite de 1 toque (o toque é a 1ª mensagem e destrava tudo)
- 1º DM pra quem nunca conversou cai em **"Solicitações de mensagem"**, não na caixa principal
