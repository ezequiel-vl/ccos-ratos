---
name: swipe
description: Guarda uma referência no swipe da ezeOS (swipe.ezeos.com.br, privado): recebe o link (ou imagem) e, se tiver, o porquê de ser bom; tira os prints sozinho (abertura, página inteira e celular), classifica por categoria, nicho e andar, escreve a nota "o que roubar daqui" e publica. Use quando o Ezequiel disser "/swipe <link>", "guarda essa referência", "salva no swipe", "adiciona no swipe", mandar um link dizendo que gostou de um site/post/anúncio, ou pedir pra tirar/editar/remover algo do swipe.
---

# Swipe da ezeOS

Coleção privada de referências de trabalho. Tudo mora em `ezeOS/swipe/`:

| Arquivo | O que é |
| --- | --- |
| `refs.json` | a lista de referências (fonte da verdade) |
| `prints/` | `<id>.jpg` (abertura ou imagem), `<id>-full.jpg` (página inteira), `<id>-cel.jpg` (celular) |
| `capturar.js` | tira os prints de um link ou de uma imagem local |
| `app.html` | a página (visual da casa); `montar.py` junta com o `refs.json` em `dist/` |
| `dist/` | o que sobe pro `swipe.ezeos.com.br` (fora do git) |

Privado: o subdomínio tem senha (Hostinger) e `noindex`. **Nunca publicar o swipe no Cloudflare** (`ezeos-publicacoes` é público).

## Adicionar uma referência

1. **Entender o pedido.** Link (ou caminho de imagem) + o que o Ezequiel disse sobre ela. Se ele não disse por que gostou, olha o print e escreve a nota você mesmo; não pergunta.
2. **Escolher o `id`:** curto, minúsculo, com hífen, único no `refs.json` (ex.: `linear-home`, `clinica-x-agendamento`).
3. **Capturar:**
   ```
   cd ezeOS/swipe
   node capturar.js <id> <url>            # site, landing, página
   node capturar.js <id> <caminho.png>    # carrossel, story, anúncio salvo
   ```
   Post do Instagram não abre sem login: pedir o print (ou usar a arte local) e passar a imagem. Abra o `prints/<id>.jpg` e confira se pegou a página certa (sem banner de cookie tapando tudo, sem tela de login). Se pegou errado, avisa.
4. **Escrever a entrada** no topo do `refs.json`:
   ```json
   {
     "id": "linear-home",
     "titulo": "Linear, home",
     "url": "https://linear.app/",
     "imagem": "caminho/local.png",
     "categoria": "site",
     "nicho": "software",
     "andar": "movimento",
     "origem": "fora",
     "nota": "...",
     "tags": ["..."],
     "data": "AAAA-MM-DD"
   }
   ```
   - `imagem` só quando a captura veio de arquivo local (aí a página mostra só a imagem).
   - `categoria`: `site`, `landing`, `link-bio`, `carrossel`, `reel`, `story`, `anuncio`, `ficha-google`, `copy`, `identidade`, `ferramenta`. Categoria nova pode, mas avisa.
   - `andar`: em qual andar da ezeOS a referência ajuda: `ponto` (existir e ser encontrado), `movimento` (atrair) ou `atendimento` (converter).
   - `origem`: `ezeos` (trabalho da casa) ou `fora`.
   - `nicho`: minúsculo, reaproveitando os que já existem (`clínica`, `advocacia`, `eventos`, `consultoria`...).
   - `data`: hoje.
5. **A nota é o que importa.** Uma ou duas frases dizendo o que roubar dali e onde usar: a mecânica, a estrutura, o detalhe visual. Concreta ("hero com o preço do concorrente riscado ao lado do nosso"), nunca elogio vago ("design incrível"). Regras da casa: sem travessão, sem "não é X, é Y", "redes sociais" e nunca só "redes".
6. **Montar e publicar** (ver abaixo). Responder com o link direto da referência: `https://swipe.ezeos.com.br/#<id>`.

Vários links de uma vez: captura todos, escreve todas as entradas, monta e publica uma vez só.

## Editar ou remover

Edita a entrada no `refs.json` (ou remove e apaga os `prints/<id>*`), monta e publica. Print velho: `node capturar.js <id> <url>` de novo.

## Montar e publicar

```
cd ezeOS/swipe
python montar.py
```

Publicar na Hostinger (plugin `hostinger`): `hosting_files_generate-upload-url` com `username: u460204468` e `domain: ezeos.com.br` (o site pai; o swipe é a pasta `swipe/` dele). Passar as credenciais por variável de ambiente e subir só o que mudou:

```
cd ezeOS/swipe
TUS_URL=<url> TUS_AUTH=<auth_key> TUS_REST=<rest_auth_key> sh subir.sh index.html prints/<id>.jpg prints/<id>-full.jpg prints/<id>-cel.jpg
```

Nunca usar o deploy de arquivo compactado (`hosting_deployStaticSiteArchiveV1`) nessa pasta: ele apaga tudo e leva junto o `.htaccess` da senha. Não mostrar as credenciais no chat.

Conferir: `curl -s -o /dev/null -w "%{http_code}" https://swipe.ezeos.com.br/` tem que dar `401` (senha pedida). Sem o plugin conectado, avisar o Ezequiel que precisa do `/mcp` e deixar a `dist/` pronta.

Trocar a senha: o Ezequiel roda `python ezeOS/swipe/definir-senha.py` num terminal dele (a senha não passa pelo chat), e depois sobe o `.htpasswd` com `python montar.py` + `sh subir.sh .htpasswd`.
