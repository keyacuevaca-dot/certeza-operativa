"""Genera los tres logotipos de Certeza Operativa (SVG con texto en trazos + PNG).

Uso:  python3 _fuente/marca.py
Salida: marca/  (1-delta, 2-horizontal, 3-vertical; con fondo petróleo y sin fondo)
Requiere: fonttools, uharfbuzz, cairosvg.
"""
from math import hypot
from pathlib import Path

import cairosvg
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = RAIZ / "assets" / "fonts"
SALIDA = RAIZ / "marca"

# Paleta: petróleo de fondo (el mismo --azul del sitio), Delta gris perla.
PETROLEO = "#0B3C49"
GRIS_DELTA = "#BFC8CC"   # claro sobre petróleo, sin llegar a blanco
TEXTO = "#EDF0F0"        # CERTEZA: blanco hueso
ACENTO = "#8FB4BD"       # OPERATIVA, filete y separadores: acero azulado
LEMA = "#BFC8CC"         # Orden · Visibilidad · Control
SEP = "punto"            # separador del lema: punto | filete | franja

SERIF = FUENTES / "Cinzel-SemiBold.ttf"
SANS = FUENTES / "Montserrat-Medium.ttf"


# ---------------------------------------------------------------- Delta
def delta(base, x0=0.0, y0=0.0):
    """Delta con grosor perpendicular uniforme y ritmo de franjas regular.

    Proporción alto/base 0.75 (la del Delta del sitio). Lado derecho:
    tramo sólido, dos franjas iguales con separaciones iguales y la apertura
    que forma la «C».
    """
    B, H = base, base * 0.75
    t = 0.15 * H                       # grosor perpendicular de los tres lados
    k = (B / 2) / H                    # avance horizontal por unidad vertical
    dx = t * hypot(B / 2, H) / H       # corrimiento horizontal equivalente a t
    ya, yb = dx / k, H - t             # vértice interior y base interior
    S = yb - ya
    yc = ya + 0.30 * S                 # fin del tramo sólido
    g, s = 0.065 * S, 0.13 * S         # separación y franja

    xo = lambda y: B / 2 + k * y       # borde exterior derecho
    xi = lambda y: B / 2 + k * y - dx  # borde interior derecho
    xl = B / 2 - k * yb + dx           # esquina interior izquierda

    def poli(pts):
        return "M" + " L".join(f"{x0 + x:.2f} {y0 + y:.2f}" for x, y in pts) + " Z"

    cuerpo = poli([(B / 2, 0), (xo(yc), yc), (xi(yc), yc), (B / 2, ya),
                   (xl, yb), (xo(yb), yb), (B, H), (0, H)])
    franjas = []
    y = yc + g
    for _ in range(2):
        franjas.append(poli([(xi(y), y), (xo(y), y), (xo(y + s), y + s), (xi(y + s), y + s)]))
        y += s + g
    return " ".join([cuerpo] + franjas), (B, H)


# ---------------------------------------------------------------- Texto
class Fuente:
    def __init__(self, ruta):
        self.tt = TTFont(ruta)
        self.gs = self.tt.getGlyphSet()
        self.hb = hb.Font(hb.Face(hb.Blob.from_file_path(str(ruta))))
        self.upem = self.tt["head"].unitsPerEm

    def texto(self, cadena, tam, x=0.0, base=0.0, track=0.0):
        """Devuelve (d, caja_tinta) con el texto ya en trazos. track en em."""
        buf = hb.Buffer()
        buf.add_str(cadena)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        e = tam / self.upem
        pen = SVGPathPen(self.gs)
        caja = BoundsPen(self.gs)
        cx = x
        n = len(buf.glyph_infos)
        for i, (inf, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            nombre = self.tt.getGlyphName(inf.codepoint)
            m = (e, 0, 0, -e, cx + pos.x_offset * e, base - pos.y_offset * e)
            self.gs[nombre].draw(TransformPen(pen, m))
            self.gs[nombre].draw(TransformPen(caja, m))
            cx += pos.x_advance * e + (track * tam if i < n - 1 else 0)
        return pen.getCommands(), caja.bounds  # bounds: (xmin, ymin, xmax, ymax)

    def ancho(self, cadena, tam, track=0.0):
        _, b = self.texto(cadena, tam, track=track)
        return b[2] - b[0]


# ---------------------------------------------------------------- Composición
def svg(ancho, alto, cuerpo, fondo=True, titulo="Certeza Operativa"):
    rect = f'<rect width="{ancho:.0f}" height="{alto:.0f}" fill="{PETROLEO}"/>' if fondo else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho:.0f} {alto:.0f}" '
            f'width="{ancho:.0f}" height="{alto:.0f}" role="img" aria-label="{titulo}">'
            f'<title>{titulo}</title>{rect}{cuerpo}</svg>\n')


def palabra_marca(serif, sans, x, y_cap, tam):
    """CERTEZA + OPERATIVA justificada al mismo ancho. Devuelve (svg, medidas)."""
    d0, b0 = serif.texto("Certeza", tam)
    cap = -b0[1]                         # altura de la C (tinta sobre la línea base)
    base1 = y_cap + cap
    d1, b1 = serif.texto("Certeza", tam, x - b0[0], base1)
    ancho = b1[2] - b1[0]

    # OPERATIVA ocupa el mismo ancho que CERTEZA con interletrado fijo de 0.62 em:
    # se despeja el tamaño en vez de abrir las letras sin control.
    tr = 0.62
    a100 = sans.ancho("OPERATIVA", 100)
    tam2 = ancho / (a100 / 100 + 8 * tr)
    _, bo = sans.texto("OPERATIVA", tam2)
    cap2 = -bo[1]
    base2 = base1 + 0.30 * cap + cap2
    _, bo = sans.texto("OPERATIVA", tam2, 0, base2, tr)
    d2, bo = sans.texto("OPERATIVA", tam2, x - bo[0], base2, tr)

    out = f'<path fill="{TEXTO}" d="{d1}"/><path fill="{ACENTO}" d="{d2}"/>'
    return out, dict(x=x, ancho=ancho, cap=cap, top=y_cap, base1=base1, base2=base2, cap2=cap2)


def lema(sans, x, ancho, y_cap, cap_max, sep="punto"):
    """ORDEN · VISIBILIDAD · CONTROL al mismo ancho que CERTEZA.

    Interletrado y hueco fijos (en em); se despeja el tamaño. Si saliera más
    grande que cap_max, se usa cap_max y el conjunto va centrado.
    """
    palabras = ["ORDEN", "VISIBILIDAD", "CONTROL"]
    tr, hueco_em = 0.30, 1.9
    _, b = sans.texto("O", 100)
    cap100 = -b[1]
    unidad = sum(sans.ancho(w, 100, tr) for w in palabras) / 100 + 2 * hueco_em
    tam = min(ancho / unidad, cap_max / cap100 * 100)
    cap = cap100 * tam / 100
    hueco = hueco_em * tam
    total = unidad * tam
    base = y_cap + cap
    cx, out = x + (ancho - total) / 2, []
    for i, w in enumerate(palabras):
        _, bb = sans.texto(w, tam, 0, base, tr)
        d, bb2 = sans.texto(w, tam, cx - bb[0], base, tr)
        out.append(f'<path fill="{LEMA}" d="{d}"/>')
        cx = bb2[2]
        if i < 2:
            mx, my = cx + hueco / 2, base - cap / 2
            if sep == "punto":
                out.append(f'<circle cx="{mx:.2f}" cy="{my:.2f}" r="{cap * 0.11:.2f}" fill="{ACENTO}"/>')
            elif sep == "filete":
                out.append(f'<rect x="{mx - cap * 0.03:.2f}" y="{my - cap * 0.75:.2f}" width="{cap * 0.06:.2f}" height="{cap * 1.5:.2f}" fill="{ACENTO}" opacity=".7"/>')
            else:  # franja: misma inclinación que las franjas del Delta
                h, w2, k = cap * 0.22, cap * 0.9, 0.6667
                pts = [(mx - w2 / 2 - k * h / 2, my - h / 2), (mx + w2 / 2 - k * h / 2, my - h / 2),
                       (mx + w2 / 2 + k * h / 2, my + h / 2), (mx - w2 / 2 + k * h / 2, my + h / 2)]
                out.append(f'<path fill="{ACENTO}" d="M' + " L".join(f"{a:.2f} {c:.2f}" for a, c in pts) + ' Z"/>')
            cx += hueco
    return "".join(out), cap


def guardar(nombre, contenido, escala=1.0):
    SALIDA.mkdir(exist_ok=True)
    ruta = SALIDA / f"{nombre}.svg"
    ruta.write_text(contenido, encoding="utf-8")
    cairosvg.svg2png(bytestring=contenido.encode(), write_to=str(SALIDA / f"{nombre}.png"), scale=escala)
    print("listo:", ruta.relative_to(RAIZ))


def main():
    serif, sans = Fuente(SERIF), Fuente(SANS)

    # 1 · Solo el Delta: cuadrado, petróleo, Delta gris perla.
    L = 1200
    base = L * 0.56
    H = base * 0.75
    x0 = (L - base) / 2
    y0 = (L - H) / 2 - H * 0.04          # el centroide del triángulo baja; se compensa
    d, _ = delta(base, x0, y0)
    guardar("1-delta-petroleo", svg(L, L, f'<path fill="{GRIS_DELTA}" d="{d}"/>', titulo="Delta de Certeza Operativa"))

    # 2 · Horizontal: Delta a la izquierda; su alto = de la cima de la C a la base de OPERATIVA.
    tam = 260
    marca, m = palabra_marca(serif, sans, 0, 0, tam)
    alto_bloque = m["base2"] - m["top"]
    sobre = alto_bloque * 0.035           # el vértice es una punta: sube un poco para verse a la par
    Hd = alto_bloque + sobre
    Bd = Hd / 0.75
    pad = alto_bloque * 0.75
    gap = Hd * 0.30
    xt = pad + Bd + gap
    d, _ = delta(Bd, pad, pad - sobre)
    marca, m = palabra_marca(serif, sans, xt, pad, tam)
    W = xt + m["ancho"] + pad
    Hh = pad + alto_bloque + pad
    cuerpo = f'<path fill="{GRIS_DELTA}" d="{d}"/>{marca}'
    guardar("2-horizontal", svg(W, Hh, cuerpo), escala=1.0)
    guardar("2-horizontal-sin-fondo", svg(W, Hh, cuerpo, fondo=False), escala=1.0)

    # 3 · Vertical completo: Delta arriba, CERTEZA, OPERATIVA, filete y lema.
    tam = 240
    _, m = palabra_marca(serif, sans, 0, 0, tam)
    ancho = m["ancho"]
    Bd = ancho * 0.36
    Hd = Bd * 0.75
    pad = ancho * 0.16
    W = ancho + 2 * pad
    y = pad
    d, _ = delta(Bd, (W - Bd) / 2, y)
    y += Hd + m["cap"] * 0.42
    marca, m = palabra_marca(serif, sans, pad, y, tam)
    y = m["base2"] + m["cap"] * 0.30
    filete = f'<rect x="{pad:.2f}" y="{y:.2f}" width="{ancho:.2f}" height="{max(1.5, m["cap"] * 0.009):.2f}" fill="{ACENTO}" opacity=".45"/>'
    y += m["cap"] * 0.30
    lem, cap_lema = lema(sans, pad, ancho, y, m["cap2"] * 0.62, SEP)
    Hv = y + cap_lema + pad
    cuerpo = f'<path fill="{GRIS_DELTA}" d="{d}"/>{marca}{filete}{lem}'
    guardar("3-vertical-completo", svg(W, Hv, cuerpo))
    guardar("3-vertical-completo-sin-fondo", svg(W, Hv, cuerpo, fondo=False))


if __name__ == "__main__":
    main()
