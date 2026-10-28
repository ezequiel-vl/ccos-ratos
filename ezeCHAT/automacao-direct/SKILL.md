---
name: automacao-direct
description: Cria automações de Instagram estilo ManyChat direto do Claude Code, sem mensalidade de ferramenta e sem app na Meta, via API da Zernio. Quem comenta uma palavra-chave num post (ou responde um story com ela) recebe DM automático com botão de link, com trava de seguidor ("segue pra receber"), rastreio de clique, dedupe e logs. Recebe a palavra-chave + o texto do DM + o link e entrega a automação ativa, funcionando em todos os posts da conta. Inclui setup guiado de primeira vez (conta Zernio grátis, conectar Instagram, chave de API). Ative em "cria uma automação de comentário", "quem comentar X recebe o link no direct", "automação estilo ManyChat", "quero fazer comenta-e-recebe", "/automacao-direct". Para publicar e agendar os posts em si use a skill publicar-agendar-posts.
---

# Automação de Direct no Instagram (comenta → recebe DM)

Transforma "comenta {PALAVRA} que eu te mando" num funil real: comentário → DM automático com botão → clique rastreado. O que o ManyChat cobra mensalidade pra fazer, aqui sai por API, com uma vantagem: a automação vale pra **todos os posts da conta** de uma vez (no ManyChat o setup é manual por post).

Ferramenta central: `materiais/scripts/zernio.py`. Referência da API: `materiais/references/zernio-api-automacoes.md`. Desenho do funil e boas práticas: `materiais/references/funil-comentario-dm.md`.

## PASSO 0 — Verificar setup (SEMPRE, antes de qualquer coisa)

```bash
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py check
```

**Se falhar por falta de chave**, conduza o setup guiado, um passo por vez, esperando confirmação. Nunca peça a senha do Instagram (o login é da pessoa, no site da Zernio):

1. **Conta Instagram Profissional** (Business ou Criador). Se for pessoal: Instagram → Configurações → Tipo de conta → Mudar para conta profissional (grátis).
2. **Conta na Zernio**: https://zernio.com — grátis pras 2 primeiras contas conectadas, sem cartão.
3. **Conectar o Instagram** no dashboard da Zernio (OAuth oficial da Meta; a senha não passa pela Zernio nem por você).
4. **Chave de API**: https://zernio.com/dashboard/api-keys → criar → pedir pra pessoa **colar a chave no chat** (começa com `sk_`).
5. **Salvar em `~/.zernio.env`**:

```bash
cat > ~/.zernio.env << 'EOF'
ZERNIO_API_KEY=sk_chave_que_a_pessoa_colou
EOF
chmod 600 ~/.zernio.env
```

6. Rode `check` de novo, confirme o @username com o usuário.

> Config compartilhada com a skill `publicar-agendar-posts`: setup feito uma vez serve pras duas.

## PASSO 1 — Coletar as 4 decisões (pergunte o que faltar)

1. **Palavra-chave.** Uma palavra memorável, MAIÚSCULA (ex: GUIA, VIBE, LISTA, AULA). Com o match por palavra isolada (padrão), palavra comum não dispara dentro de outra ("GUIA" não dispara em "guiado"). Confira com `autos` se a palavra já não está em uso em outra automação da conta.
2. **O que a pessoa recebe.** Texto curto do DM + o link do botão (página, PDF, grupo, checkout). Se o usuário deu só o link e o botão mas não o texto do DM, proponha um curto no padrão "Chegou! 👇 Toca no botão pra abrir {o material}:" e confirme antes de criar. Se o usuário não tem página de destino ainda, pare e diga: primeiro o destino, depois a automação.
3. **Trava de seguidor?** Recomende SIM pra quem quer crescer o perfil (quem não segue recebe um convite de 1 toque pra confirmar que segue antes de receber o link). SEM trava = todo mundo recebe direto (menos atrito, mais entregas).
4. **Responder o comentário publicamente?** Opcional ("te mandei no direct 📩"). Gera prova social, mas polui os comentários em post com muito volume.

## PASSO 2 — Criar a automação

**Automação padrão** (vale pra todos os posts da conta, também dispara se mandarem a palavra no direct):

```bash
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py auto-create \
  --name "GUIA - material X" \
  --keywords GUIA \
  --match word \
  --dm "Chegou! 👇 Toca no botão pra abrir o material:" \
  --button "Acessar Agora|https://exemplo.com/material" \
  --click-tag "clicou-guia" \
  --also-dms \
  --follower-gate
```

**Variante story** (quem responder um story com a palavra também recebe; crie junto quando o usuário usa stories):

```bash
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py auto-create \
  --name "GUIA - material X (story)" \
  --keywords GUIA --match word \
  --dm "Chegou! 👇 Toca no botão pra abrir o material:" \
  --button "Acessar Agora|https://exemplo.com/material" \
  --click-tag "clicou-guia" \
  --story-reply
```

Regras de montagem:
- `--match word` é o padrão e quase sempre o certo. `exact` só quando o usuário quer que o comentário seja SÓ a palavra. `contains` evite: dispara dentro de outras palavras.
- Sem trava de seguidor: remova `--follower-gate`.
- Resposta pública: adicione `--comment-reply "te mandei no direct 📩"`.
- Restringir a 1 post específico: `--post-id <id do post na Meta>` (raro; o padrão account-wide é melhor).
- DM: máx 640 caracteres quando tem botão. Até 3 botões. Emojis OK.
- Mensagens da trava (`--gate-message`, `--gate-button`, `--gate-not-following`) têm padrão genérico bom; personalize com o @ do usuário quando ele quiser.
- Na dúvida, rode com `--dry-run` primeiro e mostre o payload.

## PASSO 3 — Testar de verdade (não pule)

Peça pro usuário (ou alguém da equipe) comentar a palavra num post da conta e acompanhe:

```bash
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py auto-logs <id-da-automacao>
```

O que conferir no log:
- `status: sent` = DM entregue · `status: gated` = convite da trava enviado, e o campo `audienceOutcome` detalha (`gate_sent` → esperando o toque; vira `gate_passed` quando a pessoa toca e recebe) · `status: skipped` = dedupe ou trava pendente. Normal pra quem nunca conversou com a conta é começar em `gated`.
- `clickedAt`/`clickCount` = clique no botão rastreado
- O subcomando `api` já inclui o prefixo `/v1` da API: use `api PATCH /comment-automations/{id} '...'`.

**⚠️ Aviso importante pro usuário:** pra quem **nunca trocou mensagem** com a conta, o DM cai em **"Solicitações de mensagem"** do Instagram, não na caixa principal. É comportamento da Meta, acontece com qualquer ferramenta (ManyChat incluso). Mitigação: avisar no CTA ("olha nas solicitações 👀") e lembrar que a partir da segunda interação cai na caixa normal.

## MONITORAR / GERENCIAR

```bash
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py autos          # lista + enviados/disparos
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py auto-logs <id> # quem comentou, o que aconteceu, cliques
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py auto-off <id>  # pausa
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py auto-on <id>   # reativa
python3 ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py auto-delete <id>
```

Editar uma automação existente (trocar DM, link, keywords): `api PATCH /comment-automations/{id} '{"dmMessage": "..."}'` — campos em `materiais/references/zernio-api-automacoes.md`.

## Checklist de qualidade

- [ ] Automação criada e ATIVA (aparece no `autos`)
- [ ] Teste real feito: comentário → DM chegou (ou gate, se tem trava) → botão abre o link certo
- [ ] Log mostra o disparo e o clique
- [ ] Usuário avisado sobre a pasta "Solicitações"
- [ ] Palavra-chave única na conta (não conflita com automação existente)
- [ ] Nenhuma chave impressa no chat

## Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Comentou e "não chegou nada" | DM caiu em Solicitações | Instagram → Direct → Solicitações. A partir da 2ª interação cai na caixa normal |
| `skipped: Follow gate already pending` | Pessoa comentou de novo com a trava pendente | Normal (dedupe). Ela precisa tocar no botão do gate que já recebeu |
| Log vazio depois de comentar | Palavra não bateu (match word exige palavra isolada) ou automação pausada | Conferir grafia, `autos` pra ver se está ATIVA |
| DM recusado com erro da Meta | Limite de 750 DMs/hora, ou comentário com +7 dias | Esperar; o limite é da Meta, não da ferramenta |
| `ZERNIO_API_KEY não encontrada` | Setup não feito | PASSO 0 |

## Limites da Meta (valem pra qualquer ferramenta, ManyChat incluso)

- 1 private reply por comentário, pra sempre; comentário de até 7 dias
- ~750 private replies/hora por conta
- A relação de seguidor só é revelada pra quem já mandou mensagem pra conta (por isso existe a trava com botão de confirmação)

## O que esta skill NÃO faz

- Não publica nem agenda o post: isso é a skill `publicar-agendar-posts`.
- Não cria a página de destino do link (landing/PDF): tenha o destino pronto antes.
- Não responde conversas abertas com IA (é gatilho → DM, não chatbot de conversa contínua).
