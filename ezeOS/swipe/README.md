# Swipe da ezeOS

Referências de trabalho, da casa e de fora, com o que roubar de cada uma. Uso interno, com senha.

- **No ar:** https://swipe.ezeos.com.br/ (usuário `eze`). Também responde em ezeos.com.br/swipe/, com a mesma senha.
- **Pra adicionar:** `/swipe <link> [por que é bom]` no Claude Code. A skill está em `.claude/skills/swipe/`.

## Como funciona

| Arquivo | Papel |
| --- | --- |
| `refs.json` | a lista; cada entrada tem `id`, `titulo`, `url`, `categoria`, `nicho`, `andar`, `origem`, `nota`, `tags`, `data` (e `imagem` se veio de arquivo local) |
| `capturar.js` | `node capturar.js <id> <url ou imagem>`: grava `prints/<id>.jpg`, `-full.jpg` e `-cel.jpg` |
| `capturar-todas.sh` | captura o que ainda não tem print (`--refazer` refaz tudo) |
| `app.html` | a página; `python montar.py` junta com o `refs.json` em `dist/` |
| `subir.sh` | sobe arquivos da `dist/` por TUS (credenciais de `hosting_files_generate-upload-url` por variável de ambiente) |
| `definir-senha.py` | troca a senha: roda no terminal, digita escondido, grava só o código em `.htpasswd` |

Servidor: Hostinger, usuário `u460204468`, site `ezeos.com.br`, pasta `public_html/swipe/` (raiz do subdomínio). A `dist/` e o `.htpasswd` ficam fora do git.

## Regras

- **Nunca** publicar no Cloudflare (`ezeos-publicacoes` é público) e nunca usar o deploy de arquivo compactado da Hostinger nessa pasta: ele apaga tudo e leva junto o `.htaccess` da senha. Sempre arquivo por arquivo, com o `.htaccess` primeiro.
- O `.htaccess` exige senha. Sem `.htpasswd` no servidor, ninguém entra, nem tu.
- O playwright-core está instalado só aqui (`npm install` se a pasta `node_modules` sumir). O navegador é o Chromium do Playwright em `%LOCALAPPDATA%\ms-playwright`.
