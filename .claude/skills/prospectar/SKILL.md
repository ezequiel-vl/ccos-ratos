---
name: prospectar
description: Rotina diária de prospecção e reativação da ezeOS, e o parceiro de conversa da prospecção. Monta o lote do dia (10 abordagens nas 4 frentes: carteira de clientes antigos, mão levantada do PONTO, seguidores novos e frio com peneira), faz o diagnóstico rápido de cada empresa (ficha do Google, site, Instagram, WhatsApp), escolhe o serviço certo do cardápio, escreve a mensagem e o roteiro de áudio, conduz as respostas com o RPQ, lista os follow-ups, registra o que o Ezequiel enviou, calcula o volume necessário pra meta, testa variantes de abertura e ajuda a destravar conversa ("mandei e não respondeu", "ela respondeu isso, e agora?", "essa ficou com a minha cara?"). Use quando ele disser "/prospectar", "bora prospectar", "lista do dia", "quem eu abordo hoje", "reativar clientes antigos", "follow-up", "fulano respondeu", "mandei as mensagens", "não respondeu", "e agora?", "quantas abordagens preciso", "qual mensagem tá funcionando", ou quando o painel cobrar a prospecção ou o fechamento de sexta.
---

# Prospectar

Meta: **10 abordagens por dia útil**. Contexto e cardápio em `ezeOS/operacao/README.md`. Script da conversa do Ponto Digital em `ezeOS/ofertas/2026-10-16-ponto-digital/script-whatsapp.md`. Roteiros de abertura e áudio em `ezeOS/operacao/roteiros-abordagem.md`.

A abordagem não vende na primeira mensagem: ela abre conversa com a pessoa certa. Trabalho cirúrgico, nunca disparo em massa.

## 1. Ver o estado

```
python ezeOS/operacao/painel.py --ver
```

Quem está no funil **Prospecção** do CRM (pipeline `cc516c8b-d349-4018-b774-3ff355840166`):

```
python ezeOS/operacao/crm.py sql "select c.name, c.phone, s.name etapa, d.origin_channel, d.updated_at::date from whatsapp_hub.deals d join whatsapp_hub.contacts c on c.id=d.contact_id join whatsapp_hub.stages s on s.id=d.stage_id where d.pipeline_id='cc516c8b-d349-4018-b774-3ff355840166' order by d.updated_at"
```

Gravar no CRM: contato (`whatsapp_hub.contacts`, telefone com DDI, único por org; `org_id` `e1153767-b2bd-495f-b567-4cf46d15a0ff` explícito) + negócio (`whatsapp_hub.deals` com `pipeline_id`, `stage_id`, `title` "<serviço> · <empresa>", `origin_channel` `reativacao`, `ponto`, `morno` ou `prospeccao`, `lead_type` `Cliente` pra cliente antigo e `Lead` pra novo, `org_id` explícito). Diagnóstico e mensagem em `whatsapp_hub.crm_activities` (`type` entre: task, note, followup, call, meeting, stage_change) ligada ao deal. Escrita no banco autorizada pelo Ezequiel só pra contato e negócio de prospecção.

Quanto precisa prospectar pra meta (usa as taxas reais do CRM a partir de 30 abordados):

```
python ezeOS/operacao/funil.py calc --meta 5
```

## 2. Primeiro quem já está conversando

1. **Quem respondeu**: responder com o RPQ (seção 6). Prioridade máxima, antes de qualquer gente nova.
2. **Mão levantada**: quem comentou PONTO ou respondeu story com PONTO (`python ~/.claude/skills/automacao-direct/materiais/scripts/zernio.py auto-logs 6ae12682168a90de1622e475` e `6ae12683168a90de1622e477`). A automação já mandou uma pergunta; o Ezequiel puxa a conversa em até 24h se a pessoa não respondeu.
3. **Follow-ups do dia**: D+2 (lembrete leve) e D+5 (último toque com algo novo, tipo um print). Sem resposta depois do D+5: etapa "Sem resposta", volta pra fila em 60 dias.

## 3. Completar o lote nas 4 frentes (até 10)

| Ordem | Frente | Fonte | Abertura |
| --- | --- | --- | --- |
| 1 | **Carteira (quente)** | `operacao/prospeccao/carteira-gmn.md` (92 fichas) e `instagram-seguindo.md` | áudio de 5s + diagnóstico com número real da ficha |
| 2 | **Mão levantada** | automação PONTO | conversa já aberta pela DM automática |
| 3 | **Morno** | seguidores novos da @agenciaezeos nos últimos 3 dias que passam na peneira | boas-vindas com pergunta, pelo direct |
| 4 | **Frio** | Google Maps (nicho + cidade) e perfis que passam na peneira | áudio de 5s ou texto direto, com uma prova da tela dela |

### A peneira (só aborda quem passa em 3 dos 5)

1. Negócio local de serviço (clínica, consultório, prestador, comércio de bairro), com dono identificável.
2. O dono aparece ou responde: perfil com rosto, WhatsApp no perfil ou na ficha.
3. Está ativo: post ou story nos últimos 15 dias, ou avaliação respondida no Google.
4. Tem uma porta falhando que dá pra mostrar em print: sem site, ficha fraca, botão "Site" indo pro Instagram, e-mail @gmail.
5. Atende numa cidade onde dá pra fazer a busca "serviço + bairro" e mostrar quem aparece na frente.

Não passou: não manda. Volume vem da rotina, não de mandar pra qualquer um.

### Diagnóstico de 2 minutos (quatro portas)

- **Google:** a ficha aparece? Tem botão de site? Nota e número de avaliações? Aparece na busca "serviço + bairro"? Na carteira, pegar os números do painel (visualizações, buscas, ligações, cliques no site) no gerenciador do Google.
- **Site:** tem? Abre no celular? Tem WhatsApp com mensagem pronta?
- **Instagram:** fala com cliente ou com colega? Posta? Bio diz o que faz e onde?
- **WhatsApp:** é Business? Tem catálogo e mensagem de ausência?

Com o diagnóstico, escolhe **um** serviço do cardápio (o próximo degrau, não o pacote todo). Pra carteira de clínicas sem site (ou com site fraco), a oferta é **só o site personalizado, R$ 1.000, entrega em até 10 dias** (valor só no 1x1).

## 4. Mensagem

- **"Você" na primeira mensagem e nos follow-ups sem resposta; passa pro "tu" quando a pessoa responder.** Tom do Ezequiel: curto, primeira pessoa, sem travessão, sem "não é X, é Y", sem emoji.
- Abre com algo verificável **dela** ("busquei harmonização no Jardim Esplanada e tua clínica aparece em 4º, atrás da X"), nunca com elogio genérico nem com pitch decorado.
- **Cliente antigo:** "aqui é o Ezequiel, que montou a ficha do Google da [empresa]", **só o nome, sem citar marca** (nem Domínio Local, nem ezeOS), e traz o número de hoje.
- **Frio:** começar pelo áudio de 5s (roteiro em `roteiros-abordagem.md`), que prova que é gente e não robô. Depois o texto com a prova da tela dela.
- Termina com **uma** pergunta fácil de responder ("posso te mandar o print?"). Nunca uma lista de perguntas.
- Mão levantada nunca recebe só o link: sempre link + pergunta.
- Preço só se ela perguntar, ou na proposta (`/proposta-ponto`).

## 5. Entregar o lote

Gravar em `ezeOS/operacao/prospeccao/AAAA-MM-DD.md`, uma seção por empresa: nome, contato, frente, **variante**, diagnóstico em 3 linhas, serviço escolhido, roteiro do áudio (se tiver) e a mensagem pronta pra copiar. Subir no funil do CRM na etapa "A abordar", com o código da variante em `deals.utm_content` (`carteira-A`, `frio-B`, `morno-A`, `ponto-auto`...). As aberturas e os códigos estão em `roteiros-abordagem.md`; dentro do mesmo lote, alternar metade e metade entre as variantes da frente.

O Ezequiel envia do WhatsApp ou do direct dele. Quando ele disser quantas mandou:

```
python ezeOS/operacao/painel.py log prospeccao <n>
python ezeOS/operacao/painel.py log reativacao <n>
python ezeOS/operacao/painel.py add <data D+2> "Follow-up: <empresa>"
```

E mover os negócios pra "Abordado".

## 6. Quando a pessoa responde: RPQ

Nada de disparar pergunta atrás de pergunta. Cada resposta do Ezequiel tem três tempos:

1. **Reconhecer:** valida o que ela disse ("faz sentido", "isso é bem comum em clínica").
2. **Personalizar:** mostra que ouviu, ligando com o caso dela ou de um cliente parecido ("tive uma cliente em São Leopoldo que aparecia na busca e perdia o clique porque o botão ia pro Instagram").
3. **Questionar:** uma pergunta de intenção ("o que te fez olhar pra isso agora?", "isso tá te custando cliente hoje ou é mais incômodo?").

Interesse claro: proposta no mesmo dia (`/proposta-ponto` pro Ponto Digital), negócio pra "Proposta". Sinal de que não é a hora: agradece, marca "Não é agora" com data de retorno e segue pro próximo. Quem tem volume não precisa forçar.

## 7. Modo conversa: o Ezequiel traz o caso

Quando ele chegar com "mandei e não respondeu", "ela respondeu isso, e agora?", "minha abordagem travou aqui" ou "essa ficou com a minha cara?":

1. **Achar a pessoa no CRM** pelo nome ou telefone: etapa, frente, variante e as notas (`crm_activities`) com o que já foi mandado.
2. **Ler o caso inteiro** antes de sugerir. Se ele colou a resposta dela, ler a resposta literal.
3. **Responder com 2 ou 3 opções curtas**, no tom dele, dizendo o que cada uma tenta (reabrir, aprofundar a dor, levar pro print, levar pra proposta). Nada de opção genérica que serviria pra qualquer um.
   - **Não respondeu:** checar se está no D+2 ou D+5; se a abertura pediu demais, trocar por algo mais fácil de responder (um print, uma pergunta de sim ou não).
   - **Respondeu:** RPQ (seção 6). Se ela trouxe objeção (preço, tempo, "já tenho alguém"), reconhecer antes de qualquer argumento.
   - **Depois da proposta / negociação:** respostas prontas em `roteiros-abordagem.md` ("Depois da proposta"). Nada de desconto antes de entender o que "melhorar o valor" quer dizer; primeiro forma de pagamento, depois escopo, desconto por último. Aqui o Claudinho acompanha até o fechamento, não para na prospecção.
   - **"Ficou com a minha cara?"**: revisar contra o tom (curto, "tu", sem travessão, sem cara de script) e devolver a versão ajustada com o motivo de cada mudança.
4. **Registrar**: nota em `crm_activities` com o que aconteceu e a próxima ação; mover a etapa; follow-up com data no painel.
5. **Aprender**: se a mesma trava aparecer em 3 conversas, propor mudar a abertura ou o roteiro (nova variante em `roteiros-abordagem.md`).

## 8. Fechamento de sexta

```
python ezeOS/operacao/funil.py relatorio --dias 30
python ezeOS/operacao/funil.py calc --meta 5
```

Mostrar ao Ezequiel: abordados, respostas, propostas e fechados da semana, conversão por frente e por variante, e se o ritmo atual bate a meta. Decidir com ele qual variante sai (só com 10 envios ou mais por variante; com menos, segue testando). Anotar a decisão no "Histórico das variantes" de `roteiros-abordagem.md` e registrar `python ezeOS/operacao/painel.py log fechamento`.

## Rotina que o Claudinho cobra

**Todo dia útil:** responder quem respondeu (RPQ) · puxar a mão levantada do PONTO · boas-vindas aos seguidores novos que passam na peneira · completar 10 abordagens.
**Toda sexta:** fechamento da semana (seção 8) · pelo menos um post com CTA de palavra-chave (PONTO) na grade da semana seguinte · revisar a peneira com base em quem respondeu e quem fechou.

## Regras

- Nunca mandar mensagem no lugar do Ezequiel.
- Dado de cliente fica no workspace (`operacao/prospeccao/`, fora do git) ou no CRM, nunca em serviço externo.
- Scripts de cursos e e-books de terceiros servem de referência de estrutura, nunca copiados: tudo é reescrito no tom do Ezequiel.
