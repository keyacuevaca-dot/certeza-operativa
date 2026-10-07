#!/usr/bin/env python3
"""Genera el sitio de Comercializadora Robles.

Entrada : datos/catalogo.csv, src/ (css, js, iconos)
Salida  : dist/  (sitio estático, una carpeta por ruta)
          robles-portatil.html  (todo en un solo archivo, se abre con doble clic)

Uso: python3 scripts/build.py          (vista de revisión: noindex y cinta)
     python3 scripts/build.py --publicar   (sin cinta, indexable, con dominio y canonical)
Solo requiere Python 3.8+. No instala nada ni usa la red."""
import base64, csv, html, json, shutil, sys, urllib.parse
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PUBLICAR = '--publicar' in sys.argv
REVISION = not PUBLICAR

N = dict(
    nombre='Comercializadora Robles',
    calle='Juárez 43', colonia='Centro', cp='63830', ciudad='Santa María del Oro', estado='Nayarit',
    tel='311 910 4468', tel_href='+523119104468', wa='523119104468',
    correo='comercializadorarobles85@gmail.com',      # publicación aprobada por el negocio (7-oct-2026)
    dominio='comercializadorarobles.mx',
)
DIRECCION = '%s, colonia %s, %s, %s' % (N['calle'], N['colonia'], N['ciudad'], N['estado'])
HORARIO = [('Lunes a viernes', '9:00 a 14:00 y de 16:00 a 18:30'), ('Sábado', '9:00 a 13:00')]   # domingo: no se publica
LINEAS = [
    dict(slug='construccion', nombre='Construcción'),
    dict(slug='limpieza', nombre='Limpieza'),
    dict(slug='papeleria', nombre='Papelería'),
]
E = html.escape


def wa(msg):
    return 'https://wa.me/%s?text=%s' % (N['wa'], urllib.parse.quote(msg, safe=''))


WA_GENERAL = wa('Hola, quiero cotizar en Comercializadora Robles.')
WA_LISTA = wa('Hola, quiero cotizar esta lista:')
MAPS = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote('%s, %s, %s, México' % (N['calle'] + ' Col. ' + N['colonia'], N['ciudad'], N['estado']))

# ---------------------------------------------------------------- datos
def leer_catalogo():
    filas = list(csv.DictReader(open(RAIZ / 'datos/catalogo.csv', encoding='utf-8-sig')))
    ids = [f['id'] for f in filas]
    assert len(ids) == len(set(ids)), 'ids repetidos en catalogo.csv'
    out = []
    for f in filas:
        assert f['linea'] in {l['slug'] for l in LINEAS}, 'línea desconocida: ' + f['linea']
        out.append(dict(id=f['id'], linea=f['linea'], sub=f['subcategoria'], nombre=f['producto'], marca=f['marca'],
                        pres=f['presentacion'], precio=f['precio_mxn'], unidad=f['unidad_del_precio'], iva=f['iva_incluido'],
                        vigencia=f['vigencia_hasta'], foto=f['foto'], icono=f['icono'] or 'caja',
                        orden=int(f['orden'] or 0), activo=f['activo'] or 'sí'))
    return out


CATALOGO = leer_catalogo()
CATALOGO_JS = ('/* Generado desde datos/catalogo.csv. Reemplaza solo este archivo para actualizar el catálogo. */\n'
               'window.ROBLES_LINEAS=%s;\nwindow.ROBLES_CATALOGO=%s;\n') % (
    json.dumps(LINEAS, ensure_ascii=False), json.dumps(CATALOGO, ensure_ascii=False, indent=1))

SPRITE = (RAIZ / 'src/sprite.svg').read_text(encoding='utf-8')
CSS = (RAIZ / 'src/site.css').read_text(encoding='utf-8')
JS = (RAIZ / 'src/site.js').read_text(encoding='utf-8')
FUENTES = [('Bricolage Grotesque', '600 800', 'BricolageGrotesque-Bold.ttf'),
           ('Instrument Sans', '400 500', 'InstrumentSans-Regular.ttf'),
           ('Instrument Sans', '600 700', 'InstrumentSans-Bold.ttf')]
FONT_DIR = Path('/mnt/skills/examples/canvas-design/canvas-fonts')
FONT_LOCAL = RAIZ / 'src/fuentes'


def ruta_fuente(nombre):
    for d in (FONT_LOCAL, FONT_DIR):
        if (d / nombre).exists():
            return d / nombre
    raise SystemExit('Falta la fuente ' + nombre)


def css_fuentes(modo):
    out = ''
    for fam, peso, arch in FUENTES:
        if modo == 'portatil':
            src = 'url(data:font/ttf;base64,%s)' % base64.b64encode(ruta_fuente(arch).read_bytes()).decode()
        else:
            src = 'url(../fonts/%s)' % arch
        out += '@font-face{font-family:"%s";font-weight:%s;font-style:normal;font-display:swap;src:%s format("truetype")}\n' % (fam, peso, src)
    return out


# ---------------------------------------------------------------- contexto de enlaces
class Ctx:
    def __init__(self, modo, ruta):
        self.modo, self.ruta, self.prof = modo, ruta, ruta.count('/')

    def L(self, destino):
        if self.modo == 'portatil':
            return '#/' + destino
        return '../' * self.prof + (destino + 'index.html')

    def ancla(self, id_, texto, cls=''):
        c = (' class="%s"' % cls) if cls else ''
        return '<a%s href="#%s" data-ancla="%s">%s</a>' % (c, id_, id_, texto)

    def asset(self, p):
        return '../' * self.prof + 'assets/' + p


def ico(id_, cls='ico'):
    return '<svg class="%s" aria-hidden="true"><use href="#i-%s"/></svg>' % (cls, id_)


def boton_wa(url, texto, cls=''):
    return '<a class="btn%s" href="%s" target="_blank" rel="noopener noreferrer">%s%s</a>' % ((' ' + cls) if cls else '', url, ico('wa'), texto)


# ---------------------------------------------------------------- piezas comunes
PLANO = '''<svg class="plano" viewBox="0 0 560 440" aria-hidden="true" focusable="false">
<defs><pattern id="rej" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#00A9E9" stroke-opacity=".28" stroke-width="1"/></pattern></defs>
<rect x="6" y="6" width="548" height="428" rx="20" fill="#fff"/><rect x="6" y="6" width="548" height="428" rx="20" fill="url(#rej)" stroke="none"/><rect x="6" y="6" width="548" height="428" rx="20"/>
<path d="M130 172 260 70 390 172" stroke="#F48F07" stroke-width="7"/>
<path d="M156 160v130h208V160" stroke-width="6"/>
<rect x="228" y="214" width="64" height="76" stroke-width="5"/><path d="M280 252h.01" stroke-width="7"/>
<rect x="172" y="196" width="40" height="40" stroke-width="4.5"/><rect x="308" y="196" width="40" height="40" stroke-width="4.5"/>
<path d="M172 216h40M192 196v40M308 216h40M328 196v40" stroke-width="2" stroke-opacity=".55"/>
<path d="M40 290H520" stroke-width="3"/>
<g transform="translate(0 0)">
<use href="#i-pico" x="46" y="304" width="76" height="76"/><use href="#i-pala" x="140" y="304" width="76" height="76"/><use href="#i-caja" x="234" y="304" width="76" height="76"/>
<use href="#i-botella" x="328" y="304" width="76" height="76"/><use href="#i-escoba" x="422" y="304" width="76" height="76"/></g>
<path d="M46 402H498M46 394v16M498 394v16" stroke-width="2" stroke="#F48F07"/>
<text x="272" y="424" text-anchor="middle" font-size="15" font-weight="600" letter-spacing=".5">Construcción · Limpieza · Papelería</text>
</svg>'''

ICONOS_LINEA = {'construccion': ['pico', 'pala', 'desarmador', 'caja'], 'limpieza': ['botella', 'escoba', 'rollo', 'jabon'], 'papeleria': ['cuaderno']}
DESC_LINEA = {
    'construccion': 'Herramienta manual, discos de corte, afiladores y selladores. ¿Buscas un material para tu obra? Pregúntanos por WhatsApp.',
    'limpieza': 'Papel, cloro y aromas, jabones, utensilios e insecticidas para tu casa o negocio.',
    'papeleria': 'Cuéntanos qué necesitas y te decimos si lo tenemos.',
}


def cabecera_sitio(c, actual):
    def cur(prefijo):
        return ' aria-current="page"' if (actual == '' and prefijo == '') or (prefijo and actual.startswith(prefijo)) else ''
    sub = ''.join('<li><a href="%s" data-nav="catalogo/%s/"%s>%s</a></li>' % (c.L('catalogo/%s/' % l['slug']), l['slug'], cur('catalogo/%s/' % l['slug']), l['nombre']) for l in LINEAS)
    mov = ''.join('<li><a href="%s">%s</a></li>' % (c.L('catalogo/%s/' % l['slug']), l['nombre']) for l in LINEAS)
    cinta = '<div class="cinta" role="note">Vista previa para revisión · todavía no está publicada</div>' if REVISION else ''
    return '''%s
<header class="enc"><div class="wrap">
 <a class="marca" href="%s" aria-label="%s, inicio">%s<span><b>ROBLES</b><small>Comercializadora</small></span></a>
 <nav class="nav" aria-label="Principal"><ul>
  <li class="menu-d"><a href="%s" data-nav="catalogo/"%s>Catálogo</a><button type="button" class="sub" aria-expanded="false" aria-controls="panel-cat" aria-label="Mostrar las líneas del catálogo">%s</button>
   <ul class="panel" id="panel-cat">%s</ul></li>
  <li><a href="%s" data-nav="como-comprar/"%s>Cómo comprar</a></li>
  <li><a href="%s" data-nav="visitanos/"%s>Visítanos</a></li>
 </ul></nav>
 %s
 <button type="button" class="btn-menu" id="btn-menu" aria-expanded="false" aria-controls="movil">%sMenú</button>
</div>
<div class="movil" id="movil"><div class="wrap"><ul>
 <li><a href="%s">Inicio</a></li>
 <li><a href="%s">Catálogo</a><ul>%s</ul></li>
 <li><a href="%s">Cómo comprar</a></li>
 <li><a href="%s">Visítanos</a></li>
</ul>%s</div></div></header>''' % (
        cinta, c.L(''), N['nombre'], ico('casa'),
        c.L('catalogo/'), cur('catalogo/') if not actual.startswith('catalogo/') or actual == 'catalogo/' else ' aria-current="true"', ico('chev'), sub,
        c.L('como-comprar/'), cur('como-comprar/'), c.L('visitanos/'), cur('visitanos/'),
        boton_wa(WA_GENERAL, 'Cotiza por WhatsApp', 'cta-d'), ico('menu'),
        c.L(''), c.L('catalogo/'), mov, c.L('como-comprar/'), c.L('visitanos/'), boton_wa(WA_GENERAL, 'Cotiza por WhatsApp'))


def horario_tabla():
    return '<table class="horario"><caption class="sr">Horario de atención</caption><tbody>%s</tbody></table>' % ''.join(
        '<tr><th scope="row">%s</th><td>%s</td></tr>' % (d, h) for d, h in HORARIO)


def pie_sitio(c):
    cat = ''.join('<li><a href="%s">%s</a></li>' % (c.L('catalogo/%s/' % l['slug']), l['nombre']) for l in LINEAS)
    ext = ' · Vista previa de revisión: no está publicada.' if REVISION else ''
    return '''<footer class="pie"><div class="wrap"><div class="cols">
 <div><a class="marca" href="%s" aria-label="%s, inicio">%s<span><b>ROBLES</b><small>Comercializadora</small></span></a>
  <p>Materiales de construcción, limpieza y papelería en %s, %s.</p></div>
 <div><h2>Catálogo</h2><ul><li><a href="%s">Todo el catálogo</a></li>%s</ul></div>
 <div><h2>Cómo comprar</h2><ul><li><a href="%s">Solicitar cotización</a></li><li><a href="%s">Formas de pago</a></li><li><a href="%s">Preguntas</a></li><li><a href="%s">Visítanos</a></li></ul></div>
 <div><h2>Contacto</h2><p>%s<br>Col. %s, %s, %s</p>
  <ul><li><a href="tel:%s">%s%s</a></li><li><a href="%s" target="_blank" rel="noopener noreferrer">%sWhatsApp</a></li><li><a href="mailto:%s">%s%s</a></li></ul></div>
</div><p class="legal">© 2026 %s. Efectivo y transferencia.%s</p></div></footer>''' % (
        c.L(''), N['nombre'], ico('casa'), N['ciudad'], N['estado'], c.L('catalogo/'), cat,
        c.L('como-comprar/'), c.L('como-comprar/'), c.L('como-comprar/'), c.L('visitanos/'),
        N['calle'], N['colonia'], N['ciudad'], N['estado'], N['tel_href'], ico('tel'), N['tel'], WA_GENERAL, ico('wa'),
        N['correo'], ico('mail'), N['correo'], N['nombre'], ext)


def utilidades():
    return '''<div class="barra" role="region" aria-label="Acciones rápidas">%s<button type="button" class="btn cont solo-js" data-abrir-lista>%sMi lista <span class="n" data-n-lista hidden>0</span></button></div>
<dialog class="lista" id="lista" aria-labelledby="t-lista"><div class="cab"><h2 id="t-lista">Mi lista</h2><button type="button" class="cerrar" aria-label="Cerrar mi lista">%s</button></div>
<div class="cuerpo"><p class="lista-vacia">Tu lista está vacía. Agrega productos del catálogo o manda tu lista directo por WhatsApp.</p><ul class="items"></ul></div>
<div class="pie-l"><a id="lista-wa" class="btn" href="#" target="_blank" rel="noopener noreferrer" aria-disabled="true">%sEnviar lista por WhatsApp</a><button type="button" class="btn cont chico-b" id="lista-vaciar" hidden>Vaciar lista</button>
<p class="chico">Tu lista se guarda solo en este dispositivo. WhatsApp abre un mensaje listo; tú decides si lo envías.</p></div></dialog>
<div id="anuncio" class="sr" role="status" aria-live="polite"></div>''' % (
        boton_wa(WA_GENERAL, 'WhatsApp', 'wa'), ico('lista'), ico('x'), ico('wa'))


def json_ld(c, ruta):
    dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    negocio = {
        '@context': 'https://schema.org', '@type': 'HardwareStore', 'name': N['nombre'],
        'address': {'@type': 'PostalAddress', 'streetAddress': N['calle'] + ', Col. ' + N['colonia'], 'addressLocality': N['ciudad'],
                    'addressRegion': N['estado'], 'postalCode': N['cp'], 'addressCountry': 'MX'},
        'telephone': '+52 ' + N['tel'], 'email': N['correo'], 'paymentAccepted': 'Efectivo, Transferencia',
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': dias, 'opens': '09:00', 'closes': '14:00'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': dias, 'opens': '16:00', 'closes': '18:30'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Saturday', 'opens': '09:00', 'closes': '13:00'}]}
    if PUBLICAR:
        negocio['url'] = 'https://%s/' % N['dominio']
    bloques = [negocio]
    if ruta == 'como-comprar/':
        bloques.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in FAQ]})
    return ''.join('<script type="application/ld+json">%s</script>' % json.dumps(b, ensure_ascii=False) for b in bloques)


# ---------------------------------------------------------------- contenido
FAQ = [
    ('¿Cómo pido una cotización?', 'Escríbenos por WhatsApp. Puedes mandar un producto, tu lista completa o una foto de tu lista, adjuntándola desde el chat.'),
    ('¿Cómo puedo pagar?', 'En efectivo o por transferencia.'),
    ('¿Dónde están y a qué hora abren?', '%s. Lunes a viernes de 9:00 a 14:00 y de 16:00 a 18:30; sábado de 9:00 a 13:00.' % DIRECCION),
    ('¿Cuánto cuesta un producto?', 'Los precios te los damos por WhatsApp. Cuando publiquemos un precio, verás hasta qué fecha vale.'),
    ('¿Hacen entregas o dan factura?', 'Todavía no publicamos esa información. Pregúntanos por WhatsApp antes de venir.'),
    ('¿Tienen existencia de un producto?', 'No publicamos existencias. Pregúntanos por WhatsApp y te decimos.'),
]


def cabecera_pagina(c, migas, h1, texto, extra=''):
    m = ''.join('<li>%s</li>' % ('<a href="%s">%s</a>' % (c.L(r), t) if r is not None else '<span aria-current="page">%s</span>' % t) for t, r in migas)
    return '<div class="cabecera"><div class="wrap"><nav aria-label="Ruta de navegación"><ol class="migas">%s</ol></nav><h1>%s</h1><p>%s</p>%s</div></div>' % (m, h1, texto, extra)


def buscador(id_, cont):
    return '<div class="buscador">%s<label class="sr" for="%s">Buscar un producto</label><input id="%s" type="search" placeholder="Buscar un producto" autocomplete="off" data-en="%s"></div>' % (ico('lupa'), id_, id_, cont)


def p_inicio(c):
    lineas = ''
    for i, l in enumerate(LINEAS):
        s = l['slug']
        iconos = ''.join(ico(x) for x in ICONOS_LINEA[s])
        if s == 'papeleria':
            enlace = boton_wa(wa('Hola, quiero cotizar en papelería:'), 'Cotiza por WhatsApp', 'chico-b')
        else:
            enlace = '<a class="enlace" href="%s"><span>Ver %s</span>%s</a>' % (c.L('catalogo/%s/' % s), l['nombre'].lower(), ico('flecha'))
        lineas += '<article class="linea%s"><div class="iconos" aria-hidden="true">%s</div><h3>%s</h3><p>%s</p>%s</article>' % (
            ' grande' if s == 'construccion' else '', iconos, l['nombre'], DESC_LINEA[s], enlace)
    destacados = [i for i in CATALOGO if i['linea'] == 'construccion'][:6] + [i for i in CATALOGO if i['linea'] == 'limpieza'][:6]
    chips = ''.join('<li><a href="%s">%s%s</a></li>' % (c.L('catalogo/%s/' % i['linea']), ico(i['icono']), E(i['nombre'])) for i in destacados)
    attrs = ' '.join('data-href-%s="%s"' % (l['slug'], c.L('catalogo/%s/' % l['slug'])) for l in LINEAS)
    pasos = [('Elige o manda tu lista', 'Agrega productos del catálogo o escribe tu lista en WhatsApp.'),
             ('Pide tu precio', 'Revisamos tu lista y te respondemos por WhatsApp con el precio.'),
             ('Confirma con la tienda', 'Cuando todo esté claro, confirma tu pedido y paga en efectivo o por transferencia.')]
    return '''<section class="heroe"><div class="wrap"><div>
<h1>Materiales de construcción, limpieza y papelería en <u>Santa María del Oro</u></h1>
<p class="sub">Dinos qué necesitas y te cotizamos por WhatsApp. Elige productos del catálogo o manda tu lista como prefieras.</p>
<div class="grupo">%s<a class="btn cont" href="%s">Ver catálogo</a></div></div>%s</div></section>
<div class="hechos"><ul class="wrap"><li>%s%s, Centro</li><li>%sLunes a sábado</li><li>%sEfectivo y transferencia</li></ul></div>
<section class="sec"><div class="wrap"><div class="intro"><h2>Lo que manejamos</h2><p>Tres líneas en un solo lugar. Elige una para ver lo que hay, o escríbenos lo que buscas.</p></div><div class="lineas">%s</div></div></section>
<section class="sec gris"><div class="wrap"><div class="intro"><h2>Algunos de nuestros productos</h2><p>Toca uno para verlo en el catálogo. Los precios te los damos por WhatsApp.</p></div>
<ul class="chips" data-chips %s>%s</ul></div></section>
<section class="banda"><div class="wrap"><div><h2>¿Ya tienes tu lista?</h2><p>Mándala por WhatsApp como la tengas: escríbela, pégala o adjunta una foto desde el chat. También puedes armarla aquí y enviarla con un toque.</p></div>
<div class="grupo">%s<button type="button" class="btn cont solo-js" data-abrir-lista>%sArmar mi lista aquí</button></div></div></section>
<section class="sec"><div class="wrap"><div class="intro"><h2>Así cotizas</h2></div><ol class="pasos">%s</ol></div></section>
<section class="sec gris" id="tienda"><div class="wrap"><div class="tienda"><div><h2>Visítanos</h2><ul class="datos">
<li>%s<span><b>Dirección</b>%s<br>Col. %s, %s, %s</span></li>
<li>%s<span><b>Teléfono y WhatsApp</b><a href="tel:%s">%s</a></span></li></ul>
<div class="grupo"><a class="btn" href="%s" target="_blank" rel="noopener noreferrer">%sCómo llegar</a><a class="btn cont" href="%s">Más datos de la tienda</a></div></div>
<div><h3>Horario</h3>%s<p class="chico" style="margin-top:12px">Pago: efectivo y transferencia.</p></div></div></div></section>''' % (
        boton_wa(WA_GENERAL, 'Cotiza por WhatsApp'), c.L('catalogo/'), PLANO,
        ico('pin'), N['calle'], ico('reloj'), ico('pago'), lineas, attrs, chips,
        boton_wa(WA_LISTA, 'Enviar mi lista por WhatsApp', 'claro'), ico('lista'),
        ''.join('<li><h3>%s</h3><p>%s</p></li>' % (t, d) for t, d in pasos),
        ico('pin'), N['calle'], N['colonia'], N['ciudad'], N['estado'], ico('tel'), N['tel_href'], N['tel'], MAPS, ico('pin'), c.L('visitanos/'), horario_tabla())


AVISO_CAT = '<div class="aviso"><p><b>Estamos completando el catálogo.</b> Si no ves lo que buscas, pregúntanos por WhatsApp y te decimos si lo tenemos.</p><p>%s</p></div>'


def p_catalogo(c):
    cab = cabecera_pagina(c, [('Inicio', ''), ('Catálogo', None)], 'Catálogo',
                          'Productos por línea. Busca por nombre, agrega a tu lista o cotiza directo por WhatsApp; el precio te lo damos en el chat.')
    return cab + '<section class="sec"><div class="wrap">%s<div id="cat-todos" data-catalogo="todos"></div>%s</div></section>' % (
        buscador('buscar-todos', 'cat-todos'), AVISO_CAT % boton_wa(WA_GENERAL, 'Cotiza por WhatsApp', 'chico-b'))


def p_linea(slug):
    l = [x for x in LINEAS if x['slug'] == slug][0]
    textos = {'construccion': 'Herramienta manual, corte y afilado, y selladores. Si necesitas materiales para tu obra, pregúntanos por WhatsApp.',
              'limpieza': 'Papel y desechables, cloro y aromas, jabones, utensilios e insecticidas.',
              'papeleria': 'Todavía no publicamos productos de esta línea. Escríbenos qué necesitas.'}

    def f(c):
        cab = cabecera_pagina(c, [('Inicio', ''), ('Catálogo', 'catalogo/'), (l['nombre'], None)], l['nombre'], textos[slug])
        busc = '' if slug == 'papeleria' else buscador('buscar-' + slug, 'cat-' + slug)
        extra = '' if slug == 'papeleria' else AVISO_CAT % boton_wa(WA_GENERAL, 'Cotiza por WhatsApp', 'chico-b')
        return cab + '<section class="sec"><div class="wrap">%s<div id="cat-%s" data-catalogo="%s"></div>%s</div></section>' % (busc, slug, slug, extra)
    return f


def p_como_comprar(c):
    sub = '<ul class="subnav" aria-label="En esta página"><li>%s</li><li>%s</li><li>%s</li></ul>' % (
        c.ancla('solicitar-cotizacion', 'Solicitar cotización'), c.ancla('formas-de-pago', 'Formas de pago'), c.ancla('preguntas', 'Preguntas'))
    cab = cabecera_pagina(c, [('Inicio', ''), ('Cómo comprar', None)], 'Cómo comprar', 'Cotizas por WhatsApp, confirmas con la tienda y pagas en efectivo o por transferencia.', sub)
    pasos = [('Elige o manda tu lista', 'Agrega productos del catálogo a tu lista, o escribe tu lista directo en WhatsApp. Si tienes una foto de tu lista, adjúntala desde el chat.'),
             ('Pide tu precio', 'Te respondemos por WhatsApp con el precio de lo que pediste.'),
             ('Confirma con la tienda', 'Cuando todo esté claro, confirma tu pedido. WhatsApp solo abre un mensaje: tú decides si lo envías.')]
    faq = ''.join('<details><summary>%s%s</summary><p>%s</p></details>' % (E(q), ico('chev'), E(r)) for q, r in FAQ)
    return cab + '''<section class="sec" id="solicitar-cotizacion"><div class="wrap"><div class="intro"><h2>Solicitar cotización</h2><p>Tres pasos, sin registrarte ni crear una cuenta.</p></div>
<ol class="pasos">%s</ol><div class="grupo" style="margin-top:24px">%s<a class="btn cont" href="%s">Ver catálogo</a></div></div></section>
<section class="sec gris" id="formas-de-pago"><div class="wrap"><div class="intro"><h2>Formas de pago</h2><p>Aceptamos <b>efectivo</b> y <b>transferencia</b>. No publicamos datos bancarios en este sitio: pídelos a la tienda al confirmar tu pedido.</p></div></div></section>
<section class="sec" id="preguntas"><div class="wrap"><div class="intro"><h2>Preguntas</h2></div><div class="preguntas">%s</div>
<div class="aviso"><p>¿Tienes otra duda? Escríbenos por WhatsApp.</p><p>%s</p></div></div></section>''' % (
        ''.join('<li><h3>%s</h3><p>%s</p></li>' % (t, d) for t, d in pasos), boton_wa(WA_LISTA, 'Enviar mi lista por WhatsApp'), c.L('catalogo/'), faq,
        boton_wa(WA_GENERAL, 'Cotiza por WhatsApp', 'chico-b'))


def p_visitanos(c):
    sub = '<ul class="subnav" aria-label="En esta página"><li>%s</li><li>%s</li><li>%s</li></ul>' % (
        c.ancla('ubicacion', 'Ubicación'), c.ancla('horario', 'Horario'), c.ancla('contacto', 'Contacto'))
    cab = cabecera_pagina(c, [('Inicio', ''), ('Visítanos', None)], 'Visítanos', 'Estamos en el centro de %s. Aquí están la dirección, el horario y cómo escribirnos.' % N['ciudad'], sub)
    return cab + '''<section class="sec" id="ubicacion"><div class="wrap"><div class="dos"><div><h2>Ubicación</h2>
<ul class="datos"><li>%s<span><b>Dirección</b>%s<br>Col. %s, C.P. %s<br>%s, %s</span></li></ul>
<div class="grupo"><a class="btn" href="%s" target="_blank" rel="noopener noreferrer">%sCómo llegar</a></div>
<p class="chico" style="margin-top:12px">El botón abre tu aplicación de mapas con esta dirección.</p></div>
<div class="aviso"><p><b>Antes de venir</b>, puedes escribirnos por WhatsApp para preguntar por un producto.</p></div></div></div></section>
<section class="sec gris" id="horario"><div class="wrap"><h2>Horario</h2><div style="max-width:560px">%s</div></div></section>
<section class="sec" id="contacto"><div class="wrap"><h2>Contacto</h2><ul class="datos">
<li>%s<span><b>Teléfono</b><a href="tel:%s">%s</a></span></li>
<li>%s<span><b>WhatsApp</b><a href="%s" target="_blank" rel="noopener noreferrer">%s</a></span></li>
<li>%s<span><b>Correo</b><a href="mailto:%s">%s</a></span></li></ul>
<div class="grupo">%s</div></div></section>''' % (
        ico('pin'), N['calle'], N['colonia'], N['cp'], N['ciudad'], N['estado'], MAPS, ico('pin'), horario_tabla(),
        ico('tel'), N['tel_href'], N['tel'], ico('wa'), WA_GENERAL, N['tel'], ico('mail'), N['correo'], N['correo'],
        boton_wa(WA_GENERAL, 'Cotiza por WhatsApp'))


PAGINAS = [  # ruta, título, descripción, función
    ('', 'Comercializadora Robles · Materiales de construcción, limpieza y papelería en Santa María del Oro', 'Materiales de construcción, limpieza y papelería en Santa María del Oro, Nayarit. Cotiza por WhatsApp: elige productos o manda tu lista.', p_inicio),
    ('catalogo/', 'Catálogo · Comercializadora Robles', 'Catálogo de Comercializadora Robles: construcción, limpieza y papelería. Busca un producto y cotízalo por WhatsApp.', p_catalogo),
    ('catalogo/construccion/', 'Construcción · Comercializadora Robles', 'Herramienta manual, discos de corte, afiladores y selladores. Cotiza por WhatsApp.', p_linea('construccion')),
    ('catalogo/limpieza/', 'Limpieza · Comercializadora Robles', 'Papel, cloro y aromas, jabones, utensilios e insecticidas. Cotiza por WhatsApp.', p_linea('limpieza')),
    ('catalogo/papeleria/', 'Papelería · Comercializadora Robles', 'Papelería: escríbenos qué necesitas y te decimos si lo tenemos.', p_linea('papeleria')),
    ('como-comprar/', 'Cómo comprar · Comercializadora Robles', 'Cómo cotizar y comprar: manda tu lista por WhatsApp, confirma con la tienda y paga en efectivo o por transferencia.', p_como_comprar),
    ('visitanos/', 'Visítanos · Comercializadora Robles', 'Dirección, horario y contacto de Comercializadora Robles en Santa María del Oro, Nayarit.', p_visitanos),
]

FAVICON = 'data:image/svg+xml,' + urllib.parse.quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 24 24 6l21 18" stroke="#F48F07"/><path d="M9 21v22h30V21M20 43V31h8v12" stroke="#174F7C"/></svg>')


def head(c, ruta, titulo, desc):
    robots = '<meta name="robots" content="noindex,nofollow">' if REVISION else ''
    canon = '' if REVISION else '<link rel="canonical" href="https://%s/%s">' % (N['dominio'], ruta)
    og = '<meta property="og:type" content="website"><meta property="og:locale" content="es_MX"><meta property="og:site_name" content="%s"><meta property="og:title" content="%s"><meta property="og:description" content="%s">' % (N['nombre'], E(titulo), E(desc))
    return '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><meta name="description" content="%s"><meta name="theme-color" content="#174F7C">%s%s%s<link rel="icon" href="%s">' % (E(titulo), E(desc), robots, canon, og, FAVICON)


# ---------------------------------------------------------------- salida
def escribir(ruta_arch, texto):
    ruta_arch.parent.mkdir(parents=True, exist_ok=True)
    ruta_arch.write_text(texto, encoding='utf-8')


def construir_dist():
    dist = RAIZ / 'dist'
    if dist.exists():
        shutil.rmtree(dist)
    (dist / 'assets/css').mkdir(parents=True); (dist / 'assets/js').mkdir(parents=True); (dist / 'assets/fonts').mkdir(parents=True)
    for _, _, arch in FUENTES:
        shutil.copy(ruta_fuente(arch), dist / 'assets/fonts' / arch)
    for f in (RAIZ / 'licencias').glob('*.txt'):
        shutil.copy(f, dist / 'assets/fonts' / f.name)
    escribir(dist / 'assets/css/site.css', css_fuentes('dist') + CSS)
    escribir(dist / 'assets/js/site.js', JS)
    escribir(dist / 'assets/js/catalogo.js', CATALOGO_JS)
    for ruta, titulo, desc, fn in PAGINAS:
        c = Ctx('dist', ruta)
        cuerpo = fn(c)
        pagina = '''<!doctype html><html lang="es-MX"><head>%s<link rel="stylesheet" href="%s">%s</head><body>
<a class="saltar" href="#contenido">Saltar al contenido</a>%s%s<main id="contenido">%s</main>%s%s
<noscript><div class="wrap"><p class="aviso">Para ver el catálogo necesitas activar JavaScript. Mientras tanto, cotiza por WhatsApp: %s</p></div></noscript>
<script src="%s"></script><script src="%s"></script></body></html>''' % (
            head(c, ruta, titulo, desc), c.asset('css/site.css'), json_ld(c, ruta), SPRITE, cabecera_sitio(c, ruta), cuerpo, pie_sitio(c), utilidades(),
            boton_wa(WA_GENERAL, 'abrir WhatsApp'), c.asset('js/catalogo.js'), c.asset('js/site.js'))
        escribir(dist / (ruta + 'index.html'), pagina)
    c = Ctx('dist', '')
    escribir(dist / '404.html', '''<!doctype html><html lang="es-MX"><head>%s<link rel="stylesheet" href="assets/css/site.css"></head><body>%s%s<main id="contenido"><section class="sec"><div class="wrap"><div class="intro"><h1>No encontramos esta página</h1><p>Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos por WhatsApp.</p></div><div class="grupo"><a class="btn" href="index.html">Ir al inicio</a>%s</div></div></section></main>%s<script src="assets/js/catalogo.js"></script><script src="assets/js/site.js"></script></body></html>''' % (
        head(c, '404', 'Página no encontrada · Comercializadora Robles', 'Página no encontrada.'), SPRITE, cabecera_sitio(c, '404'), boton_wa(WA_GENERAL, 'Cotiza por WhatsApp', 'cont'), pie_sitio(c)))
    escribir(dist / 'robots.txt', 'User-agent: *\nDisallow: /\n' if REVISION else 'User-agent: *\nAllow: /\nSitemap: https://%s/sitemap.xml\n' % N['dominio'])
    if PUBLICAR:
        urls = ''.join('<url><loc>https://%s/%s</loc></url>' % (N['dominio'], r) for r, *_ in PAGINAS if r != 'catalogo/papeleria/')
        escribir(dist / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % urls)


def construir_portatil():
    secciones = ''
    for ruta, titulo, desc, fn in PAGINAS:
        c = Ctx('portatil', ruta)
        secciones += '<div class="pagina" data-ruta="%s" data-titulo="%s" hidden>%s</div>\n' % (ruta, E(titulo), fn(c))
    c = Ctx('portatil', '')
    c_home = PAGINAS[0]
    doc = '''<!doctype html><html lang="es-MX"><head>%s<style>%s%s</style>%s</head><body>
<a class="saltar" href="#contenido" data-ancla="contenido">Saltar al contenido</a>%s%s<main id="contenido">
%s</main>%s%s
<script>window.ROBLES_PORTATIL=true;</script><script>%s</script><script>%s</script></body></html>''' % (
        head(c, '', c_home[1], c_home[2]), css_fuentes('portatil'), CSS, json_ld(c, ''), SPRITE, cabecera_sitio(c, ''), secciones, pie_sitio(c), utilidades(), CATALOGO_JS, JS)
    escribir(RAIZ / 'robles-portatil.html', doc)


if __name__ == '__main__':
    construir_dist()
    construir_portatil()
    print('Listo: dist/ (%d páginas + 404) y robles-portatil.html (%d KB). Modo: %s. Productos: %d.' % (
        len(PAGINAS), (RAIZ / 'robles-portatil.html').stat().st_size // 1024, 'PUBLICAR' if PUBLICAR else 'revisión', len(CATALOGO)))
