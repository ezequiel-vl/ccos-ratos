"""Varredura semanal dos clientes ativos: site no ar, SEO básico e Instagram.

  python varredura.py            # gera varreduras/AAAA-MM-DD.md e imprime o resumo

O que fica de fora daqui e o Claudinho confere na mão (skill /varredura):
ficha do Google, posição nas buscas, posts da Thaminy e da Ilha (sem Zernio ainda).
"""
import json
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.request
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "varreduras")
ZERNIO = os.path.expanduser("~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py")

ATIVOS = [
    {"nome": "ezeOS", "site": "https://ezeos.com.br/", "instagram": "@agenciaezeos", "zernio": ""},
    {"nome": "Ilha Eventos", "site": "https://ilhaeventos.com.br/", "instagram": "(sem Instagram ainda)", "zernio": None},
    {"nome": "ThaminyIlha Cerimonial", "site": "https://thaminyilha.com.br/", "instagram": "@thaminyilha.cerimonial", "zernio": None},
]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def baixar(url):
    t0 = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as r:
            corpo = r.read(800_000).decode("utf-8", "ignore")
            return r.status, corpo, round(time.time() - t0, 2), r.geturl(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, "", round(time.time() - t0, 2), url, {}
    except Exception as e:
        return None, str(e), None, url, {}


def achar(padrao, txt):
    m = re.search(padrao, txt, re.I | re.S)
    return m.group(1).strip() if m else None


def checar_site(url):
    st, html, seg, final, hdr = baixar(url)
    r = {"status": st, "tempo": seg, "final": final, "ok": [], "problemas": []}
    if st != 200:
        r["problemas"].append(f"site respondeu {st} ({html[:80] if st is None else ''})")
        return r
    titulo = achar(r"<title[^>]*>(.*?)</title>", html)
    desc = achar(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html) or \
        achar(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', html)
    robots = achar(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'](.*?)["\']', html) or ""
    canon = achar(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', html)
    og = achar(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']', html)
    h1 = len(re.findall(r"<h1[\s>]", html, re.I))
    schema = re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', html)
    viewport = "name=\"viewport\"" in html or "name='viewport'" in html

    (r["ok"] if titulo else r["problemas"]).append(f"título: {titulo[:70] if titulo else 'FALTANDO'}")
    if desc:
        r["ok"].append(f"descrição: {len(desc)} caracteres")
        if not 70 <= len(desc) <= 170:
            r["problemas"].append(f"descrição com {len(desc)} caracteres (ideal 70 a 160)")
    else:
        r["problemas"].append("meta descrição FALTANDO")
    if "noindex" in robots.lower() or "noindex" in hdr.get("X-Robots-Tag", "").lower():
        r["problemas"].append("NOINDEX: o Google não indexa essa página")
    (r["ok"] if canon else r["problemas"]).append(f"canonical: {canon or 'faltando'}")
    (r["ok"] if og else r["problemas"]).append(f"imagem de compartilhamento (og:image): {'ok' if og else 'faltando'}")
    if h1 != 1:
        r["problemas"].append(f"{h1} títulos H1 na página (ideal 1)")
    if any(t in schema for t in ("LocalBusiness", "ProfessionalService", "Organization", "EventVenue", "MedicalBusiness")):
        r["ok"].append(f"schema: {', '.join(sorted(set(schema)))[:80]}")
    else:
        r["problemas"].append("sem schema de negócio local (LocalBusiness)")
    if not viewport:
        r["problemas"].append("sem meta viewport (celular)")
    if seg and seg > 3:
        r["problemas"].append(f"lento: {seg}s pra responder")

    base = re.match(r"https?://[^/]+", final).group(0)
    for arq in ("robots.txt", "sitemap.xml"):
        s, corpo, *_ = baixar(f"{base}/{arq}")
        if s == 200 and ("<urlset" in corpo or "<sitemapindex" in corpo or arq == "robots.txt"):
            r["ok"].append(f"{arq}: ok")
        else:
            r["problemas"].append(f"{arq}: não encontrado ({s})")
    return r


def checar_zernio(cliente):
    try:
        cmd = [sys.executable, ZERNIO] + (["--cliente", cliente] if cliente else []) + ["posts", "--status", "published"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=20, encoding="utf-8",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        datas = sorted(l.split()[2][:10] for l in p.stdout.splitlines() if len(l.split()) >= 3 and l.split()[1] == "published")
        sete = [d for d in datas if (date.today() - date.fromisoformat(d)).days <= 7]
        return f"{len(sete)} post(s) nos últimos 7 dias, último em {datas[-1] if datas else 'nunca'}"
    except Exception as e:
        return f"não consegui ler a Zernio ({e.__class__.__name__})"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(SAIDA, exist_ok=True)
    hoje = date.today().isoformat()
    L = [f"# Varredura semanal, {hoje}", ""]
    resumo = []
    for a in ATIVOS:
        r = checar_site(a["site"])
        ig = checar_zernio(a["zernio"]) if a["zernio"] is not None else "fora da Zernio, conferir no app"
        L += [f"## {a['nome']}", "", f"**Site:** {a['site']} (status {r['status']}, {r['tempo']}s)",
              f"**Instagram:** {a['instagram']}: {ig}", ""]
        if r["problemas"]:
            L.append("**Problemas:**")
            L += [f"- {p}" for p in r["problemas"]]
        L.append("")
        L.append("**Ok:** " + "; ".join(r["ok"]))
        L += ["", "**Conferir na mão:** ficha do Google (fotos novas, avaliações respondidas, post da semana), "
              "posição na busca do serviço principal, posts da semana.", ""]
        resumo.append(f"{a['nome']}: {len(r['problemas'])} problema(s), Instagram: {ig}")
    caminho = os.path.join(SAIDA, f"{hoje}.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("\n".join(resumo))
    print(f"\nrelatório: {caminho}")


if __name__ == "__main__":
    main()
