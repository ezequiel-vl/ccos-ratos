# Como pedir — publicar-agendar-posts

## Primeira vez (setup, ~5 minutos)

Cole no Claude Code:

```
Quero configurar a skill publicar-agendar-posts pra postar no meu Instagram.
Me guia no setup do zero, ainda não tenho conta na Zernio.
```

O Claude vai te guiar: conta grátis na Zernio → conectar seu Instagram (login oficial da Meta, sua senha não passa por ninguém) → colar a chave de API. Uma vez só; a skill automacao-direct usa a mesma config.

## Publicar agora

```
Publica agora no meu Instagram o carrossel que tá na pasta ./meu-post
com a legenda do arquivo ./legenda.txt
```

## Agendar

```
Agenda esse reel (./video.mp4) pra sexta-feira às 19h,
legenda: "3 ferramentas de IA que uso todo dia..."
```

## Grade da semana

```
Tenho 5 carrosséis nas pastas ./posts/seg a ./posts/sex, cada uma com legenda.txt dentro.
Agenda um por dia, sempre às 20h, começando segunda.
```

## Gerenciar

```
O que tá agendado no meu Instagram?
```

```
Cancela o post agendado de quinta.
```

## Dicas

- Nomeie os slides com zero à esquerda (`01.png, 02.png...`) pra ordem sair certa.
- A primeira linha da legenda é o que aparece antes do "...mais": comece com número ou promessa.
- Se o post faz parte de funil de DM ("comenta X que te mando"), crie a automação com a skill **automacao-direct** e use o primeiro comentário do post pro CTA.
- Quer só conferir antes de postar? Peça "faz um dry-run primeiro".
