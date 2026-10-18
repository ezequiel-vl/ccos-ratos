"""Preenche a proposta do Ponto Digital a partir de um JSON com os dados da clínica.

Uso:
    python preencher.py dados.json saida.html

O modelo fica em ezeOS/ofertas/2026-10-16-ponto-digital/proposta-modelo.html.
Imprime o slug sugerido pra publicação. Sai com erro se faltar dado obrigatório
ou se sobrar algum {{CAMPO}} sem trocar.
"""
import datetime
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
MODELO = RAIZ / "ezeOS/ofertas/2026-10-16-ponto-digital/proposta-modelo.html"

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]
NUMEROS = {1: "Uma das quatro falhou.", 2: "Duas das quatro falharam.",
           3: "Três das quatro falharam.", 4: "As quatro falharam."}
OBRIGATORIOS = ["clinica", "visualizacoes", "periodo", "servico", "bairro", "dominio", "portas"]


def erro(msg):
    sys.exit(f"ERRO: {msg}")


def slugify(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def milhar(valor):
    if isinstance(valor, int):
        return f"{valor:,}".replace(",", ".")
    return str(valor).strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        erro("uso: python preencher.py dados.json saida.html")
    d = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    faltando = [k for k in OBRIGATORIOS if not d.get(k)]
    if faltando:
        erro("faltam campos: " + ", ".join(faltando))

    portas = d["portas"]
    for k in ("nome", "busca", "site", "email"):
        if portas.get(k) not in ("ok", "falhou"):
            erro(f'portas.{k} precisa ser "ok" ou "falhou"')
    if portas["site"] == "ok":
        erro("a clínica já tem site ligado na ficha. Essa proposta é pra quem não tem; adaptar à mão.")
    if portas["busca"] == "falhou" and not d.get("concorrente"):
        erro("porta da busca falhou: informar quem aparece antes (concorrente)")

    e = {k: html.escape(milhar(v)) for k, v in d.items() if not isinstance(v, (dict, bool))}
    clinica, busca = e["clinica"], f'"{e["servico"]} {e["bairro"]}"'

    hoje = datetime.date.fromisoformat(d["data"]) if d.get("data") else datetime.date.today()
    validade = hoje + datetime.timedelta(days=int(d.get("validade_dias", 7)))

    if portas["busca"] == "falhou":
        frase_busca = f"e hoje quem busca {busca} encontra a {e['concorrente']} antes de você."
        p2 = f"A {e['concorrente']} aparece antes" + (", com site ligado na ficha." if d.get("concorrente_tem_site", True) else ".")
    else:
        frase_busca = f"e hoje você aparece na busca por {busca} só com a ficha. O site é o que segura essa posição quando a concorrência ligar o dela."
        p2 = f"A {clinica} aparece entre as primeiras."

    provedor = e.get("email_provedor", "@gmail")
    textos = {
        "nome": ("A ficha aparece, com telefone e endereço.", "A ficha não aparece na busca pelo nome."),
        "busca": (p2, p2),
        "site": ("", "Não existe site, o botão não leva a lugar nenhum."),
        "email": ("O e-mail termina com o nome da clínica.", f"É um endereço {provedor}, sem o nome da clínica."),
    }
    falhas = sum(1 for v in portas.values() if v == "falhou")

    campos = {
        "CLINICA": clinica,
        "NOME": e.get("nome", ""),
        "DATA": f"{hoje.day} {MESES[hoje.month - 1][:3]} {hoje.year}",
        "VALIDADE": f"{validade.day} de {MESES[validade.month - 1]}",
        "VISUALIZACOES": e["visualizacoes"],
        "PERIODO": e["periodo"],
        "SERVICO": e["servico"],
        "BAIRRO": e["bairro"],
        "DOMINIO": e["dominio"],
        "FRASE_BUSCA": frase_busca,
        "FRASE_PORTAS": NUMEROS[falhas],
    }
    for i, k in enumerate(("nome", "busca", "site", "email"), start=1):
        ok = portas[k] == "ok"
        campos[f"P{i}_CLASSE"] = "ok" if ok else "falhou"
        campos[f"P{i}_STATUS"] = "Abriu" if ok else "Falhou"
        campos[f"P{i}_TEXTO"] = textos[k][0 if ok else 1]

    saida = MODELO.read_text(encoding="utf-8")
    for k, v in campos.items():
        saida = saida.replace("{{" + k + "}}", v)
    sobra = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", saida)))
    if sobra:
        erro("campos sem trocar: " + ", ".join(sobra))

    destino = Path(sys.argv[2])
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(saida, encoding="utf-8", newline="\n")
    print(f"OK {destino}")
    print(f"slug: proposta-{slugify(d['clinica'])}")


if __name__ == "__main__":
    main()
