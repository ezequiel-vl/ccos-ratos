"""Finaliza uma arte do Ze: preto e branco puro e, opcionalmente, cola o lettering FUIEU original.

uso:
  python ze_final.py entrada.(png|jpeg) saida.png
  python ze_final.py entrada.jpeg saida.png --fuieu X Y LARGURA [ROT] [preto|branco]

X Y = centro do lettering em px; LARGURA em px; ROT em graus (padrão 0); cor padrão preto.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

REFS = Path(__file__).resolve().parents[3] / "clientes/Fuieu/personagem-ze/referencias"


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    src, dst = args[0], args[1]

    a = np.asarray(Image.open(src).convert("RGB")).astype(float)
    gray = a @ np.array([0.299, 0.587, 0.114])
    img = Image.fromarray(np.clip(gray, 0, 255).astype(np.uint8)).convert("RGBA")

    if "--fuieu" in args:
        i = args.index("--fuieu")
        x, y, w = (int(float(v)) for v in args[i + 1:i + 4])
        rest = args[i + 4:]
        rot = float(rest[0]) if rest and rest[0] not in ("preto", "branco") else 0.0
        cor = "branco" if "branco" in rest else "preto"
        lg = Image.open(REFS / f"lettering-fuieu-{cor}.png").convert("RGBA")
        lg = lg.crop(lg.getchannel("A").getbbox())
        h = round(lg.height * w / lg.width)
        lg = lg.resize((w, h), Image.LANCZOS)
        if rot:
            lg = lg.rotate(rot, resample=Image.BICUBIC, expand=True)
        # leve maciez de tinta spray
        lg.putalpha(lg.getchannel("A").filter(ImageFilter.GaussianBlur(max(1.0, w / 500))))
        img.alpha_composite(lg, (x - lg.width // 2, y - lg.height // 2))

    img.convert("RGB").save(dst, optimize=True)
    print(f"{dst}: {img.size[0]}x{img.size[1]} px, preto e branco")


if __name__ == "__main__":
    main()
