---
name: publicar-site
description: >
  Publica um arquivo HTML no ar via Cloudflare Pages e retorna um link compartilhável.
  Use quando o usuário disser "publica", "coloca no ar", "quero um link", "deploy",
  "publica esse HTML", "publicar-site" ou após criar uma proposta/landing page.
---

# /publicar-site — Deploy no Cloudflare Pages

## O que faz

Envia um arquivo HTML pro Cloudflare Pages e retorna uma URL pública com HTTPS.
O link funciona em qualquer dispositivo e pode ser compartilhado direto com o cliente.

Cada publicação vira uma pasta própria no site. Publicar algo novo **não derruba**
os links antigos — todos continuam no ar.

## Como usar

```
/publicar-site propostas/proposta-cliente-x.html
```

Sem argumento: perguntar qual arquivo publicar.

---

## Pré-requisitos

Variáveis no `.env` da raiz do workspace:

```
CLOUDFLARE_API_TOKEN=...
CLOUDFLARE_ACCOUNT_ID=...
CLOUDFLARE_PROJECT_NAME=ezeos-publicacoes
```

Se faltar alguma, seguir o bloco **Configuração inicial** no fim deste arquivo.
Wrangler não precisa estar instalado — roda via `npx`.

---

## Workflow

### 1. Validar entrada

- Arquivo existe? Se não, avisar e parar.
- Termina em `.html`? Se não, perguntar antes de seguir.

### 2. Carregar credenciais

Ler o `.env` e exportar pro processo (PowerShell):

```powershell
Get-Content .env | Where-Object { $_ -match '^CLOUDFLARE_' } | ForEach-Object {
  $k, $v = $_ -split '=', 2
  Set-Item -Path "env:$k" -Value $v
}
```

Se `CLOUDFLARE_API_TOKEN` ou `CLOUDFLARE_ACCOUNT_ID` vierem vazios, ir pra **Configuração inicial**.

Nunca imprimir o valor do token na conversa.

### 3. Montar a pasta de publicação

O site inteiro vive em `_publicado/` na raiz do workspace. Estrutura:

```
_publicado/
  proposta-cliente-x/index.html
  landing-clinica/index.html
```

Gerar o slug a partir do nome do arquivo: minúsculo, sem acento, espaços viram `-`,
sem a extensão. Ex: `Proposta Cliente X.html` → `proposta-cliente-x`.

```powershell
New-Item -ItemType Directory -Force "_publicado/<slug>"
Copy-Item "<arquivo>" "_publicado/<slug>/index.html" -Force
```

Se a pasta do slug já existir, avisar que vai substituir aquela publicação
(a URL continua a mesma) e seguir.

### 4. Garantir que o projeto existe

Na primeira publicação o projeto ainda não existe no Cloudflare:

```powershell
npx --yes wrangler@latest pages project create $env:CLOUDFLARE_PROJECT_NAME --production-branch=main
```

Se o retorno disser que o projeto já existe, ignorar o erro e seguir.

### 5. Deploy

```powershell
npx --yes wrangler@latest pages deploy _publicado --project-name=$env:CLOUDFLARE_PROJECT_NAME --branch=main --commit-dirty=true
```

### 6. Devolver o link

```
https://<CLOUDFLARE_PROJECT_NAME>.pages.dev/<slug>/
```

**Output:**
> "Publicado. Link: https://ezeos-publicacoes.pages.dev/proposta-cliente-x/"

Abrir o link no navegador só se o usuário pedir.

---

## Erros comuns

| Erro | Causa | O que fazer |
|---|---|---|
| `Authentication error [code: 10000]` | Token inválido ou sem permissão de Pages | Refazer o token com permissão `Cloudflare Pages: Edit` |
| `Project not found` | `CLOUDFLARE_PROJECT_NAME` não bate com o painel | Rodar o passo 4 ou corrigir o nome no `.env` |
| `Unable to authenticate request` | Falta `CLOUDFLARE_ACCOUNT_ID` | Conferir o `.env` |
| npx trava baixando | Sem internet | Avisar e parar |

---

## Configuração inicial

Guiar o usuário assim, um passo por vez:

> "Preciso de duas coisas do Cloudflare. Leva uns 3 minutos.
>
> **1. Account ID**
> - Entra em dash.cloudflare.com (cria conta grátis se não tiver)
> - Menu lateral → Compute (Workers) → Workers & Pages
> - O Account ID aparece na coluna da direita. Copia.
>
> **2. API Token**
> - Vai em dash.cloudflare.com/profile/api-tokens
> - Create Token → Create Custom Token
> - Nome: `ezeos-deploy`
> - Permissions: `Account` → `Cloudflare Pages` → `Edit`
> - Account Resources: a tua conta
> - Continue → Create Token → copia o token (só aparece uma vez)
>
> Me manda os dois que eu salvo no `.env`."

Ao receber, gravar no `.env` (sem aspas, uma var por linha) e confirmar só com
"Salvo." — nunca ecoar o token de volta.

---

## Regras

- Nunca commitar `.env` nem imprimir o token
- `_publicado/` é conteúdo de cliente: fica fora do git
- Domínio próprio (ex: propostas.ezeos.com.br): conectar no painel do Cloudflare Pages
  depois da primeira publicação. A skill continua igual.
