"""Gera o calendário visual do lançamento do Endereço Fixo a partir dos .md desta pasta.

Uso:  python gerar.py <pasta-de-saida>
Ex.:  python gerar.py ../../../../_publicado/ezeos-calendario

Lê os textos de ../0X-*.md (fonte única), copia logo, PNGs e MP4 do Manifesto pra <saida>/assets/
e escreve <saida>/index.html. Mudou um texto? Roda de novo e publica com /publicar-site.
"""
import html
import re
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
POSTS = AQUI.parent
RAIZ = POSTS.parents[2]
CARROSSEIS = ["manifesto", "metodo", "isca", "vida-depois", "solucoes", "vendas"]
REELS = RAIZ / "ezeOS" / "videos" / "out" / "reels"  # renderizados no Remotion (fora do git)


# ---------- markdown mínimo (o que os nossos .md usam) ----------
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def md(texto, nivel=4):
    linhas = texto.splitlines()
    out, i = [], 0
    while i < len(linhas):
        l = linhas[i]
        s = l.strip()
        if not s:
            i += 1
            continue
        if s.startswith("#"):
            n = len(s) - len(s.lstrip("#"))
            tag = f"h{min(6, nivel + n - 2)}"
            out.append(f"<{tag}>{inline(s[n:].strip())}</{tag}>")
            i += 1
        elif s == "---":
            out.append("<hr>")
            i += 1
        elif s.startswith(">"):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                bloco.append(re.sub(r"^\s*>\s?", "", linhas[i]))
                i += 1
            out.append("<blockquote>" + md("\n".join(bloco), nivel) + "</blockquote>")
        elif s.startswith("|"):
            rows = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                cells = [c.strip() for c in linhas[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            tb = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tabela"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
        elif re.match(r"^([-·]|\d+\.)\s", s):
            ordenada = bool(re.match(r"^\d+\.", s))
            itens = []
            while i < len(linhas) and re.match(r"^\s*([-·]|\d+\.)\s", linhas[i]):
                itens.append(re.sub(r"^\s*([-·]|\d+\.)\s", "", linhas[i]))
                i += 1
            tag = "ol" if ordenada else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in itens) + f"</{tag}>")
        else:
            par = []
            while i < len(linhas) and linhas[i].strip() and not re.match(r"^\s*(#|>|\||---$|[-·]\s|\d+\.\s)", linhas[i]):
                par.append(linhas[i].strip())
                i += 1
            out.append("<p>" + "<br>".join(inline(x) for x in par) + "</p>")
    return "\n".join(out)


def ler(nome):
    t = (POSTS / nome).read_text(encoding="utf-8")
    return re.sub(r"^# .*\n", "", t, count=1)


def secoes(texto, marcador="## "):
    """Divide em {titulo: corpo} pelas linhas que começam com o marcador."""
    partes, atual, corpo = {}, None, []
    for l in texto.splitlines():
        if l.startswith(marcador) and not l.startswith(marcador + "#"):
            if atual:
                partes[atual] = "\n".join(corpo)
            atual, corpo = l[len(marcador):].strip(), []
        elif atual:
            corpo.append(l)
    if atual:
        partes[atual] = "\n".join(corpo)
    return partes


# ---------- peças do calendário ----------
SETA = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


def peca(pid, tipo, quando, titulo, resumo, porque, extra="", texto=None, status=None):
    det = ""
    if texto:
        det = f'<details><summary>Ver texto completo</summary><div class="md">{texto}</div></details>'
    st = f'<span class="status">{status}</span>' if status else ""
    return f"""
<article class="piece card luz" data-id="{pid}">
  <div class="top"><span class="type">{tipo}</span><span class="when">{quando}</span></div>
  <h3>{titulo}</h3>
  <p class="body">{resumo}</p>
  {st}
  {extra}
  <p class="why"><b>Por que aqui:</b> {porque}</p>
  {det}
  <button class="mark" type="button"><i></i><span>marcar publicado</span></button>
</article>"""


def galeria(nome):
    pasta = POSTS / nome / "instagram"
    total = len(sorted(pasta.glob("slide-*.png")))
    if not total:
        return ""
    thumbs = "".join(
        f'<button class="th" type="button" data-g="{nome}" data-n="{n}" data-t="{total}" aria-label="Slide {n}"><img src="assets/{nome}/slide-{n:02d}.png" alt="Slide {n}" loading="lazy"></button>'
        for n in range(1, total + 1))
    return f"""<div class="gal">{thumbs}</div>
<p class="galnota">Toca num slide pra ver com motion. Arte pronta: {total} MP4 + {total} PNG.</p>"""


def main():
    if len(sys.argv) != 2:
        sys.exit("uso: python gerar.py <pasta-de-saida>")
    saida = Path(sys.argv[1]).resolve()
    shutil.copy(RAIZ / "marca/logo/ezeos-horizontal-branco.png", saida / "assets/logo-branco.png")
    for nome in CARROSSEIS:
        (saida / "assets" / nome).mkdir(parents=True, exist_ok=True)
        for src in sorted((POSTS / nome / "instagram").glob("slide-*.*")):
            if src.suffix in (".png", ".mp4"):
                shutil.copy(src, saida / "assets" / nome / src.name)
    (saida / "assets" / "reels").mkdir(parents=True, exist_ok=True)
    for src in sorted(REELS.glob("reel-*.mp4")):
        shutil.copy(src, saida / "assets" / "reels" / src.name)

    story_bio = secoes(ler("01-story-e-bio.md"))
    sb_story = secoes(story_bio["Story de Reposicionamento"], "### ")
    story_txt = sb_story["Opção 2 (meta do dono que lê) · ESCOLHIDA"]
    story_linhas = [re.sub(r"^>\s?", "", l) for l in story_txt.splitlines() if l.startswith(">")]
    story_html = "".join(f"<p>{inline(l)}</p>" if l.strip() else '<p class="vazio"></p>' for l in story_linhas)

    script = ler("09-script-automatico.md")
    rotina = secoes(ler("10-rotina-stories.md"))
    reels = secoes(ler("08-reels-ads.md"))

    def post(arq):
        return md(ler(arq))

    # ----- reels -----
    def reel_card(chave, pid, quando, porque):
        corpo = reels[chave]
        num = chave.split(":")[0].split()[-1]
        mp4 = REELS / f"reel-0{num}.mp4"
        hook = re.search(r"\*\*Texto na tela:\*\*\s*\n>\s*(.+)", corpo).group(1)
        video = re.search(r"\*\*Vídeo \(([^)]+)\):\*\*\s*(.+)", corpo)
        extra = f'<div class="hook">{inline(hook)}</div><p class="vid"><b>Vídeo ({video.group(1)}):</b> {inline(video.group(2))}</p><p class="leg">Legenda: <b>Comente: PONTO</b></p>'
        nome = chave.split(": ", 1)[1]
        if mp4.exists():
            extra = f'<video class="reel" src="assets/reels/{mp4.name}" controls muted playsinline preload="metadata"></video>' + extra
            return peca(pid, "Reels", quando, nome.capitalize(), "", porque, extra, status="vídeo pronto (Remotion)")
        return peca(pid, "Reels", quando, nome.capitalize(), "", porque, extra, status="roteiro pronto · gravar")

    # ----- rotina de stories -----
    dias = ["Segunda: teste ao vivo", "Terça: bastidor de instalação", "Quarta: enquete", "Quinta: objeção da semana", "Sexta: vaga da semana"]
    rotina_html = "".join(
        f'<details class="dia card"><summary><span class="type">{d.split(":")[0]}</span><b>{d.split(": ")[1].capitalize()}</b></summary><div class="md">{md(rotina[d], 5)}</div></details>'
        for d in dias)

    # ----- semanas -----
    S1 = [
        peca("s1-story", "Story", "Seg 26 · manhã", "Story de reposicionamento",
             "O pacto público: em 7 dias eu mostro as quatro portas e quais estão fechadas na empresa de quem segue. Fixar em destaque “Comece aqui”.",
             "abre o perfil novo antes do primeiro post. A Isca da sexta cumpre a promessa.",
             extra=f'<div class="story">{story_html}</div>', status="texto pronto"),
        peca("s1-manifesto", "Carrossel", "Seg 26 · 07h30", "Manifesto · Endereço Fixo",
             "Finca a bandeira: aparecer cobra de novo toda vez, endereço continua trabalhando. Termina na frase do aluguel e no Comente PONTO.",
             "primeira peça do feed, define o que o perfil defende.",
             extra=galeria("manifesto"), texto=post("02-manifesto.md"), status="arte pronta com motion"),
        reel_card("Reel 1: a busca", "s1-reel1", "Ter 27 · 19h30", "o reel mais simples de gravar, puxa a primeira porta do teste."),
        peca("s1-metodo", "Carrossel", "Qua 28 · 07h30", "1/3 · Apresentação do Método",
             "As três etapas e a ordem em que elas funcionam. Anúncio, robô e post diário como peças certas no lugar errado.",
             "depois da bandeira, o leitor precisa entender o caminho.",
             extra=galeria("metodo"), texto=post("03-metodo-1-de-3.md"), status="arte pronta com motion"),
        reel_card("Reel 2: o botão vazio", "s1-reel2", "Qui 29 · 19h30", "prova em dois toques a diferença entre ter e não ter endereço."),
        peca("s1-isca", "Carrossel", "Sex 30 · 07h30", "Isca · Diagnóstico das quatro portas",
             "Comente PONTO e eu testo as quatro portas da sua empresa e mando o resultado no direct, com áudio de 1 minuto.",
             "cumpre a promessa do story antes do dia 7 e enche o direct de diagnósticos.",
             extra=galeria("isca"), texto=post("06-isca-diagnostico.md"), status="arte pronta com motion"),
        peca("s1-ads", "Anúncio", "Sáb 31 → Qua 04/11", "Teste de anúncio: Reel 1 contra Reel 2",
             "Mesmo orçamento pros dois por 5 dias. Fica o que trouxer mais PONTO por real investido.",
             "com 3 posts no feed, quem chega pelo anúncio já encontra um perfil com argumento.",
             status="configurar no Gerenciador"),
    ]
    S2 = [
        peca("s2-vida", "Carrossel", "Seg 02/11 · 07h30", "2/3 · A vida depois do método",
             "Uma terça-feira hora por hora com a empresa instalada: 7h40 te acham no Google, 20h50 a empresa fechada responde.",
             "abre a segunda semana com desejo, depois da semana de argumento.",
             extra=galeria("vida-depois"), texto=post("04-vida-depois-2-de-3.md"), status="arte pronta com motion"),
        reel_card("Reel 3: o anúncio sem destino", "s2-reel3", "Ter 03/11 · 19h30", "prepara a destruição das soluções comuns da quarta."),
        peca("s2-solucoes", "Carrossel", "Qua 04/11 · 07h30", "3/3 · Contrapor soluções comuns",
             "Social media, site do conhecido e pacote de posts: cada um pinta um andar e ninguém constrói o térreo.",
             "quem já contratou e se frustrou entende por que não deu certo.",
             extra=galeria("solucoes"), texto=post("05-solucoes-comuns-3-de-3.md"), status="arte pronta com motion"),
        reel_card("Reel 4: a instalação em 10 dias", "s2-reel4", "Qui 05/11 · 19h30", "mostra o trabalho sendo feito na véspera da oferta."),
        peca("s2-vendas", "Carrossel", "Sex 06/11 · 07h30", "Vendas · Ponto Digital",
             "O Ponto Digital item por item: 10 dias corridos, preço fechado na proposta, garantia de prazo e as vagas do mês.",
             "fecha as duas semanas com a oferta, pra quem já leu o argumento inteiro.",
             extra=galeria("vendas"), texto=post("07-vendas-ponto-digital.md"), status="arte pronta com motion"),
        reel_card("Reel 5: o @gmail", "s2-reel5", "Sáb 07/11 · 10h00", "peça leve de fim de semana, reforça a porta do e-mail."),
    ]

    grade = [
        ("1", "26/10 a 01/11", ["<b>Story</b> + <b>Manifesto</b><small>bio nova no ar</small>", "<b>Reel 1</b><small>a busca</small>", "<b>1/3 Método</b>", "<b>Reel 2</b><small>o botão vazio</small>", "<b>Isca</b><small>diagnóstico</small>", "<b>Anúncio</b><small>R1 × R2</small>", "<i>respira</i>"]),
        ("2", "02 a 08/11", ["<b>2/3 Vida depois</b>", "<b>Reel 3</b><small>anúncio sem destino</small>", "<b>3/3 Soluções</b><small>fim do teste</small>", "<b>Reel 4</b><small>instalação</small>", "<b>Vendas</b><small>Ponto Digital</small>", "<b>Reel 5</b><small>o @gmail</small>", "<i>respira</i>"]),
    ]
    grade_html = "".join(
        f'<tr><td class="sem"><b>{n}</b><small>{d}</small></td>' + "".join(f"<td>{c}</td>" for c in cel) + "</tr>"
        for n, d, cel in grade)

    prep = [
        peca("p-bio", "Preparo", "até dom 25", "Bio nova, nome e destaques",
             "Opção B no ar, nome “ezeOS | Sua empresa no digital”, link ezeos.com.br/#teste e os 5 destaques fixos.",
             "o visitante que chegar pelo Manifesto já encontra o perfil novo.",
             extra="""<div class="perfil">
  <div class="pf-top"><div class="avatar"><i></i></div><div><b>ezeOS | Sua empresa no digital</b><small>@agenciaezeos · Agência de marketing</small></div></div>
  <p>Onde o seu cliente procurar, você vai estar lá.<br>Instalo sua empresa no digital em 10 dias<br>Site · Google · E-mail · WhatsApp</p>
  <a>ezeos.com.br/#teste</a>
  <div class="dest"><span><i></i>Comece aqui</span><span><i></i>O teste</span><span><i></i>O método</span><span><i></i>Ponto Digital</span><span><i></i>Dúvidas</span></div>
</div>""", texto=md(ler("01-story-e-bio.md")), status="decidido · Bio B"),
        peca("p-auto", "Preparo", "até dom 25", "Resposta automática do PONTO",
             "Quem comenta ou manda PONTO recebe o fluxo do direct: promessa, como funciona, preço, garantia e as perguntas do diagnóstico.",
             "todo post a partir do Manifesto pede a palavra. Sem resposta automática, o primeiro dia vira fila no direct.",
             texto=md(script), status="texto pronto · configurar ManyChat"),
    ]

    pend = [
        ("Desabafo", "precisa de história real: a tua ou de cliente que autorize."),
        ("Cards de prova", "entram quando os números de Boell, Dra. Carina e Tabuleiro estiverem organizados."),
    ]
    pend_html = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in pend)

    pagina = PAGINA
    for k, v in {"PREP": "".join(prep), "S1": "".join(S1), "S2": "".join(S2), "GRADE": grade_html,
                 "ROTINA": rotina_html, "PEND": pend_html, "SETA": SETA}.items():
        pagina = pagina.replace("<!--" + k + "-->", v)
    (saida / "index.html").write_text(pagina, encoding="utf-8", newline="\n")
    print("ok", saida / "index.html")


PAGINA = (AQUI / "pagina.html").read_text(encoding="utf-8")

if __name__ == "__main__":
    main()
