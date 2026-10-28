---
name: publicar-agendar-posts
description: Publica e agenda posts no Instagram (carrossel, reel, story, feed) direto do Claude Code via API da Zernio, sem app na Meta e sem ferramenta paga de agendamento. Recebe as mídias (pasta de slides, imagem ou vídeo) + legenda e publica na hora, agenda pra data/hora, ou monta a grade da semana inteira. Inclui setup guiado de primeira vez (conta Zernio grátis, conectar Instagram, chave de API). Ative em "publica esse post no Instagram", "agenda esse carrossel pra sexta 20h", "agenda meus posts da semana", "posta esse reel", "/publicar-agendar-posts". Para automação de comentário → DM (estilo ManyChat) use a skill automacao-direct. Para publicar cortes em vários perfis de uma vez via Upload-Post use a skill cortes-multi-perfil.
---

# Publicar e Agendar Posts no Instagram (Zernio)

Transforma mídia + legenda em post publicado ou agendado no Instagram, direto do terminal, sem abrir o app.

Ferramenta central: `materiais/scripts/zernio.py` (Python 3 puro, sem instalar nada). Referência da API: `materiais/references/zernio-api.md`.

## PASSO 0 — Verificar setup (SEMPRE, antes de qualquer coisa)

Rode:

```bash
python3 ~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py check
```

**Se falhar por falta de chave**, conduza o setup guiado com o usuário, um passo por vez, esperando a confirmação de cada um. Nunca peça a senha do Instagram (o login é feito pelo usuário, no site da Zernio):

1. **Conta Instagram Profissional.** Pergunte se o Instagram da pessoa é conta Profissional (Business ou Criador). Se for pessoal: Instagram → Configurações → Tipo de conta → Mudar para conta profissional (grátis, 1 minuto).
2. **Conta na Zernio.** Peça pra pessoa criar conta em https://zernio.com — é grátis pras 2 primeiras contas conectadas, sem cartão de crédito.
3. **Conectar o Instagram.** No dashboard da Zernio, clicar em conectar conta → Instagram → fazer o login. É um OAuth oficial da Meta: a pessoa loga direto na página do Instagram, a senha nunca passa pela Zernio nem por você.
4. **Chave de API.** Pedir pra pessoa abrir https://zernio.com/dashboard/api-keys, criar uma chave e **colar a chave no chat** (começa com `sk_`).
5. **Salvar a chave** em `~/.zernio.env` (permissão 600):

```bash
cat > ~/.zernio.env << 'EOF'
ZERNIO_API_KEY=sk_chave_que_a_pessoa_colou
EOF
chmod 600 ~/.zernio.env
```

6. **Confirmar:** rode `check` de novo. Deve listar a conta com `pode postar: True`. O comando salva a conta padrão sozinho. Mostre o @username pro usuário e pergunte se é a conta certa.

> A config `~/.zernio.env` é compartilhada com a skill `automacao-direct`: setup feito uma vez serve pras duas.

## PASSO 1 — Entender o pedido (modos)

| Pedido | Modo |
|---|---|
| "publica agora", "posta esse..." | PUBLICAR (`--now`) |
| "agenda pra {dia} {hora}" | AGENDAR (`--schedule`) |
| "agenda a semana", vários posts | GRADE (vários `--schedule`) |
| "o que tá agendado?", "cancela o post X" | GERENCIAR |

Se o pedido não disser a data/hora de um agendamento, pergunte. Se não disser qual mídia usar, pergunte o caminho da pasta ou dos arquivos. **Não invente legenda**: se não veio legenda, pergunte se é pra escrever uma (e escreva no tom de voz do usuário, se ele tiver documento de voz) ou se ele já tem pronta.

## PASSO 2 — Montar e executar o comando

O script fica em `~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py`. Use path completo.

**Carrossel a partir de uma pasta de slides** (ordem alfabética dos arquivos, máx 10):

```bash
python3 ~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py post \
  --media-dir "./slides-do-post" \
  --caption-file "./legenda.txt" \
  --first-comment "Comenta GUIA que eu te mando o material no direct 👇" \
  --schedule "2026-09-01 20:00"
```

**Reel** (vídeo 9:16, máx 90s):

```bash
python3 ~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py post \
  --media "./video.mp4" --caption "..." --now
```

**Story** (sem legenda visível, sem first comment):

```bash
python3 ~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py post --media "./capa.png" --story --now
```

**Imagem única no feed:** só `--media arquivo.png` + legenda.

Regras de montagem:
- Legenda longa ou com aspas: sempre via `--caption-file` (escreva um .txt temporário), nunca inline.
- Legenda tem limite de 2.200 caracteres e só os primeiros 125 aparecem antes do "mais": a primeira linha precisa segurar sozinha.
- `--first-comment` é o lugar do CTA com palavra-chave quando o post tem automação de DM (skill `automacao-direct`). **Se a legenda já contém o CTA, repita no first comment mesmo assim** (o CTA duplicado é prática recomendada: legenda pro alcance, comentário fixado pra quem rola os comentários).
- Fuso padrão: America/Sao_Paulo. Se o usuário estiver em outro fuso, use `--tz`.
- Mídia local sobe automaticamente (upload presigned). Não use links de Google Drive/Dropbox como `--media` URL, não funcionam: baixe o arquivo primeiro.
- Na dúvida se o pedido era pra publicar de verdade, rode primeiro com `--dry-run` e mostre o payload. O dry-run é 100% seco: não sobe mídia nenhuma (as URLs aparecem como `<upload pendente: ...>`) e não cria nada.

## PASSO 3 — Verificar (não confie no "enviado")

- Publicação imediata: aguarde ~1 min e rode `post-get <id>` até `status: published`, e **entregue a URL do post** (`platformPostUrl`) pro usuário.
- Agendamento: rode `posts --status scheduled` e mostre a linha do post com data/hora, confirmando o fuso.
- Falhou (`failed`)? Leia o campo `erro` do `post-get`, corrija (mídia fora de especificação é o motivo mais comum) e use `post-retry` ou recrie.

## GERENCIAR

```bash
python3 ~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py posts --status scheduled
python3 ~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py post-get <id>
python3 ~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py post-delete <id>
```

## Checklist de qualidade (antes de dar o trabalho por encerrado)

- [ ] Post publicado tem URL entregue ao usuário (ou agendado confirmado na lista com data/hora certa)
- [ ] Slides do carrossel na ordem certa (confira a ordem alfabética da pasta ANTES de enviar: `01.png, 02.png...`)
- [ ] Legenda dentro de 2.200 chars, primeira linha forte (primeiros 125 chars visíveis)
- [ ] First comment com CTA quando o post faz parte de funil de DM
- [ ] Nenhuma chave ou token impresso no chat

## Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `ZERNIO_API_KEY não encontrada` | Setup não feito | PASSO 0 |
| `401` | Chave errada/revogada | Gerar nova em zernio.com/dashboard/api-keys e atualizar `~/.zernio.env` |
| `failed` com erro de mídia | Formato/tamanho fora do padrão | Ver limites em `materiais/references/zernio-api.md`; converter com ffmpeg se precisar |
| Slides fora de ordem | Nomes de arquivo sem zero à esquerda (`1.png, 10.png, 2.png`) | Renomear pra `01.png, 02.png...` |
| Post não aparece na hora agendada | Fuso errado | Conferir `--tz` e o horário em `posts --status scheduled` (mostrado em UTC) |
| "mais de uma conta Instagram" | Várias contas conectadas | Passar `--account @usuario` |

## O que esta skill NÃO faz

- Não posta em TikTok/YouTube/LinkedIn (a API da Zernio suporta; esta skill foca Instagram. Peça que eu adapto o comando).
- Não cria a automação de comentário → DM: isso é a skill `automacao-direct`.
- Não edita vídeo nem gera arte: chega aqui com a mídia pronta.
