---
name: nota-de-call
description: Transforma a transcrição de uma call ou reunião com cliente ou prospect (gravada no OpenWhispr, local) em nota em português com resumo, combinados, objeções, o que o cliente pediu, o que o Ezequiel prometeu e tarefas com data no painel. Salva na pasta do cliente. Use quando o Ezequiel disser "/nota-de-call", "nota da call", "resume a reunião", "transcrição da call com [nome]", "fiz uma call com [nome]", ou colar uma transcrição de reunião.
---

# Nota de call

Entrada: a nota do OpenWhispr, lida direto do banco local dele (somente leitura) com o script da skill. O OpenWhispr só grava e transcreve, em modelo local. O resumo e as tarefas são feitos aqui, nunca pela IA do app (a nuvem dele fica desligada de propósito, áudio de cliente não sai do PC). Se o Ezequiel colar a transcrição na conversa, usar o texto colado.

## 0. Ler a transcrição

Na pasta da skill (`.claude/skills/nota-de-call/`):

```
python -I ler_nota.py listar 5      # últimas notas: id, data (UTC), duração, título
python -I ler_nota.py ler ultima    # transcrição da mais recente
python -I ler_nota.py ler <id>      # transcrição de uma nota específica
python -I ler_nota.py ler <nome>    # acha pelo título, sem ligar pra maiúscula e acento
```

- O Ezequiel pode renomear a nota no OpenWhispr (ex.: "Reunião com Fernando") e depois pedir "busca a reunião do Fernando". Usar `ler fernando`. Se houver mais de uma nota com o nome, o script lista com id e data e eu pergunto qual.
- Sem o Ezequiel dizer qual, rodar `listar`, mostrar as 3 mais recentes e confirmar qual é a call antes de seguir. Não presumir que a mais recente é a certa.
- Saída: `[mm:ss] Voce:` é o microfone dele. `[mm:ss] Outros:` é o áudio do computador (o outro lado). Se o app separar mais de uma voz, vem `Outros 1`, `Outros 2`.
- Horário do banco é UTC, Brasília é UTC menos 3h.
- O script não escreve nada no banco e nada sai da máquina. Nunca abrir o banco por outro caminho nem ler tokens ou outras tabelas.
- Fala do microfone costuma sair mais truncada que a do áudio do sistema. Frase que não faz sentido vai pra `[confirmar]`, não vira conteúdo da nota.

## 1. Identificar a call

Perguntar só o que não der pra tirar da transcrição:
- **Quem**: cliente ativo, prospect ou parceiro. Casar com a pasta em `clientes/`. Se não existir pasta e for prospect com chance real, sugerir `/novo-projeto`.
- **Data** da call (padrão: hoje).

A transcrição rotula "Você" (Ezequiel) e "Outros" (todo mundo do outro lado). A separação mic/sistema é confiável. A separação entre pessoas dentro de "Outros" não é: se tiver mais de uma pessoa do outro lado, separar pelo contexto e avisar que a divisão é suposição.

## 2. Ler o contexto antes de escrever

- `clientes/<cliente>/briefing.md` (e o `CLAUDE.md` da pasta, se houver)
- Notas de call anteriores em `clientes/<cliente>/calls/`
- `_contexto/estrategia.md` só pra casar a tarefa com a meta M1, M2 ou M3

Transcrição de voz erra nome próprio, marca, preço e termo técnico. Corrigir pelo briefing quando for óbvio. Quando não for, marcar `[confirmar]` em vez de chutar. Número, valor e data nunca ficam sem conferir: se a transcrição estiver ambígua, `[confirmar]`.

## 3. Montar a nota

Arquivo: `clientes/<cliente>/calls/AAAA-MM-DD-tema.md`

```
# Call com <nome> · <data>
Duração aproximada · Quem participou

## Resumo
3 a 5 linhas: objetivo da call e o que saiu dela.

## O que o cliente pediu ou quer
- ...

## Combinados
- Eu (Ezequiel) fico de: ... até <data>
- <Cliente> fica de: ... até <data>

## Objeções e dúvidas
- Objeção na fala dele (trecho curto entre aspas) → como foi respondida, ou "ficou em aberto"

## Valores, prazos e decisões
Só o que foi dito de fato. Sem inventar.

## Próximo passo
Uma linha.

## Pra checar
- [confirmar] itens que a transcrição deixou duvidosos
```

Regras de escrita: tom informal e direto, primeira pessoa do Ezequiel, sem travessão, sem o contraste "não é X. É Y.". Frases curtas. Nada de texto de IA genérico. Se uma seção ficar vazia, escrever "nada combinado" em vez de encher.

Não colocar o que não foi dito. Nota que parece mais certa do que a conversa foi é pior que nota curta.

## 4. Transcrição bruta

Salvar completa em `clientes/<cliente>/calls/_transcricoes/AAAA-MM-DD-tema.md`. A pasta `clientes/` é ignorada pelo git (`/clientes/` no `.gitignore`), então nada disso vai pro GitHub no `/syncar`.

## 5. Tarefas no painel

Cada combinado do Ezequiel com data vira:

```
python ezeOS/operacao/painel.py add AAAA-MM-DD "título curto" <cliente> --meta M1 --pronto "critério de pronto"
```

- Meta: M1 se for venda ou proposta, M2 se for entrega ou cobrança de cliente ativo, M3 se for conteúdo ou post.
- Prazo sem data dita na call: propor uma data e avisar antes de gravar.
- O que o cliente ficou de mandar também entra, com data de cobrança, pra o Claudinho lembrar de puxar.

Mostrar a lista do que foi gravado no painel e pedir ok se alguma data foi sugerida por mim.

## 6. Fechar

Entregar ao Ezequiel, em poucas linhas:
1. Caminho da nota salva.
2. As 3 coisas mais importantes da call.
3. As tarefas que entraram no painel, com data.
4. O que ficou `[confirmar]`.

Se a call foi com prospect e saiu interesse, oferecer o próximo passo da escada (proposta via `/proposta-ponto`, site via `/site-do-instagram`) e a mensagem de WhatsApp de follow-up, sem enviar nada.

## Limites

- Nunca mandar transcrição de cliente pra serviço externo (nuvem de resumo, ferramenta online).
- Avisar o cliente que a call está sendo gravada. Lembrar o Ezequiel disso se ele não tiver dito.
- Gravação de call com mais de uma voz do outro lado vem como "Outros". Não atribuir fala a uma pessoa específica sem ter certeza.
- O áudio de reunião não fica guardado no OpenWhispr, só o texto. Retenção de transcrições no app: 90 dias.
