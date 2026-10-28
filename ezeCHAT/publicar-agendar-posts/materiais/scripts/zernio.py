#!/usr/bin/env python3
"""
zernio.py — publica, agenda e automatiza posts no Instagram via API da Zernio.

Sem dependências externas (Python 3 padrão + curl, que já vem no macOS/Linux).

Config: a chave fica em ~/.zernio.env (compartilhada entre as skills Zernio):
    ZERNIO_API_KEY=sk_sua_chave_aqui
    ZERNIO_ACCOUNT_ID=...   (preenchido automaticamente pelo `status`)
    ZERNIO_PROFILE_ID=...   (idem)

Comandos principais:
  python3 zernio.py check                # valida config e conexão (rode primeiro)
  python3 zernio.py status               # contas conectadas + saúde
  python3 zernio.py post --media foto.jpg --caption "..." --now
  python3 zernio.py post --media-dir ./slides --caption-file legenda.txt --schedule "2026-09-01 20:00"
  python3 zernio.py posts --status scheduled
  python3 zernio.py auto-create --keywords GUIA --dm "..." --button "Abrir|https://..."
  python3 zernio.py autos                # automações + stats
  python3 zernio.py auto-logs <id>       # log de cada disparo

Todos os comandos de escrita aceitam --dry-run (mostra o que seria enviado, não envia).
"""

import argparse
import json
import mimetypes
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://zernio.com/api/v1"
GLOBAL_ENV = Path.home() / ".zernio.env"
SKILL_ENV = Path(__file__).resolve().parent.parent.parent / ".env"  # raiz da skill (fallback)
DEFAULT_TZ = "America/Sao_Paulo"

SETUP_MSG = """\
ERRO: ZERNIO_API_KEY não encontrada.

Como resolver (5 minutos, grátis pra até 2 contas):
  1. Crie sua conta em https://zernio.com (não precisa de cartão)
  2. No dashboard, conecte seu Instagram (precisa ser conta Profissional: Business ou Criador)
  3. Em https://zernio.com/dashboard/api-keys crie uma chave (começa com sk_)
  4. Salve a chave no arquivo ~/.zernio.env com esta linha:
       ZERNIO_API_KEY=sk_sua_chave_aqui
  5. Rode: python3 {script} check
""".format(script=Path(__file__).resolve())


# ---------------------------------------------------------------- config

def load_env_file(path):
    env = {}
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def get_config():
    cfg = {}
    cfg.update(load_env_file(SKILL_ENV))
    cfg.update(load_env_file(GLOBAL_ENV))  # global vence
    for k in ("ZERNIO_API_KEY", "ZERNIO_ACCOUNT_ID", "ZERNIO_PROFILE_ID"):
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


def save_global_var(key, value):
    """Grava/atualiza uma var no ~/.zernio.env, preservando o resto."""
    lines = GLOBAL_ENV.read_text().splitlines() if GLOBAL_ENV.exists() else []
    out, done = [], False
    for line in lines:
        if line.strip().startswith(f"{key}=") or line.strip().startswith(f"#{key}="):
            out.append(f"{key}={value}")
            done = True
        else:
            out.append(line)
    if not done:
        out.append(f"{key}={value}")
    GLOBAL_ENV.write_text("\n".join(out) + "\n")
    os.chmod(GLOBAL_ENV, 0o600)


CFG = get_config()
API_KEY = CFG.get("ZERNIO_API_KEY")


def require_key():
    if not API_KEY:
        sys.exit(SETUP_MSG)


# ---------------------------------------------------------------- HTTP

def api(method, path, body=None, query=None):
    require_key()
    url = f"{BASE}{path}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            err = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
        except ValueError:
            err = raw
        if e.code == 401:
            sys.exit(f"ERRO 401: chave inválida ou expirada.\n{err}\n\nConfira a chave em ~/.zernio.env "
                     "(gere outra em https://zernio.com/dashboard/api-keys se precisar).")
        sys.exit(f"ERRO {e.code} {method} {path}:\n{err}")
    except urllib.error.URLError as e:
        sys.exit(f"ERRO de rede ao chamar a Zernio: {e.reason}\nConfira sua internet e tente de novo.")


def pretty(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def dry_or_send(args, method, path, body):
    if args.dry_run:
        print(f"--dry-run ativo. NÃO enviado. Payload de {method} {path}:")
        pretty(body)
        return None
    return api(method, path, body)


# ---------------------------------------------------------------- contas

def pid_of(v):
    """profileId pode vir como string ou como objeto {'_id': ...} (populated)."""
    if isinstance(v, dict):
        return v.get("_id")
    return v


def get_accounts():
    return api("GET", "/accounts").get("accounts", [])


def resolve_account(args):
    """Resolve a conta alvo: --account (id ou @user) > config > única conta IG."""
    want = getattr(args, "account", None) or CFG.get("ZERNIO_ACCOUNT_ID")
    accounts = get_accounts()
    ig = [a for a in accounts if a.get("platform") == "instagram"]
    if want:
        for a in accounts:
            if a.get("_id") == want or a.get("username", "").lstrip("@") == str(want).lstrip("@"):
                return a
        sys.exit(f"ERRO: conta '{want}' não encontrada entre as conectadas. Rode `python3 zernio.py accounts`.")
    if len(ig) == 1:
        return ig[0]
    if not ig:
        sys.exit("ERRO: nenhuma conta Instagram conectada. Conecte no dashboard da Zernio e rode `check`.")
    sys.exit("ERRO: mais de uma conta Instagram conectada. Diga qual usar com --account <id|@usuario>.")


def cmd_check(args):
    if not API_KEY:
        sys.exit(SETUP_MSG)
    accounts = get_accounts()
    print("Chave OK, API respondendo.")
    if not accounts:
        print("\nFalta conectar o Instagram: entre em https://zernio.com/dashboard, clique em "
              "conectar conta, escolha Instagram e faça o login (a conta precisa ser Profissional).")
        return
    cmd_status(args)


def cmd_status(args):
    accounts = get_accounts()
    if not accounts:
        print("Nenhuma conta conectada ainda. Conecte o Instagram no dashboard da Zernio.")
        return
    health = api("GET", "/accounts/health")
    print("=== Contas conectadas ===")
    for a in accounts:
        print(f"  {a.get('platform'):<12} @{a.get('username','?'):<25} _id={a.get('_id')}")
    print("\n=== Saúde ===")
    for h in health.get("accounts", []):
        print(f"  @{h.get('username')}: {h.get('status')} | pode postar: {h.get('canPost')} "
              f"| token válido até: {h.get('tokenExpiresAt', '?')}")
    ig = [a for a in accounts if a.get("platform") == "instagram"]
    if ig and not CFG.get("ZERNIO_ACCOUNT_ID"):
        acc = ig[0]
        save_global_var("ZERNIO_ACCOUNT_ID", acc["_id"])
        pid = pid_of(acc.get("profileId")) or pid_of(acc.get("profile"))
        if not pid:
            for h in health.get("accounts", []):
                if h.get("accountId") == acc["_id"] and pid_of(h.get("profileId")):
                    pid = pid_of(h["profileId"])
        if pid:
            save_global_var("ZERNIO_PROFILE_ID", pid)
        print(f"\nConta padrão salva em ~/.zernio.env: @{acc.get('username')}")


def cmd_accounts(args):
    for a in get_accounts():
        print(f"{a.get('platform'):<12} @{a.get('username','?'):<25} _id={a.get('_id')}")


def cmd_api(args):
    body = json.loads(args.body) if args.body else None
    pretty(api(args.method.upper(), args.path, body))


# ---------------------------------------------------------------- mídia

def upload_file(path):
    p = Path(path).expanduser()
    if not p.exists():
        sys.exit(f"ERRO: arquivo não existe: {p}")
    ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    pre = api("POST", "/media/presign", {"filename": p.name, "contentType": ctype})
    r = subprocess.run(
        ["curl", "-sf", "-X", "PUT", pre["uploadUrl"],
         "-H", f"Content-Type: {ctype}", "--data-binary", f"@{p}"],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERRO no upload de {p.name}: {r.stderr or 'falha no curl'}")
    return pre["publicUrl"]


def cmd_upload(args):
    for f in args.files:
        url = upload_file(f)
        print(f"{Path(f).name} -> {url}")


def media_item(ref):
    """Aceita path local (faz upload) ou URL http(s). Detecta image/video pela extensão."""
    if ref.startswith("http://") or ref.startswith("https://"):
        url, name = ref, urllib.parse.urlparse(ref).path
    else:
        url, name = upload_file(ref), ref
    ext = Path(name).suffix.lower()
    mtype = "video" if ext in (".mp4", ".mov", ".m4v") else "image"
    return {"type": mtype, "url": url}


def expand_media(args):
    refs = list(args.media or [])
    if getattr(args, "media_dir", None):
        d = Path(args.media_dir).expanduser()
        if not d.is_dir():
            sys.exit(f"ERRO: pasta não existe: {d}")
        found = sorted(
            f for f in d.iterdir()
            if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".mp4", ".mov", ".m4v")
            and not f.name.startswith(".")
        )
        if not found:
            sys.exit(f"ERRO: nenhuma mídia (.png/.jpg/.mp4/.mov) em {d}")
        refs = [str(f) for f in found] + refs
    return refs


# ---------------------------------------------------------------- posts

def cmd_post(args):
    acc = resolve_account(args)
    caption = args.caption or ""
    if args.caption_file:
        caption = Path(args.caption_file).expanduser().read_text().strip()
    if len(caption) > 2200:
        sys.exit(f"ERRO: legenda com {len(caption)} caracteres (limite do Instagram: 2.200).")

    refs = expand_media(args)
    if not refs:
        sys.exit("ERRO: Instagram exige mídia. Use --media (pode repetir a flag) ou --media-dir <pasta>.")
    if len(refs) > 10:
        sys.exit(f"ERRO: {len(refs)} mídias (máximo 10 por carrossel).")
    if args.dry_run:
        # dry-run 100% seco: nada sobe pra lugar nenhum
        items = [{"type": "video" if Path(r).suffix.lower() in (".mp4", ".mov", ".m4v") else "image",
                  "url": f"<upload pendente: {Path(r).name}>"} for r in refs]
    else:
        items = [media_item(m) for m in refs]

    psd = {}
    if args.story:
        psd["contentType"] = "story"
    if args.reel_only:
        psd["shareToFeed"] = False
    if args.first_comment:
        psd["firstComment"] = args.first_comment
    if args.thumbnail:
        psd["instagramThumbnail"] = args.thumbnail
    if args.collaborators:
        psd["collaborators"] = [c.strip().lstrip("@") for c in args.collaborators.split(",")]
    if args.ai_label:
        psd["isAiGenerated"] = True

    platform_entry = {"platform": "instagram", "accountId": acc["_id"]}
    if psd:
        platform_entry["platformSpecificData"] = psd

    body = {"content": caption, "mediaItems": items, "platforms": [platform_entry]}

    if args.schedule:
        body["scheduledFor"] = args.schedule.replace(" ", "T")
        body["timezone"] = args.tz
    elif args.now:
        body["publishNow"] = True
    # nem --schedule nem --now: vira rascunho (draft), não publica

    res = dry_or_send(args, "POST", "/posts", body)
    if res:
        post = res.get("post", res)
        mode = "AGENDADO" if args.schedule else ("PUBLICANDO" if args.now else "RASCUNHO")
        print(f"{mode} — post _id={post.get('_id')}  status={post.get('status')}")
        if args.now:
            print("Confira em ~1 min com: python3 zernio.py post-get " + str(post.get("_id")))


def cmd_posts(args):
    res = api("GET", "/posts", query={"status": args.status} if args.status else None)
    posts = res.get("posts", res if isinstance(res, list) else [])
    if not posts:
        print("Nenhum post." if isinstance(posts, list) else "")
        return
    for p in posts:
        when = p.get("scheduledFor") or p.get("publishedAt") or ""
        content = (p.get("content") or "").replace("\n", " ")[:60]
        print(f"{p.get('_id')}  {p.get('status', '?'):<11} {when:<22} {content}")


def cmd_post_get(args):
    res = api("GET", f"/posts/{args.post_id}")
    p = res.get("post", res)
    print(f"status: {p.get('status')}")
    for pl in p.get("platforms", []):
        print(f"  {pl.get('platform')}: {pl.get('status')} | url: {pl.get('platformPostUrl')} | erro: {pl.get('error')}")


def cmd_post_delete(args):
    if args.dry_run:
        print(f"--dry-run: DELETE /posts/{args.post_id} (não enviado)")
        return
    pretty(api("DELETE", f"/posts/{args.post_id}"))


def cmd_post_retry(args):
    pretty(api("POST", f"/posts/{args.post_id}/retry"))


# ---------------------------------------------------------------- automações

def parse_button(spec):
    if "|" not in spec:
        sys.exit(f"ERRO: botão deve ser 'Texto|https://url' (recebi: {spec})")
    title, url = spec.split("|", 1)
    return {"type": "url", "title": title.strip(), "url": url.strip()}


def cmd_auto_create(args):
    acc = resolve_account(args)
    profile_id = args.profile or CFG.get("ZERNIO_PROFILE_ID") or pid_of(acc.get("profileId")) or pid_of(acc.get("profile"))
    if not profile_id:
        health = api("GET", "/accounts/health")
        for h in health.get("accounts", []):
            if h.get("accountId") == acc["_id"]:
                profile_id = pid_of(h.get("profileId"))
    if not profile_id:
        sys.exit("ERRO: profileId não resolvido. Rode `python3 zernio.py status` primeiro.")

    dm = args.dm or ""
    if args.dm_file:
        dm = Path(args.dm_file).expanduser().read_text().strip()
    if not dm:
        sys.exit("ERRO: --dm ou --dm-file é obrigatório (o texto que chega no direct).")

    body = {
        "profileId": profile_id,
        "accountId": acc["_id"],
        "keywords": [k.strip() for k in args.keywords.split(",")] if args.keywords else [],
        "matchMode": args.match,
        "dmMessage": dm,
    }
    if args.name:
        body["name"] = args.name
    if args.story_reply:
        body["trigger"] = "story_reply"
    if args.post_id:
        body["platformPostId"] = args.post_id
    if args.button:
        if len(args.button) > 3:
            sys.exit("ERRO: máximo 3 botões.")
        body["buttons"] = [parse_button(b) for b in args.button]
    if args.comment_reply:
        body["commentReply"] = args.comment_reply
    if args.dm_variations:
        body["dmMessageVariations"] = args.dm_variations
    if args.exclude:
        body["excludeKeywords"] = [k.strip() for k in args.exclude.split(",")]
    if args.typo:
        body["typoTolerance"] = True
    if args.also_dms:
        body["alsoMatchInDms"] = True
    if args.click_tag:
        body["clickTag"] = args.click_tag
    if args.dm_delay:
        body["dmDelaySeconds"] = args.dm_delay
    if args.follower_gate:
        body["audience"] = {"followerStatus": "follower", "whenUnknown": "verify"}
        body["followGate"] = {
            "message": args.gate_message,
            "buttonLabel": args.gate_button,
            "notFollowingMessage": args.gate_not_following,
        }

    res = dry_or_send(args, "POST", "/comment-automations", body)
    if res:
        auto = res.get("automation", res)
        print(f"Automação criada e ATIVA: id={auto.get('id') or auto.get('_id')}  keywords={auto.get('keywords')}")
        print("Teste comentando a palavra num post seu. Acompanhe com: python3 zernio.py autos")


def cmd_autos(args):
    res = api("GET", "/comment-automations",
              query={"profileId": args.profile or CFG.get("ZERNIO_PROFILE_ID")})
    autos = res.get("automations", res if isinstance(res, list) else [])
    if not autos:
        print("Nenhuma automação criada ainda.")
        return
    for a in autos:
        stats = a.get("stats", {}) or {}
        scope = a.get("platformPostId") or "todos os posts"
        active = "ATIVA " if a.get("isActive") else "PAUSADA"
        trig = "story" if a.get("trigger") == "story_reply" else "comentário"
        print(f"[{active}] {a.get('id') or a.get('_id')}  kw={a.get('keywords')}  "
              f"gatilho={trig}  escopo={scope}  enviados={stats.get('totalSent', 0)}  "
              f"disparos={stats.get('totalTriggered', 0)}")


def cmd_auto_get(args):
    pretty(api("GET", f"/comment-automations/{args.automation_id}"))


def cmd_auto_toggle(args, active):
    if args.dry_run:
        print(f"--dry-run: PATCH isActive={active} em {args.automation_id} (não enviado)")
        return
    api("PATCH", f"/comment-automations/{args.automation_id}", {"isActive": active})
    print("Automação " + ("ATIVADA." if active else "PAUSADA."))


def cmd_auto_delete(args):
    if args.dry_run:
        print(f"--dry-run: DELETE /comment-automations/{args.automation_id} (não enviado)")
        return
    pretty(api("DELETE", f"/comment-automations/{args.automation_id}"))


def cmd_auto_logs(args):
    pretty(api("GET", f"/comment-automations/{args.automation_id}/logs"))


# ---------------------------------------------------------------- parser

def main():
    ap = argparse.ArgumentParser(description="CLI da Zernio — publicar, agendar e automatizar Instagram")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, **kw):
        p = sub.add_parser(name, **kw)
        p.set_defaults(fn=fn)
        return p

    add("check", cmd_check, help="Valida config + conexão (rode este primeiro)")
    add("status", cmd_status, help="Contas conectadas + saúde; salva conta padrão")
    add("accounts", cmd_accounts, help="Lista contas conectadas")

    p = add("api", cmd_api, help="Chamada crua: zernio.py api GET /accounts")
    p.add_argument("method")
    p.add_argument("path")
    p.add_argument("body", nargs="?", help="JSON string (pra POST/PATCH)")

    p = add("upload", cmd_upload, help="Sobe arquivos de mídia, devolve a URL pública")
    p.add_argument("files", nargs="+")

    p = add("post", cmd_post, help="Cria post no Instagram (rascunho por padrão; --schedule ou --now)")
    p.add_argument("--account", help="id ou @usuario (padrão: única conta IG conectada)")
    p.add_argument("--caption", help="Legenda (máx 2.200 caracteres)")
    p.add_argument("--caption-file", help="Arquivo .txt com a legenda")
    p.add_argument("--media", action="append", default=[], help="Arquivo local ou URL (repetível; 2+ = carrossel)")
    p.add_argument("--media-dir", help="Pasta com os slides/mídias (ordem alfabética; ideal p/ carrossel)")
    p.add_argument("--story", action="store_true", help="Publica como story")
    p.add_argument("--reel-only", action="store_true", help="Reel só na aba Reels (fora do feed)")
    p.add_argument("--first-comment", help="Primeiro comentário automático (não vale pra story)")
    p.add_argument("--thumbnail", help="URL de capa custom (reel)")
    p.add_argument("--collaborators", help="@usuarios separados por vírgula (máx 3, contas públicas)")
    p.add_argument("--ai-label", action="store_true", help="Marca o post como mídia gerada por IA")
    p.add_argument("--schedule", help='"YYYY-MM-DD HH:MM" no fuso --tz')
    p.add_argument("--tz", default=DEFAULT_TZ, help=f"Fuso horário (padrão: {DEFAULT_TZ})")
    p.add_argument("--now", action="store_true", help="Publica imediatamente")
    p.add_argument("--dry-run", action="store_true")

    p = add("posts", cmd_posts, help="Lista posts")
    p.add_argument("--status", help="scheduled | draft | published | failed")
    p = add("post-get", cmd_post_get, help="Status + link de um post")
    p.add_argument("post_id")
    p = add("post-delete", cmd_post_delete, help="Cancela rascunho/agendado")
    p.add_argument("post_id")
    p.add_argument("--dry-run", action="store_true")
    p = add("post-retry", cmd_post_retry, help="Retenta post que falhou")
    p.add_argument("post_id")

    p = add("auto-create", cmd_auto_create, help="Cria automação comentário → DM")
    p.add_argument("--account", help="id ou @usuario")
    p.add_argument("--profile", help="profileId (padrão: config)")
    p.add_argument("--name", help="Nome de exibição da automação")
    p.add_argument("--keywords", help="Palavras-chave separadas por vírgula. ex: GUIA,QUERO")
    p.add_argument("--match", default="word", choices=["exact", "word", "contains"],
                   help="word = palavra isolada (padrão, recomendado); exact = comentário inteiro; contains = em qualquer lugar")
    p.add_argument("--exclude", help="Palavras que bloqueiam o disparo, separadas por vírgula")
    p.add_argument("--typo", action="store_true", help="Tolerar erros de digitação (só com --match word)")
    p.add_argument("--dm", help="Texto do DM")
    p.add_argument("--dm-file", help="Arquivo .txt com o texto do DM")
    p.add_argument("--dm-variations", action="append", default=[], help="Variação do DM (repetível, máx 5)")
    p.add_argument("--button", action="append", default=[], help='"Texto|https://url" (repetível, máx 3)')
    p.add_argument("--comment-reply", help="Resposta pública ao comentário (opcional)")
    p.add_argument("--post-id", help="Restringir a 1 post específico (padrão: todos os posts)")
    p.add_argument("--story-reply", action="store_true", help="Gatilho = resposta a story (em vez de comentário)")
    p.add_argument("--also-dms", action="store_true", help="Palavra mandada no direct também dispara")
    p.add_argument("--click-tag", help="Etiqueta aplicada a quem clica no link (segmentação)")
    p.add_argument("--dm-delay", type=int, help="Segundos de espera antes do DM (máx 86400)")
    p.add_argument("--follower-gate", action="store_true",
                   help="Só entrega pra seguidores; quem não segue recebe convite de 1 toque")
    p.add_argument("--gate-message", default="Que bom que você se interessou! O sistema só libera o envio pra quem segue o perfil. Já segue? Então toca no botão aqui embaixo que eu te mando 👇")
    p.add_argument("--gate-button", default="Me envia ✅")
    p.add_argument("--gate-not-following", default="Olhei aqui e você ainda não tá seguindo... vai lá no perfil, toca em seguir e depois volta e toca de novo no botão, ok?")
    p.add_argument("--dry-run", action="store_true")

    p = add("autos", cmd_autos, help="Lista automações + estatísticas")
    p.add_argument("--profile")
    p = add("auto-get", cmd_auto_get, help="Detalhe de uma automação")
    p.add_argument("automation_id")
    p = add("auto-on", lambda a: cmd_auto_toggle(a, True), help="Reativa automação")
    p.add_argument("automation_id")
    p.add_argument("--dry-run", action="store_true")
    p = add("auto-off", lambda a: cmd_auto_toggle(a, False), help="Pausa automação")
    p.add_argument("automation_id")
    p.add_argument("--dry-run", action="store_true")
    p = add("auto-delete", cmd_auto_delete, help="Apaga automação e seus logs")
    p.add_argument("automation_id")
    p.add_argument("--dry-run", action="store_true")
    p = add("auto-logs", cmd_auto_logs, help="Log de cada disparo (quem comentou, o que aconteceu)")
    p.add_argument("automation_id")

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
