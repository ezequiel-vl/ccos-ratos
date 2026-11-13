"""Calculadora e relatório do funil de prospecção (CRM, pipeline Prospecção).

  python funil.py calc [--meta 5] [--dias 21]    # quantas abordagens por dia pra bater a meta de fechamentos
  python funil.py relatorio [--dias 30]          # conversão por frente e por variante de abertura

Taxas: usa as reais do CRM quando já tem 30 ou mais abordados; antes disso, usa as estimativas abaixo.
Frente = deals.origin_channel (reativacao, ponto, morno, prospeccao).
Variante = deals.utm_content (ex.: carteira-A, frio-B), gravada pelo /prospectar em cada envio.
"""
import sys
from collections import defaultdict

from crm import sql

PIPE = "cc516c8b-d349-4018-b774-3ff355840166"
ESTIMADO = {"resposta": 0.25, "proposta": 0.30, "fechamento": 0.35}
RESPONDEU = {"Respondeu", "Proposta", "Fechou", "Não é agora"}
PROPOSTA = {"Proposta", "Fechou"}
MIN_AMOSTRA = 30


def dados(dias=None):
    filtro = f"and d.created_at > now() - interval '{int(dias)} days'" if dias else ""
    return sql(f"""
        select coalesce(d.origin_channel, 'sem frente') frente, coalesce(d.utm_content, 'sem variante') variante,
               s.name etapa
        from whatsapp_hub.deals d join whatsapp_hub.stages s on s.id = d.stage_id
        where d.pipeline_id = '{PIPE}' and d.archived_at is null {filtro}""")


def taxas(linhas):
    ab = [l for l in linhas if l["etapa"] != "A abordar"]
    resp = [l for l in ab if l["etapa"] in RESPONDEU]
    prop = [l for l in ab if l["etapa"] in PROPOSTA]
    fech = [l for l in ab if l["etapa"] == "Fechou"]
    return {
        "abordados": len(ab), "responderam": len(resp), "propostas": len(prop), "fechados": len(fech),
        "resposta": len(resp) / len(ab) if ab else None,
        "proposta": len(prop) / len(resp) if resp else None,
        "fechamento": len(fech) / len(prop) if prop else None,
    }


def pct(x):
    return "  -  " if x is None else f"{x * 100:4.0f}%"


def calc(meta=5, dias_uteis=21):
    t = taxas(dados())
    reais = t["abordados"] >= MIN_AMOSTRA and all(t[k] for k in ("resposta", "proposta", "fechamento"))
    r = {k: t[k] for k in ESTIMADO} if reais else dict(ESTIMADO)
    propostas = meta / r["fechamento"]
    conversas = propostas / r["proposta"]
    abordagens = conversas / r["resposta"]
    origem = f"taxas reais do CRM ({t['abordados']} abordados)" if reais else \
        f"taxas estimadas (CRM tem {t['abordados']} abordados; uso as reais a partir de {MIN_AMOSTRA})"
    print(f"Meta: {meta} fechamentos no mês · {origem}")
    print(f"  resposta {pct(r['resposta'])} · proposta {pct(r['proposta'])} · fechamento {pct(r['fechamento'])}")
    print(f"  {meta} fechamentos <- {propostas:.0f} propostas <- {conversas:.0f} conversas <- {abordagens:.0f} abordagens")
    print(f"  = {abordagens / dias_uteis:.1f} abordagens por dia útil ({dias_uteis} dias úteis)")


def relatorio(dias=30):
    linhas = dados(dias)
    print(f"Funil Prospecção, últimos {dias} dias\n")
    for chave, titulo in (("frente", "POR FRENTE"), ("variante", "POR VARIANTE DE ABERTURA")):
        grupos = defaultdict(list)
        for l in linhas:
            grupos[l[chave]].append(l)
        print(f"{titulo}\n  {'':22} abord  resp  taxa   prop  fech")
        for nome, ls in sorted(grupos.items(), key=lambda kv: -len(kv[1])):
            t = taxas(ls)
            print(f"  {nome[:22]:22} {t['abordados']:5} {t['responderam']:5} {pct(t['resposta'])} {t['propostas']:5} {t['fechados']:5}")
        print()
    t = taxas(linhas)
    print(f"TOTAL: {t['abordados']} abordados · resposta {pct(t['resposta'])} · proposta {pct(t['proposta'])} · fechamento {pct(t['fechamento'])}")
    a_abordar = sum(1 for l in linhas if l["etapa"] == "A abordar")
    print(f"Na fila (A abordar): {a_abordar}")


def arg(nome, padrao):
    a = sys.argv
    return type(padrao)(a[a.index(nome) + 1]) if nome in a else padrao


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "calc":
        calc(arg("--meta", 5), arg("--dias", 21))
    elif cmd == "relatorio":
        relatorio(arg("--dias", 30))
    else:
        print(__doc__)
