# Contexto da Empresa — ezeOS

**Nome:** Ezequiel
**Negócio:** ezeOS
**O que faz:** Agência solo de marketing. Instala a empresa do cliente no digital por inteiro (site, Google Meu Negócio, e-mail no domínio, redes, WhatsApp Business) e depois faz ela atrair e atender. Público: negócios locais e prestadores de serviço (clínicas, advogados, cerimonialistas).
**Tese:** o dono já investiu em ponto, fachada e vitrine pra existir na rua. A ezeOS monta o estabelecimento digital dele com o mesmo critério. Frase institucional: "A gente instala a sua empresa no digital." Posicionamento completo em `marca/2026-10-15-posicionamento-ezeos.md`.
**Perfil:** freelancer
**Atende clientes:** Sim, clientes externos
**Equipe:** Solo (Ezequiel cuida de tudo)
**Ferramentas:** Notion, Google Calendar, Canva (em migração pra geração via Claude), WordPress, Cloudflare Pages (publicação de HTML com link público via skill `/publicar-site` — projeto `ezeos-publicacoes`)
**Principais entregas:**
- Ponto Digital: site institucional com SEO local, Google Meu Negócio completo, e-mail no domínio, WhatsApp Business configurado, perfis padronizados
- Reposicionamento de perfil no Instagram (bio, comunicação, discurso)
- Linha de conteúdo estratégico (Posts N3) que atrai cliente, não colega
- Agente de IA no WhatsApp pra qualificação e aquecimento de leads
- Scripts de fechamento personalizados
- Propostas comerciais

## Arquitetura de marca

| Marca | Papel |
| --- | --- |
| **ezeOS** | a agência, a casa, qualquer negócio local |
| **eze.clinicas** | vertical de clínicas estéticas e odontológicas (era "Domínio Local"), em `ezeOS/verticais/clinicas/` |
| **eze.cc** | marca pessoal do Ezequiel, público freelancer e agência, destino SOLO.OS |

Vertical com nome próprio vende melhor pra clínica, porque ela quer contratar quem entende de clínica. A casa continua atendendo padaria, advogado e cerimonialista sem conflito de discurso.

## Serviços e preços

Escada de ascensão. Cada degrau entregue cria a dor do seguinte.

| Degrau | Produto | Faixa | Formato |
| --- | --- | --- | --- |
| 1 | **Ponto Digital** (site + GMN + e-mail no domínio + WhatsApp Business + perfis) | R$ 1.500 a R$ 2.000 | entrega única |
| 1r | **Manutenção do Ponto** (hospedagem, atualizações, posts no GMN, avaliações) | R$ 150 a R$ 300/mês | recorrente |
| 2 | **Reposicionamento Estratégico** (discurso, bio, linha de conteúdo N3) | R$ 2.000 | entrega única |
| 2r | **Movimento** (conteúdo N3, tráfego pago, landing pages) | R$ 800 a R$ 1.500/mês | recorrente |
| 3 | **Sistema de Demanda Contínua** (Atrair + Capturar + Converter) | R$ 5.000 | entrega única |
| 4 | **Mega CRM** (instalação + licença) | a definir | única + recorrente |

Guardrail do Ponto Digital: escopo fechado, 7 a 10 dias, teto de 15 horas por entrega, base de templates própria. Sem isso a porta de entrada barata engole a operação solo.

## Método principal

Os serviços se organizam em três andares, na lógica do negócio físico: **Ponto** (a empresa existe e é encontrada), **Movimento** (gente passa na porta) e **Atendimento** (quem chega vira cliente). O Sistema de Demanda Contínua é o nome do combo Movimento + Atendimento.

### Sistema de Demanda Contínua — 3 etapas:
1. **Atrair** — perfil que fala com o cliente certo, não com o colega
2. **Capturar** — agente de IA no WhatsApp que recebe, qualifica e aquece o lead sem depender do Ezequiel estar disponível
3. **Converter** — o lead chega pronto pra fechar, Ezequiel só fecha

Frase-âncora: "Você não precisa de mais um post. Precisa de demanda que não depende de sorte."

## Produto próprio: Mega CRM

CRM white-label self-hosted que a ezeOS instala pra cliente. Junta WhatsApp oficial
(templates, campanhas, inbox com IA, RAG) com camada de CRM, então o mesmo contato
atravessa comercial, entrega e educação numa timeline só.

Stack: React 18 + Vite + TypeScript + Tailwind no front, Supabase no back (Postgres,
Auth, Realtime, Edge Functions, pgvector), WhatsApp via Zernio, deploy na Vercel.

Código em `../eze-crm/`, fora do workspace, repositório privado
`github.com/ezequiel-vl/eze-crm`. Fica separado porque a Vercel faz deploy a partir
do git, e misturar com o workspace faria commit de briefing disparar redeploy.

Modelo: a ezeOS instala e entrega, não opera o CRM do cliente no dia a dia. Depois
da entrega fica só suporte eventual e atualização de versão. A infra (Supabase e
Vercel) fica no nome do cliente e ele paga.

Cada instalação é isolada: repositório, projeto Supabase e projeto Vercel próprios.
Uma instância nunca enxerga dado da outra.

Status em setembro de 2026: código publicado, nenhuma instância no ar ainda. Preço
da instalação e do suporte ainda não definidos. Contexto operacional e registro de
quem tem o quê ficam em `CRM/` no workspace.

## Clientes ativos
- **Boell Estética e Saúde Integrativa** (São José-SC) — clínica de estética avançada e saúde integrativa. Duas campanhas: Soroterapia e Capilar (posts N3 → WhatsApp + landing page por procedimento). Profissionais: Coren/SC e CRO/SC (não CRM — publicidade segue Coren/CRO). Pasta: `clientes/BoellEsteticaAvancada/`
- **Fernando Morinelli** (Santa Cruz do Sul-RS): gestão e estratégia empresarial, mentoria executiva, reestruturação e securitização. Sócio da Exitus Estratégia Empresarial e da 8sec Securitizadora, presidente do BNI Imigrante. Entrega: criação do produto Mentoria Executiva (Mesa de Decisão) + marca pessoal no Instagram @morinelli_gestao. Tom: autoridade sóbria, anti-jargão, sem coach motivacional. Status: pré-fechamento, oferta em definição. Pasta: `clientes/FernandoMorinelli/`
- **Tabuleiro**: produto digital de uma cliente (infoproduto de espiritualidade aplicada, R$37). Método de aplicação prática do livro *O Jogo da Vida*, em três etapas: LIMPAR, ARMAR, RODAR. A ezeOS cuida de Instagram, landing pages e estratégia de vendas. Público: mulheres 35-55 leitoras de prosperidade e fé, metade cristã praticante. Restrição forte: vocabulário de manifestação proibido e nada de promessa de dinheiro ou prova inventada. Pasta: `clientes/Tabuleiro/`

## Prospects
- **Espaço Cellebra** (São Leopoldo-RS) — salão de festas com pacote fechado (15 anos, formaturas, casamentos, empresarial), capacidade 90 convidados. Razão social Cellebra Eventos Ltda, duas sócias-administradoras: Carmem Severo Marca (contato) e Gisiele Gosmão Soller. Demanda é operação interna, não captação: lista digital de recepção (igual à da Thaminy), base de clientes com tag por área/ano pra disparo sazonal segmentado, e um "CRM" de escopo ainda indefinido. Reunião de diagnóstico 14/10/2026. Pasta: `clientes/Espaço Cellebra/`

## Contexto adicional
- Ezequiel cuida do marketing e comunicação da **ThaminyIlha.Cerimonial** (empresa da esposa)
- Tem o projeto **SOLO.OS** — curso onde ensina outros freelancers e agências a construir um sistema operacional pra seus negócios

## Projetos próprios (marcas de vestuário)
- **La Clika** — marca própria de streetwear, estética chicana (México/EUA), público rap/gangsta rap. Camisetas oversized suedine (preto e off white). Relançamento de marca que já existiu há ~5 anos; drop inicial de 4 estampas previsto pra primeira semana de outubro/2026. Domínio `www.laclika.com.br`, Instagram `@laclika.br`. Pasta: `clientes/LaClika/`
- **KYRIE** — marca própria de streetwear católico, camisetas oversized suedine. Domínio `www.kyriewear.com.br`, Instagram `@kyriewear`. Pasta: `clientes/Kyrie/`
