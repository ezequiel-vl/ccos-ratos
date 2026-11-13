"""Junta tiles capturados com zoom(save_to_disk) numa imagem só.

Uso:
  python -I costura.py saida.jpg LARGURA_CSS ALTURA_CSS tile1.png:0 tile2.png:506 [...]

LARGURA_CSS/ALTURA_CSS = tamanho exibido no overlay (o "w" e o "h" que o _showW devolve).
Cada tile vai com o deslocamento CSS usado no _showW. A altura da janela é 738 CSS.
A última linha de cada captura vem escura: é trocada pela de cima antes de colar.
"""
import sys
from PIL import Image

VIEW_H = 738


def limpa(im):
    w, h = im.size
    linha = im.crop((0, h - 3, w, h - 2))
    for y in (h - 1, h - 2):
        im.paste(linha, (0, y))
    return im


def costura(saida, css_w, css_h, tiles):
    primeiro = Image.open(tiles[0][0])
    k = primeiro.width / css_w  # px reais por px de CSS
    W, H = round(css_w * k), round(css_h * k)
    out = Image.new('RGB', (W, H))
    for arq, off in tiles:
        t = limpa(Image.open(arq).convert('RGB')).resize((W, round(VIEW_H * k)), Image.LANCZOS)
        out.paste(t, (0, round(off * k)))
    out.save(saida, quality=84, optimize=True, progressive=True)
    print(saida, out.size)


if __name__ == '__main__':
    saida, cw, ch = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    tiles = [(a.rsplit(':', 1)[0], int(a.rsplit(':', 1)[1])) for a in sys.argv[4:]]
    costura(saida, cw, ch, tiles)
