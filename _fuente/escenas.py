# Escenas del encabezado de cada página interna: fondo temático + emblema dentro del cuadro redondeado de la marca.
# Línea en grafito y acero con pocos trazos en turquesa: la esencia de Certeza Operativa con la «gracia» de cada giro.
# El movimiento va solo con movimiento permitido, dura menos de 5 s y termina quieto (WCAG 2.2.2); sin él, la escena
# se ve completa desde el inicio. Se usa en construir.py: escena(slug), acento(slug, titulo) e icono_chip(slug).
import math
import random
import re

W, H = 640, 600
CX, CY, LADO, RADIO = 330, 300, 300, 56
X0, Y0, X1, Y1 = CX - LADO // 2, CY - LADO // 2, CX + LADO // 2, CY + LADO // 2   # 180, 150, 480, 450
GRIS = '#A9ACAF'

# Emblemas en cuadrícula de 24, la misma familia de línea que los íconos del sitio: (trazo base, trazo en turquesa)
EMBLEMAS = {
    'cubiertos': ('<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10"/><path d="M17 21V3c-2.2 1.4-3.5 3.8-3.5 6.5V13H17"/>', ''),
    'tienda': ('<path d="M4.5 10.5V20h15v-9.5"/><path d="M3 10l1.6-5.5h14.8L21 10"/><path d="M3 10a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/>',
               '<path d="M10 20v-5h4v5"/>'),
    'camion': ('<path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7z"/>',
               '<circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>'),
    'grua': ('<path d="M6 21V5M3 5h18M6 5l4-2.5M17 5v6"/><path d="M3 21h8"/>', '<rect x="14.5" y="11" width="5" height="4" rx=".8"/>'),
    'fabrica': ('<path d="M3 21V10l5 3V10l5 3V10l5 3V5h3v16z"/>', '<path d="M7 17h2M11 17h2M15 17h2"/>'),
    'auto': ('<path d="M4 15.5V12l2-4.5h12l2 4.5v3.5z"/><path d="M4 12h16"/>',
             '<circle cx="7.5" cy="16.5" r="1.8"/><circle cx="16.5" cy="16.5" r="1.8"/>'),
    'campana': ('<path d="M5 17a7 7 0 0 1 14 0"/><path d="M3 20h18M4 17h16"/>', '<path d="M12 10V7.6M10.4 7.4h3.2"/>'),
    'maletin': ('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8.5 7V5.5A1.5 1.5 0 0 1 10 4h4a1.5 1.5 0 0 1 1.5 1.5V7"/>',
                '<path d="M12 10.5v6M9 13.5h6"/>'),
    'llave': ('<path d="M14.5 4.5a4.5 4.5 0 0 0-4.4 5.6L3.8 16.4a1.9 1.9 0 0 0 2.7 2.7l6.3-6.3a4.5 4.5 0 0 0 5.6-4.4l-2.6 2.6-2.4-.6-.6-2.4z"/>', ''),
    'brote': ('<path d="M12 21v-8"/><path d="M12 15c0-3.2-2.4-5.2-5.6-5.2 0 3.2 2.4 5.2 5.6 5.2z"/><path d="M5 21h14"/>',
              '<path d="M12 13c0-4 3-6.5 7-6.5 0 4-3 6.5-7 6.5z"/>'),
    'escudo': ('<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.2-7.5 9.5-4.3-1.3-7.5-4.9-7.5-9.5V6z"/>', '<path d="M8.8 12.2l2.2 2.2 4.4-4.6"/>'),
    'checklist': ('<rect x="4.5" y="3" width="15" height="18" rx="2"/><path d="M11.5 8.5h5M11.5 12.5h5M11.5 16.5h5"/>',
                  '<path d="M7.6 8.6l.9.9 1.5-1.6M7.6 12.6l.9.9 1.5-1.6M7.6 16.6l.9.9 1.5-1.6"/>'),
    'ojo': ('<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/>', '<circle cx="12" cy="12" r="3.2"/>'),
    'balanza': ('<path d="M12 4.5V20M8 20h8M4.5 7h15"/><path d="M4.5 7 2.2 13M4.5 7l2.3 6M19.5 7l-2.3 6M19.5 7l2.3 6"/>',
                '<path d="M2 13a2.5 2.5 0 0 0 5 0zM17 13a2.5 2.5 0 0 0 5 0z"/>'),
    'ciclo': ('<path d="M19.5 12a7.5 7.5 0 0 1-12.9 5.2"/><path d="M4.5 12a7.5 7.5 0 0 1 12.9-5.2"/>', '<path d="M17.4 3.5v3.3h-3.3M6.6 20.5v-3.3h3.3"/>'),
    'apps': ('<rect x="3.5" y="3.5" width="7" height="7" rx="1.8"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.8"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.8"/>',
             '<path d="M17 13.5v7M13.5 17h7"/>'),
    'manual': ('<path d="M12 6.5C10.3 5.2 7.9 4.5 3.5 4.5v13c4.4 0 6.8.7 8.5 2 1.7-1.3 4.1-2 8.5-2v-13c-4.4 0-6.8.7-8.5 2zM12 6.5v13"/>',
               '<path d="M14.8 9.4c1.1-.5 2.3-.8 3.7-.9M14.8 12.6c1.1-.5 2.3-.8 3.7-.9"/>'),
    'megafono': ('<path d="M4 10v4a1.5 1.5 0 0 0 1.5 1.5h2L14 19V5L7.5 8.5h-2A1.5 1.5 0 0 0 4 10z"/><path d="M7.5 15.5l1.4 4h2.4l-1-3.6"/>',
                 '<path d="M17.5 9a4 4 0 0 1 0 6M19.8 6.8a7.2 7.2 0 0 1 0 10.4"/>'),
    'tijeras': ('<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.4 7.8 20 16.5M8.4 16.2 20 7.5"/>', ''),
    'birrete': ('<path d="M2.5 9.5 12 5l9.5 4.5L12 14z"/><path d="M6.5 11.6V16c0 1.4 2.5 2.8 5.5 2.8s5.5-1.4 5.5-2.8v-4.4"/>', '<path d="M21.5 9.5v5"/>'),
    'chip': ('<rect x="6.5" y="6.5" width="11" height="11" rx="2"/><path d="M9.5 3.5v3M14.5 3.5v3M9.5 17.5v3M14.5 17.5v3M3.5 9.5h3M3.5 14.5h3M17.5 9.5h3M17.5 14.5h3"/>',
             '<rect x="9.5" y="9.5" width="5" height="5" rx="1"/>'),
}

# Cada página: (fondo, emblema, palabra del título en turquesa, como «Evoluciona» en inicio)
TEMAS = {
    'alimentos-y-bebidas': ('mesa', 'cubiertos', 'Alimentos'),
    'comercio-y-tiendas': ('estantes', 'tienda', 'Comercio'),
    'distribucion-y-logistica': ('rutas', 'camion', 'Distribución'),
    'construccion-e-ingenieria': ('plano', 'grua', 'Construcción'),
    'fabricacion-y-produccion': ('engranes', 'fabrica', 'Fabricación'),
    'automotriz': ('velocimetro', 'auto', 'Automotriz'),
    'turismo-y-hospitalidad': ('costa', 'campana', 'Turismo'),
    'servicios-profesionales': ('agenda', 'maletin', 'Servicios'),
    'reparacion-y-mantenimiento': ('taller', 'llave', 'Reparación'),
    'campo-y-pesca': ('surcos', 'brote', 'Campo'),
    'limpieza-y-seguridad': ('escudos', 'escudo', 'Limpieza'),
    'orden': ('reticula', 'checklist', 'Orden'),
    'visibilidad': ('radar', 'ojo', 'Visibilidad'),
    'control': ('cuadre', 'balanza', 'Control'),
    'mejora-continua': ('tendencia', 'ciclo', 'Mejora'),
    'herramientas': ('ajustes', 'apps', 'Herramientas'),
    'metodos': ('diagrama', 'manual', 'Métodos'),
    'marketing-digital': ('arcos', 'megafono', 'Marketing'),
    'ia-y-automatizacion': ('circuito', 'chip', 'IA'),
    'nosotros': ('regla', 'delta', 'hacemos'),
}


# ---------- Utilidades ----------
def n(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def pt(grados, r, cx=CX, cy=CY):
    a = math.radians(grados)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def dentro(x, y, m=3):
    """¿El punto queda dentro del cuadro redondeado del emblema, con margen m?"""
    if not (X0 + m <= x <= X1 - m and Y0 + m <= y <= Y1 - m):
        return False
    cx, cy = min(max(x, X0 + RADIO), X1 - RADIO), min(max(y, Y0 + RADIO), Y1 - RADIO)
    return math.hypot(x - cx, y - cy) <= RADIO - m


def tapado(x0, y0, x1, y1):
    """True si el rectángulo queda por completo detrás del cuadro: no hace falta dibujarlo."""
    return all(dentro(x, y) for x in (x0, x1) for y in (y0, y1))


def dib(d, ms=0, cls=''):
    """Trazo que se dibuja solo al cargar (stroke-dashoffset sobre pathLength=1)."""
    return f'<path class="{("e-dibuja " + cls).strip()}" pathLength="1" style="--d:{ms}ms" d="{d}"/>'


def arco(r, a_ini, a_fin, cx=CX, cy=CY):
    (x1, y1), (x2, y2) = pt(a_ini, r, cx, cy), pt(a_fin, r, cx, cy)
    return f'M{n(x1)} {n(y1)}A{r} {r} 0 {1 if a_fin - a_ini > 180 else 0} 1 {n(x2)} {n(y2)}'


def raya(a, r1, r2, cx=CX, cy=CY):
    (x1, y1), (x2, y2) = pt(a, r1, cx, cy), pt(a, r2, cx, cy)
    return f'M{n(x1)} {n(y1)}L{n(x2)} {n(y2)}'


def patron(ident, ancho, alto, contenido, x=0, y=0):
    return (f'<defs><pattern id="{ident}" width="{ancho}" height="{alto}" patternUnits="userSpaceOnUse" x="{x}" y="{y}">{contenido}</pattern></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{ident})" stroke="none"/>')


def _tri(cx, cy, s, rot):
    return [(cx + s * math.cos(math.radians(-90 + 120 * k + rot)), cy + s * math.sin(math.radians(-90 + 120 * k + rot))) for k in range(3)]


def _redondo(pts, r):
    d = ''
    for i in range(3):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % 3]
        a = (p1[0] + (p0[0] - p1[0]) * r, p1[1] + (p0[1] - p1[1]) * r)
        b = (p1[0] + (p2[0] - p1[0]) * r, p1[1] + (p2[1] - p1[1]) * r)
        d += ('M' if i == 0 else 'L') + f'{n(a[0])} {n(a[1])}Q{n(p1[0])} {n(p1[1])} {n(b[0])} {n(b[1])}'
    return d + 'Z'


# ---------- Fondos: cada uno devuelve (textura que se desvanece hacia la orilla, figuras nítidas) ----------
def mesa():
    # Plato alrededor del cuadro y tres hilos de vapor que suben sin parar
    tex = f'<circle cx="{CX}" cy="{CY}" r="236"/><circle class="e-tenue" cx="{CX}" cy="{CY}" r="268"/>'
    fig = ''
    for k, x in enumerate((270, 330, 390)):
        s = 15 if k % 2 == 0 else -15
        d = f'M{x} 146' + ''.join(f'c{s * (-1) ** j} -11 {s * (-1) ** j} -33 0 -44' for j in range(3))
        fig += f'<g class="v-vapor" style="--d2:{2.6 + k * 1.5:.1f}s">' + dib(d, 350 + k * 220, 'e-lento' + (' e-acento' if k == 1 else '')) + '</g>'
    return tex, fig


def estantes():
    # Anaqueles con productos que se acomodan y etiquetas de precio en turquesa que se mecen
    r = random.Random('estantes')
    tex, etiquetas = '', 0
    for k, y in enumerate((126, 246, 366, 486)):
        tex += f'<path d="M0 {y}H640"/>'
        x = 18 + r.uniform(0, 20)
        while True:
            w, h = r.choice((34, 44, 56, 66)), r.choice((36, 50, 64, 78))
            if x + w > 622:
                break
            if not tapado(x, y - h, x + w, y):
                ms = int(120 + x * 1.1 + k * 80)
                tex += f'<rect class="e-sube" style="--d:{ms}ms" x="{n(x)}" y="{y - h}" width="{w}" height="{h}" rx="6"/>'
                if etiquetas < 6 and 70 < x < 560 and r.random() < .3:
                    etiquetas += 1
                    tx = x + w / 2
                    tex += (f'<g class="v-columpio" style="transform-origin:{n(tx)}px {y + 8}px;--t:{3 + etiquetas * .35:.2f}s;--d2:{2.4 + etiquetas * .3:.1f}s">'
                            f'<path class="e-acento e-sube" style="--d:{ms + 320}ms" d="M{n(tx - 8)} {y + 8}h16v12l-8 6-8-6z"/></g>')
            x += w + r.choice((8, 12, 16))
    return tex, ''


def rutas():
    # Mapa con rutas de reparto que corren sin parar alrededor del cuadro; salida y llegada en turquesa
    tex = patron('esc-malla', 80, 80, f'<path d="M80 0H0V80" fill="none" stroke="{GRIS}" stroke-opacity=".14" stroke-width="1.5"/>', 20, -10)
    pins = [(78, 132), (352, 60), (586, 176), (590, 420), (300, 548), (66, 404)]
    fig = ''
    for k in range(len(pins)):
        (x1, y1), (x2, y2) = pins[k], pins[(k + 1) % len(pins)]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        L = math.hypot(mx - CX, my - CY) or 1
        mx, my = mx + (mx - CX) / L * 46, my + (my - CY) / L * 46
        fig += f'<path class="e-ruta v-fluye" style="--paso:-12;--t:.9s" d="M{x1} {y1}Q{n(mx)} {n(my)} {x2} {y2}"/>'
    for k, (x, y) in enumerate(pins):
        cls = 'e-pin e-pop' + (' e-acento' if k in (0, 3) else '')
        fig += (f'<g class="{cls}" style="--d:{250 + k * 150}ms"><path class="e-relleno" d="M{x} {y + 15}C{x - 6} {y + 8} {x - 10} {y + 3} {x - 10} {y - 4}'
                f'A10 10 0 0 1 {x + 10} {y - 4}C{x + 10} {y + 3} {x + 6} {y + 8} {x} {y + 15}Z"/><circle cx="{x}" cy="{y - 4}" r="3.4"/></g>')
    return tex, fig


def plano():
    # Plano de ingeniería: cuadrícula alineada al cuadro, cotas en turquesa, cuadro de datos, norte y un láser que lo recorre
    tex = patron('esc-plano', 100, 100,
                 f'<path d="M20 0V100M40 0V100M60 0V100M80 0V100M0 20H100M0 40H100M0 60H100M0 80H100" fill="none" stroke="{GRIS}" stroke-opacity=".09" stroke-width="1"/>'
                 f'<path d="M100 0H0V100" fill="none" stroke="{GRIS}" stroke-opacity=".22" stroke-width="1.5"/>', X0, Y0)
    tex += '<g class="v-extra v-escaner"><path class="e-acento" style="stroke-width:14;stroke-opacity:.06" d="M20 0V600"/><path class="e-acento" style="stroke-opacity:.5" d="M20 0V600"/></g>'
    yc, xc = 104, 122
    fig = dib(f'M{X0} {Y0 - 12}V{yc - 10}M{X1} {Y0 - 12}V{yc - 10}', 200)
    fig += dib(f'M{X0} {yc}H{X1}M{X0 + 13} {yc - 6}L{X0} {yc}L{X0 + 13} {yc + 6}M{X1 - 13} {yc - 6}L{X1} {yc}L{X1 - 13} {yc + 6}', 450, 'e-acento')
    fig += dib(f'M{X0 - 12} {Y0}H{xc - 10}M{X0 - 12} {Y1}H{xc - 10}', 300)
    fig += dib(f'M{xc} {Y0}V{Y1}M{xc - 6} {Y0 + 13}L{xc} {Y0}L{xc + 6} {Y0 + 13}M{xc - 6} {Y1 - 13}L{xc} {Y1}L{xc + 6} {Y1 - 13}', 650, 'e-acento')
    fig += '<g class="e-sube" style="--d:950ms"><rect class="e-relleno" x="502" y="392" width="108" height="72" rx="4"/><path d="M502 416H610M502 440H610M556 440V464"/></g>'
    fig += '<g class="e-pop" style="--d:1150ms"><circle class="e-relleno" cx="566" cy="214" r="24"/><path d="M566 182V246"/><path class="e-acento" d="M566 192l8 18h-16z"/></g>'
    return tex, fig


def _engrane(cx, cy, ro, ri, dientes, inv=False, t=40):
    pts = []
    for k in range(dientes * 4):
        a = 2 * math.pi * (k + .5) / (dientes * 4)
        rr = ro if k % 4 in (1, 2) else ri
        pts.append(f'{n(cx + rr * math.cos(a))},{n(cy + rr * math.sin(a))}')
    return (f'<g class="v-gira{" e-inv" if inv else ""}" style="transform-origin:{cx}px {cy}px;--t:{t}s"><polygon class="e-relleno" points="{" ".join(pts)}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{n(ri * .42)}"/><circle class="e-tenue" cx="{cx}" cy="{cy}" r="{n(ri * .16)}"/></g>')


def engranes():
    # Engranes que giran sin parar, cada uno a su paso, y una banda con cajas que llegan
    fig = (_engrane(110, 110, 88, 73, 12, t=48) + _engrane(562, 92, 54, 44, 9, True, 30) + _engrane(74, 352, 44, 36, 8, True, 26)
           + _engrane(590, 330, 64, 53, 10, t=40))
    tex = '<path d="M30 522H610M30 562H610"/>' + ''.join(f'<circle cx="{x}" cy="542" r="18"/>' for x in (50, 330, 610))
    for k, (x, w, h) in enumerate([(128, 46, 40), (196, 58, 54), (282, 40, 34), (398, 54, 46), (474, 46, 60)]):
        cls = 'e-desliza e-relleno' + (' e-acento' if k == 3 else '')
        fig += f'<rect class="{cls}" style="--d:{200 + k * 110}ms;--dx:-48px" x="{x}" y="{522 - h}" width="{w}" height="{h}" rx="5"/>'
    return tex, fig


def velocimetro():
    # Tablero de auto: carátula con marcas, avance en turquesa que acelera y desacelera, y carretera que corre bajo el cuadro
    R = 262
    tex = f'<path d="{arco(R, 150, 390)}"/>' + ''.join(f'<path d="{raya(150 + k * 12, R + 7, R + 7 + (22 if k % 5 == 0 else 11))}"/>' for k in range(21))
    tex += '<path d="M146 600L296 452M514 600L364 452"/>'
    fig = f'<path class="e-acento v-medida" pathLength="1" d="{arco(R - 20, 150, 336)}"/>'
    xe, ye = pt(150 + 186 * .9, R - 20)
    fig += (f'<g class="v-aguja" style="transform-origin:{CX}px {CY}px"><circle class="e-acento e-pop e-relleno" style="--d:2050ms" cx="{n(xe)}" cy="{n(ye)}" r="7"/></g>')
    fig += '<path class="e-carril v-fluye" style="--paso:-34;--t:.8s" d="M330 600V462"/>'
    return tex, fig


def costa():
    # Costa de Nayarit: olas que corren, nubes que se mecen, aves y sol en turquesa
    tex = '<path class="e-tenue" d="M0 452H640"/>'
    for k in range(5):
        amp = 6 + k * 1.5
        ola = dib(f'M-104 {476 + k * 24}' + f'q20 {n(-amp)} 40 0t40 0' * 11, 150 + k * 130, 'e-lento')
        tex += f'<g class="v-ola" style="--dx:{"-80px" if k % 2 == 0 else "80px"};--t:{8 + k * 1.3:.1f}s">{ola}</g>'
    fig = ('<g class="v-nube" style="--dx:18px;--t:15s"><path d="M40 286H150a20 20 0 0 0-26-26a28 28 0 0 0-52 4a20 20 0 0 0-32 22z"/></g>'
           '<g class="v-nube" style="--dx:-16px;--t:18s;--d2:2s"><path d="M498 346H604a18 18 0 0 0-22-24a26 26 0 0 0-48 4a18 18 0 0 0-36 20z"/></g>')
    fig += ('<g class="e-sube e-acento" style="--d:500ms;--dy:26px"><circle cx="560" cy="150" r="36"/>'
            + ''.join(f'<path d="{raya(a, 48, 62, 560, 150)}"/>' for a in range(0, 360, 45)) + '</g>')
    fig += '<g class="e-sube" style="--d:900ms"><path d="M84 190q9-8 18 0q9-8 18 0"/><path d="M126 160q7-6 14 0q7-6 14 0"/></g>'
    return tex, fig


def agenda():
    # Agenda de citas: días del mes, palomitas en turquesa y un cursor que va de una cita a otra
    tex, fig = '', ''
    for fila in range(6):
        for col in range(7):
            x, y = 24 + col * 86, 34 + fila * 88
            if not tapado(x, y, x + 70, y + 70):
                tex += f'<rect x="{x}" y="{y}" width="70" height="70" rx="14"/>'
    for k, (fila, col) in enumerate([(0, 1), (1, 6), (3, 0), (5, 2), (4, 6), (5, 5)]):
        x, y = 24 + col * 86, 34 + fila * 88
        fig += dib(f'M{x + 21} {y + 37}l10 10 19-21', 400 + k * 220, 'e-acento')
    paradas = [(1, 0), (3, 1), (4, 0), (1, 6), (2, 6), (4, 6)]
    props = ';'.join(f'--x{k + 1}:{24 + c * 86}px;--y{k + 1}:{34 + f * 88}px' for k, (f, c) in enumerate(paradas))
    fig += f'<rect class="v-extra v-cursor e-acento" style="{props}" x="-5" y="-5" width="80" height="80" rx="17"/>'
    return tex, fig


def taller():
    # Tablero perforado de taller con herramientas colgadas; la tuerca en turquesa se aprieta de sexto en sexto de vuelta
    tex = patron('esc-perfo', 36, 36, f'<circle cx="18" cy="18" r="2.6" fill="{GRIS}" fill-opacity=".3"/>', 6, 12)
    fig = ('<g class="e-sube" style="--d:200ms"><rect class="e-relleno" x="70" y="200" width="36" height="96" rx="12"/>'
           '<path d="M80 220v56M88 220v56M96 220v56"/><path d="M88 296v118"/><path class="e-relleno" d="M81 414h14l-3 24h-8z"/></g>')
    fig += ('<g class="e-sube" style="--d:350ms"><rect class="e-relleno" x="566" y="236" width="16" height="200" rx="7"/>'
            '<path class="e-relleno" d="M528 196h86a8 8 0 0 1 8 8v24a8 8 0 0 1-8 8h-86l-14-12v-16z"/></g>')
    hexa = ' '.join(f'{n(pt(a, 28, 100, 140)[0])},{n(pt(a, 28, 100, 140)[1])}' for a in range(0, 360, 60))
    fig += f'<g class="v-trinquete e-acento" style="transform-origin:100px 140px"><polygon class="e-relleno" points="{hexa}"/><circle cx="100" cy="140" r="11"/></g>'
    fig += ('<g class="e-sube" style="--d:500ms"><rect class="e-relleno" x="520" y="486" width="84" height="76" rx="18"/><circle cx="562" cy="524" r="14"/>'
            '<path d="M520 548H436M448 548v-8M460 548v-8M472 548v-12M484 548v-8M496 548v-8M508 548v-12"/></g>')
    fig += '<g class="e-sube" style="--d:650ms"><circle class="e-relleno" cx="596" cy="96" r="10"/><path d="M590 102l12-12"/><circle class="e-relleno" cx="150" cy="530" r="10"/><path d="M144 536l12-12"/></g>'
    return tex, fig


def surcos():
    # Campo: surcos que nacen debajo del cuadro, lomas, sol en turquesa que brilla y una planta
    hy = 230
    tex = f'<path d="M0 {hy}H640"/><path class="e-tenue" d="M0 {hy}Q86 192 176 {hy}M462 {hy}Q550 200 640 {hy - 4}"/>'
    tex += ''.join(f'<path class="e-tenue" d="M0 {y}H640"/>' for y in (292, 362, 456, 560))
    tex += ''.join(dib(f'M{CX} {hy}L{CX + k * 96} 600', 150 + abs(k) * 90) for k in range(-7, 8))
    fig = (f'<g class="e-sube e-acento" style="--d:600ms;--dy:22px"><path d="M526 {hy}a40 40 0 0 1 80 0"/>'
           f'<g class="v-respira" style="transform-origin:566px {hy}px">' + ''.join(f'<path d="{raya(a, 52, 66, 566, hy)}"/>' for a in (195, 225, 255, 285, 315, 345)) + '</g></g>')
    fig += '<g class="e-sube" style="--d:1200ms"><path d="M96 572v-30"/><path class="e-relleno" d="M96 552c0-11 8-18 19-18 0 11-8 18-19 18zM96 558c0-9-7-14-15-14 0 9 7 14 15 14z"/></g>'
    return tex, fig


def _escudo(s):
    w, h = 420 * s, 480 * s
    x0, y0 = CX - w / 2, CY - h / 2
    return (f'M{n(CX)} {n(y0)}L{n(x0 + w)} {n(y0 + h * .15)}V{n(y0 + h * .5)}C{n(x0 + w)} {n(y0 + h * .8)} {n(CX + w * .2)} {n(y0 + h * .95)} {n(CX)} {n(y0 + h)}'
            f'C{n(CX - w * .2)} {n(y0 + h * .95)} {n(x0)} {n(y0 + h * .8)} {n(x0)} {n(y0 + h * .5)}V{n(y0 + h * .15)}Z')


def escudos():
    # Escudos alrededor del cuadro (seguridad), destellos en turquesa que titilan y burbujas que suben (limpieza)
    tex = f'<path d="{_escudo(1.06)}"/><path class="e-tenue" d="{_escudo(.84)}"/>'
    fig = ''
    for k, (x, y, s) in enumerate([(82, 96, 20), (582, 150, 26), (100, 470, 15), (556, 520, 19), (530, 300, 11)]):
        fig += (f'<g class="v-destello" style="--t:{2.8 + k * .45:.2f}s;--d2:{2.6 + k * .7:.1f}s"><path class="e-acento e-pop" style="--d:{400 + k * 260}ms" '
                f'd="M{x} {y - s}Q{x} {y} {x + s} {y}Q{x} {y} {x} {y + s}Q{x} {y} {x - s} {y}Q{x} {y} {x} {y - s}z"/></g>')
    for k, (x, y, r) in enumerate([(70, 300, 14), (126, 250, 8), (44, 230, 6), (600, 420, 12), (566, 376, 7), (150, 560, 9)]):
        fig += (f'<g class="v-burbuja" style="--t:{5.5 + k * .6:.1f}s;--d2:{2.6 + k * .9:.1f}s"><circle class="e-sube" style="--d:{300 + k * 150}ms;--dy:30px" '
                f'cx="{x}" cy="{y}" r="{r}"/></g>')
    return tex, fig


def reticula():
    # Orden: casilleros con etiqueta; los de turquesa ya están en su lugar, uno llega a su sitio y una ronda los revisa uno por uno
    tex, fig = '', ''
    teal = {(0, 1), (1, 3), (2, 0), (3, 2)}
    for fila in range(4):
        for col in range(4):
            x, y = 46 + col * 148, 16 + fila * 148
            if tapado(x, y, x + 124, y + 124):
                continue
            ms = 150 + (fila + col) * 120
            celda = f'<rect class="e-relleno" x="{x}" y="{y}" width="124" height="124" rx="18"/><path d="M{x + 22} {y + 98}h44"/>'
            if (fila, col) == (3, 2):
                fig += f'<g class="e-desliza e-acento" style="--d:900ms;--dx:44px;--dy:40px">{celda}</g>'
            elif (fila, col) in teal:
                fig += f'<g class="e-sube e-acento" style="--d:{ms}ms">{celda}</g>'
            else:
                tex += f'<g class="e-sube" style="--d:{ms}ms">{celda}</g>'
    ronda = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0), (2, 0), (1, 0)]
    fig += ''.join(f'<rect class="v-extra v-ronda e-acento" style="--d2:{2.4 + k:.1f}s" x="{46 + c * 148}" y="{16 + f * 148}" width="124" height="124" rx="18"/>'
                   for k, (f, c) in enumerate(ronda))
    return tex, fig


def radar():
    # Visibilidad: radar que barre sin parar; en la primera vuelta descubre los puntos en turquesa
    tex = ''.join(f'<circle cx="{CX}" cy="{CY}" r="{r}"/>' for r in (186, 252, 318))
    tex += f'<path class="e-tenue" d="M{CX - 330} {CY}H{CX + 330}M{CX} {CY - 320}V{CY + 320}"/>'
    tex += ''.join(f'<path class="e-tenue" d="{raya(a, 318, 318 - (12 if a % 30 == 0 else 6))}"/>' for a in range(0, 360, 10))
    a0, vuelta = -38, 6000
    x, y = pt(a0, 318)
    xc, yc = pt(a0 - 30, 318)
    fig = (f'<g class="e-barrido" style="transform-origin:{CX}px {CY}px"><path class="e-cono" d="M{CX} {CY}L{n(xc)} {n(yc)}A318 318 0 0 1 {n(x)} {n(y)}Z"/>'
           f'<path class="e-acento" d="M{CX} {CY}L{n(x)} {n(y)}"/></g>')
    for (x, y) in [(160, 128), (528, 430), (470, 92), (122, 486), (566, 236)]:
        ang = (math.degrees(math.atan2(y - CY, x - CX)) - a0) % 360
        fig += f'<circle class="e-acento e-pop e-relleno" style="--d:{int(vuelta * ang / 360)}ms" cx="{x}" cy="{y}" r="6"/>'
    return tex, fig


def cuadre():
    # Control: libro de cuentas con conceptos, importes, palomitas que se vuelven a revisar una por una y doble raya del total
    r = random.Random('cuadre')
    tex, fig, k = '', '', 0
    filas = list(range(40, 576, 38))
    tex += ''.join(f'<path class="e-tenue" d="M18 {y}H622"/>' for y in filas)
    tex += '<path d="M78 14V586M546 14V586M552 14V586"/>'
    for i, y in enumerate(filas):
        ty = y - 13
        fuera = ty < Y0 - 6 or ty > Y1 + 6
        L = r.choice((180, 230, 290, 340)) if fuera else r.choice((44, 58, 72))
        tex += f'<path d="M92 {ty}h{L}"/>'
        a = r.choice((22, 34, 46))
        tex += f'<path d="M{612 - a} {ty}H612"/>'
        if i % 2 == 0:
            fig += dib(f'M34 {ty - 1}l7 7 13-14', 300 + k * 170, 'e-acento v-palomea').replace('style="', f'style="--d2:{3 + k}s;', 1)
            k += 1
    fig += dib('M562 566H612M562 572H612', 300 + k * 170 + 150, 'e-acento')
    return tex, fig


def tendencia():
    # Mejora continua: línea de avance que sube detrás del cuadro; un pulso la recorre y el último Delta, en turquesa, late al llegar
    tex = ''.join(f'<path class="e-tenue" d="M0 {y}H640"/>' for y in (118, 198, 278, 358, 438, 518))
    pts = [(14, 512), (58, 476), (98, 490), (142, 440), (172, 452), (250, 380), (330, 340), (410, 300), (488, 262), (520, 272), (560, 214), (594, 226), (624, 168)]
    largos = [0]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        largos.append(largos[-1] + math.hypot(xb - xa, yb - ya))
    linea = 'M' + 'L'.join(f'{x} {y}' for x, y in pts)
    tex += dib(linea, 150, 'e-lento')
    tex += f'<path class="v-extra v-viaje e-acento" pathLength="1" style="--l:.1;--t:5s;--d2:2.6s" d="{linea}"/>'
    fig = dib('M{} {}L{} {}L{} {}'.format(*pts[-3], *pts[-2], *pts[-1]), 1500, 'e-acento')
    for k, (x, y) in enumerate(pts):
        if k in (0, 4) or X0 - 8 < x < X1 + 8:
            continue
        ms = 150 + int(1500 * largos[k] / largos[-1])
        if k == len(pts) - 1:
            fig += (f'<g class="v-latido" style="--d2:2.6s"><path class="e-acento e-pop e-relleno" style="--d:{ms + 250}ms" '
                    f'd="{_redondo(_tri(x, y, 14, 0), .22)}"/></g>')
        else:
            fig += f'<path class="e-pop e-relleno" style="--d:{ms}ms;stroke-opacity:.6" d="{_redondo(_tri(x, y, 9, 0), .25)}"/>'
    return tex, fig


def ajustes():
    # Herramientas adaptadas: controles deslizantes que se siguen ajustando a su negocio
    tex, fig = '', ''
    pos = [126, 418, 246, 74, 522, 98, 538, 64, 334, 184, 462]
    for k, y in enumerate(pos):
        x = 40 + 56 * k
        tex += f'<path d="M{x} 24V576"/>'
        cls = 'e-relleno e-desliza' + (' e-acento' if k in (2, 9) else '')
        a = (14 + (k * 7) % 9) * (1 if k % 2 == 0 else -1)
        fig += (f'<g class="v-ajuste" style="--a:{a}px;--t:{6 + (k * 5) % 4:.0f}s;--d2:{2.2 + k * .25:.2f}s">'
                f'<circle class="{cls}" style="--d:{150 + k * 90}ms;--dy:{CY - y}px" cx="{x}" cy="{y}" r="13"/></g>')
    return tex, fig


def diagrama():
    # Métodos: diagrama de flujo que rodea al cuadro, flechas en turquesa y un punto que recorre el proceso sin parar
    cajas = [(40, 40), (252, 40), (464, 40), (464, 496), (252, 496), (40, 496), (40, 268)]
    fig = ''.join(f'<rect class="e-relleno" x="{x}" y="{y}" width="136" height="64" rx="12"/><path class="e-tenue" d="M{x + 22} {y + 32}h{50 + (k % 3) * 14}"/>'
                  for k, (x, y) in enumerate(cajas))
    fig += '<path class="e-relleno" d="M532 254l46 46-46 46-46-46z"/>'
    flechas = ['M176 72H248M240 66l8 6-8 6', 'M388 72H460M452 66l8 6-8 6', 'M532 104V248M526 240l6 8 6-8', 'M532 346V490M526 482l6 8 6-8',
               'M464 528H392M400 522l-8 6 8 6', 'M252 528H180M188 522l-8 6 8 6', 'M108 496V336M102 344l6-8 6 8', 'M108 268V108M102 116l6-8 6 8']
    fig += ''.join(dib(d, 300 + k * 210, 'e-acento') for k, d in enumerate(flechas))
    fig += '<path class="v-extra v-punto e-acento" pathLength="1" style="--t:16s" d="M108 72H532V528H108Z"/>'
    return '', fig


def arcos():
    # Marketing digital: ondas que se difunden una tras otra, barras que crecen y mensajes que llegan
    tex = ''.join(f'<path class="e-onda v-difunde" style="--d:{150 + k * 130}ms;--d2:{2.4 + k * .22:.2f}s" d="M24 {576 - (58 + k * 64)}A{58 + k * 64} {58 + k * 64} 0 0 1 {24 + 58 + k * 64} 576"/>'
                  for k in range(1, 8))
    fig = ''.join(f'<rect class="e-acento e-sube" style="--d:{500 + k * 160}ms" x="{500 + k * 30}" y="{566 - h}" width="20" height="{h}" rx="5"/>'
                  for k, h in enumerate((56, 92, 132, 178)))
    fig += ('<g class="e-pop" style="--d:900ms"><path class="e-relleno" d="M486 44h108a16 16 0 0 1 16 16v28a16 16 0 0 1-16 16h-64l-18 16v-16h-26a16 16 0 0 1-16-16V60a16 16 0 0 1 16-16z"/>'
            '<path d="M506 68h66M506 82h40"/></g>'
            '<g class="e-pop e-acento" style="--d:1250ms"><path class="e-relleno" d="M540 132h64a14 14 0 0 1 14 14v18a14 14 0 0 1-14 14h-12v14l-16-14h-36a14 14 0 0 1-14-14v-18a14 14 0 0 1 14-14z"/>'
            '<path d="M552 155h40"/></g>')
    return tex, fig


def circuito():
    # IA: el cuadro es el chip; pistas de circuito salen de sus cuatro lados y por ellas corren pulsos de datos sin parar
    r = random.Random('circuito')
    tex = patron('esc-puntos', 24, 24, f'<circle cx="12" cy="12" r="1.3" fill="{GRIS}" fill-opacity=".24"/>', 6, 0)
    lados = {'arriba': ((0, -1), (1, 0), Y0), 'derecha': ((1, 0), (0, 1), W - X1), 'abajo': ((0, 1), (-1, 0), H - Y1), 'izquierda': ((-1, 0), (0, -1), X0)}
    fig, pulsos, datos, k = '', '', '', 0
    for lado, ((ox, oy), (ax, ay), libre) in lados.items():
        for o in (-110, -66, -22, 22, 66, 110):
            if r.random() < .18:
                continue
            ex, ey = (CX, Y0) if lado == 'arriba' else (X1, CY) if lado == 'derecha' else (CX, Y1) if lado == 'abajo' else (X0, CY)
            sx, sy = ex + ax * o - ox * 12, ey + ay * o - oy * 12
            a, b = r.choice((22, 30, 38)), r.choice((0, 22, 36, 52))
            c = max(18, min(r.choice((30, 50, 70, 90)), libre - 30 - a - b))
            sg = (o > 0) - (o < 0) or 1
            p1 = (sx + ox * (a + 12), sy + oy * (a + 12))
            p2 = (p1[0] + ox * b + ax * sg * b, p1[1] + oy * b + ay * sg * b)
            p3 = (p2[0] + ox * c, p2[1] + oy * c)
            d = f'M{n(sx)} {n(sy)}L{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}L{n(p3[0])} {n(p3[1])}'
            fig += f'<path d="{d}"/><circle class="e-relleno" cx="{n(p3[0])}" cy="{n(p3[1])}" r="6.5"/>'
            ritmo = f'--t:{3.6 + (k * 7) % 5 * .5:.1f}s;--d2:{2.2 + (k * 11) % 13 * .37:.2f}s'
            if k % 3 == 0:
                ms = 300 + (k // 3) * 260
                pulsos += dib(d, ms, 'e-acento')
                pulsos += f'<circle class="e-acento e-pop e-relleno" style="--d:{ms + 1100}ms" cx="{n(p3[0])}" cy="{n(p3[1])}" r="6.5"/>'
                datos += f'<path class="v-extra v-viaje v-claro" pathLength="1" style="{ritmo}" d="{d}"/>'
            elif k % 2:
                datos += f'<path class="v-extra v-viaje e-acento" pathLength="1" style="{ritmo}" d="{d}"/>'
            k += 1
    return tex, fig + pulsos + datos


def regla():
    # Nosotros: medimos antes de proponer. Dos escuadras con regla en esquinas opuestas del cuadro, marcas en turquesa
    # en sus orillas, dos marcas que miden sin parar y papel de ingeniería de fondo
    tex = patron('esc-cruces', 40, 40, f'<path d="M20 15v10M15 20h10" fill="none" stroke="{GRIS}" stroke-opacity=".22" stroke-width="1.2"/>', X0 - 20, Y0 - 20)
    fig = dib('M110 86H420V110H134V380H110Z', 150, 'e-lento e-relleno') + dib('M550 514H240V490H526V220H550Z', 450, 'e-lento e-relleno')
    marcas = ''
    for v in range(140, 420, 10):
        marcas += f'M{v} 110v-{12 if (v - X0) % 50 == 0 else 6}'
    for v in range(116, 380, 10):
        marcas += f'M134 {v}h-{12 if (v - Y0) % 50 == 0 else 6}'
    for v in range(250, 526, 10):
        marcas += f'M{v} 490v{12 if (X1 - v) % 50 == 0 else 6}'
    for v in range(226, 490, 10):
        marcas += f'M526 {v}h{12 if (Y1 - v) % 50 == 0 else 6}'
    fig += f'<path class="e-sube" style="--d:1000ms" d="{marcas}"/>'
    fig += (f'<path class="e-tenue e-guia e-sube" style="--d:1250ms" d="M{X0} 124V{Y0 - 6}M148 {Y0}H{X0 - 6}M{X1} 476V{Y1 + 6}M512 {Y1}H{X1 + 6}"/>')
    fig += (f'<path class="e-acento e-pop e-relleno" style="--d:1400ms" d="M{X0 - 6} 113h12l-6 9zM137 {Y0 - 6}v12l9-6zM{X1 - 6} 487h12l-6-9zM523 {Y1 - 6}v12l-9-6z"/>')
    fig += (f'<path class="v-extra v-mide-x e-acento e-relleno" d="M{X0 - 6} 113h12l-6 9z"/>'
            f'<path class="v-extra v-mide-y e-acento e-relleno" d="M523 {Y1 - 6}v12l-9-6z"/>')
    return tex, fig


FONDOS = {f.__name__: f for f in (mesa, estantes, rutas, plano, engranes, velocimetro, costa, agenda, taller, surcos, escudos,
                                  reticula, radar, cuadre, tendencia, ajustes, diagrama, arcos, circuito, regla)}


# ---------- Emblema ----------
def _a_trazos(svg):
    """Convierte rect y circle en path para que pathLength (el dibujo al cargar) funcione igual en todos los navegadores."""
    def attrs(m):
        return {k: float(v) for k, v in re.findall(r'([\w-]+)="([^"]*)"', m.group(0)) if k in ('x', 'y', 'width', 'height', 'rx', 'cx', 'cy', 'r')}

    def rect(m):
        a = attrs(m)
        x, y, w, h, r = a['x'], a['y'], a['width'], a['height'], a.get('rx', 0)
        if not r:
            return f'<path d="M{n(x)} {n(y)}h{n(w)}v{n(h)}h{n(-w)}z"/>'
        return (f'<path d="M{x + r:g} {y:g}H{x + w - r:g}A{r:g} {r:g} 0 0 1 {x + w:g} {y + r:g}V{y + h - r:g}A{r:g} {r:g} 0 0 1 {x + w - r:g} {y + h:g}'
                f'H{x + r:g}A{r:g} {r:g} 0 0 1 {x:g} {y + h - r:g}V{y + r:g}A{r:g} {r:g} 0 0 1 {x + r:g} {y:g}z"/>')

    def circ(m):
        a = attrs(m)
        cx, cy, r = a['cx'], a['cy'], a['r']
        return f'<path d="M{cx - r:g} {cy:g}a{r:g} {r:g} 0 1 0 {2 * r:g} 0a{r:g} {r:g} 0 1 0 {-2 * r:g} 0"/>'

    return re.sub(r'<circle\b[^>]*/>', circ, re.sub(r'<rect\b[^>]*/>', rect, svg))


def figura(nombre):
    base, acento_ = EMBLEMAS[nombre]
    trazos = re.findall(r'<path\b[^>]*/>', _a_trazos(base))
    trazos += [t.replace('<path', '<path class="e-acento"', 1) for t in re.findall(r'<path\b[^>]*/>', _a_trazos(acento_))]
    cuerpo = ''.join(t.replace('<path', f'<path pathLength="1" style="--d:{k * 110}ms"', 1) for k, t in enumerate(trazos))
    escala = (LADO - 110) / 24
    return f'<g class="e-figura" transform="translate({X0 + 55} {Y0 + 55}) scale({escala:.4f})">{cuerpo}</g>'


def escena(slug):
    """SVG completo del encabezado de la página `slug`, o None si no tiene tema."""
    if slug not in TEMAS:
        return None
    fondo, emblema, _ = TEMAS[slug]
    textura, figuras = FONDOS[fondo]()
    if emblema == 'delta':
        w = LADO - 124
        h = w * 133 / 175
        fig = (f'<g class="e-sube" style="--d:250ms"><svg x="{X0 + (LADO - w) / 2:g}" y="{n(Y0 + (LADO - h) / 2)}" width="{w}" height="{n(h)}" viewBox="0 0 175 133">'
               '<use href="#mark"/></svg></g>')
    else:
        fig = figura(emblema)
    return (f'<svg class="escena e-{fondo}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            '<defs><radialGradient id="esc-desv" r="60%"><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="esc-mascara" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#esc-desv)"/></mask></defs>'
            f'<g class="e-fondo"><g mask="url(#esc-mascara)">{textura}</g>{figuras}</g>'
            f'<rect class="e-marco" x="{X0}" y="{Y0}" width="{LADO}" height="{LADO}" rx="{RADIO}"/>{fig}</svg>')


def acento(slug, titulo):
    """Titular partido alrededor de la palabra en turquesa: (antes, palabra, después), o None."""
    palabra = TEMAS.get(slug, (None, None, None))[2]
    if not palabra or palabra not in titulo:
        return None
    a, b = titulo.split(palabra, 1)
    return a, palabra, b


def icono(emblema, clase='otros-ico'):
    """Emblema pequeño en línea (cuadrícula de 24), con su trazo en turquesa aparte."""
    if emblema not in EMBLEMAS:
        return ''
    base, acento_ = EMBLEMAS[emblema]
    extra = f'<g class="ico-a">{acento_}</g>' if acento_ else ''
    return f'<svg class="{clase}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{base}{extra}</svg>'


def icono_chip(slug, clase='otros-ico'):
    """Emblema de la página `slug` para los enlaces «Otras industrias», «Otras soluciones» y la cinta de giros."""
    return icono(TEMAS.get(slug, (None, None, None))[1], clase)
