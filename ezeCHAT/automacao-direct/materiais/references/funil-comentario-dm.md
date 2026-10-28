# O funil comentário → DM (desenho e boas práticas)

O fluxo clássico do ManyChat, replicado por API:

```
Post com CTA "comenta {PALAVRA}"
   ↓
Pessoa comenta {PALAVRA}
   ↓
[trava de seguidor?]
   ├── já segue e já conversou com a conta → DM direto
   └── desconhecido → convite de 1 toque ("já segue? toca aqui 👇")
         └── tocou → follow confirmado → DM com o material
   ↓
DM com botão → clique rastreado → etiqueta aplicada (clickTag)
   ↓
Pessoa no seu destino: página, PDF, grupo, checkout
```

## Boas práticas de palavra-chave

- **UMA palavra, MAIÚSCULA no CTA** (a detecção não diferencia maiúscula/minúscula, mas o CTA em caps performa melhor).
- Com `matchMode: word` pode ser palavra natural (GUIA, AULA, LISTA, QUERO): dispara só como palavra isolada, então "GUIA" não dispara em "guiado" nem "guiando".
- Uma palavra por oferta. Ofertas diferentes = automações diferentes, cada uma com sua palavra.
- Antes de criar, `autos` pra conferir que a palavra não colide com automação existente da conta.

## Boas práticas do DM

- Curto, direto, botão em destaque. A pessoa pediu o material: entregue, não faça discurso.
- Botão com verbo: "Acessar Agora", "Baixar o guia", "Entrar no grupo".
- `clickTag` sempre: é de graça e deixa a lista de quem clicou pronta pra remarketing (broadcast/sequência).
- Volume alto? Use `dmMessageVariations` (2-3 variações) pra Meta não ver mensagem idêntica em massa.

## Boas práticas do CTA no post

- Legenda: CTA na última linha ("Comenta GUIA que eu te mando o material no direct 💬").
- Primeiro comentário: repita o CTA (via skill publicar-agendar-posts, flag `--first-comment`).
- **Sempre avise sobre "Solicitações"**: "primeira vez aqui? o direct cai nas solicitações de mensagem 👀". Sem esse aviso, parte dos leads acha que não recebeu nada.

## Trava de seguidor: quando usar

| Situação | Recomendação |
|---|---|
| Perfil em crescimento, material valioso | Trava ON: converte curioso em seguidor antes de entregar |
| Anúncio pago apontando pro post | Trava OFF: atrito mata conversão paga |
| Material raso/isca leve | Trava OFF: não vale o atrito |

O convite de 1 toque tem função dupla: além de checar o follow, o toque conta como "primeira mensagem" pra Meta, o que destrava o envio e move a conversa pra caixa principal nas próximas interações.

## Métricas que importam (do `auto-logs`)

- **disparos** (totalTriggered): quantos comentários bateram na palavra
- **enviados** (totalSent): quantos DMs saíram
- **gate_passed vs gate_sent**: quantos desconhecidos completaram a trava (taxa baixa = mensagem do gate ruim ou material fraco)
- **clickCount**: cliques no botão (a métrica que paga a conta)
- **misses**: comentários que não bateram em nenhuma palavra (olhe de vez em quando: às vezes o público comenta variação que você não previu)
