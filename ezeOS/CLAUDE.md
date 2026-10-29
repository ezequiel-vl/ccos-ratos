# ezeOS

A casa. Essa pasta guarda o trabalho da própria agência, não o de cliente.

## Contexto

No início de toda conversa dentro dessa pasta, ler:

1. `../marca/2026-10-15-posicionamento-ezeos.md` (tese, escada de ofertas, frases da marca)
2. `../marca/design-guide.md` (sistema visual)
3. `../_contexto/preferencias.md` (restrições de escrita)

Usar naturalmente, sem listar o que foi lido.

## Estrutura

```
ezeOS/
  CLAUDE.md          ← este arquivo
  site/              ← o site da ezeOS
  posts/             ← carrosséis, reels e roteiros da casa
  videos/            ← vídeos em Remotion (reels, anúncio, story, versão contínua de carrossel). Carrossel continua em HTML (posts/.../_base). Ver videos/README.md
  ofertas/           ← escopo, proposta e script de cada degrau da escada
    2026-10-16-ponto-digital/  ← escopo, script e modelo da proposta do degrau 1. Proposta por clínica sai com /proposta-ponto
  swipe/             ← referências de trabalho com o que roubar de cada uma, no ar com senha em swipe.ezeos.com.br. Adicionar com /swipe <link>. Ver swipe/README.md
  verticais/
    clinicas/        ← eze.clinicas, a vertical de clínicas
```

A pasta se chama `posts/` e não `conteudo/` de propósito: `conteudo/` está no `.gitignore` e o material da casa precisa ser versionado.

## Regras

- Entregável vai pra subpasta certa, nomeado com data: `2026-10-15-tema.md` ou `2026-10-15-tema/`
- Material da casa fala com dono de negócio local, não com marqueteiro
- A escada de ofertas é a referência de tudo que se vende. Degrau 1 é o Ponto Digital, degrau 3 é o Sistema de Demanda Contínua
- O sistema visual é um só pra casa e pras verticais. O que muda entre elas é a cor de sinal
- Marca pessoal do Ezequiel (eze.cc) não mora aqui, fica em `../clientes/eze.cc/`
