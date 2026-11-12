"""Prepara uma arte do Ze para DTF.

uso:
  python ze_dtf.py entrada.png saida.png ALTURA_CM [--sem-fundo] [--sem-branco]

--sem-fundo : remove o fundo claro (papel/cinza) ligado à borda da imagem
--sem-branco: remove todo branco/quase branco (camiseta branca; o tecido faz o branco)
Saída: PNG 300 dpi, alpha binário (sem semitransparência), sem pontinhos soltos.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

DPI = 300


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print(__doc__)
        sys.exit(1)
    src, dst, cm = args[0], args[1], float(args[2])
    sem_fundo = "--sem-fundo" in args
    sem_branco = "--sem-branco" in args

    im = Image.open(src).convert("RGBA")
    a = np.asarray(im).astype(float)
    rgb, alpha = a[..., :3], a[..., 3]
    keep = alpha > 127

    lum = rgb.mean(-1)
    if sem_fundo:
        # fecha pequenas falhas do contorno preto antes de achar o fundo,
        # senão o papel "vaza" para dentro de áreas brancas do desenho
        escuro = lum < 128
        selado = ndimage.binary_dilation(escuro, iterations=6)
        lab, _ = ndimage.label(~selado)
        borda = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
        fundo = np.isin(lab, borda[borda > 0])
        # devolve ao fundo a faixa entre ele e o traço (só pelo lado de fora)
        fundo = ndimage.binary_dilation(fundo, iterations=6) & ~escuro & (lum > 170)
        keep &= ~fundo
    if sem_branco:
        tinta = (255 - rgb).max(-1) / 255.0
        keep &= tinta >= 0.35

    lab, n = ndimage.label(keep)
    if n:
        sizes = ndimage.sum(keep, lab, np.arange(1, n + 1))
        small = np.zeros(n + 1, bool)
        small[1:] = sizes < 12
        keep &= ~small[lab]

    out = np.zeros_like(a)
    out[..., :3] = rgb
    out[..., 3] = np.where(keep, 255, 0)
    img = Image.fromarray(out.astype(np.uint8), "RGBA")
    img = img.crop(img.getchannel("A").getbbox())

    alvo = round(cm / 2.54 * DPI)
    w = round(img.width * alvo / img.height)
    img = img.resize((w, alvo), Image.LANCZOS)
    al = np.asarray(img.getchannel("A"))
    img.putalpha(Image.fromarray(np.where(al >= 128, 255, 0).astype(np.uint8)))
    img.save(dst, dpi=(DPI, DPI), optimize=True)
    print(f"{dst}: {w}x{alvo} px = {w / DPI * 2.54:.1f} x {cm:.1f} cm @ {DPI} dpi")


if __name__ == "__main__":
    main()
