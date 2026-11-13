---
name: varredura
description: Varredura semanal (segunda) dos clientes ativos da ezeOS (a própria ezeOS, Ilha Eventos e ThaminyIlha Cerimonial). Checa site no ar e SEO técnico, posts da semana, ficha do Google, e transforma o que achou em tarefas com data no painel e em propostas de melhoria. Use quando o Ezequiel disser "/varredura", "varre os clientes", "como estão os sites", "checa o SEO", ou quando o painel cobrar a varredura.
---

# Varredura semanal dos ativos

## 1. Parte automática

```
python ezeOS/operacao/varredura.py
```

Gera `ezeOS/operacao/varreduras/AAAA-MM-DD.md` com site (status, título, descrição, noindex, canonical, og:image, H1, schema, robots, sitemap, tempo) e posts dos últimos 7 dias de quem está na Zernio.

## 2. Parte na mão (pelo navegador, quando a extensão Claude in Chrome estiver conectada)

- **Ficha do Google** de cada um: foto nova no mês, avaliações respondidas, post da semana, horário certo.
- **Busca do serviço principal** em aba anônima ("cerimonialista porto alegre", "eventos corporativos [cidade]", "agência site negócio local [cidade]"): posição e quem aparece antes.
- **Instagram** de quem não está na Zernio: quantos posts na semana, stories, se a bio e o link estão certos.

## 3. Virar ação

Cada problema vira uma tarefa com data no painel (`painel.py add`), e cada oportunidade vira uma proposta de melhoria pro Ezequiel aprovar. Comparar com a varredura anterior em `varreduras/` e dizer o que melhorou e o que piorou.

Fechar com:

```
python ezeOS/operacao/painel.py log varredura
```

## Clientes ativos

| Cliente | Site | Instagram | Zernio |
| --- | --- | --- | --- |
| ezeOS | ezeos.com.br | @agenciaezeos | sim (`~/.zernio.env`) |
| Ilha Eventos | ilhaeventos.com.br | ainda não tem | não |
| ThaminyIlha Cerimonial | thaminyilha.com.br | @thaminyilha.cerimonial | não |

Cliente ativo novo entra na lista `ATIVOS` do `varredura.py` e nesta tabela.
