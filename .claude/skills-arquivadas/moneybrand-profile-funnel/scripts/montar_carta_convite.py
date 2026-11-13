"""Monta a carta convite do aluno como página HTML, no modelo do programa.

Uso:
    python scripts/montar_carta_convite.py carta.json carta-convite.html

Formato do JSON (campos opcionais podem ser omitidos):
{
  "titulo_pagina": "Nome do mecanismo · Um convite",
  "pre_headline": "Para quem é a carta, em uma linha.",
  "headline": "A ideia principal, em uma frase.",
  "abertura": ["E aí, Nome aqui.", "Parágrafo curto.", "..."],
  "secoes": [
    {"titulo": "Opcional", "paragrafos": ["...", "..."]},
    {"titulo": "Opcional", "lista": ["benefício 1", "benefício 2"]},
    {"titulo": "O método: Nome", "passos": [{"passo": "Passo 1", "explicacao": "Opcional"}]}
  ],
  "provas": ["Relato real 1", "Relato real 2"],
  "chamada_paragrafos": ["Se isso faz sentido pra você, me chama no WhatsApp."],
  "chamada_botao": "Me chama no WhatsApp",
  "chamada_link": "https://wa.me/5500000000000",
  "assinatura": "-nome"
}

Se "provas" vier vazio ou ausente, a página mostra um espaço marcado lembrando que as provas entram depois.
"""
import html
import json
import sys
from pathlib import Path

MODELO = Path(__file__).resolve().parent.parent / "assets" / "carta-convite-modelo.html"


def esc(texto):
    return html.escape(str(texto), quote=False)


def paragrafos(itens, indent="  "):
    return "\n".join(f"{indent}<p>{esc(p)}</p>" for p in itens if str(p).strip())


def montar_corpo(dados):
    partes = []
    if dados.get("abertura"):
        partes.append(paragrafos(dados["abertura"]))
    for secao in dados.get("secoes", []):
        bloco = []
        if secao.get("titulo"):
            bloco.append(f"  <h2>{esc(secao['titulo'])}</h2>")
        if secao.get("paragrafos"):
            bloco.append(paragrafos(secao["paragrafos"]))
        if secao.get("lista"):
            itens = "\n".join(f"    <li>{esc(i)}</li>" for i in secao["lista"])
            bloco.append(f"  <ul>\n{itens}\n  </ul>")
        if secao.get("passos"):
            itens = []
            for p in secao["passos"]:
                if isinstance(p, str):
                    itens.append(f"    <li>{esc(p)}</li>")
                else:
                    extra = f"<span>{esc(p['explicacao'])}</span>" if p.get("explicacao") else ""
                    itens.append(f"    <li>{esc(p.get('passo', ''))}{extra}</li>")
            bloco.append("  <ol>\n" + "\n".join(itens) + "\n  </ol>")
        partes.append("\n".join(bloco))
    provas = [p for p in dados.get("provas", []) if str(p).strip()]
    if provas:
        partes.append("  <h2>Quem já passou por isso</h2>\n" + paragrafos(provas))
    else:
        partes.append('  <div class="provas">Espaço das provas: quando os primeiros clientes chegarem, os relatos reais entram aqui.</div>')
    if dados.get("chamada_paragrafos"):
        partes.append(paragrafos(dados["chamada_paragrafos"]))
    return "\n\n".join(partes)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    dados = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    pagina = MODELO.read_text(encoding="utf-8")
    trocas = {
        "{{TITULO_PAGINA}}": esc(dados.get("titulo_pagina", "Um convite")),
        "{{PRE_HEADLINE}}": esc(dados.get("pre_headline", "")),
        "{{HEADLINE}}": esc(dados.get("headline", "")),
        "{{CORPO}}": montar_corpo(dados),
        "{{CHAMADA_LINK}}": html.escape(dados.get("chamada_link", "#"), quote=True),
        "{{CHAMADA_BOTAO}}": esc(dados.get("chamada_botao", "Me chama no WhatsApp")),
        "{{ASSINATURA}}": esc(dados.get("assinatura", "")),
    }
    for chave, valor in trocas.items():
        pagina = pagina.replace(chave, valor)
    Path(sys.argv[2]).write_text(pagina, encoding="utf-8")
    print(f"Página gerada: {sys.argv[2]}")


if __name__ == "__main__":
    main()
