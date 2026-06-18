# ezeOS — Codex OS

## O que é esse workspace
Workspace operacional da ezeOS, agência solo do Ezequiel. Aqui ficam os clientes, projetos e ferramentas do dia a dia.

**Estrutura de pastas:**
- `clientes/` — uma pasta por cliente com briefing e materiais
- `clientes/ThaminyIlha.Cerimonial/` — conta da esposa (marketing e comunicação)
- `SOLO.OS/` — projeto e curso onde Ezequiel ensina freelancers e agências a montar o sistema operacional do negócio
- `briefings/` — briefings avulsos e documentos de entrada
- `propostas/` — propostas comerciais geradas
- `conteudo/` — conteúdo produzido (posts, textos, roteiros)
- `templates/skills/` — templates de skills prontos pra personalizar com /mapear
- `templates/ferramentas/catalogo.md` — APIs e ferramentas disponíveis pra usar em skills

## Sobre o negócio
ezeOS é a agência solo do Ezequiel. O serviço principal é o Sistema de Demanda Contínua — uma estrutura que transforma a presença no Instagram de prestadores de serviço em fluxo previsível de clientes, via três etapas: Atrair, Capturar e Converter. Ezequiel cuida de tudo: estratégia, entrega e operação.

## O que mais fazemos aqui
- Reposicionamento de perfil no Instagram (bio, comunicação, discurso)
- Criação de linha de conteúdo estratégico (Posts N3)
- Instalação de agente de IA no WhatsApp pra qualificação de leads
- Scripts de fechamento e propostas personalizados por cliente
- Gestão de marketing da ThaminyIlha.Cerimonial
- Desenvolvimento do curso SOLO.OS

## Clientes e contexto
Atende clientes externos (prestadores de serviço: clínicas, advogados, cerimonialistas). Operação 100% solo. Cada cliente tem pasta própria dentro de `clientes/`.

## Tom de voz
Informal e direto. Primeira pessoa, como se o Ezequiel estivesse falando. Sem travessão. Sem contraste de duas frases curtas estilo "não é X. É Y." Nada que cheira a texto de IA genérico.

## Ferramentas conectadas
- Notion (MCP disponível)
- Google Calendar (MCP disponível)
- Canva (em migração pra geração via Codex)
- WordPress (sites de clientes)

## Adicionar novo cliente

Ao criar pasta pra novo cliente:
1. Copiar `clientes/_modelo-cliente/` com o nome do cliente
2. Preencher `briefing.md` com dados do cliente
3. O `AGENTS.md` dentro da pasta já vem configurado pra ler o briefing automaticamente
4. Quando abrir a pasta do cliente no Codex, o contexto já tá carregado

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (se existirem e estiverem configurados):

1. `_contexto/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `_contexto/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `_contexto/estrategia.md` — foco atual, prioridades, o que pode esperar

Usar essas informações como base pra qualquer resposta ou decisão. Ao sugerir prioridades, formatos ou abordagens, considerar o foco atual descrito em `estrategia.md`.

Para qualquer tarefa visual (carrossel, proposta, slide, landing page), consultar `marca/design-guide.md` como referência de estilo.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas usar o contexto naturalmente.

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe uma skill relevante em `.Codex/skills/` ou `.Codex/commands/`.
Se encontrar, seguir as instruções da skill.
Se não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível (o usuário provavelmente vai pedir de novo no futuro), perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

Não perguntar pra tarefas pontuais ou perguntas simples. Só quando o padrão de repetição for claro.

---

## Aprender com correções

Quando o usuário corrigir algo, melhorar uma resposta ou dar uma instrução que parece permanente, perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** → `_contexto/empresa.md`
- **Sobre preferências e estilo** → `_contexto/preferencias.md`
- **Sobre prioridades e foco atual** → `_contexto/estrategia.md`
- **Regra de comportamento nessa pasta** → `AGENTS.md`

Salvar com uma linha nova clara, sem reformatar o arquivo inteiro. Confirmar o que foi salvo mostrando a linha adicionada.

---

## Manter contexto atualizado

Ao terminar uma tarefa que mudou algo relevante no projeto (novo cliente, nova skill, mudança de foco, novo processo, ferramenta instalada, estrutura de pastas alterada), perguntar:

> "Isso mudou algo no teu contexto. Quer que eu atualize os arquivos de memória?"

Se sim, identificar o que precisa atualizar:

- **Novo cliente, serviço, ferramenta, equipe** → `_contexto/empresa.md`
- **Mudança de prioridade ou foco** → `_contexto/estrategia.md`
- **Correção de tom ou estilo** → `_contexto/preferencias.md`
- **Nova pasta, regra de organização, skill criada** → `AGENTS.md`
- **Mudança visual (cores, fontes, logo)** → `marca/design-guide.md`

Mostrar o que vai mudar antes de salvar. Não reformatar o arquivo inteiro, só adicionar ou editar a linha relevante.

Quando NÃO perguntar: tarefas pontuais, perguntas simples, mudanças já salvas pelo bloco "Aprender com correções".

Dica: se não sabe se algo mudou, rode /atualizar pra uma varredura completa.

---

## Criação de skills

Quando o usuário pedir pra criar uma nova skill:

1. Verificar se existe um template relevante em `templates/skills/`. Se existir, usar como base
2. Perguntar: "Essa skill é específica pra esse projeto ou vai ser útil em qualquer projeto?"
   - Específica desse negócio → `.Codex/skills/nome-da-skill/SKILL.md`
   - Útil em qualquer projeto → `~/.Codex/skills/nome-da-skill/SKILL.md`
3. Ler `_contexto/empresa.md` e `_contexto/preferencias.md` pra calibrar o conteúdo
4. Criar arquivos de apoio dentro da pasta da skill se necessário
