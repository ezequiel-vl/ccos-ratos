"""Painel da operação da ezeOS.

Uso:
  python painel.py                 # gancho SessionStart (lê o JSON do Claude Code no stdin)
  python painel.py --texto         # resumo curto (notificação do Windows)
  python painel.py --ver           # painel completo no terminal
  python painel.py feito <id>      # marca um compromisso da agenda como feito
  python painel.py add AAAA-MM-DD "título" [cliente] [--meta M1] [--pronto "critério"]
  python painel.py editar <id> [--meta M2] [--pronto "critério"]
  python painel.py log prospeccao 10      # registra abordagens enviadas hoje
  python painel.py log reativacao 3
  python painel.py log varredura

Dados: agenda.json (compromissos com data) e log.jsonl (o que foi feito).
Metas (M1, M2, M3) definidas em _contexto/estrategia.md. Cada tarefa leva a meta que ataca e o
critério de pronto; o painel mostra o critério nos itens de hoje e atrasados e lista quem está sem meta.
"""
import json
import os
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
AGENDA = os.path.join(AQUI, "agenda.json")
LOG = os.path.join(AQUI, "log.jsonl")
CACHE_ZERNIO = os.path.join(AQUI, ".cache-zernio.json")
ZERNIO = os.path.expanduser("~/.claude/skills/publicar-agendar-posts/materiais/scripts/zernio.py")

META_PROSPECCAO = 10            # abordagens por dia útil
INICIO_PROSPECCAO = date(2026, 11, 16)
DIA_VARREDURA = 0               # segunda
DIAS_SEM_POST_ALERTA = 2

# pastas que contam como "operação" (o painel só aparece nelas)
RAIZES = ["ezeos/ccos-ratos", "ezeos/eze-crm", "ezeos/ezeevents"]
# projetos paralelos: aqui o Claudinho cobra o foco antes de começar
PARALELOS = {
    "clientes/kyrie": "KYRIE",
    "clientes/laclika": "La Clika",
    "clientes/fuieu": "FUIEU",
    "clientes/fora odorico": "Fora Odorico",
    "clientes/tabuleiro": "Tabuleiro",
    "solo.os": "SOLO.OS",
    "ezeos/ezeevents": "ezeEVENTS",
}

DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def ler_agenda():
    try:
        with open(AGENDA, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def salvar_agenda(itens):
    with open(AGENDA, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)
        f.write("\n")


def ler_log():
    out = []
    try:
        with open(LOG, encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    try:
                        out.append(json.loads(linha))
                    except Exception:
                        pass
    except FileNotFoundError:
        pass
    return out


def registrar(tipo, n=None):
    item = {"data": date.today().isoformat(), "hora": datetime.now().strftime("%H:%M"), "tipo": tipo}
    if n is not None:
        item["n"] = n
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def dia_util(d):
    return d.weekday() < 5


def ultimo_dia_util(antes_de):
    d = antes_de - timedelta(days=1)
    while not dia_util(d):
        d -= timedelta(days=1)
    return d


def fmt(d):
    return f"{DIAS[d.weekday()]} {d.strftime('%d/%m')}"


def zernio_status():
    """Último post publicado e próximos agendados da @agenciaezeos (cache de 3h)."""
    try:
        with open(CACHE_ZERNIO, encoding="utf-8") as f:
            c = json.load(f)
        if time.time() - c.get("ts", 0) < 3 * 3600:
            return c
    except Exception:
        pass
    res = {"ts": time.time(), "ultimo": None, "agendados": [], "ok": False}
    try:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        for status, chave in (("published", "ultimo"), ("scheduled", "agendados")):
            p = subprocess.run([sys.executable, ZERNIO, "posts", "--status", status],
                               capture_output=True, text=True, timeout=8, env=env, encoding="utf-8")
            datas = []
            for linha in p.stdout.splitlines():
                partes = linha.split()
                if len(partes) >= 3 and partes[1] == status:
                    datas.append(partes[2][:16])
            if chave == "ultimo":
                res["ultimo"] = max(datas) if datas else None
            else:
                res["agendados"] = sorted(datas)
        res["ok"] = True
        with open(CACHE_ZERNIO, "w", encoding="utf-8") as f:
            json.dump(res, f)
    except Exception:
        pass
    return res


def montar(cwd=""):
    hoje = date.today()
    agenda = ler_agenda()
    log = ler_log()
    cobrar, hoje_itens, proximos, sem_meta = [], [], [], []

    # 1. agenda
    for it in agenda:
        if it.get("status") == "feito":
            continue
        try:
            d = date.fromisoformat(it["data"])
        except Exception:
            continue
        tag = f"{it['id']}·{it['meta']}" if it.get("meta") else it["id"]
        if not it.get("meta"):
            sem_meta.append(it["id"])
        rot = f"[{tag}] {it['titulo']}" + (f" ({it['cliente']})" if it.get("cliente") else "")
        pronto = f"\n      pronto quando: {it['pronto']}" if it.get("pronto") else ""
        if d < hoje:
            atraso = (hoje - d).days
            cobrar.append(f"ATRASADO {atraso}d: {rot}, era {fmt(d)}{pronto}")
        elif d == hoje:
            hoje_itens.append(rot + pronto)
        elif d <= hoje + timedelta(days=3):
            proximos.append(f"{fmt(d)}: {rot}")

    # 2. prospecção diária
    def soma(tipo, dia):
        return sum(int(e.get("n", 0)) for e in log if e.get("tipo") == tipo and e.get("data") == dia.isoformat())

    prosp_txt = None
    if hoje >= INICIO_PROSPECCAO:
        if dia_util(hoje):
            feito = soma("prospeccao", hoje) + soma("reativacao", hoje)
            prosp_txt = f"Prospecção hoje: {feito}/{META_PROSPECCAO} abordagens"
            if feito < META_PROSPECCAO:
                hoje_itens.insert(0, f"Prospecção: faltam {META_PROSPECCAO - feito} abordagens hoje (/prospectar)")
        ontem = ultimo_dia_util(hoje)
        if ontem >= INICIO_PROSPECCAO:
            f_ontem = soma("prospeccao", ontem) + soma("reativacao", ontem)
            if f_ontem < META_PROSPECCAO:
                cobrar.append(f"Prospecção de {fmt(ontem)} ficou em {f_ontem}/{META_PROSPECCAO}")

    # 3. varredura semanal dos ativos
    varreduras = sorted(e["data"] for e in log if e.get("tipo") == "varredura")
    ultima_v = date.fromisoformat(varreduras[-1]) if varreduras else None
    segunda = hoje - timedelta(days=(hoje.weekday() - DIA_VARREDURA) % 7)
    if ultima_v is None or ultima_v < segunda:
        txt = "Varredura semanal dos ativos (ezeOS, Ilha Eventos, Thaminy): posts, site e SEO (/varredura)"
        if hoje == segunda:
            hoje_itens.append(txt)
        else:
            cobrar.append(txt + f", era {fmt(segunda)}")

    # 3b. fechamento da semana (sexta): conversão por frente e variante
    if hoje >= INICIO_PROSPECCAO:
        fechamentos = [e["data"] for e in log if e.get("tipo") == "fechamento"]
        sexta = hoje - timedelta(days=(hoje.weekday() - 4) % 7)
        if sexta >= INICIO_PROSPECCAO and not any(d >= sexta.isoformat() for d in fechamentos):
            txt = "Fechamento da semana: conversão por frente e variante (python ezeOS/operacao/funil.py relatorio), descartar a pior abertura"
            if hoje == sexta:
                hoje_itens.append(txt)
            elif hoje > sexta:
                cobrar.append(txt + f", era {fmt(sexta)}")

    # 4. Instagram da ezeOS
    ig_txt = None
    z = zernio_status()
    if z.get("ok"):
        ult = z.get("ultimo")
        ag = [a for a in z.get("agendados", []) if a >= datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")]
        if ult:
            d_ult = date.fromisoformat(ult[:10])
            dias = (hoje - d_ult).days
            ig_txt = f"@agenciaezeos: último post {fmt(d_ult)} ({dias}d), {len(ag)} agendado(s)"
            if not ag and dias >= DIAS_SEM_POST_ALERTA:
                cobrar.append(f"Instagram da ezeOS parado há {dias} dias e nada agendado")

    # 5. foco
    c = (cwd or "").replace("\\", "/").lower()
    paralelo = next((nome for chave, nome in PARALELOS.items() if chave in c), None)

    return {"hoje": hoje, "cobrar": cobrar, "hoje_itens": hoje_itens, "proximos": proximos,
            "prosp": prosp_txt, "ig": ig_txt, "paralelo": paralelo, "sem_meta": sem_meta}


def texto_completo(p):
    L = [f"PAINEL DA EZEOS, {fmt(p['hoje'])}"]
    if p["cobrar"]:
        L.append("\nCOBRAR (atrasado):")
        L += [f"  - {x}" for x in p["cobrar"]]
    L.append("\nHOJE:")
    L += [f"  - {x}" for x in p["hoje_itens"]] or ["  - nada marcado"]
    if p["proximos"]:
        L.append("\nPRÓXIMOS 3 DIAS:")
        L += [f"  - {x}" for x in p["proximos"]]
    if p.get("sem_meta"):
        L.append(f"\nSEM META (ligar a M1/M2/M3 ou cortar): {', '.join(p['sem_meta'])}")
    extras = [x for x in (p["prosp"], p["ig"]) if x]
    if extras:
        L.append("\n" + "\n".join(extras))
    return "\n".join(L)


def texto_curto(p):
    partes = []
    if p["cobrar"]:
        partes.append(f"{len(p['cobrar'])} atrasado(s)")
    if p["hoje_itens"]:
        partes.append(f"{len(p['hoje_itens'])} pra hoje")
    if p["prosp"]:
        partes.append(p["prosp"].replace("Prospecção hoje: ", "prospecção "))
    return "Claudinho: " + (", ".join(partes) if partes else "tudo em dia")


def gancho():
    try:
        dados = json.load(sys.stdin)
    except Exception:
        dados = {}
    cwd = dados.get("cwd") or os.getcwd()
    c = cwd.replace("\\", "/").lower()
    if not any(r in c for r in RAIZES):
        return  # fora da operação: silêncio
    p = montar(cwd)
    instr = [
        "Você é o Claudinho, sócio e CEO operacional da ezeOS (regras em ezeOS/operacao/README.md).",
        "Na PRIMEIRA resposta desta conversa, antes de qualquer outra coisa, mostre ao Ezequiel o que está atrasado e o que é de hoje, em poucas linhas, e cobre.",
    ]
    if p["paralelo"]:
        instr.append(
            f"ATENÇÃO FOCO: a conversa abriu em projeto paralelo ({p['paralelo']}). Antes de trabalhar nele, "
            "pergunte se a prospecção e os itens de hoje da ezeOS já foram feitos. Se não, proponha fazer isso primeiro. "
            "Se ele decidir seguir no paralelo mesmo assim, respeite e siga.")
    if not p["cobrar"] and not p["hoje_itens"]:
        instr[1] = "Painel em dia. Não precisa cobrar nada; só siga o pedido."
    ctx = "\n".join(instr) + "\n\n" + texto_completo(p)
    print(json.dumps({
        "systemMessage": texto_curto(p),
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ctx},
    }, ensure_ascii=False))


def separar_opcoes(args):
    """Tira --meta e --pronto da lista de argumentos."""
    pos, op, i = [], {}, 0
    while i < len(args):
        if args[i] in ("--meta", "--pronto") and i + 1 < len(args):
            op[args[i][2:]] = args[i + 1]
            i += 2
        else:
            pos.append(args[i])
            i += 1
    return pos, op


def main():
    a, op = separar_opcoes(sys.argv[1:])
    if not a:
        return gancho()
    cmd = a[0]
    if cmd == "--texto":
        print(texto_curto(montar()))
    elif cmd == "--ver":
        print(texto_completo(montar(os.getcwd())))
    elif cmd == "feito" and len(a) >= 2:
        itens = ler_agenda()
        for it in itens:
            if it["id"] == a[1]:
                it["status"] = "feito"
                it["feito_em"] = date.today().isoformat()
                print(f"feito: {it['titulo']}")
                if it.get("pronto"):
                    print(f"  confere: {it['pronto']}")
        salvar_agenda(itens)
    elif cmd == "editar" and len(a) >= 2 and op:
        itens = ler_agenda()
        for it in itens:
            if it["id"] == a[1]:
                it.update(op)
                print(f"{it['id']} editado: {op}")
        salvar_agenda(itens)
    elif cmd == "add" and len(a) >= 3:
        itens = ler_agenda()
        novo_id = f"a{max([int(i['id'][1:]) for i in itens if i['id'][1:].isdigit()] or [0]) + 1}"
        it = {"id": novo_id, "data": a[1], "titulo": a[2], "status": "pendente"}
        if len(a) >= 4:
            it["cliente"] = a[3]
        it.update(op)
        itens.append(it)
        salvar_agenda(itens)
        print(f"{novo_id} adicionado: {a[1]} {a[2]}" + ("" if op.get("meta") else "  (sem meta: use --meta)"))
    elif cmd == "log" and len(a) >= 2:
        registrar(a[1], int(a[2]) if len(a) >= 3 else None)
        print(f"registrado: {a[1]} {a[2] if len(a) >= 3 else ''}")
    else:
        print(__doc__)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
