# eze.clinicas

Vertical de clínicas da ezeOS. Era a marca "Domínio Local".

## Contexto do cliente

No início de toda conversa, ler `briefing.md` pra entender:
- Segmento e cliente ideal
- Tom de voz da marca
- Serviços e posicionamento
- Identidade visual

Usar essas informações como base pra qualquer tarefa. Não listar o que foi lido. Só usar o contexto naturalmente.

## Tom de voz geral

Ler `../../../_contexto/preferencias.md` pra restrições gerais de escrita da ezeOS.
As preferências específicas estão no `briefing.md` deste diretório e têm prioridade sobre o geral.

## Skills disponíveis

- `/carrossel` — cria carrossel completo (texto + visual HTML + PNG). Já sabe que é pra este cliente

## Estrutura de pastas

```
ezeOS/verticais/clinicas/
  briefing.md        ← contexto e identidade
  CLAUDE.md          ← este arquivo
  carrossel/         ← carrosseis criados (pasta/data-tema/)
  propostas/         ← propostas geradas
  conteudo/          ← textos, roteiros, materiais avulsos
```

## Regras

- Todo entregável vai pra subpasta correspondente (carrossel/, propostas/, conteudo/)
- Nomear arquivos com data: `2026-06-23-tema.md` ou `2026-06-23-tema/`
- Conteúdo fala com dono de clínica, não com marqueteiro
- Identidade visual: o sistema é o da casa (`../../../marca/design-guide.md`). A vertical só troca a cor de sinal pelo carmim `#ef064a`
- Se o briefing estiver incompleto, perguntar antes de criar
