"""Acesso ao CRM da ezeOS (eze-crm, Supabase) pela API de gestão.

Lê o token de ../../../eze-crm/.env.deploy na hora; nada de credencial aqui.

  python crm.py sql "select ..."          # consulta (imprime JSON)
  python crm.py sql-arquivo consulta.sql
"""
import json
import os
import sys
import urllib.request

ENV = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../eze-crm/.env.deploy"))


def _cfg():
    cfg = {}
    with open(ENV, encoding="utf-8") as f:
        for linha in f:
            if "=" in linha and not linha.strip().startswith("#"):
                k, v = linha.strip().split("=", 1)
                cfg[k] = v.strip().strip('"')
    return cfg["SUPABASE_ACCESS_TOKEN"], cfg["PROJECT_REF"]


def sql(query):
    token, ref = _cfg()
    req = urllib.request.Request(
        f"https://api.supabase.com/v1/projects/{ref}/database/query",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "ezeos-operacao"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"CRM respondeu {e.code}: {e.read().decode()[:400]}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) >= 3 and sys.argv[1] == "sql":
        print(json.dumps(sql(sys.argv[2]), ensure_ascii=False, indent=1, default=str))
    elif len(sys.argv) >= 3 and sys.argv[1] == "sql-arquivo":
        with open(sys.argv[2], encoding="utf-8") as f:
            print(json.dumps(sql(f.read()), ensure_ascii=False, indent=1, default=str))
    else:
        print(__doc__)
