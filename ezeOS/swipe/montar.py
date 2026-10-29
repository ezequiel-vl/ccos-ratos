"""Monta o swipe: junta app.html + refs.json numa página só e copia os prints.

Uso: python montar.py            -> dist/ (pasta que sobe pro swipe.ezeos.com.br)
A dist/ fica fora do git. Nunca publicar no Cloudflare (ezeos-publicacoes é público).
"""
import json
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DIST = AQUI / "dist"
RAIZ_SERVIDOR = "/home/u460204468/domains/ezeos.com.br/public_html/swipe"
HTACCESS = f"""# Swipe da ezeOS: uso interno, com senha (python definir-senha.py)
RewriteEngine On
RewriteCond %{{HTTPS}} off
RewriteRule ^ https://%{{HTTP_HOST}}%{{REQUEST_URI}} [L,R=301]

AuthType Basic
AuthName "Swipe ezeOS"
AuthUserFile {RAIZ_SERVIDOR}/.htpasswd
Require valid-user

<FilesMatch "^\\.ht">
  Require all denied
</FilesMatch>

<IfModule mod_headers.c>
  Header set X-Robots-Tag "noindex, nofollow, noarchive"
</IfModule>
"""

refs = json.loads((AQUI / "refs.json").read_text(encoding="utf-8"))
ids = [r["id"] for r in refs]
assert len(ids) == len(set(ids)), "id repetido no refs.json"
faltando = [i for i in ids if not (AQUI / "prints" / f"{i}.jpg").exists()]
if faltando:
    raise SystemExit("sem print: " + ", ".join(faltando) + "  (rode: node capturar.js <id> <url>)")

app = (AQUI / "app.html").read_text(encoding="utf-8")
dados = json.dumps(refs, ensure_ascii=False).replace("</", r"<\/")
assert app.count("/*__REFS__*/[]") == 1
html = app.replace("/*__REFS__*/[]", dados)

if DIST.exists():
    shutil.rmtree(DIST)
(DIST / "prints").mkdir(parents=True)
(DIST / "index.html").write_text(html, encoding="utf-8", newline="\n")
(DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
# Senha (Basic Auth). Sem o .htpasswd no servidor a pasta fica trancada pra todo mundo.
(DIST / ".htaccess").write_text(HTACCESS, encoding="utf-8", newline="\n")
if (AQUI / ".htpasswd").exists():
    shutil.copy2(AQUI / ".htpasswd", DIST / ".htpasswd")
usados = 0
for f in (AQUI / "prints").iterdir():
    base = f.stem.removesuffix("-full").removesuffix("-cel")
    if base in ids:
        shutil.copy2(f, DIST / "prints" / f.name)
        usados += 1
print(f"ok {len(refs)} referências, {usados} prints -> {DIST}")
