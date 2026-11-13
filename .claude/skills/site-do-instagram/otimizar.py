"""Otimiza um site estático da família Renata (site/index.html + assets/).

Uso:  python otimizar.py <pasta-do-site> [--max 1200] [--qualidade 78]

Faz, sem mudar nada visível:
1. Fotos: JPG/PNG citados no index.html com lado maior > --max são reduzidos; todos
   regravados em JPG progressivo (só troca o arquivo se ficar menor). og-compartilhar fica 1200x630.
2. <img> sem width/height ganha as dimensões reais do arquivo (evita CLS) e a regra base
   `img{...}` ganha `height:auto` pra não esticar foto em regra que só define largura.
3. Fontes do Google Fonts viram woff2 em assets/fontes/ (subset latin, que cobre acentos do
   português), com @font-face no <style> e preload das usadas no topo. Some a ida ao Google.

Roda de novo sem estragar nada (idempotente).
"""
import argparse, io, os, re, sys, urllib.request
from PIL import Image

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def fotos(site, html, maximo, qualidade):
    refs = sorted(set(re.findall(r"assets/[\w./-]+\.(?:jpe?g|png)", html, re.I)))
    antes = depois = 0
    for ref in refs:
        f = os.path.join(site, ref)
        if not os.path.exists(f):
            print("  FALTA", ref)
            continue
        if ref.lower().endswith(".png"):
            continue  # png citado é raro (logo/transparência); não mexe
        tam0 = os.path.getsize(f)
        im = Image.open(f)
        im.load()
        if im.mode != "RGB":
            im = im.convert("RGB")
        if "og-compartilhar" not in ref and max(im.size) > maximo:
            im.thumbnail((maximo, maximo), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=qualidade, optimize=True, progressive=True)
        novo = buf.getvalue()
        if len(novo) < tam0:
            with open(f, "wb") as o:
                o.write(novo)
        antes += tam0
        depois += min(len(novo), tam0)
    print(f"  fotos: {antes // 1024} KB -> {depois // 1024} KB ({len(refs)} arquivos)")


def dimensoes(site, html):
    n = 0

    def troca(m):
        nonlocal n
        tag = m.group(0)
        if re.search(r"\swidth=", tag):
            return tag
        src = re.search(r'src="([^"]+)"', tag)
        if not src or src.group(1).startswith(("http", "data:")):
            return tag
        f = os.path.join(site, src.group(1))
        if not os.path.exists(f):
            return tag
        w, h = Image.open(f).size
        n += 1
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)

    html = re.sub(r"<img\b[^>]*>", troca, html)
    # regra base precisa de height:auto, senão o atributo height estica a foto
    html = re.sub(r"(\n\s*img\{)(?![^}]*height:auto)([^}]*)\}",
                  lambda m: f"{m.group(1)}{m.group(2)};height:auto}}", html, count=1)
    print(f"  <img> com width/height adicionados: {n}")
    return html


def fontes(site, html):
    m = re.search(r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]+)" rel="stylesheet">', html)
    if not m:
        print("  fontes: já locais (ou sem Google Fonts)")
        return html
    url = m.group(1).replace("&amp;", "&")
    css = baixar(url).decode()
    pasta = os.path.join(site, "assets", "fontes")
    os.makedirs(pasta, exist_ok=True)
    faces, arquivos = [], {}
    # o Google comenta o subset antes de cada bloco: /* latin */ @font-face{...}
    for subset, bloco in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]+\})", css):
        if subset != "latin":
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", bloco).group(1)
        est = re.search(r"font-style:\s*(\w+)", bloco).group(1)
        src = re.search(r"url\((https://[^)]+\.woff2)\)", bloco).group(1)
        if src not in arquivos:
            nome = f"{fam.lower().replace(' ', '-')}-{est}-{len(arquivos)}.woff2"
            with open(os.path.join(pasta, nome), "wb") as o:
                o.write(baixar(src))
            arquivos[src] = nome
        faces.append(bloco.replace(src, f"assets/fontes/{arquivos[src]}"))
    # blocos com mesmo arquivo (fonte variável) viram um só, com faixa de peso
    juntos = {}
    for b in faces:
        arq = re.search(r"url\(([^)]+)\)", b).group(1)
        peso = int(re.search(r"font-weight:\s*(\d+)", b).group(1))
        lo, hi, base = juntos.get(arq, (peso, peso, b))
        juntos[arq] = (min(lo, peso), max(hi, peso), base)
    regras = []
    for arq, (lo, hi, b) in juntos.items():
        b = re.sub(r"font-weight:\s*\d+", f"font-weight:{lo}{' ' + str(hi) if hi != lo else ''}", b)
        regras.append(re.sub(r"\s+", " ", b))
    total = sum(os.path.getsize(os.path.join(pasta, a)) for a in arquivos.values())
    # preload: só as faces normais (italic carrega quando aparecer)
    pre = "".join(
        f'<link rel="preload" href="{arq}" as="font" type="font/woff2" crossorigin>\n'
        for arq in juntos if "-normal-" in arq)
    html = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\n', "", html)
    html = html.replace(m.group(0) + "\n", pre)
    html = html.replace("<style>\n", "<style>\n" + "\n".join(regras) + "\n", 1)
    print(f"  fontes: {len(arquivos)} woff2 locais, {total // 1024} KB")
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--max", type=int, default=1200)
    ap.add_argument("--qualidade", type=int, default=78)
    a = ap.parse_args()
    idx = os.path.join(a.site, "index.html")
    html = open(idx, encoding="utf-8").read()
    print(a.site)
    fotos(a.site, html, a.max, a.qualidade)
    html = dimensoes(a.site, html)
    html = fontes(a.site, html)
    open(idx, "w", encoding="utf-8", newline="").write(html)


if __name__ == "__main__":
    sys.exit(main())
