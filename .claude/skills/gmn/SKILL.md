---
name: gmn
description: >
  Diagnostica e atualiza a ficha do Google Meu Negócio (GMN) de um cliente da ezeOS pelo Claude in
  Chrome, com o Ezequiel logado: lê os 3 primeiros do ranking, monta categoria, descrição, serviços
  com descrição, áreas, posts e respostas de avaliação, mostra tudo pra aprovação e só então aplica
  na ficha e confere na tela. Use quando o Ezequiel disser "/gmn", "atualiza o GMN de [cliente]",
  "otimiza a ficha do Google", "responde as avaliações de [cliente]", "post na ficha", "monta a
  ficha do Google", "diagnóstico do GMN", ou quando a /varredura apontar ficha parada.
---

# /gmn: ficha do Google do cliente, do diagnóstico à tela

Entrada: cliente (e o que fazer: diagnóstico, montar a ficha, post, avaliações).
Saída: pacote de texto aprovado, aplicado na ficha e conferido na tela.

Roda pela extensão Claude in Chrome, com o Ezequiel logado na conta que administra a ficha. Não usa API nem ferramenta de terceiro. Contexto da oferta: `ezeOS/ofertas/2026-10-16-ponto-digital/oferta.md` (bloco "Google Meu Negócio" e plano Ficha ativa).

## Regras que não se negociam

1. **Nada é gravado na ficha sem o ok do Ezequiel** sobre o texto exato. Mostrar, esperar o ok, aplicar.
2. **Número, endereço, horário, telefone e serviço nunca são inventados.** Vêm do briefing, do site do cliente ou do Ezequiel. Se faltar, perguntar.
3. **Não mexer no nome da empresa** nem enfiar palavra-chave nele. Nome diferente do real é motivo de suspensão da ficha.
4. **Palavra-chave com cidade ou bairro só onde o cliente atende de verdade.** Cidade vizinha forçada não entra. Nada de lista de palavras solta: o texto tem que ler como gente falando.
5. **NAP igual ao site**: nome, endereço, telefone e horário da ficha batem com o site, o WhatsApp Business e o Instagram. Se estiver diferente, avisar antes de escolher qual vale.
6. **Foto só real** (espaço, equipe, atendimento, trabalho). Foto de banco não sobe.
7. **Uma mudança por vez e em ritmo humano.** Edição em massa e repetida pode acionar revisão do Google. Em ficha de cliente, aplicar por bloco (categorias, depois descrição, depois serviços), conferindo cada um.
8. **Dado de cliente fica em `clientes/<cliente>/gmn/`**, nunca em pasta versionada da casa. A skill não salva nada de cliente fora dali.
9. **Tom do Ezequiel**: informal e direto nos documentos pra ele. O texto que vai na ficha é do cliente: claro, profissional, sem travessão, sem "não é X, é Y", sem cara de texto de IA genérico. Se o cliente tiver voz própria no `briefing.md`, seguir.
10. Se a ficha estiver suspensa, o Chrome pedir verificação ou o login travar: parar e avisar. Recuperação de ficha suspensa está fora do escopo (ver `oferta.md`).

## Limites do Google (conferir na tela antes de aplicar, mudam)

| Campo | Limite aproximado |
| --- | --- |
| Nome | 58 caracteres (não mexer) |
| Descrição da empresa | 750 caracteres, e só os 250 primeiros aparecem antes do "mais" |
| Descrição de serviço | 300 caracteres |
| Post | 1.500 caracteres, o começo é o que vale |
| Categorias | 1 principal + até 9 adicionais |

Se a tela mostrar outro limite, valer a tela.

## 1. Preparar

1. Ler `clientes/<cliente>/briefing.md` (serviço principal, bairro, região, voz, o que o cliente quer vender). Sem pasta de cliente, perguntar o básico.
2. Ler o site do cliente, se existir (serviços, horário, endereço, telefone).
3. Carregar as ferramentas do Chrome numa chamada só e rodar `tabs_context_mcp` antes de abrir qualquer aba. Abrir aba nova, nunca reaproveitar a do Ezequiel sem ele pedir.
4. Pedir pro Ezequiel confirmar que está logado na conta que gerencia a ficha. Ele passa o login e a verificação, eu não.

## 2. Diagnóstico (só leitura)

Faz parte do `/proposta-ponto` e da `/varredura`. Não grava nada. Duas fases:

- **Fase A, leitura pública (Google Maps, sem login):** nome, posição, nota, nº de avaliações, categorias, site, telefone, endereço, aba Sobre, avaliações e se têm resposta. Dá pra fazer de qualquer ficha, inclusive de concorrente e de prospect. Testado em 2026-11-13 na ficha da Dra. Renata.
- **Fase B, leitura no painel (precisa do login do Ezequiel):** descrição da empresa, serviços cadastrados e suas descrições, posts, fotos, horário completo, desempenho. O Maps público não mostra isso. Só rodar com o Ezequiel logado na conta que administra a ficha.

Passos:

1. Buscar no Google, do jeito que o cliente do cliente busca ("[serviço] [bairro/cidade]"), e anotar os 3 primeiros do mapa.
2. De cada um, ler da ficha pública: categoria principal e adicionais, nº e nota das avaliações, se responde avaliação, descrição, serviços e se têm descrição, horário, fotos (quantas e se são reais), site, último post.
3. Ler a ficha do cliente do mesmo jeito.
4. Entregar tabela comparando: **o que eles têm que o cliente não tem** e **onde a descrição ou o serviço deles está fraco** (oportunidade). Só fato lido na tela. Impressão minha vai marcada como impressão.
5. Salvar em `clientes/<cliente>/gmn/AAAA-MM-DD-diagnostico.md`.

Checklist da ficha do cliente (marcar ok ou falta):
- [ ] categoria principal certa e categorias adicionais de nicho (serviço de alta margem como categoria quando existir)
- [ ] descrição da empresa com o que faz, onde atende, há quanto tempo, sem lista de palavra-chave
- [ ] cada serviço cadastrado com descrição
- [ ] área de atendimento ou endereço correto
- [ ] horário completo, incluindo feriado
- [ ] fotos reais (capa, logo, espaço, equipe, trabalho)
- [ ] site e WhatsApp ligados
- [ ] link curto de avaliação pronto
- [ ] NAP igual ao site e ao WhatsApp
- [ ] post nos últimos 7 a 14 dias
- [ ] avaliações respondidas e rápido

## 3. Montar o pacote (ainda não grava)

Escrever em `clientes/<cliente>/gmn/AAAA-MM-DD-pacote.md`:

- **Categorias**: principal + adicionais, com o porquê de cada uma em uma linha
- **Descrição da empresa**: com a contagem de caracteres. Os primeiros 250 já dizem o que faz e onde
- **Serviços**: nome + descrição de até 300 caracteres cada, com a cidade só se o cliente atende lá de verdade
- **Áreas de atendimento**: só as reais
- **Fotos**: lista do que falta pedir ao cliente, e legenda e nome de arquivo com o serviço (ex.: `harmonizacao-facial-sao-sebastiao-do-cai.jpg`)
- **Primeiro post**: texto + imagem sugerida
- **O que ficou fora e por quê** (ex.: cidade vizinha não usada)

Mostrar o resumo no chat e pedir o ok. Ajustar até ele aprovar. Pacote aprovado vira a fonte do que vai pra tela.

## 4. Aplicar (só com o ok)

Pelo Chrome, no gerenciador da ficha:

1. Um bloco por vez: categorias, descrição, serviços, áreas, horário.
2. Depois de cada bloco, recarregar e conferir na tela que o texto salvo é o aprovado (ler a página, não presumir). Se o Google pedir revisão ou mostrar "em análise", avisar.
3. Foto: só sobe o que o Ezequiel ou o cliente mandou. Alt e nome de arquivo seguem o pacote.
4. Se aparecer diálogo de confirmação do navegador, avisar o Ezequiel antes de clicar (pode travar a extensão).
5. Se algo falhar 2 ou 3 vezes (botão que não responde, campo que não salva), parar e dizer onde travou. Não ficar insistindo.

Ao fim, `AAAA-MM-DD-aplicado.md` na mesma pasta com o que mudou, antes e depois, e o que o Google deixou "em análise".

## 5. Post e avaliações (rotina do plano Ficha ativa)

- **Post semanal**: texto curto, começa pelo que importa, um CTA (ligar, WhatsApp, site), imagem real. Mostrar pro Ezequiel, aprovar, publicar, conferir que apareceu.
- **Resposta de avaliação**: responder rápido, com o nome da pessoa e o serviço dito por ela quando fizer sentido, agradecimento sem exagero, sem script igual em todas. **Avaliação negativa**: nunca responder sozinha, preparar a resposta e mostrar. Nada de dado de paciente ou cliente na resposta (clínica tem regra de sigilo).
- Lote de respostas: mostrar todas juntas pra aprovação, e publicar em ritmo humano, não tudo de uma vez.

## 6. Relatório mensal (Ficha ativa)

Ler no painel da ficha: visualizações, cliques no site, ligações, rotas e pedidos de mensagem do período, e comparar com o mês anterior. Só número que está na tela. Salvar em `clientes/<cliente>/gmn/AAAA-MM-relatorio.md`. Se visualização sobe e contato não, registrar: é o gancho pro Movimento.

## 7. Fechar

- Painel: `python ezeOS/operacao/painel.py feito <id>` se for item da agenda. Próximo post ou revisão com data: `painel.py add`.
- Avisar o que ficou pendente do cliente (foto, acesso, serviço a confirmar).
- Se a conversa for virar rotina de vários clientes, sugerir conversa nova por cliente (economia de limite).

## Modelo

Tarefa de aplicar e postar roda bem em Sonnet. Diagnóstico estratégico, texto da ficha e resposta a avaliação negativa pedem Opus.
