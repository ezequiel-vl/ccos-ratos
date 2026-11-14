"""Baixa um video do YouTube e entrega texto (legenda) + quadros pra Claude "ouvir" e "ver".

Uso:
  python -I video.py <url> [--intervalo 30] [--altura 480] [--sem-video] [--max-min 60]
  python -I video.py limpar [<id>|tudo]

Saida em %TEMP%/ezeos-video/<id>/ :
  info.txt          titulo, canal, duracao, data, idioma
  transcript.txt    legenda limpa, com [mm:ss] a cada ~30s
  frames/f_MMSS.jpg quadros (640 px de largura) com o minuto/segundo no nome

Ferramentas (yt-dlp e ffmpeg portateis) ficam em ~/.cache/ezeos-video e sao baixadas na primeira
vez. Nada e instalado no sistema. Precisa de Node.js (ja instalado) pro YouTube.
Sem legenda no video: entrega so os quadros e avisa (transcricao do audio nao esta implementada).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

TOOLS = os.path.join(os.path.expanduser("~"), ".cache", "ezeos-video")
WORK = os.path.join(tempfile.gettempdir(), "ezeos-video")
YTDLP = os.path.join(TOOLS, "yt-dlp.exe")
FFMPEG = os.path.join(TOOLS, "ffmpeg.exe")
YTDLP_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"


def log(msg):
    print(msg, flush=True)


def run(cmd, check=True):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout or "erro sem mensagem").strip()[-800:])
    return p


def garantir_ferramentas():
    os.makedirs(TOOLS, exist_ok=True)
    if not os.path.exists(YTDLP):
        log("Baixando yt-dlp (primeira vez)...")
        urllib.request.urlretrieve(YTDLP_URL, YTDLP)
    if not os.path.exists(FFMPEG):
        log("Baixando ffmpeg portatil (primeira vez)...")
        lib = os.path.join(TOOLS, "pylib")
        run([sys.executable, "-m", "pip", "install", "--quiet", "--target", lib, "imageio-ffmpeg"])
        bins = os.path.join(lib, "imageio_ffmpeg", "binaries")
        exe = next((f for f in os.listdir(bins) if f.lower().startswith("ffmpeg") and f.endswith(".exe")), None)
        if not exe:
            raise RuntimeError("ffmpeg nao encontrado depois da instalacao")
        shutil.copy(os.path.join(bins, exe), FFMPEG)


def ytdlp(*args, check=True):
    cmd = [YTDLP, "--no-playlist", "--no-warnings", "--ffmpeg-location", FFMPEG]
    if shutil.which("node"):
        cmd += ["--js-runtimes", "node"]
    return run(cmd + list(args), check=check)


def mmss(seg):
    seg = int(seg)
    h, r = divmod(seg, 3600)
    return f"{h}:{r // 60:02d}:{r % 60:02d}" if h else f"{r // 60:02d}:{r % 60:02d}"


def limpar_vtt(texto):
    linhas, ultimo = [], ""
    for blk in texto.split("\n\n"):
        m = re.search(r"(\d+):(\d+):(\d+)\.\d+ -->", blk)
        if not m:
            continue
        h, mi, s = map(int, m.groups())
        for l in blk.splitlines()[1:]:
            if "-->" in l:
                continue
            l = re.sub(r"<[^>]+>", "", l).strip()
            if l and l != ultimo:
                linhas.append((h * 3600 + mi * 60 + s, l))
                ultimo = l
    out, prev = [], None
    for sec, l in linhas:
        if prev is None or sec - prev >= 30:
            out.append(f"\n[{mmss(sec)}] ")
            prev = sec
        out.append(l + " ")
    return "".join(out).strip(), len(linhas)


def escolher_legenda(info):
    idioma = (info.get("language") or "").split("-")[0] or "en"
    manuais = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}
    for cand in (idioma, "pt", "en"):
        for k in manuais:
            if k == cand or k.startswith(cand + "-"):
                return k, False
    for cand in (f"{idioma}-orig", "pt-orig", "en-orig", idioma, "en"):
        if cand in auto:
            return cand, True
    return None, False


def baixar_legenda(url, lang, auto, pasta):
    flag = "--write-auto-subs" if auto else "--write-subs"
    for espera in (0, 25, 60, 120):
        if espera:
            log(f"YouTube limitou os pedidos (429). Aguardando {espera}s...")
            time.sleep(espera)
        p = ytdlp("--skip-download", flag, "--sub-langs", lang, "--sub-format", "vtt",
                  "-o", os.path.join(pasta, "legenda.%(ext)s"), url, check=False)
        achou = [f for f in os.listdir(pasta) if f.endswith(".vtt")]
        if achou:
            return os.path.join(pasta, achou[0])
        if "429" not in (p.stderr or ""):
            break
    return None


def main_baixar(url, intervalo, altura, sem_video, max_min):
    garantir_ferramentas()
    p = ytdlp("--skip-download", "--dump-single-json", url)
    info = json.loads(p.stdout)
    vid = info["id"]
    dur = info.get("duration") or 0
    if dur > max_min * 60:
        sys.exit(f"Video de {mmss(dur)} passa do limite de {max_min} min. Use --max-min {int(dur / 60) + 1} se quiser mesmo.")
    pasta = os.path.join(WORK, vid)
    os.makedirs(pasta, exist_ok=True)

    with open(os.path.join(pasta, "info.txt"), "w", encoding="utf-8") as f:
        f.write(f"titulo: {info.get('title')}\ncanal: {info.get('channel') or info.get('uploader')}\n"
                f"duracao: {mmss(dur)}\ndata: {info.get('upload_date')}\nidioma: {info.get('language')}\n"
                f"url: {info.get('webpage_url')}\n")
    log(f"Titulo: {info.get('title')} | Canal: {info.get('channel')} | {mmss(dur)} | {info.get('upload_date')}")

    lang, auto = escolher_legenda(info)
    transcript = None
    if lang:
        vtt = baixar_legenda(url, lang, auto, pasta)
        if vtt:
            texto, n = limpar_vtt(open(vtt, encoding="utf-8").read())
            transcript = os.path.join(pasta, "transcript.txt")
            open(transcript, "w", encoding="utf-8").write(texto)
            log(f"Legenda ({'automatica' if auto else 'manual'}, {lang}): {len(texto)} caracteres -> {transcript}")
        else:
            log("AVISO: nao consegui baixar a legenda (limite do YouTube). Tente de novo em alguns minutos.")
    else:
        log("AVISO: video sem legenda. Sem texto, so quadros (transcricao de audio nao implementada).")

    if not sem_video:
        mp4 = os.path.join(pasta, "v.mp4")
        if not os.path.exists(mp4):
            ytdlp("-f", f"bv*[height<={altura}]+ba/b[height<={altura}]", "--merge-output-format", "mp4",
                  "-o", os.path.join(pasta, "v.%(ext)s"), url)
        passo = max(intervalo, int(dur / 60) + 1) if dur else intervalo
        fr = os.path.join(pasta, "frames")
        shutil.rmtree(fr, ignore_errors=True)
        os.makedirs(fr)
        run([FFMPEG, "-v", "error", "-y", "-i", mp4, "-vf", f"fps=1/{passo},scale=640:-1", "-q:v", "5",
             os.path.join(fr, "n_%03d.jpg")])
        for nome in sorted(os.listdir(fr)):
            n = int(re.search(r"(\d+)", nome).group(1))
            t = (n - 1) * passo
            os.rename(os.path.join(fr, nome), os.path.join(fr, f"f_{t // 60:02d}{t % 60:02d}.jpg"))
        log(f"Quadros: {len(os.listdir(fr))} (1 a cada {passo}s) -> {fr}")
        log("Nome do quadro = minuto e segundo: f_0630.jpg e o quadro de 06:30.")
    log(f"PASTA: {pasta}")


def main_limpar(alvo):
    if not os.path.isdir(WORK):
        return log("Nada pra limpar.")
    if alvo in (None, "tudo"):
        shutil.rmtree(WORK, ignore_errors=True)
        return log("Tudo limpo.")
    shutil.rmtree(os.path.join(WORK, alvo), ignore_errors=True)
    log(f"Limpo: {alvo}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "limpar":
        return main_limpar(a[1] if len(a) > 1 else None)

    def opt(nome, padrao):
        return int(a[a.index(nome) + 1]) if nome in a else padrao

    main_baixar(a[0], opt("--intervalo", 30), opt("--altura", 480), "--sem-video" in a, opt("--max-min", 60))


if __name__ == "__main__":
    main()
