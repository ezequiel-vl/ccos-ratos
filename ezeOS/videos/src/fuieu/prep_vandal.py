"""Separa a arte fuieu-school.png em camadas pra animar no Remotion."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = r"c:/Users/EZEQUIEL/Documents/ezeOS/ccos-ratos/clientes/Fuieu/estampas/Vandal School"
MARCA = r"c:/Users/EZEQUIEL/Documents/ezeOS/ccos-ratos/clientes/Fuieu/marca"
OUT = r"c:/Users/EZEQUIEL/Documents/ezeOS/ccos-ratos/ezeOS/videos/public/fuieu-vandal"
os.makedirs(OUT, exist_ok=True)

im = Image.open(f"{SRC}/fuieu-school.png").convert("RGB")
W, H = im.size
rgb = np.array(im).astype(np.uint8)
lum = np.array(im.convert("L")).astype(np.int32)


def poly_mask(pts, grow=0):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    if grow > 0:
        m = m.filter(ImageFilter.MaxFilter(grow * 2 + 1))
    return np.array(m) > 127


def rect_mask(x0, y0, x1, y1):
    m = np.zeros((H, W), bool)
    m[y0:y1, x0:x1] = True
    return m


def dilate(mask, r):
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(r * 2 + 1))
    return np.array(m) > 127


def erode(mask, r):
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(r * 2 + 1))
    return np.array(m) > 127


ink = lum < 200  # traço

# braço do professor (Ze) apontando
ARM = [(612, 742), (700, 786), (787, 789), (812, 765), (819, 753), (828, 747), (845, 749), (865, 754), (915, 717), (933, 724),
       (935, 742), (922, 765), (928, 800), (913, 827), (888, 835), (862, 845), (830, 875), (797, 906),
       (762, 940), (693, 968), (645, 960), (622, 900), (610, 820)]
arm = poly_mask(ARM)

# cabeça do aluno: mancha preta grossa (abertura tira as linhas do graffiti)
hb = rect_mask(990, 840, 1275, 1070) & (lum < 215)
head = dilate(erode(hb, 12), 13) & rect_mask(990, 840, 1275, 1070)

protect = arm | head

# conteúdo do quadro
from scipy import ndimage

# equação: componentes de traço que cabem inteiros na faixa de cima (o graffiti é um componente gigante e fica de fora)
lab, n = ndimage.label(ink)
EQBOX = (655, 395, 1075, 585)
eq_raw = np.zeros((H, W), bool)
eq_items = []  # (x0, comp mask) pra agrupar por ícone
for k, sl in enumerate(ndimage.find_objects(lab), start=1):
    ys_, xs_ = sl
    if xs_.start >= EQBOX[0] and xs_.stop <= EQBOX[2] and ys_.start >= EQBOX[1] and ys_.stop <= EQBOX[3]:
        eq_raw |= lab == k
EQ = dilate(eq_raw, 6)
GR = rect_mask(730, 470, 1670, 970)
eq_ink = dilate(ink & EQ, 3) & EQ & ~protect
gr_ink = dilate(ink & GR, 3) & GR & ~protect & ~EQ & ~rect_mask(1480, 928, 1560, 1000)


def ink_layer(mask, name):
    a = np.clip(255 - lum, 0, 255).astype(np.uint8)
    a[~mask] = 0
    out = np.zeros((H, W, 4), np.uint8)
    out[..., 3] = a
    Image.fromarray(out, "RGBA").save(f"{OUT}/{name}")


# graffiti em tela cheia (mesmo sistema de coordenadas da cena)
ink_layer(gr_ink, "graffiti.png")

# ícones da equação: cada um recortado, com caixa
# cada ícone = caixa 2D (ordem: balaclava, +, luva, +, lata, =)
EQ_BOXES = [(655, 440, 790, 580), (757, 480, 787, 514), (790, 400, 916, 560), (905, 484, 937, 521), (936, 400, 1013, 548), (1013, 455, 1075, 500)]
PRIOR = [1, 3, 0, 2, 4, 5]  # sinais de + têm prioridade sobre os vizinhos
owner = np.full((H, W), -1, int)
for k in PRIOR:
    x0, y0, x1, y1 = EQ_BOXES[k]
    sel = np.zeros((H, W), bool); sel[y0:y1, x0:x1] = True
    owner[sel & (owner < 0) & eq_ink] = k
eq_boxes = []
a_full = np.clip(255 - lum, 0, 255).astype(np.uint8)
for k in range(6):
    m = owner == k
    ys, xs = np.where(m)
    x0, x1, y0, y1 = xs.min() - 2, xs.max() + 3, ys.min() - 2, ys.max() + 3
    a = a_full[y0:y1, x0:x1].copy()
    a[~m[y0:y1, x0:x1]] = 0
    o = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    o[..., 3] = a
    Image.fromarray(o, "RGBA").save(f"{OUT}/eq-{k}.png")
    eq_boxes.append({"x": int(x0), "y": int(y0), "w": int(x1 - x0), "h": int(y1 - y0)})

# braço: RGB original dentro do polígono (borda suave de 1 px)
am = Image.fromarray((arm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
arm_rgba = np.dstack([rgb, np.array(am)])
ys, xs = np.where(arm)
ax0, ay0, ax1, ay1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
Image.fromarray(arm_rgba[ay0:ay1, ax0:ax1], "RGBA").save(f"{OUT}/arm.png")

# cabeça do aluno
hm = Image.fromarray((head * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
head_rgba = np.dstack([rgb, np.array(hm)])
ys, xs = np.where(head)
hx0, hy0, hx1, hy1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
Image.fromarray(head_rgba[hy0:hy1, hx0:hx1], "RGBA").save(f"{OUT}/head.png")

# base: tira o quadro e o braço (fica branco), cabeça continua
base = rgb.copy()
CAN = rect_mask(1480, 928, 1560, 1000)
base[eq_ink | gr_ink] = 255
base[rect_mask(655, 322, 1728, 990) & ~protect & ~CAN] = 255
base[dilate(arm, 2) & ~head & rect_mask(690, 0, W, H)] = 255
Image.fromarray(base).save(f"{OUT}/base.png")

# título VANDAL SCHOOL: letra por letra
t = Image.open(f"{SRC}/vandal school.png").convert("L")
tl = np.array(t).astype(np.int32)
tink = tl < 160
cols = tink.any(axis=0)
letters, start = [], None
for i, v in enumerate(list(cols) + [False]):
    if v and start is None:
        start = i
    if not v and start is not None:
        letters.append((start, i))
        start = None
ta = np.clip(255 - tl, 0, 255).astype(np.uint8)
title_boxes = []
for k, (s, e) in enumerate(letters):
    x0, x1 = max(0, s - 3), min(t.width, e + 3)
    ys = np.where(tink[:, x0:x1].any(axis=1))[0]
    y0, y1 = max(0, ys.min() - 3), min(t.height, ys.max() + 4)
    o = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    o[..., 3] = ta[y0:y1, x0:x1]
    Image.fromarray(o, "RGBA").save(f"{OUT}/t-{k}.png")
    title_boxes.append({"x": int(x0), "y": int(y0), "w": int(x1 - x0), "h": int(y1 - y0)})

# lettering FUIEU original
f = Image.open(f"{MARCA}/lettering-fuieu-preto.png").convert("RGBA")
f.save(f"{OUT}/fuieu-tag.png")

meta = {
    "scene": {"w": W, "h": H},
    "arm": {"x": int(ax0), "y": int(ay0), "w": int(ax1 - ax0), "h": int(ay1 - ay0)},
    "head": {"x": int(hx0), "y": int(hy0), "w": int(hx1 - hx0), "h": int(hy1 - hy0)},
    "eq": eq_boxes,
    "title": {"w": t.width, "h": t.height, "letters": title_boxes},
    "tag": {"w": f.width, "h": f.height},
}
with open(f"{OUT}/meta.json", "w") as fh:
    json.dump(meta, fh, indent=1)
print(json.dumps(meta))
