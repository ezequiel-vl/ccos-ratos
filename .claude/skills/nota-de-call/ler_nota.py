"""Le notas de reuniao do OpenWhispr (banco local, SOMENTE LEITURA).

Uso:
  python -I ler_nota.py listar [N]        # ultimas N notas (padrao 5): id, data, duracao, titulo
  python -I ler_nota.py ler ultima        # transcricao da nota mais recente
  python -I ler_nota.py ler <id>          # transcricao de uma nota
  python -I ler_nota.py ler <nome>        # acha pelo titulo (ex.: ler fernando); se houver mais de
                                          # uma com esse nome, lista e pede o id

Saida: uma fala por linha, "[mm:ss] Voce: texto" ou "[mm:ss] Outros: texto".
Fala vinda do microfone = Voce. Fala vinda do audio do computador = Outros
(com o numero da voz quando o app separa mais de uma, ex.: Outros 2).
Nunca grava nada no banco. Nada sai da maquina.
"""
import json
import os
import sqlite3
import sys
import unicodedata

DB = os.path.join(os.environ.get("APPDATA", ""), "open-whispr", "transcriptions.db")


def conectar():
    if not os.path.exists(DB):
        sys.exit(f"Banco nao encontrado: {DB}. O OpenWhispr esta instalado e ja gravou alguma nota?")
    uri = "file:" + DB.replace("\\", "/") + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def mmss(seg):
    seg = int(seg or 0)
    return f"{seg // 60:02d}:{seg % 60:02d}"


def norm(t):
    t = unicodedata.normalize("NFD", t or "")
    return "".join(ch for ch in t if unicodedata.category(ch) != "Mn").lower()


def achar_por_titulo(c, termo):
    rows = c.execute(
        "select id, created_at, audio_duration_seconds, title from notes "
        "where deleted_at is null and transcript is not null and transcript != '' order by id desc"
    ).fetchall()
    t = norm(termo)
    return [r for r in rows if t in norm(r[3])]


def listar(n):
    c = conectar()
    rows = c.execute(
        "select id, created_at, audio_duration_seconds, title, "
        "length(coalesce(transcript,'')) from notes where deleted_at is null "
        "order by id desc limit ?", (n,)
    ).fetchall()
    if not rows:
        print("Nenhuma nota.")
        return
    for i, criado, dur, titulo, tam in rows:
        d = mmss(dur) if dur else "--:--"
        print(f"id {i} | {criado} UTC | {d} | {titulo} | transcricao: {tam} caracteres")
    print("(data em UTC: Brasilia = UTC menos 3h)")


def ler(alvo):
    c = conectar()
    if alvo == "ultima":
        row = c.execute(
            "select id, title, created_at, transcript from notes "
            "where deleted_at is null and transcript is not null and transcript != '' "
            "order by id desc limit 1"
        ).fetchone()
    else:
        if not alvo.isdigit():
            achadas = achar_por_titulo(c, alvo)
            if not achadas:
                sys.exit(f"Nenhuma nota com '{alvo}' no titulo. Use 'listar' pra ver as notas.")
            if len(achadas) > 1:
                print(f"{len(achadas)} notas com '{alvo}' no titulo. Escolha o id:")
                for i, criado, dur, titulo in achadas[:10]:
                    print(f"id {i} | {criado} UTC | {mmss(dur) if dur else '--:--'} | {titulo}")
                sys.exit(2)
            alvo = str(achadas[0][0])
        row = c.execute(
            "select id, title, created_at, transcript from notes where id = ? and deleted_at is null",
            (int(alvo),),
        ).fetchone()
    if not row:
        sys.exit("Nota nao encontrada ou sem transcricao.")
    i, titulo, criado, bruto = row
    print(f"# nota {i} | {titulo} | {criado} UTC")
    try:
        falas = json.loads(bruto)
    except (TypeError, ValueError):
        print(bruto)  # texto simples, sem divisao por voz
        return
    vozes = {f.get("speaker") for f in falas if f.get("source") == "system"}
    for f in falas:
        if f.get("source") == "mic":
            quem = "Voce"
        else:
            quem = "Outros"
            if len(vozes) > 1:
                quem += " " + str(f.get("speaker", "?")).replace("speaker_", "")
        print(f"[{mmss(f.get('timestamp'))}] {quem}: {f.get('text', '').strip()}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if not a or a[0] not in ("listar", "ler"):
        sys.exit(__doc__)
    if a[0] == "listar":
        listar(int(a[1]) if len(a) > 1 else 5)
    else:
        if len(a) < 2:
            sys.exit("Falta o alvo: 'ultima' ou o id da nota.")
        ler(a[1])


if __name__ == "__main__":
    main()
