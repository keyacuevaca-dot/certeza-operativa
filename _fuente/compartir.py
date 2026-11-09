# Genera assets/compartir.jpg (1200 × 630) para la vista previa al compartir en WhatsApp y redes.
# Parte del montaje de la portada (assets/encabezado.webp). Uso: python _fuente/compartir.py
# Necesita Pillow (pip install pillow).
import os
import re
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def ruta(*p): return os.path.join(RAIZ, *p)

S = 2                                  # se dibuja al doble y se reduce al final, para bordes suaves
W, H = 1200 * S, 630 * S
GRAFITO = (30, 35, 40)                 # --petroleo (#1E2328)
ACENTO = (40, 183, 181)                # --acento-encabezado (#28B7B5)
BLANCO = (241, 243, 245)               # --texto-claro (#F1F3F5)

# 1) Foto a la derecha, a todo lo alto
lienzo = Image.new('RGB', (W, H), GRAFITO)
foto = Image.open(ruta('assets', 'encabezado.webp')).convert('RGB')
fw = round(foto.width * H / foto.height)
lienzo.paste(foto.resize((fw, H), Image.LANCZOS), (W - fw, 0))

# 2) Degradado grafito de izquierda a derecha, como en la portada
paradas = [(0, .97), (.36, .95), (.47, .78), (.56, .30), (.63, 0)]
capa = Image.new('L', (W, 1))
for x in range(W):
    t, v = x / W, 0.0
    for (a, va), (b, vb) in zip(paradas, paradas[1:]):
        if a <= t <= b:
            v = va + (vb - va) * (t - a) / (b - a)
            break
    capa.putpixel((x, 0), round(v * 255))
lienzo = Image.composite(Image.new('RGB', (W, H), GRAFITO), lienzo, capa.resize((W, H)))

# 3) Titular: «Evoluciona» en acento y «tu negocio» en blanco, Outfit 700
d = ImageDraw.Draw(lienzo)
titular = ImageFont.truetype(ruta('assets', 'fonts', 'Outfit-Bold.ttf'), 104 * S)
x0 = 64 * S
d.text((x0, 136 * S), 'Evoluciona', font=titular, fill=ACENTO)
d.text((x0, 244 * S), 'tu negocio', font=titular, fill=BLANCO)

# 4) Marca abajo a la izquierda: el triángulo de assets/marca.svg, en la plata metálica del logo actual
svg = open(ruta('assets', 'marca.svg'), encoding='utf-8').read()
def poligonos(d_attr):
    # Solo usa M, L, H y Z (así está dibujado el triángulo); tras M, los pares siguientes son líneas
    figuras, actual, cmd, nums, y = [], [], None, [], 0.0
    for tok in re.findall(r'[MLHZ]|-?\d*\.?\d+', d_attr):
        if tok in 'MLHZ':
            cmd = tok
            if tok == 'Z' and actual:
                figuras.append(actual)
                actual = []
            continue
        n = float(tok)
        if cmd == 'H':
            actual.append((n, y))
        else:
            nums.append(n)
            if len(nums) == 2:
                x, y = nums
                nums = []
                actual.append((x, y))
                if cmd == 'M':
                    cmd = 'L'
    if actual:
        figuras.append(actual)
    return figuras
formas = [f for d_attr in re.findall(r' d="([^"]+)"', svg) for f in poligonos(d_attr)]
vx, vy, vw, vh = 38, 8, 175, 133                        # viewBox de marca.svg
bw = 58 * S; bh = round(bw * vh / vw)
bx, by = x0, 528 * S
mascara = Image.new('L', (bw, bh), 0)
dm = ImageDraw.Draw(mascara)
for f in formas:
    dm.polygon([((px - vx) * bw / vw, (py - vy) * bh / vh) for px, py in f], fill=255)
plata = Image.new('RGB', (bw, bh))
paradas_plata = [(0, (244, 246, 248)), (.55, (195, 203, 212)), (1, (138, 150, 163))]
for yy in range(bh):
    for xx in range(bw):
        t = (xx / bw + yy / bh) / 2
        for (a, ca), (b, cb) in zip(paradas_plata, paradas_plata[1:]):
            if a <= t <= b:
                k = (t - a) / (b - a)
                plata.putpixel((xx, yy), tuple(round(ca[i] + (cb[i] - ca[i]) * k) for i in range(3)))
                break
lienzo.paste(plata, (bx, by), mascara)

# 5) «CERTEZA OPERATIVA» en Crimson Pro, con un poco de espacio entre letras
nombre = ImageFont.truetype(ruta('assets', 'fonts', 'CrimsonPro-Bold.ttf'), 28 * S)
texto, separacion = 'CERTEZA OPERATIVA', 0.06 * 28 * S
caja = nombre.getbbox('CERTEZA')
ty = by + bh / 2 - (caja[1] + caja[3]) / 2
tx = bx + bw + 18 * S
for letra in texto:
    d.text((tx, ty), letra, font=nombre, fill=BLANCO)
    tx += nombre.getlength(letra) + separacion

final = lienzo.resize((1200, 630), Image.LANCZOS)
destino = ruta('assets', 'compartir.jpg')
final.save(destino, quality=85, optimize=True, progressive=True)
print(destino, final.size, os.path.getsize(destino) // 1024, 'KB')
