# Página de lanzamiento: una sola página estática de 5 bloques, armada desde negocio.json.
# Uso:   python3 componentes/W1/construir.py ruta/a/negocio.json [--salida carpeta]
# Lee las fotos de la carpeta fotos/ junto a negocio.json y escribe en <carpeta del json>/salida/pagina/
# (o en --salida): index.html, img/, robots.txt, sitemap.xml y CNAME si hay dominio, y reporte.txt.
# Requiere Pillow (pip install -r componentes/requirements.txt). Sin recursos externos: carga rápida en celular.
import argparse
import datetime as dt
import json
import os
import shutil
import sys
from html import escape as esc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comun as c  # noqa: E402

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit('Falta Pillow. Instálelo con: pip install -r componentes/requirements.txt')

ANCHOS = (480, 960)  # versiones de cada foto: celular y pantalla grande


# ---------- Color: contraste AA automático ----------
def _lum(hexa):
    hexa = hexa.lstrip('#')
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda v: v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def contraste(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


TINTA, BLANCO = '#14212B', '#FFFFFF'


def texto_sobre(fondo):
    return BLANCO if contraste(fondo, BLANCO) >= contraste(fondo, TINTA) else TINTA


# ---------- Fotos ----------
def procesar_fotos(n, dest, av):
    """Hace versiones WebP de 480 y 960 px, la imagen para redes (1200×630) y el ícono."""
    src = os.path.join(n['_carpeta'], 'fotos')
    os.makedirs(os.path.join(dest, 'img'), exist_ok=True)
    fotos = []
    for i, f in enumerate([f for f in n.get('fotos') or [] if f.get('archivo')]):
        ruta = os.path.join(src, f['archivo'])
        if not os.path.exists(ruta):
            av.error(f'No encuentro la foto {f["archivo"]} en {src}.')
            continue
        if not f.get('alt'):
            av.aviso(f'La foto {f["archivo"]} no tiene texto alternativo (alt): escriba qué se ve.')
        im = ImageOps.exif_transpose(Image.open(ruta)).convert('RGB')
        if im.width < 960:
            av.aviso(f'La foto {f["archivo"]} mide {im.width} px de ancho; se ve mejor desde 1200 px.')
        base = f'foto-{i + 1}'
        versiones = []
        for w in ANCHOS:
            w2 = min(w, im.width)
            h2 = round(im.height * w2 / im.width)
            nombre = f'{base}-{w}.webp'
            im.resize((w2, h2), Image.LANCZOS).save(os.path.join(dest, 'img', nombre), 'WEBP', quality=72, method=6)
            versiones.append((nombre, w2, h2))
        fotos.append({'alt': f.get('alt') or f'Foto de {n["nombre"]}', 'v': versiones})
        if i == 0:
            og = ImageOps.fit(im, (1200, 630), Image.LANCZOS)
            og.save(os.path.join(dest, 'img', 'vista-previa.jpg'), 'JPEG', quality=80, optimize=True, progressive=True)
    if len(fotos) < 3:
        av.aviso(f'Hay {len(fotos)} foto(s); la página pide de 3 a 5.')
    if not fotos:
        av.aviso('Sin fotos: la vista previa en redes saldrá sin imagen.')

    logo = None
    if n.get('logo'):
        ruta = os.path.join(src, n['logo'])
        if not os.path.exists(ruta):
            av.error(f'No encuentro el logo {n["logo"]} en {src}.')
        elif ruta.lower().endswith('.svg'):
            shutil.copy(ruta, os.path.join(dest, 'img', 'logo.svg'))
            logo = ('logo.svg', 96, 96)
        else:
            im = Image.open(ruta).convert('RGBA')
            im.thumbnail((192, 192), Image.LANCZOS)
            im.save(os.path.join(dest, 'img', 'logo.png'), 'PNG', optimize=True)
            logo = ('logo.png', im.width, im.height)
            ico = ImageOps.pad(im, (180, 180), color=(255, 255, 255, 0))
            ico.save(os.path.join(dest, 'img', 'icono.png'), 'PNG', optimize=True)
    return fotos, logo


# ---------- Bloques ----------
ICON_WA = ('<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.5-.3Z"/></svg>')
ICON_TEL = '<svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>'
ICON_MAPA = '<svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12Z"/><circle cx="12" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>'


def boton_wa(n, clase='btn wa', texto='Escríbanos por WhatsApp'):
    return f'<a class="{clase}" href="{esc(c.wa(n))}" data-wa>{ICON_WA}<span>{texto}</span></a>'


def bloque_presentacion(n, logo):
    # tamaño final escrito en el HTML (72 px de alto) para que la página no salte al cargar el logo
    img = (f'<img class="logo" src="img/{logo[0]}" width="{round(72 * logo[1] / logo[2])}" height="72" alt="Logo de {esc(n["nombre"])}">'
           if logo else '')
    desde = f'<p class="desde">Desde {esc(str(n["desde"]))}</p>' if n.get('desde') else ''
    tel = (f'<a class="btn sec" href="tel:{c.tel_e164(n)}">{ICON_TEL}<span>Llamar</span></a>'
           if c.tel_e164(n) else '')
    return f'''<header class="hero" id="inicio">
  <div class="in">
    {img}
    <h1>{esc(n["nombre"])}</h1>
    <p class="frase">{esc(n["frase"])}</p>
    <p class="estado" id="estado">Horario abajo</p>
    <div class="acciones">{boton_wa(n)}{tel}</div>
    {desde}
  </div>
</header>'''


def bloque_ofrece(n):
    items, sin_precio = [], False
    for s in [s for s in n.get('servicios') or [] if s.get('nombre')]:
        p = c.precio_valido(s)
        sin_precio |= p is None
        desc = f'<p>{esc(s["descripcion"])}</p>' if s.get('descripcion') else ''
        pr = f'<p class="precio">{esc(p)}</p>' if p else ''
        items.append(f'<li><h3>{esc(s["nombre"])}</h3>{desc}{pr}</li>')
    nota = '<p class="nota">Pregunte el precio por WhatsApp; le respondemos en horario de atención.</p>' if sin_precio else ''
    dif = ''.join(f'<li>{esc(d)}</li>' for d in n.get('diferenciadores') or [])
    dif = f'<ul class="chips" aria-label="Por qué elegirnos">{dif}</ul>' if dif else ''
    pago = (f'<p class="pago"><b>Formas de pago:</b> {esc(c.lista_y(n["formas_pago"]))}.</p>'
            if n.get('formas_pago') else '')
    return f'''<section id="servicios" aria-labelledby="t-servicios">
  <div class="in">
    <h2 id="t-servicios">Qué ofrecemos</h2>
    {dif}
    <ul class="servicios">{"".join(items)}</ul>
    {nota}{pago}
  </div>
</section>'''


def bloque_fotos(n, fotos):
    if not fotos:
        return ''
    figs = []
    for i, f in enumerate(fotos):
        (a, wa_, ha), (b, wb, hb) = f['v']
        figs.append(f'<li><img src="img/{a}" srcset="img/{a} {wa_}w, img/{b} {wb}w" '
                    f'sizes="(min-width: 760px) 360px, calc(100vw - 32px)" width="{wa_}" height="{ha}" '
                    f'alt="{esc(f["alt"])}" loading="lazy" decoding="async"></li>')
    return f'''<section id="fotos" aria-labelledby="t-fotos">
  <div class="in">
    <h2 id="t-fotos">Fotos</h2>
    <ul class="galeria">{"".join(figs)}</ul>
  </div>
</section>'''


def bloque_ubicacion(n):
    filas = ''.join(f'<div><dt>{esc(c.texto_dias(d))}</dt><dd>{esc(c.texto_tramos(t))}</dd></div>'
                    for d, t in c.grupos_horario(n))
    esp = f'<p class="nota">{esc(n["horario_especial"])}</p>' if n.get('horario_especial') else ''
    if c.muestra_direccion(n):
        ref = (n.get('direccion') or {}).get('referencia')
        ref = f'<p class="nota">{esc(ref)}</p>' if ref else ''
        lugar = f'''<p class="dir">{esc(c.direccion_linea(n))}</p>{ref}
    <a class="btn sec" href="{esc(c.como_llegar(n))}">{ICON_MAPA}<span>Cómo llegar</span></a>'''
    else:
        lugar = ''
    zonas = (f'<p class="dir"><b>Vamos a:</b> {esc(c.lista_y(n["areas_servicio"]))}.</p>'
             if n.get('areas_servicio') and n.get('atencion') in ('area', 'ambos') else '')
    titulo = 'Ubicación y horario' if c.muestra_direccion(n) else 'Zona y horario'
    return f'''<section id="ubicacion" aria-labelledby="t-ubicacion">
  <div class="in dos">
    <div>
      <h2 id="t-ubicacion">{titulo}</h2>
      {lugar}{zonas}
    </div>
    <div>
      <h3>Horario</h3>
      <dl class="horario">{filas}</dl>
      {esp}
    </div>
  </div>
</section>'''


REDES = {'facebook': 'Facebook', 'instagram': 'Instagram', 'tiktok': 'TikTok'}


def bloque_contacto(n):
    redes = ''.join(f'<li><a href="{esc(u)}" rel="me">{REDES[k]}</a></li>'
                    for k, u in (n.get('redes') or {}).items() if u and k in REDES)
    redes = f'<ul class="redes" aria-label="Redes sociales">{redes}</ul>' if redes else ''
    tel = (f'<p>Teléfono: <a href="tel:{c.tel_e164(n)}">{c.tel_bonito(n)}</a></p>' if c.tel_e164(n) else '')
    return f'''<section class="final" id="contacto" aria-labelledby="t-contacto">
  <div class="in">
    <h2 id="t-contacto">¿Le ayudamos?</h2>
    <p>Mándenos un mensaje y le respondemos en horario de atención.</p>
    {boton_wa(n)}
    {tel}
    {redes}
  </div>
</section>'''


def pie(n):
    cred = (' · Página hecha con <a href="https://keyacuevaca-dot.github.io/certeza-operativa/">Certeza Operativa</a>'
            if n.get('credito') else '')
    return f'<footer><p>© {dt.date.today().year} {esc(n["nombre"])} · {esc(n.get("ciudad", ""))}, {esc(n.get("estado", ""))}{cred}</p></footer>'


# ---------- Datos estructurados LocalBusiness (schema.org) ----------
def jsonld(n, fotos, url_base):
    d = {'@context': 'https://schema.org', '@type': n.get('tipo_schema') or 'LocalBusiness',
         'name': n['nombre'], 'description': n.get('descripcion_corta') or n.get('frase')}
    if url_base:
        d['url'] = url_base
        d['@id'] = url_base + '#negocio'
        if fotos:
            d['image'] = [url_base + 'img/vista-previa.jpg'] + [url_base + 'img/' + f['v'][1][0] for f in fotos]
    if c.tel_e164(n):
        d['telephone'] = c.tel_e164(n)
    dirc = n.get('direccion') or {}
    addr = {'@type': 'PostalAddress', 'addressLocality': n.get('ciudad'), 'addressRegion': n.get('estado'),
            'addressCountry': n.get('pais') or 'MX'}
    if c.muestra_direccion(n):
        addr['streetAddress'] = ', '.join(x for x in [dirc.get('calle'), dirc.get('colonia')] if x)
        if dirc.get('cp'):
            addr['postalCode'] = dirc['cp']
        g = n.get('geo') or {}
        if g.get('lat') is not None and g.get('lng') is not None:
            d['geo'] = {'@type': 'GeoCoordinates', 'latitude': g['lat'], 'longitude': g['lng']}
    d['address'] = addr
    if n.get('areas_servicio') and n.get('atencion') in ('area', 'ambos'):
        d['areaServed'] = [{'@type': 'City', 'name': z} for z in n['areas_servicio']]
    esp = []
    for dias, t in c.grupos_horario(n):
        for a, b in t:
            esp.append({'@type': 'OpeningHoursSpecification', 'dayOfWeek': [c.DIA_SCHEMA[x] for x in dias],
                        'opens': a, 'closes': b})
    d['openingHoursSpecification'] = esp
    if n.get('mapa_url'):
        d['hasMap'] = n['mapa_url']
    same = [u for u in (n.get('redes') or {}).values() if u]
    if same:
        d['sameAs'] = same
    if n.get('formas_pago'):
        d['paymentAccepted'] = ', '.join(n['formas_pago'])
    return json.dumps(d, ensure_ascii=False, indent=1).replace('</', '<\\/')


# ---------- Estilos ----------
def css(n):
    p = (n.get('colores') or {}).get('principal') or '#1D4E6B'
    a = (n.get('colores') or {}).get('acento') or '#F2B33D'
    return f''':root{{--p:{p};--pt:{texto_sobre(p)};--a:{a};--at:{texto_sobre(a)};--wa:#128C4A;--fg:#14212B;--mu:#4A5866;--bg:#FFFFFF;--bg2:#F3F5F7;--ln:#D9DFE5;--r:12px}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;font:17px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",sans-serif;color:var(--fg);background:var(--bg);padding-bottom:76px}}
img{{max-width:100%;height:auto;display:block}}a{{color:inherit}}
h1,h2,h3{{line-height:1.15;margin:0 0 .5em;text-wrap:balance}}h1{{font-size:clamp(2rem,8vw,3rem)}}h2{{font-size:1.6rem}}h3{{font-size:1.1rem}}
p{{margin:0 0 .8em}}ul{{margin:0;padding:0;list-style:none}}
.in{{max-width:960px;margin:0 auto;padding:0 16px}}section{{padding:44px 0}}section:nth-of-type(even){{background:var(--bg2)}}
.hero{{background:var(--p);color:var(--pt);padding:44px 0 40px}}
.hero .logo{{height:72px;width:auto;margin-bottom:16px;border-radius:8px}}
.frase{{font-size:1.2rem;max-width:34ch}}.desde{{opacity:.85;font-size:.95rem;margin-top:14px}}
.estado{{visibility:hidden;display:inline-block;font-weight:600;font-size:.95rem;padding:2px 10px;border-radius:999px;background:rgba(255,255,255,.16)}}
.acciones{{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}}
.btn{{display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:10px 18px;border-radius:var(--r);font-weight:700;text-decoration:none;border:2px solid transparent}}
.btn.wa{{background:var(--wa);color:#fff}}.btn.sec{{border-color:currentColor}}
.hero .btn.wa{{background:var(--a);color:var(--at)}}
.btn:focus-visible,a:focus-visible{{outline:3px solid var(--a);outline-offset:3px}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px}}.chips li{{background:var(--bg2);border:1px solid var(--ln);border-radius:999px;padding:4px 12px;font-size:.95rem}}
.servicios{{display:grid;gap:12px}}.servicios li{{background:var(--bg);border:1px solid var(--ln);border-radius:var(--r);padding:16px}}
.servicios p{{color:var(--mu);margin:0}}.servicios .precio{{color:var(--fg);font-weight:600;margin-top:6px}}
.nota{{color:var(--mu);font-size:.95rem;margin-top:12px}}.pago{{margin-top:12px}}
.galeria{{display:grid;gap:12px}}.galeria img{{border-radius:var(--r);width:100%;aspect-ratio:4/3;object-fit:cover;background:var(--ln)}}
.dir{{font-size:1.1rem}}.dos{{display:grid;gap:24px}}
.horario div{{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--ln)}}.horario dt{{font-weight:600}}.horario dd{{margin:0;text-align:right}}
.final{{background:var(--p)!important;color:var(--pt);text-align:center}}.final .btn.wa{{background:var(--a);color:var(--at);margin:6px 0 14px}}
.redes{{display:flex;justify-content:center;gap:18px;flex-wrap:wrap}}.redes a{{display:inline-block;padding:10px 4px;min-height:44px;font-weight:600}}
footer{{text-align:center;color:var(--mu);font-size:.9rem;padding:20px 16px}}
.fijo[hidden]{{display:none}}.fijo{{position:fixed;left:12px;right:12px;bottom:12px;z-index:5;justify-content:center;box-shadow:0 6px 20px rgba(0,0,0,.25)}}
.cinta{{margin:0;background:#7A3E00;color:#fff;text-align:center;font-size:.9rem;padding:6px 12px}}
@media (min-width:760px){{body{{padding-bottom:0}}.fijo{{display:none}}.servicios{{grid-template-columns:repeat(2,1fr)}}.galeria{{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}.dos{{grid-template-columns:1fr 1fr}}}}
@media (prefers-reduced-motion:no-preference){{html{{scroll-behavior:smooth}}}}'''


# ---------- Estado abierto/cerrado (opcional; si falla, no se muestra nada) ----------
def js(n):
    h = {d: c.tramos(n, d) for d in c.DIAS}
    zona = n.get('zona_horaria') or 'America/Mazatlan'
    return ('(function(){try{var H=' + json.dumps(h) + ',Z=' + json.dumps(zona) + ','
            'K=["dom","lun","mar","mie","jue","vie","sab"],'
            'p=new Intl.DateTimeFormat("en-US",{timeZone:Z,weekday:"short",hour:"2-digit",minute:"2-digit",hourCycle:"h23"}).formatToParts(new Date()),'
            'o={};p.forEach(function(x){o[x.type]=x.value});'
            'var d=K[["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].indexOf(o.weekday)],m=o.hour+":"+o.minute,'
            'a=(H[d]||[]).some(function(t){return m>=t[0]&&m<t[1]}),e=document.getElementById("estado");'
            'e.textContent=a?"Abierto ahora":"Cerrado ahora · escríbanos y le respondemos al abrir";e.style.visibility="visible"}catch(_){}'
            # el botón fijo se oculta mientras se ve el botón de la portada
            'try{var f=document.querySelector(".fijo"),h=document.querySelector(".hero");'
            'new IntersectionObserver(function(x){f.hidden=x[0].isIntersecting}).observe(h)}catch(_){}})();')


def construir(ruta_json, salida=None):
    n = c.cargar(ruta_json)
    av = c.Avisos()
    c.validar_basico(n, av)
    dest = salida or os.path.join(n['_carpeta'], 'salida', 'pagina')
    if av.errores:
        return None, av
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    fotos, logo = procesar_fotos(n, dest, av)

    url = (n.get('dominio') or '').strip().rstrip('/')
    url_base = url + '/' if url else ''
    if not url:
        av.aviso('Sin dominio: la vista previa en Facebook y WhatsApp necesita la dirección final (dominio) para mostrar la foto. Vuelva a construir cuando se publique.')
    titulo = f'{n["nombre"]} · {n["giro"]} en {n["ciudad"]}'
    desc = n.get('descripcion_corta') or n.get('frase')
    if len(desc) > 155:
        av.aviso(f'La descripción corta tiene {len(desc)} caracteres; Google suele cortar después de unos 155.')
    for k, col in (n.get('colores') or {}).items():
        r = contraste(col, texto_sobre(col))
        if r < 4.5:
            av.aviso(f'El color {k} {col} no llega a contraste AA con ningún texto ({r:.1f}:1). Elija un tono más oscuro o más claro.')

    preview = n.get('vista_previa', True)
    robots = '<meta name="robots" content="noindex, nofollow">' if preview else ''
    cinta = (f'<p class="cinta">Vista previa: esta página todavía no está publicada. {esc(n.get("cinta") or "")}</p>'
             if preview else '')
    og_img = (url_base + 'img/vista-previa.jpg') if fotos else ''
    meta_og = ['<meta property="og:type" content="website">',
               f'<meta property="og:title" content="{esc(titulo)}">',
               f'<meta property="og:description" content="{esc(desc)}">',
               '<meta property="og:locale" content="es_MX">',
               f'<meta name="twitter:card" content="{"summary_large_image" if og_img else "summary"}">']
    if url_base:
        meta_og.append(f'<meta property="og:url" content="{esc(url_base)}">')
    if og_img:
        meta_og += [f'<meta property="og:image" content="{esc(og_img if url_base else "img/vista-previa.jpg")}">',
                    '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
                    f'<meta property="og:image:alt" content="{esc(fotos[0]["alt"])}">']
    canon = f'<link rel="canonical" href="{esc(url_base)}">' if url_base else ''
    icono = ('<link rel="icon" href="img/icono.png"><link rel="apple-touch-icon" href="img/icono.png">' if logo and logo[0] == 'logo.png'
             else f'<link rel="icon" href="data:image/svg+xml,{_favicon(n)}">')

    html = f'''<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
{canon}
{chr(10).join(meta_og)}
<meta name="theme-color" content="{esc((n.get("colores") or {}).get("principal") or "#1D4E6B")}">
{icono}
<style>{css(n)}</style>
<script type="application/ld+json">{jsonld(n, fotos, url_base)}</script>
</head>
<body>
{cinta}
{bloque_presentacion(n, logo)}
<main>
{bloque_ofrece(n)}
{bloque_fotos(n, fotos)}
{bloque_ubicacion(n)}
{bloque_contacto(n)}
</main>
{pie(n)}
{boton_wa(n, "btn wa fijo")}
<script>{js(n)}</script>
</body>
</html>
'''
    with open(os.path.join(dest, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    with open(os.path.join(dest, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write('User-agent: *\nAllow: /\n' + (f'Sitemap: {url_base}sitemap.xml\n' if url_base else ''))
    if url_base:
        with open(os.path.join(dest, 'sitemap.xml'), 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                    f'<url><loc>{esc(url_base)}</loc><lastmod>{dt.date.today().isoformat()}</lastmod></url></urlset>\n')
        with open(os.path.join(dest, 'CNAME'), 'w', encoding='utf-8') as f:
            f.write(url.split('://', 1)[-1] + '\n')
    if preview:
        av.aviso('Está en vista previa (cinta y noindex). Para publicar: "vista_previa": false, con el sí del cliente.')
    _reporte(dest, n, av, 'Página de lanzamiento')
    return dest, av


def _favicon(n):
    from urllib.parse import quote
    p = (n.get('colores') or {}).get('principal') or '#1D4E6B'
    letra = esc(n['nombre'].strip()[:1].upper())
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{p}"/>'
           f'<text x="32" y="44" font-size="36" font-family="system-ui,sans-serif" font-weight="700" text-anchor="middle" fill="{texto_sobre(p)}">{letra}</text></svg>')
    return quote(svg)


def _reporte(dest, n, av, que):
    lineas = [f'{que} · {n["nombre"]} · {dt.datetime.now():%Y-%m-%d %H:%M}', '']
    lineas += ['Pendientes y avisos:'] + [f'{i}. {t}' for i, t in enumerate(av.avisos, 1)] if av.avisos else ['Sin avisos.']
    with open(os.path.join(dest, 'reporte.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas) + '\n')


def imprimir(av, dest, que):
    if av.errores:
        print(f'{que}: no se construyó. Corrija en negocio.json:')
        for i, t in enumerate(av.errores, 1):
            print(f'  {i}. {t}')
        return 1
    print(f'{que}: lista en {dest}')
    for i, t in enumerate(av.avisos, 1):
        print(f'  aviso {i}. {t}')
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Arma la página de lanzamiento desde negocio.json')
    ap.add_argument('negocio')
    ap.add_argument('--salida')
    a = ap.parse_args()
    dest, av = construir(a.negocio, a.salida)
    sys.exit(imprimir(av, dest, 'Página'))
