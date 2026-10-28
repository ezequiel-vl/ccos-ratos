# Zernio API — referência condensada (posts no Instagram)

Base: `https://zernio.com/api/v1` · Auth: header `Authorization: Bearer sk_...`
Doc completa: https://docs.zernio.com

## Conceitos

- **Profile** = pasta que agrupa contas (uma "marca"). **Account** = conta social conectada.
- IDs são strings de 24 chars em campo `_id`.
- Preço: 2 primeiras contas conectadas grátis pra sempre (sem cartão); da 3ª à 10ª, US$6/conta/mês. Tudo incluso (posts ilimitados, automações, inbox, analytics).

## Criar post — `POST /v1/posts`

```json
{
  "content": "legenda",
  "mediaItems": [{"type": "image|video", "url": "https://..."}],
  "platforms": [{
    "platform": "instagram",
    "accountId": "...",
    "platformSpecificData": { }
  }],
  "scheduledFor": "2026-09-01T20:00:00",
  "timezone": "America/Sao_Paulo"
}
```

Modos: `scheduledFor`+`timezone` = agenda · `publishNow: true` = publica já · nenhum = rascunho.
Status do post: `scheduled → publishing → published` (ou `failed`/`partial`). Publicado traz `platformPostUrl`.

### platformSpecificData (Instagram)

| Campo | Efeito |
|---|---|
| `contentType: "story"` | Story. Sem esse campo: vídeo único vira Reel, imagem vai pro feed |
| `shareToFeed: false` | Reel só na aba Reels |
| `firstComment` | 1º comentário automático (feed/carrossel; não funciona em story) |
| `collaborators: ["user"]` | Até 3 colaboradores (contas públicas Business/Creator) |
| `instagramThumbnail` | URL de capa do Reel (1080x1920) |
| `isAiGenerated: true` | Selo de mídia gerada por IA |
| `userTags` | Marcar pessoas (imagem exige x/y 0.0-1.0) |

## Limites da Meta (valem pra qualquer ferramenta)

- **100 posts por 24h** (janela móvel) por conta; carrossel conta como 1
- Legenda: 2.200 chars; primeiros 125 visíveis antes do "mais"
- Carrossel: até 10 mídias, mesma proporção do 1º item
- Reel: 9:16, 3s-90s, H.264, até 300 MB · Story: 9:16, até 60s, 100 MB · Feed: 4:5 a 1.91:1
- Imagens: JPEG/PNG até 8 MB (acima disso a Zernio comprime sozinha)
- Story via API: sem legenda visível, sem link sticker (limitação do Instagram)

## Upload de mídia — `POST /v1/media/presign`

```
{"filename": "foto.jpg", "contentType": "image/jpeg"}
→ {"uploadUrl": "PUT aqui", "publicUrl": "usar no mediaItems"}
```

PUT do arquivo no `uploadUrl` (sem auth). Válido 1h; o arquivo fica 7 dias em storage temporário até um post publicar com ele. **Links de Drive/Dropbox NÃO funcionam** como URL de mídia (devolvem HTML). URLs do Supabase Storage funcionam (a Zernio faz proxy).

## Gerenciar posts

- `GET /v1/posts?status=scheduled` — listar
- `GET /v1/posts/{id}` — detalhe/status
- `DELETE /v1/posts/{id}` — cancela rascunho/agendado (publicado não deleta)
- `POST /v1/posts/{id}/retry` — retenta um failed

## Contas

- `GET /v1/accounts` — lista conectadas
- `GET /v1/accounts/health` — saúde/token/canPost por conta (tokens renovam sozinhos)

## Erros comuns da API

| HTTP | Significado |
|---|---|
| 401 | Chave inválida → gerar nova no dashboard |
| 400 `platform_error` | A Meta recusou (mídia fora de spec, limite de rate) — o payload traz o erro da Meta verbatim |
