# Genera las páginas estáticas del sitio (GitHub Pages, sin compilación en el servidor).
# Uso: python _fuente/construir.py   → reescribe index.html, catalogo.html, servicios.html, nosotros.html,
#      industrias/*.html, soluciones/*.html y sitemap.xml. La carpeta _fuente no se publica.
import json, math, os
from html import escape as esc
from urllib.parse import quote
from contenido import WA_NUM, TEL, PIEZA, PILAR_NOMBRE, INDUSTRIAS, SOLUCIONES, CATALOGO, HORAS_ESCALA

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = 'https://keyacuevaca-dot.github.io/certeza-operativa/'
ANIO = 2026


def wa(msg):
    return f'https://wa.me/{WA_NUM}?text={quote(msg)}'


WA_PRO = wa('Hola, quiero platicar con Certeza Operativa sobre mi negocio.')
WA_PLATICA = wa('Hola, quiero agendar una plática de 15 minutos sin costo para mi negocio.')

# ---------- Silueta propia: el Delta que se forma con líneas (mejora continua) ----------
def _tri(cx, cy, s, rot):
    return [(cx + s * math.cos(math.radians(-90 + 120 * k + rot)), cy + s * math.sin(math.radians(-90 + 120 * k + rot))) for k in range(3)]


def _redondo(pts, r):
    d = ''
    for i in range(3):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % 3]
        a = (p1[0] + (p0[0] - p1[0]) * r, p1[1] + (p0[1] - p1[1]) * r)
        b = (p1[0] + (p2[0] - p1[0]) * r, p1[1] + (p2[1] - p1[1]) * r)
        d += ('M' if i == 0 else 'L') + f'{a[0]:.1f} {a[1]:.1f}Q{p1[0]:.1f} {p1[1]:.1f} {b[0]:.1f} {b[1]:.1f}'
    return d + 'Z'


def lineart(n=34, giro=-46, dx=190, dy=170, x0=230, y0=410, s0=170, flecha=False):
    ease = lambda t: t * t * (3 - 2 * t)
    centro = lambda t: (x0 + dx * ease(t) + 30 * math.sin(t * math.pi), y0 - dy * ease(t) - 40 * math.sin(t * math.pi))
    out = []
    for i in range(n):
        t = i / (n - 1); e = ease(t)
        cx, cy = centro(t)
        out.append(f'<path d="{_redondo(_tri(cx, cy, s0 + 60 * math.sin(t * math.pi), giro * (1 - e)), .34 - .30 * e)}" stroke-opacity="{.10 + .62 * t ** 1.3:.2f}"/>')
    svg = '<g>' + ''.join(out) + '</g>'
    if flecha:
        # flecha simple de mejora continua: pasa por debajo del Delta final y sale hacia arriba a la derecha
        cx, cy = centro(1); q = s0
        P0, P1, P2, P3 = (cx - .95 * q, cy + .95 * q), (cx + .05 * q, cy + 1.0 * q), (cx + .70 * q, cy + .45 * q), (cx + .92 * q, cy - .15 * q)
        ang = math.atan2(P3[1] - P2[1], P3[0] - P2[0])
        h = [(P3[0] - 18 * math.cos(ang + a), P3[1] - 18 * math.sin(ang + a)) for a in (.5, -.5)]
        svg += (f'<path class="flecha" d="M{P0[0]:.0f} {P0[1]:.0f}C{P1[0]:.0f} {P1[1]:.0f} {P2[0]:.0f} {P2[1]:.0f} {P3[0]:.0f} {P3[1]:.0f}'
                f'M{h[0][0]:.0f} {h[0][1]:.0f}L{P3[0]:.0f} {P3[1]:.0f} {h[1][0]:.0f} {h[1][1]:.0f}"/>')
    return svg


# ---------- Piezas compartidas ----------
def sprite():
    return '''<svg class="sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
  <symbol id="mark" viewBox="38 8 175 133"><path fill="currentColor" d="M125.5 12.5 165.2 72H138.5L125.5 52.5 82.8 116.5H194.9L208.5 137H42.5Z"/><path fill="currentColor" d="M140.2 74.6H166.9L173.3 84.2H146.6ZM148.1 86.8H174.8L181.2 96.4H154.5Z"/></symbol>
  <symbol id="certeza" viewBox="0 0 433.6 72.8"><path fill="currentColor" d="M66 42.2L66.8 42.2L67 58.9Q64.7 62.8 60.9 66.0Q57.1 69.1 51.7 71.0Q46.2 72.8 38.9 72.8L38.9 72.8Q27.3 72.7 18.5 68.3Q9.7 63.9 4.9 55.8Q0 47.6 0 36.3L0 36.3Q0 25.2 4.8 17.1Q9.6 8.9 18.4 4.5Q27.2 0 39.3 0L39.3 0Q47.1 0 53.3 1.8Q59.5 3.5 63.8 5.9L63.8 5.9L64.6 22L63.7 22Q61.2 12.5 54.9 8.2Q48.5 3.8 40 3.8L40 3.8Q31.8 3.8 25.9 7.8Q19.9 11.7 16.7 19.0Q13.4 26.2 13.4 36.1L13.4 36.1Q13.4 46 16.6 53.4Q19.7 60.7 25.5 64.8Q31.2 68.8 38.9 69L38.9 69Q46.4 69 52.0 66.5Q57.5 63.9 61.0 58Q64.6 52.1 66 42.2L66 42.2ZM124.8 54.4L125.7 54.4L121.3 71.4L76.4 71.4L76.4 70.4L77.7 70.4Q80.0 70.4 81.6 68.9Q83.2 67.3 83.3 65.1L83.3 65.1L83.3 17.7Q83.2 15.4 81.6 13.9Q80.0 12.4 77.7 12.4L77.7 12.4L76.4 12.4L76.4 11.4L109.5 11.4Q112.4 11.4 115.7 10.9Q119.0 10.3 120.3 9.8L120.3 9.8L120.3 24.2L119.2 24.2L119.2 23.1Q119.2 19.5 117.2 17.3Q115.2 15.1 111.5 15.1L111.5 15.1L95.0 15.1L95.0 39.7L108.2 39.7Q111.3 39.7 113.0 37.8Q114.7 35.9 114.7 33.1L114.7 33.1L114.7 32.2L115.7 32.2L115.7 51L114.7 51L114.7 50.1Q114.7 47.3 113.0 45.4Q111.3 43.5 108.2 43.4L108.2 43.4L95.0 43.4L95.0 67.7L107.9 67.7Q112.5 67.7 115.8 66.1Q119.0 64.4 121.2 61.4Q123.4 58.4 124.8 54.4L124.8 54.4ZM157.3 71.4L138.7 71.4L132.1 71.4L132.1 70.4L133.3 70.4Q135.6 70.4 137.2 68.8L137.2 68.8Q138.5 67.5 138.7 65.8L138.7 65.8L138.7 16.9Q138.5 15.1 137.2 13.9L137.2 13.9Q135.6 12.4 133.4 12.4L133.4 12.4L132.1 12.4L132.1 11.4L160.9 11.4Q165.3 11.4 169.2 12.3Q173.0 13.2 176.0 15.2Q178.9 17.1 180.6 20.2Q182.2 23.3 182.2 27.7L182.2 27.7Q182.2 31.4 180.6 35.0Q179.0 38.5 175.8 41.0Q172.6 43.4 167.8 44L167.8 44Q170.3 44.8 172.9 47.4Q175.4 50 176.8 52.3L176.8 52.3Q177.1 52.8 178.3 54.6Q179.4 56.3 181.1 58.7Q182.8 61 184.6 63.3L184.6 63.3Q186.6 65.9 188.2 67.5Q189.8 69 191.6 69.7Q193.3 70.4 195.5 70.4L195.5 70.4L195.5 71.4L188.9 71.4Q183.5 71.4 179.8 70.4Q176.1 69.4 173.6 67.3Q171.0 65.2 168.9 62.1L168.9 62.1Q168.2 61 167.1 59.1Q165.9 57.2 164.7 55.2Q163.5 53.1 162.5 51.3Q161.5 49.4 161.2 48.4L161.2 48.4Q159.7 45.4 157.7 43.8Q155.7 42.2 153.8 42.1L153.8 42.1L153.8 41.2Q153.9 41.2 154.9 41.3Q155.9 41.3 157.4 41.2L157.4 41.2Q159.7 41.1 162.1 40.5Q164.4 39.9 166.3 37.9Q168.2 35.9 169.2 31.7L169.2 31.7Q169.5 30.9 169.7 29.7Q169.8 28.5 169.7 27L169.7 27Q169.6 23.6 168.5 21.4Q167.4 19.1 165.7 17.8Q164.0 16.5 162.0 15.9Q160.0 15.3 158.2 15.2L158.2 15.2Q155.3 15.1 153.1 15.2L153.1 15.2Q151.2 15.2 150.5 15.2L150.5 15.2L150.5 65.1Q150.6 67.4 152.3 68.9Q154.0 70.4 156.1 70.4L156.1 70.4L157.2 70.4L157.3 71.4ZM248.3 9.7L248.3 9.7L248.3 24.1L247.2 24.1L247.2 22.9Q247.3 19.4 245.3 17.3Q243.2 15.1 239.5 15L239.5 15L225.8 15L225.8 65.1Q225.8 67.3 227.5 68.9Q229.1 70.4 231.4 70.4L231.4 70.4L232.4 70.4L232.4 71.4L207.2 71.4L207.2 70.4L208.3 70.4Q210.6 70.4 212.2 68.9Q213.8 67.3 213.9 65.1L213.9 65.1L213.9 15L200.2 15Q196.5 15.1 194.5 17.3Q192.4 19.4 192.4 22.9L192.4 22.9L192.4 24.1L191.4 24.1L191.4 9.7Q192.2 10 194.0 10.4Q195.8 10.8 198.0 11.1Q200.2 11.3 202.1 11.3L202.1 11.3L237.5 11.3Q239.5 11.3 241.7 11.1Q243.9 10.8 245.8 10.4Q247.6 10 248.3 9.7ZM302.5 54.4L303.4 54.4L299 71.4L254.1 71.4L254.1 70.4L255.4 70.4Q257.7 70.4 259.3 68.9Q260.9 67.3 261 65.1L261 65.1L261 17.7Q260.9 15.4 259.3 13.9Q257.7 12.4 255.4 12.4L255.4 12.4L254.1 12.4L254.1 11.4L287.2 11.4Q290.1 11.4 293.4 10.9Q296.7 10.3 298 9.8L298 9.8L298 24.2L296.9 24.2L296.9 23.1Q296.9 19.5 294.9 17.3Q292.9 15.1 289.2 15.1L289.2 15.1L272.7 15.1L272.7 39.7L285.9 39.7Q289 39.7 290.7 37.8Q292.4 35.9 292.4 33.1L292.4 33.1L292.4 32.2L293.4 32.2L293.4 51L292.4 51L292.4 50.1Q292.4 47.3 290.7 45.4Q289 43.5 285.9 43.4L285.9 43.4L272.7 43.4L272.7 67.7L285.6 67.7Q290.2 67.7 293.5 66.1Q296.7 64.4 298.9 61.4Q301.1 58.4 302.5 54.4L302.5 54.4ZM360.1 10.1L360.1 10.1L360.1 10.9L325.8 67.8L346.4 67.8Q351.1 67.7 354.4 66.1Q357.7 64.5 360 61.5Q362.3 58.5 363.7 54.4L363.7 54.4L364.7 54.4L360 71.4L309.8 71.4L309.8 70.5L344.2 14.9L320.1 14.9Q316.4 15 314.4 17.2Q312.3 19.4 312.3 23L312.3 23L312.3 24.1L311.2 24.1L311.2 9.7Q312.1 10 313.9 10.4Q315.8 10.7 318.1 11.0Q320.3 11.2 322.2 11.3L322.2 11.3L349.5 11.3Q351.5 11.3 353.8 11.1Q356 10.9 357.8 10.6Q359.5 10.3 360.1 10.1ZM398.1 9.1L399 9.1L425 64.6L425 64.6Q426.4 67.7 428.6 69.1Q430.8 70.4 432.8 70.4L432.8 70.4L433.6 70.4L433.6 71.4L407.2 71.4L407.2 70.4L408 70.4Q409.7 70.4 411.1 68.9L411.1 68.9Q412.4 67.4 411.4 64.7L411.4 64.7L407 54.2L384.5 54.2L379.9 64.8Q378.9 67.4 380.3 68.9L380.3 68.9Q381.7 70.4 383.4 70.4L383.4 70.4L384.2 70.4L384.2 71.4L364.5 71.4L364.5 70.4L365.3 70.4Q367.4 70.4 369.6 69.1L369.6 69.1Q371.5 67.9 372.9 65.3L372.9 65.3L393.7 20.6Q393.8 20.2 394.4 18.8Q395.1 17.4 395.9 15.5Q396.7 13.6 397.4 11.9Q398 10.1 398.1 9.1L398.1 9.1ZM395.8 27.6L386 50.6L405.5 50.6L395.8 27.6Z"/></symbol>
  <symbol id="s-ig" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle fill="currentColor" stroke="none" cx="17.3" cy="6.7" r="1.2"/></symbol>
  <symbol id="s-fb" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path fill="currentColor" stroke="none" d="M13.1 19.5v-6.6h2.3l.4-2.6h-2.7V8.7c0-.8.3-1.3 1.4-1.3h1.4V5.2c-.3 0-1.1-.1-2.1-.1-2.1 0-3.4 1.3-3.4 3.5v1.7H8.1v2.6h2.3v6.6z"/></symbol>
  <symbol id="s-wa" viewBox="0 0 24 24"><path d="M12 2.8a9.2 9.2 0 0 0-7.9 13.9L2.8 21.2l4.6-1.2A9.2 9.2 0 1 0 12 2.8z"/><path fill="currentColor" stroke="none" d="M9.2 7.6c-.5.5-.9 1.5.1 3.1 1.1 1.8 3 3.3 4.9 3.9 1 .3 1.7-.2 1.9-.8l.1-.7-1.5-.8-.7.6c-1-.3-2.3-1.5-2.7-2.6l.6-.7-.7-1.6-.8-.4z"/></symbol>
  <symbol id="s-tel" viewBox="0 0 24 24"><path fill="currentColor" stroke="none" d="M6.6 3.6h2.8l1.2 3.9-2 1.4c1 2.2 2.8 4 5 5l1.4-2 3.9 1.2v2.8c0 1.6-1.3 2.9-2.9 2.9C9.6 18.5 4.6 13.5 4.3 7.1c0-1.6.7-3.5 2.3-3.5z"/></symbol>
</svg>'''


SOC = [('https://www.instagram.com/certezaoperativa/', 'Instagram de Certeza Operativa', 's-ig'),
       ('https://www.facebook.com/profile.php?id=61594375394266', 'Facebook de Certeza Operativa', 's-fb')]


def social(extra=False):
    items = list(SOC)
    if extra:
        items += [(wa('Hola, quiero informes de Certeza Operativa.'), f'WhatsApp: {TEL}', 's-wa'), ('tel:+523114469363', f'Llamar al {TEL}', 's-tel')]
    lis = ''.join(f'<li><a href="{esc(h)}"{" target=\"_blank\" rel=\"noopener\"" if h.startswith("http") else ""} aria-label="{esc(l)}" title="{esc(l.split(" de ")[0].split(":")[0])}"><svg viewBox="0 0 24 24" aria-hidden="true"><use href="#{i}"/></svg></a></li>' for h, l, i in items)
    return f'<ul class="social" aria-label="Redes y contacto">{lis}</ul>'


def boton_wa(cls='btn primary', href=None, corto=False, id_=''):
    # Un solo botón en todo el sitio: WhatsApp. «corto» deja visible solo «Escríbanos» en celulares muy angostos.
    txt = '<span>Escríbanos<span class="lg"> por WhatsApp</span></span>' if corto else 'Escríbanos por WhatsApp'
    ida = f' id="{id_}"' if id_ else ''
    return f'<a class="{cls}"{ida} href="{href or WA_PRO}"><svg class="ic-wa" viewBox="0 0 24 24" aria-hidden="true"><use href="#s-wa"/></svg>{txt}</a>'


def head(titulo, desc, ruta, base, extra=''):
    url = SITIO + ('' if ruta == 'index.html' else ruta)
    return f'''<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0D3441">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="{base}assets/favicon.svg">
<link rel="preload" href="{base}assets/fonts/CrimsonPro-Bold.ttf" as="font" type="font/ttf" crossorigin>
<link rel="preload" href="{base}assets/fonts/Outfit-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link rel="preload" href="{base}assets/fonts/Outfit-Bold.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{base}assets/estilo.css">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="Certeza Operativa">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITIO}assets/portada.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Certeza Operativa: el triángulo de la marca formado por líneas y la frase Mejorando empresas de México.">
<meta name="twitter:card" content="summary_large_image">
{extra}</head>
<body>
'''


def _barra(base, lista):
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site">
  <div class="wrap bar">
    <a class="logo" href="{base}index.html" aria-label="Certeza Operativa, inicio"><svg viewBox="0 0 175 133" aria-hidden="true"><use href="#mark"/></svg></a>
    <nav class="menu" aria-label="Principal">
      <button class="burger" type="button" aria-expanded="false" aria-controls="menu-lista" aria-label="Abrir menú"><span></span><span></span><span></span></button>
      <ul id="menu-lista">
        {lista}
        <li class="cta">{boton_wa()}</li>
      </ul>
      {boton_wa('btn primary small', corto=True)}
    </nav>
  </div>
</header>
'''


def menu_simple(base):
    # Inicio y catálogo: tres enlaces y un botón
    pre = f'{base}index.html'
    return _barra(base, ''.join(f'<li><a class="mtop" href="{pre}#{a}">{t}</a></li>' for a, t in [('que', 'Qué resolvemos'), ('como', 'Cómo trabajamos'), ('preguntas', 'Preguntas')]))


def menu(base, actual):
    # Páginas internas: conservan los paneles desplegables
    def item(href, b, s, ruta):
        cur = ' aria-current="page"' if ruta == actual else ''
        return f'<li><a href="{base}{href}"{cur}><b>{esc(b)}</b><span>{esc(s)}</span></a></li>'
    ind = ''.join(item(f'industrias/{i["slug"]}.html', i['nombre'], i['corto'], f'industrias/{i["slug"]}.html') for i in INDUSTRIAS)
    sol = ''.join(item(f'soluciones/{s["slug"]}.html', s['nombre'], s['tl'], f'soluciones/{s["slug"]}.html') for s in SOLUCIONES)
    srv = ''.join(item(h, b, s, '') for h, b, s in [
        ('catalogo.html', 'Catálogo de trabajos', 'Catorce trabajos con precio cerrado.'),
        ('servicios.html#empieza', 'Primera visita sin costo', 'Y su plan en una hoja, el mismo día.'),
        ('servicios.html#trabajos', 'Trabajos con precio cerrado', 'Para ordenar, ver y controlar su negocio.'),
        ('servicios.html#pagina-web', 'Página web', 'Para que lo encuentren, lo conozcan o le pidan cotización.'),
        ('servicios.html#canva', 'Documentos y tableros con Canva', 'Con su marca, en la cuenta de su negocio.'),
        ('servicios.html#acompanamiento', 'Acompañamiento', 'Revisiones y ajustes hasta que su equipo lo use solo.')])
    nos = ''.join(item(h, b, s, '') for h, b, s in [
        ('nosotros.html#como', 'Cómo lo hacemos', 'Medimos, proponemos y verificamos con usted.'),
        ('nosotros.html#esperar', 'Lo que puede esperar', 'Compromisos por escrito.'),
        ('nosotros.html#quien', 'Quién le atiende', 'Sede en Nayarit, atención por WhatsApp.'),
        ('index.html#preguntas', 'Preguntas frecuentes', 'Lo que más nos preguntan.')])
    def top(pid, nombre, h, p, lista, cls='', ver=None):
        verlink = f'<a class="link" href="{base}{ver[0]}">{esc(ver[1])}</a>' if ver else f'<a class="link" href="{WA_PRO}">Escríbanos por WhatsApp</a>'
        return f'''<li><button class="mtop" type="button" aria-expanded="false" aria-controls="{pid}">{nombre}<span class="chev" aria-hidden="true"></span></button>
        <div class="panel" id="{pid}"><div class="wrap"><div class="intro"><h2>{esc(h)}</h2><p>{esc(p)}</p>{verlink}</div><ul class="{cls}">{lista}</ul></div></div></li>'''
    return _barra(base, '\n        '.join([
        top('p-ind', 'Industrias', 'Industrias', 'Cada giro tiene sus propios dolores de cabeza. Elija el suyo y vea cómo lo ordenamos.', ind, 'c3'),
        top('p-sol', 'Soluciones', 'Soluciones', 'Cuatro resultados que un dueño nota en su día a día, y las herramientas y métodos con que los logramos.', sol, 'c3'),
        top('p-srv', 'Servicios', 'Servicios', 'De la primera visita al acompañamiento. Empezar no cuesta.', srv, '', ('catalogo.html', 'Vea el catálogo completo')),
        top('p-nos', 'Nosotros', 'Nosotros', 'Cómo lo hacemos, qué puede esperar y quién le atiende.', nos, '', ('nosotros.html', 'Conozca cómo trabajamos'))]))


def pie(base):
    col = lambda t, links: f'<div><h3>{t}</h3><ul>' + ''.join(f'<li><a href="{base}{h}">{esc(n)}</a></li>' for h, n in links) + '</ul></div>'
    return f'''<footer>
  <div class="wrap">
    <div class="top">
      <div>
        <a class="marca" href="{base}index.html" aria-label="Certeza Operativa, volver al inicio"><svg class="m-logo" viewBox="0 0 175 133" aria-hidden="true"><use href="#mark"/></svg><svg class="m-nombre" viewBox="0 0 433.6 118" aria-hidden="true"><use href="#certeza" width="433.6" height="72.8"/><text x="0" y="114" textLength="433.6" lengthAdjust="spacing">OPERATIVA</text></svg></a>
        {social(True)}
      </div>
      {col('Industrias', [(f'industrias/{i["slug"]}.html', i['nombre']) for i in INDUSTRIAS])}
      {col('Soluciones', [(f'soluciones/{s["slug"]}.html', s['nombre']) for s in SOLUCIONES])}
      {col('Servicios', [('catalogo.html', 'Catálogo de trabajos'), ('servicios.html#empieza', 'Primera visita sin costo'), ('servicios.html#trabajos', 'Trabajos con precio cerrado'), ('servicios.html#pagina-web', 'Página web'), ('servicios.html#canva', 'Documentos con Canva')])}
      {col('Nosotros', [('nosotros.html#como', 'Cómo lo hacemos'), ('nosotros.html#esperar', 'Lo que puede esperar'), ('nosotros.html#quien', 'Quién le atiende'), ('index.html#preguntas', 'Preguntas frecuentes'), ('index.html#empieza', 'Empiece aquí')])}
    </div>
    <div class="legal">
      <p>© {ANIO} Certeza Operativa · Tepic, Nayarit · WhatsApp 311 446 9363</p>
      <p>Los nombres de herramientas mencionados son marcas de sus dueños; se muestran solo como referencia de lo que ya usan los negocios. Certeza Operativa no está afiliada a ellas.</p>
    </div>
  </div>
</footer>
{boton_wa('btn primary float', id_='float')}
<script src="{base}assets/sitio.js" defer></script>
</body>
</html>
'''


def pagina(ruta, titulo, desc, cuerpo, extra_head='', barra=None):
    base = '../' * ruta.count('/')
    html = head(titulo, desc, ruta, base, extra_head) + sprite() + (barra(base) if barra else menu(base, ruta)) + '<main id="contenido">\n' + cuerpo(base) + '\n</main>\n' + pie(base)
    dst = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(html)
    return ruta


def horas_txt(h):
    return f'{h:g}'.replace('.', ',')


# ---------- Inicio ----------
# Cada banda responde una sola pregunta del dueño: ¿es para mí?, ¿qué obtengo?, ¿cuánto arriesgo?, ¿por qué les creo?, ¿cómo empiezo?
def inicio(base):
    preguntas = ['¿Le deben y no sabe cuánto?', '¿Su caja no cuadra al cierre?', '¿Se le acaba lo que más vende?',
                 '¿Todo pasa por usted?', '¿Le preguntan precios todo el día?', '¿Aparece su negocio en Google Maps?']
    familias = ''.join(f'''<li class="tarjeta familia"><h3>{esc(f["familia"])}</h3><p class="tl">{esc(f["sub"])}</p><ul>{''.join(f'<li><b>{esc(t["nombre"])}</b><span>{esc(t["promesa"])}</span></li>' for t in f["trabajos"])}</ul></li>''' for f in CATALOGO)
    pasos = [('Platicamos 15 minutos.', 'Por WhatsApp o llamada. Sin costo.'),
             ('Visitamos su negocio.', 'Vemos un caso real con sus papeles. Sin costo.'),
             ('Precio cerrado por escrito.', 'No cambia sin su autorización por escrito.'),
             ('Su equipo lo usa solo.', 'Medimos un número antes y después.')]
    caso = [('Cómo estaba', '[POR LLENAR] Giro del negocio y el problema en palabras del dueño, con el número de antes.'),
            ('Qué se entregó', '[POR LLENAR] El trabajo con precio cerrado y lo que quedó en manos del equipo.'),
            ('Qué cambió', '[POR LLENAR] El mismo número, medido después, y desde cuándo el equipo lo usa solo.')]
    faq = [('¿Cuánto cuesta?', 'Depende de lo que necesite. Se lo damos por escrito después de la visita y no cambia sin su autorización.'),
           ('¿Y si no me funciona?', 'El trabajo termina cuando su equipo lo usa solo, y medimos un número antes y después.'),
           ('¿De quién es lo que entregan?', 'De su negocio. Todo queda a su nombre.'),
           ('¿Atienden fuera de Tepic?', 'Atendemos negocios de Nayarit por WhatsApp; la visita se acuerda en la primera plática.')]
    return f'''
<section class="oscuro hero" aria-labelledby="t-hero">
  <div class="wrap">
    <div>
      <p class="kicker">Para micro y pequeños negocios de Nayarit</p>
      <h1 id="t-hero">Su negocio en orden, a la vista y con la caja cuadrada.</h1>
      <p class="lead">Vemos cómo trabaja hoy, le decimos qué se le está yendo y lo resolvemos con herramientas sencillas que su equipo usa solo.</p>
      <div class="actions">
        {boton_wa()}
        <a class="btn ghost" href="#que">Vea qué resolvemos</a>
      </div>
      <ul class="confianza" aria-label="Lo que le aseguramos"><li>Primera visita sin costo</li><li>Precio cerrado por escrito antes de empezar</li><li>Lo entregado es de su negocio</li></ul>
    </div>
    <svg class="lineart" viewBox="0 0 640 600" aria-hidden="true">{lineart(x0=170, y0=470, dx=150, dy=190, s0=150)}</svg>
  </div>
</section>

<section class="claro" aria-labelledby="t-pasa">
  <div class="wrap">
    <div class="head"><h2 id="t-pasa">¿Le pasa esto?</h2></div>
    <ul class="rejilla">{''.join(f'<li class="tarjeta pregunta">{esc(p)}</li>' for p in preguntas)}</ul>
    <p class="remate">Si dijo sí a alguna, tenemos un trabajo con precio cerrado para eso.</p>
  </div>
</section>

<section class="oscuro" id="que" aria-labelledby="t-que">
  <div class="wrap">
    <div class="head"><h2 id="t-que">Qué resolvemos</h2></div>
    <ul class="rejilla">{familias}</ul>
    <p class="mas"><a class="link" href="{base}catalogo.html">Vea el catálogo completo</a></p>
  </div>
</section>

<section class="claro" id="como" aria-labelledby="t-como">
  <div class="wrap">
    <div class="head"><h2 id="t-como">Cómo trabajamos</h2></div>
    <ol class="pasos">{''.join(f'<li><h3>{esc(h)}</h3><p>{esc(p)}</p></li>' for h, p in pasos)}</ol>
    <p class="nota" style="margin-top:28px">Horas útiles: las que dejan algo entregado. Cada bloque de trabajo queda registrado con evidencia.</p>
  </div>
</section>

<!-- Caso real: Kevin quita «hidden» cuando el dueño del caso dé su permiso -->
<section class="oscuro caso" id="caso" aria-labelledby="t-caso" hidden>
  <div class="wrap">
    <div class="head"><h2 id="t-caso">Un caso real</h2></div>
    <ul class="rejilla">{''.join(f'<li class="tarjeta"><h3>{esc(h)}</h3><p>{esc(p)}</p></li>' for h, p in caso)}</ul>
  </div>
</section>

<section class="claro" id="preguntas" aria-labelledby="t-faq">
  <div class="wrap">
    <div class="head"><h2 id="t-faq">Preguntas frecuentes</h2></div>
    <div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)}</div>
  </div>
</section>

<section class="oscuro cierre" id="empieza" aria-labelledby="t-empieza">
  <div class="wrap">
    <h2 id="t-empieza">Empiece con una plática de 15 minutos</h2>
    <div class="actions">{boton_wa(href=WA_PLATICA)}</div>
    <p class="nota">Certeza Operativa · WhatsApp 311 446 9363 · Tepic, Nayarit</p>
  </div>
</section>'''


# ---------- Catálogo ----------
def catalogo():
    def trabajo(t):
        h = horas_txt(t['horas'])
        pct = round(t['horas'] / HORAS_ESCALA * 100, 1)
        return f'''<li class="tarjeta trabajo"><p class="gancho">{esc(t["gancho"])}</p><h3>{esc(t["nombre"])}</h3><p class="promesa">{esc(t["promesa"])}</p><ul>{''.join(f'<li>{esc(p)}</li>' for p in t["puntos"])}</ul><p class="para"><b>Para:</b> {esc(t["para"])}</p><div class="horas"><small aria-hidden="true">{h} horas útiles</small><div class="barra" role="img" aria-label="{h} horas útiles"><i style="width:{pct:g}%"></i></div></div></li>'''

    def cuerpo(base):
        cols = ''.join(f'''<section class="cat-col" aria-labelledby="f{k}"><h2 id="f{k}">{esc(f["familia"])}</h2><p class="sub">{esc(f["sub"])}</p><ul>{''.join(trabajo(t) for t in f["trabajos"])}</ul></section>''' for k, f in enumerate(CATALOGO))
        return f'''
<section class="oscuro cat-intro" aria-labelledby="t-cat">
  <div class="wrap">
    <h1 id="t-cat">Elija lo que necesita su negocio</h1>
    <p class="lead">Catorce trabajos con precio cerrado. Cada uno empieza por el problema que usted ya conoce y termina cuando su equipo lo usa solo.</p>
  </div>
</section>

<div class="claro" style="padding:var(--banda) 0">
  <div class="wrap cat-cols">{cols}</div>
</div>

<section class="oscuro" aria-label="Antes de elegir">
  <div class="wrap cat-pie">
    <div class="tarjeta"><h2>Horas útiles</h2><p>Las que dejan algo entregado, registradas con evidencia. No se rebasan sin su autorización por escrito. Cada trabajo es de 5 horas como mínimo.</p></div>
    <div class="tarjeta"><h2>Lo que no hacemos</h2><ul><li>Contabilidad ni declaraciones.</li><li>Asesoría legal.</li><li>Google Maps suelto: siempre va dentro de un trabajo.</li></ul></div>
    <div class="tarjeta" id="empieza"><h2>Empiece sin costo</h2><p>La primera plática y la visita son sin costo. Le damos el precio cerrado por escrito después de la visita.</p>{boton_wa(href=WA_PLATICA)}</div>
  </div>
</section>'''
    return pagina('catalogo.html', 'Catálogo de trabajos · Certeza Operativa',
                  'Catorce trabajos con precio cerrado para micro y pequeños negocios de Nayarit: cobranza, caja, inventario, cotizaciones y presencia en internet.',
                  cuerpo, barra=menu_simple)


# ---------- Páginas internas ----------
def ph(base, migas, h1, lead, tipos='', variante=0, wa_msg=None):
    m = ''.join(f'<li><a href="{base}{h}">{esc(n)}</a></li>' if h else f'<li aria-current="page">{esc(n)}</li>' for h, n in migas)
    giros = [(-46, 230, 410), (40, 250, 400), (-30, 240, 420), (52, 220, 400)]
    g, x0, y0 = giros[variante % 4]
    return f'''<section class="ph" aria-labelledby="t-ph">
  <div class="wrap">
    <div>
      <nav aria-label="Ruta"><ol class="migas">{m}</ol></nav>
      <h1 id="t-ph">{esc(h1)}</h1>
      {f'<p class="tipos">{esc(tipos)}</p>' if tipos else ''}
      <p class="lead">{esc(lead)}</p>
      <div class="actions">{boton_wa(href=wa_msg)}</div>
    </div>
    <svg class="lineart" viewBox="0 0 640 600" aria-hidden="true">{lineart(giro=g, x0=x0, y0=y0)}</svg>
  </div>
</section>'''


def cta(base, titulo='Empiece con una plática de 15 minutos, sin costo.'):
    return f'''<section class="oscuro cta-band"><div class="wrap"><h2>{esc(titulo)}</h2><div class="actions">{boton_wa(href=WA_PLATICA)}</div></div></section>'''


def industria(i, k):
    def cuerpo(base):
        ay = ''.join(f'<article class="ay"><small>{PILAR_NOMBRE[PIEZA[n][0]]}</small><h3>{esc(n)}</h3><p>{esc(PIEZA[n][2])}</p></article>' for n in i['piezas'])
        otros = ''.join(f'<a href="{o["slug"]}.html">{esc(o["nombre"])}</a>' for o in INDUSTRIAS if o is not i)
        return ph(base, [('index.html', 'Inicio'), ('index.html#que', 'Industrias'), (None, i['nombre'])], i['nombre'], i['lead'], i['tipos'], k,
                  wa(f'Hola, mi negocio es del giro {i["nombre"]} y quiero platicar con Certeza Operativa.')) + f'''
<section class="bloque blanco" aria-labelledby="t-voces"><div class="wrap">
  <div class="head"><h2 id="t-voces">¿Le suena alguna de estas preguntas?</h2><p class="sub">Si sí, empezamos por ahí.</p></div>
  <ul class="voces">{''.join(f'<li>{esc(v)}</li>' for v in i['voces'])}</ul>
</div></section>
<section class="bloque" aria-labelledby="t-ayuda"><div class="wrap">
  <div class="head"><h2 id="t-ayuda">Cómo le ayudamos.</h2><p class="sub">Piezas concretas que se juntan en un trabajo con precio cerrado y un número que medimos antes y después. Usted elige cuáles y en qué orden.</p></div>
  <div class="ayuda">{ay}</div>
  <p class="mas"><a class="link" href="{base}catalogo.html">Vea el catálogo completo</a></p>
</div></section>
<section class="bloque blanco" aria-labelledby="t-herr"><div class="wrap dos">
  <div class="head"><h2 id="t-herr">Herramientas que suelen usar estos negocios.</h2><p class="sub">Partimos de lo que ya tiene. Si algo no lo usa, no lo instalamos.</p></div>
  <ul class="chips">{''.join(f'<li>{esc(h)}</li>' for h in i['herramientas'])}</ul>
</div></section>
<section class="bloque" aria-labelledby="t-otras"><div class="wrap">
  <h2 id="t-otras" style="font-size:30px">Otras industrias</h2>
  <div class="otros">{otros}</div>
</div></section>
{cta(base)}'''
    return pagina(f'industrias/{i["slug"]}.html', f'{i["nombre"]} · Certeza Operativa', f'{i["lead"]} Para micro y pequeños negocios de Nayarit.', cuerpo)


def solucion(s, k):
    def cuerpo(base):
        otros = ''.join(f'<a href="{o["slug"]}.html">{esc(o["nombre"])}</a>' for o in SOLUCIONES if o is not s)
        ent = ''.join(f'<li>{esc(a)}<span>{esc(b)}</span></li>' for a, b in s['entregables'])
        return ph(base, [('index.html', 'Inicio'), ('index.html#que', 'Soluciones'), (None, s['nombre'])], s['nombre'], s['lead'], s['tl'], k + 1) + f'''
<section class="bloque blanco" aria-labelledby="t-suena"><div class="wrap">
  <div class="head"><h2 id="t-suena">¿Le suena?</h2></div>
  <ul class="voces">{''.join(f'<li>{esc(v)}</li>' for v in s['voces'])}</ul>
</div></section>
<section class="bloque" aria-labelledby="t-ent"><div class="wrap dos">
  <div class="head"><h2 id="t-ent">Lo que entregamos.</h2><p class="sub">Sencillo, con su marca y pensado para que su equipo lo use sin nosotros.</p></div>
  <ul class="lista2">{ent}</ul>
</div></section>
<section class="bloque blanco" aria-labelledby="t-mide"><div class="wrap dos">
  <div class="head"><h2 id="t-mide">Cómo sabemos que funcionó.</h2><p class="sub">Cada trabajo tiene un número que importa. Lo medimos con usted antes y después.</p></div>
  <div class="mide"><svg viewBox="0 0 175 133" aria-hidden="true"><use href="#mark"/></svg><div><h3>{esc(s['mide'][0])}</h3><p>{esc(s['mide'][1])}</p></div></div>
</div></section>
<section class="bloque" aria-labelledby="t-otras"><div class="wrap">
  <h2 id="t-otras" style="font-size:30px">Otras soluciones</h2>
  <div class="otros">{otros}</div>
</div></section>
{cta(base)}'''
    return pagina(f'soluciones/{s["slug"]}.html', f'{s["nombre"]} · Certeza Operativa', f'{s["lead"]}', cuerpo)


def servicios():
    def cuerpo(base):
        webs = [('Página de lanzamiento', 'Una sola página para que lo encuentren y le escriban: oferta, qué ofrece y a quién, contacto, ubicación y datos del negocio.', '5 a 7 días hábiles'),
                ('Sitio completo', 'Hasta 5 secciones para que lo conozcan antes de escribirle, por ejemplo inicio, servicios, nosotros, preguntas y contacto.', '10 a 14 días hábiles'),
                ('Sitio con catálogo', 'El sitio completo con sus productos, listos para pedir cotización: hasta 30 con foto, descripción y presentación.', '15 a 20 días hábiles')]
        web = ''.join(f'<article class="ay"><h3>{a}</h3><p>{b}</p><em>Lista en {d}.</em></article>' for a, b, d in webs)
        return ph(base, [('index.html', 'Inicio'), (None, 'Servicios')], 'Servicios', 'De la primera visita al acompañamiento. Empezar no cuesta y cada trabajo tiene precio cerrado por escrito antes de empezar.', '', 2) + f'''
<section class="bloque blanco"><div class="wrap">
  <article class="svc" id="empieza"><div><h2>Primera visita sin costo</h2><p class="tl">Y su plan en una hoja, el mismo día.</p></div><div>
    <ul class="lista2"><li>Primera visita<span>Una visita corta: doce preguntas y un caso real de su negocio, de punta a punta. También platicamos con alguien de su equipo. Hasta 90 minutos en micro y 2 horas en pequeña.</span></li><li>Plan en una hoja<span>El mismo día de la visita. Trae el problema en sus palabras, dos o tres hechos y una acción gratis para hoy. También el siguiente paso con precio cerrado y fecha, y la lista corta de papeles.</span></li></ul>
    <div class="actions" style="margin-top:22px">{boton_wa(href=WA_PLATICA)}</div></div></article>
  <article class="svc" id="trabajos"><div><h2>Trabajos con precio cerrado</h2><p class="tl">Cada trabajo tiene precio cerrado y un número que medimos antes y después. Se arma con piezas de Orden, Visibilidad y Control.</p><p style="margin-top:18px"><a class="link" href="{base}catalogo.html">Vea el catálogo completo</a></p></div><div><ul class="lista2"><li>Orden<span>Precios a la vista, tareas por escrito y un responsable para cada pendiente.</span></li><li>Visibilidad<span>Saber cada semana cómo va el negocio, en una sola vista.</span></li><li>Control<span>Que la caja cuadre y los cobros no se olviden.</span></li></ul></div></article>
  <article class="svc" id="pagina-web"><div><h2>Página web</h2><p class="tl">Elija por lo que quiere que haga su cliente al entrar: escribirle, conocerlo o pedirle cotización. Las tres incluyen su dominio propio conectado y publicado, un botón de WhatsApp con mensaje listo y un diseño que se ve bien en el celular. Hay versión con más extras; se la explicamos en la primera visita.</p></div><div class="webs">{web}</div></article>
  <article class="svc" id="canva"><div><h2>Documentos y tableros con Canva</h2><p class="tl">Con su marca, en la cuenta de Canva de su negocio, para que usted y su equipo los usen, los editen y los descarguen en PDF.</p></div><div>
    <ul class="lista2"><li>Orden<span>Lista de precios, procedimientos y quién hace qué.</span></li><li>Visibilidad<span>Tablero de la semana con 5 números.</span></li><li>Control<span>Cierre de caja, calendario de cobro y mensajes de cobranza listos.</span></li></ul></div></article>
  <article class="svc" id="acompanamiento"><div><h2>Acompañamiento</h2><p class="tl">Hasta que su equipo lo use solo.</p></div><div>
    <ul class="lista2"><li>Prueba con un caso real<span>Lo usamos con usted una semana o un cierre real, y ajustamos.</span></li><li>Capacitación<span>Para que usted y su equipo lo usen sin nosotros.</span></li><li>Extras cuando hacen falta<span>Más secciones, más productos o su perfil en Google Maps.</span></li></ul></div></article>
</div></section>
{cta(base)}'''
    return pagina('servicios.html', 'Servicios · Certeza Operativa', 'Primera visita sin costo, trabajos con precio cerrado, página web, documentos con Canva y acompañamiento para micro y pequeños negocios de Nayarit.', cuerpo)


def nosotros():
    def cuerpo(base):
        return ph(base, [('index.html', 'Inicio'), (None, 'Nosotros')], 'Cómo lo hacemos', 'Somos claros: medimos, proponemos y adaptamos herramientas sencillas a su operación. Usted verifica cada resultado.', 'Para micro y pequeños negocios · Sede en Tepic, Nayarit.', 3) + f'''
<section class="bloque blanco" id="como"><div class="wrap dos">
  <div class="head"><h2>Medimos antes de proponer.</h2><p class="sub">No llegamos con una receta. Primero vemos un caso real de su negocio y después proponemos lo mínimo que resuelve el problema.</p></div>
  <ol class="lista2 num"><li>Lo visitamos<span>La primera visita es sin costo y dura hasta 90 minutos. Doce preguntas, un caso real y una plática con alguien de su equipo.</span></li><li>Le damos un plan en una hoja<span>El mismo día de la visita, con una acción gratis para hoy y la lista corta de papeles.</span></li><li>Medimos su punto de partida<span>Elegimos un solo número que importe y lo medimos con sus papeles, no de memoria.</span></li><li>Lo resolvemos con precio cerrado<span>Si la causa resulta otra, le cotizamos de nuevo por escrito antes de empezar.</span></li><li>Su equipo lo usa solo<span>Capacitamos a quien lo va a usar. Termina cuando su equipo completa un ciclo sin nosotros.</span></li><li>Medimos la mejora<span>Comparamos el número de antes con el de hoy. Lo que funcionó queda escrito.</span></li></ol>
</div></section>
<section class="bloque" id="esperar"><div class="wrap dos">
  <div class="head"><h2>Lo que puede esperar.</h2><p class="sub">Compromisos que quedan por escrito.</p></div>
  <ul class="lista2"><li>Las horas útiles autorizadas no se rebasan<span>Sin su autorización por escrito.</span></li><li>Cada bloque de trabajo queda registrado<span>Con fecha y evidencia; puede pedir el registro.</span></li><li>Los cambios después de aprobar<span>Se acuerdan y se cotizan por escrito antes de hacerlos.</span></li><li>Lo que entregamos queda a nombre de su negocio<span>Así lo dejamos por escrito antes de empezar.</span></li></ul>
</div></section>
<section class="bloque blanco" id="quien"><div class="wrap dos">
  <div class="head"><h2>Quién le atiende.</h2><p class="sub">Sede en Tepic, Nayarit. Atendemos por WhatsApp y, cuando hace falta, en su negocio.</p></div>
  <div class="persona"><span class="av"><svg viewBox="0 0 175 133" aria-hidden="true"><use href="#mark"/></svg></span><div><h3 style="font-size:28px">Kevin Yammil Cueva Cardona</h3><p>Fundador de Certeza Operativa, con formación en Ingeniería Civil. Hoy atiende micro y pequeños negocios de Tepic y Nayarit.</p></div></div>
</div></section>
{cta(base)}'''
    return pagina('nosotros.html', 'Nosotros · Certeza Operativa', 'Cómo trabajamos en seis pasos, de la primera visita sin costo a medir la mejora. Compromisos por escrito. Sede en Tepic, Nayarit.', cuerpo)


def portada_jsonld():
    data = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Certeza Operativa",
            "description": "Ordenamos micro y pequeños negocios de Nayarit: cobranza, caja, inventario, cotizaciones y presencia en internet.",
            "url": SITIO, "image": SITIO + "assets/portada.png", "logo": SITIO + "assets/favicon.svg", "telephone": "+523114469363",
            "areaServed": {"@type": "AdministrativeArea", "name": "Nayarit, México"},
            "sameAs": [h for h, _, _ in SOC]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>\n'


if __name__ == '__main__':
    rutas = [pagina('index.html', 'Certeza Operativa · Su negocio en orden, en Nayarit',
                    'Para micro y pequeños negocios de Nayarit: cobranza, caja, inventario, cotizaciones y presencia en internet. Primera visita sin costo y precio cerrado por escrito antes de empezar.',
                    inicio, portada_jsonld(), barra=menu_simple)]
    rutas.append(catalogo())
    rutas += [industria(i, k) for k, i in enumerate(INDUSTRIAS)]
    rutas += [solucion(s, k) for k, s in enumerate(SOLUCIONES)]
    rutas += [servicios(), nosotros()]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITIO}{"" if r == "index.html" else r}</loc></url>\n' for r in rutas) + '</urlset>\n'
    open(os.path.join(RAIZ, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
    print('\n'.join(rutas))
