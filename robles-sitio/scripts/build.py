#!/usr/bin/env python3
"""Genera el sitio de Comercializadora Robles.

Entrada : datos/catalogo.csv, src/ (css, js, iconos)
Salida  : dist/  (sitio estático, una carpeta por ruta)
          robles-portatil.html  (todo en un solo archivo, se abre con doble clic)

Uso: python3 scripts/build.py              (vista de revisión: cinta y noindex)
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
MARCAS_EXTRA = ['Truper']      # el negocio la mencionó como marca que maneja; aún sin producto asignado
LINEAS = [
    dict(slug='construccion', nombre='Construcción'),
    dict(slug='limpieza', nombre='Limpieza'),
    dict(slug='papeleria', nombre='Papelería'),
]
DESC_LINEA = {
    'construccion': 'Herramienta manual, corte y afilado, y selladores. ¿Buscas un material para tu obra? Pregúntanos por WhatsApp.',
    'limpieza': 'Papel y desechables, cloro y aromas, jabones, utensilios e insecticidas para tu casa o negocio.',
    'papeleria': 'Todavía no publicamos productos de esta línea. Cuéntanos qué necesitas y te decimos si lo tenemos.',
}
E = html.escape


def wa(msg):
    return 'https://wa.me/%s?text=%s' % (N['wa'], urllib.parse.quote(msg, safe=''))


WA_GENERAL = wa('Hola, quiero cotizar en Comercializadora Robles.')
MAPS = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote('%s Col. %s, %s, %s, México' % (N['calle'], N['colonia'], N['ciudad'], N['estado']))

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
                        vigencia=f['vigencia_hasta'], foto=f['foto'], icono=f['icono'] or '',
                        orden=int(f['orden'] or 0), activo=f['activo'] or 'sí'))
    return out


CATALOGO = leer_catalogo()
CATALOGO_JS = ('/* Generado desde datos/catalogo.csv. Reemplaza solo este archivo para actualizar el catálogo. */\n'
               'window.ROBLES_LINEAS=%s;\nwindow.ROBLES_CATALOGO=%s;\n') % (
    json.dumps(LINEAS, ensure_ascii=False), json.dumps(CATALOGO, ensure_ascii=False, indent=1))
ACTIVOS = [i for i in CATALOGO if i['activo'].lower() != 'no']
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
            return '#' + (destino.rstrip('/').replace('/', '~') or 'inicio')
        return '../' * self.prof + (destino + 'index.html')

    def ancla(self, id_, texto):
        return f'<a href="#{id_}" data-ancla="{id_}">{texto}</a>'

    def asset(self, p):
        return '../' * self.prof + 'assets/' + p


def ico(id_):
    return f'<svg class="ico" aria-hidden="true"><use href="#i-{id_}"/></svg>'


def boton_wa(url, texto, cls=''):
    c = ('btn ' + cls).strip()
    return f'<a class="{c}" href="{url}" target="_blank" rel="noopener noreferrer">{ico("wa")}{texto}</a>'


def pl(n, uno, varios):
    return '%d %s' % (n, uno if n == 1 else varios)


def lineas_activas():
    out = []
    for l in LINEAS:
        prods = [i for i in ACTIVOS if i['linea'] == l['slug']]
        subs = []
        for p in prods:
            if p['sub'] not in subs:
                subs.append(p['sub'])
        out.append((l, prods, subs))
    return out


def attrs_href(c):
    return ' '.join(f'data-href-{l["slug"]}="{c.L("catalogo/%s/" % l["slug"])}"' for l in LINEAS)


def buscador_form(c, id_, placeholder):
    return (f'<form class="busca" role="search" data-busqueda data-destino="{c.L("catalogo/")}">'
            f'<label class="sr" for="{id_}">Buscar un producto</label>{ico("lupa")}'
            f'<input id="{id_}" name="q" type="search" placeholder="{placeholder}" autocomplete="off"></form>')


# ---------------------------------------------------------------- piezas comunes
def cabecera_sitio(c, actual):
    def cur(prefijo):
        return ' aria-current="page"' if (actual == '' and prefijo == '') or (prefijo and actual.startswith(prefijo)) else ''
    cat_cur = ' aria-current="page"' if actual == 'catalogo/' else (' aria-current="true"' if actual.startswith('catalogo/') else '')
    sub = ''.join(f'<li><a href="{c.L("catalogo/%s/" % l["slug"])}" data-nav="catalogo/{l["slug"]}/"{cur("catalogo/%s/" % l["slug"])}>{l["nombre"]}</a></li>' for l in LINEAS)
    mov = ''.join(f'<li><a href="{c.L("catalogo/%s/" % l["slug"])}">{l["nombre"]}</a></li>' for l in LINEAS)
    cinta = '<div class="cinta" role="note">Vista previa para revisión · todavía no está publicada</div>' if REVISION else ''
    return f'''{cinta}
<div class="util"><div class="wrap">
 <span>{ico("pin")}{N["calle"]}, Col. {N["colonia"]} · {N["ciudad"]}, {N["estado"]}</span>
 <span>{ico("reloj")}Lun a vie 9:00–14:00 y 16:00–18:30 · Sáb 9:00–13:00</span>
 <span>{ico("tel")}<a href="tel:{N["tel_href"]}">{N["tel"]}</a></span>
</div></div>
<header class="enc"><div class="wrap">
 <a class="marca" href="{c.L("")}" aria-label="{N["nombre"]}, inicio">{ico("casa")}<span><b>ROBLES</b><small>Comercializadora</small></span></a>
 <nav class="nav" aria-label="Principal"><ul>
  <li class="menu-d"><a href="{c.L("catalogo/")}" data-nav="catalogo/"{cat_cur}>Catálogo</a><button type="button" class="sub" aria-expanded="false" aria-controls="panel-cat" aria-label="Mostrar las líneas del catálogo">{ico("chev")}</button>
   <ul class="panel" id="panel-cat">{sub}</ul></li>
  <li><a href="{c.L("como-comprar/")}" data-nav="como-comprar/"{cur("como-comprar/")}>Cómo comprar</a></li>
  <li><a href="{c.L("visitanos/")}" data-nav="visitanos/"{cur("visitanos/")}>Visítanos</a></li>
 </ul></nav>
 <form class="busca busca-h" role="search" data-busqueda data-destino="{c.L("catalogo/")}"><label class="sr" for="busca-h">Buscar un producto</label>{ico("lupa")}<input id="busca-h" name="q" type="search" placeholder="Buscar" autocomplete="off"></form>
 <button type="button" class="btn cont compacto btn-lista lista-d solo-js" data-abrir-lista>{ico("lista")}Mi lista <span class="n" data-n-lista hidden>0</span></button>
 {boton_wa(WA_GENERAL, "Cotiza por WhatsApp", "cta-d compacto")}
 <button type="button" class="btn-menu" id="btn-menu" aria-expanded="false" aria-controls="movil">{ico("menu")}Menú</button>
</div>
<div class="movil" id="movil"><div class="wrap">
 <form class="busca" role="search" data-busqueda data-destino="{c.L("catalogo/")}"><label class="sr" for="busca-m">Buscar un producto</label>{ico("lupa")}<input id="busca-m" name="q" type="search" placeholder="Buscar un producto" autocomplete="off"></form>
 <ul><li><a href="{c.L("")}">Inicio</a></li><li><a href="{c.L("catalogo/")}">Catálogo</a><ul>{mov}</ul></li>
 <li><a href="{c.L("como-comprar/")}">Cómo comprar</a></li><li><a href="{c.L("visitanos/")}">Visítanos</a></li></ul>
 {boton_wa(WA_GENERAL, "Cotiza por WhatsApp")}</div></div></header>'''


def horario_tabla():
    filas = ''.join(f'<tr><th scope="row">{d}</th><td>{h}</td></tr>' for d, h in HORARIO)
    return f'<table class="horario"><caption class="sr">Horario de atención</caption><tbody>{filas}</tbody></table>'


def pie_sitio(c):
    cat = ''.join(f'<li><a href="{c.L("catalogo/%s/" % l["slug"])}">{l["nombre"]}</a></li>' for l in LINEAS)
    ext = ' · Vista previa de revisión: no está publicada.' if REVISION else ''
    return f'''<footer class="pie"><div class="wrap"><div class="cols">
 <div><a class="marca" href="{c.L("")}" aria-label="{N["nombre"]}, inicio">{ico("casa")}<span><b>ROBLES</b><small>Comercializadora</small></span></a>
  <p>Materiales de construcción, limpieza y papelería en {N["ciudad"]}, {N["estado"]}.</p></div>
 <nav aria-label="Catálogo"><h2>Catálogo</h2><ul><li><a href="{c.L("catalogo/")}">Todo el catálogo</a></li>{cat}</ul></nav>
 <nav aria-label="Cómo comprar"><h2>Cómo comprar</h2><ul><li><a href="{c.L("como-comprar/")}">Solicitar cotización</a></li><li><a href="{c.L("como-comprar/")}">Formas de pago</a></li><li><a href="{c.L("como-comprar/")}">Preguntas</a></li><li><a href="{c.L("visitanos/")}">Visítanos</a></li></ul></nav>
 <div><h2>Contacto</h2><p>{N["calle"]}, Col. {N["colonia"]}<br>{N["ciudad"]}, {N["estado"]}</p>
  <ul><li><a href="tel:{N["tel_href"]}">{ico("tel")}{N["tel"]}</a></li><li><a href="{WA_GENERAL}" target="_blank" rel="noopener noreferrer">{ico("wa")}WhatsApp</a></li><li><a href="mailto:{N["correo"]}">{ico("mail")}{N["correo"]}</a></li></ul></div>
</div><p class="legal">© 2026 {N["nombre"]}. Efectivo y transferencia.{ext}</p></div></footer>'''


def utilidades():
    return f'''<div class="barra" role="region" aria-label="Acciones rápidas">{boton_wa(WA_GENERAL, "WhatsApp")}<button type="button" class="btn cont btn-lista solo-js" data-abrir-lista>{ico("lista")}Mi lista <span class="n" data-n-lista hidden>0</span></button></div>
<dialog class="lista" id="lista" aria-labelledby="t-lista"><div class="cab"><h2 id="t-lista">Mi lista</h2><button type="button" class="cerrar" aria-label="Cerrar mi lista">{ico("x")}</button></div>
<div class="cuerpo"><p class="lista-vacia">Tu lista está vacía. Agrega productos del catálogo o manda tu lista directo por WhatsApp.</p><ul class="items"></ul></div>
<div class="pie-l"><a id="lista-wa" class="btn" href="#" target="_blank" rel="noopener noreferrer" aria-disabled="true">{ico("wa")}Enviar lista por WhatsApp</a><button type="button" class="btn cont compacto" id="lista-vaciar" hidden>Vaciar lista</button>
<p class="chico">Tu lista se guarda solo en este dispositivo. WhatsApp abre un mensaje listo; tú decides si lo envías.</p></div></dialog>
<div id="anuncio" class="sr" role="status" aria-live="polite"></div>'''


FAQ = [
    ('¿Cómo pido una cotización?', 'Escríbenos por WhatsApp. Puedes mandar un producto, tu lista completa o una foto de tu lista, adjuntándola desde el chat.'),
    ('¿Cómo puedo pagar?', 'En efectivo o por transferencia.'),
    ('¿Dónde están y a qué hora abren?', '%s. Lunes a viernes de 9:00 a 14:00 y de 16:00 a 18:30; sábado de 9:00 a 13:00.' % DIRECCION),
    ('¿Cuánto cuesta un producto?', 'Los precios te los damos por WhatsApp. Cuando publiquemos un precio, verás hasta qué fecha vale.'),
    ('¿Hacen entregas o dan factura?', 'Todavía no publicamos esa información. Pregúntanos por WhatsApp antes de venir.'),
    ('¿Tienen existencia de un producto?', 'No publicamos existencias. Pregúntanos por WhatsApp y te decimos.'),
]


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
def encabezado_sec(titulo, texto=''):
    p = f'<p>{texto}</p>' if texto else ''
    return f'<div class="enc-sec"><h2>{titulo}</h2>{p}</div>'


def cabecera_pagina(c, migas, h1, texto, extra=''):
    m = ''.join('<li>%s</li>' % (f'<a href="{c.L(r)}">{t}</a>' if r is not None else f'<span aria-current="page">{t}</span>') for t, r in migas)
    return f'<div class="cabecera"><div class="wrap"><nav aria-label="Ruta de navegación"><ol class="migas">{m}</ol></nav><h1>{h1}</h1><p>{texto}</p>{extra}</div></div>'


def p_inicio(c):
    # Líneas
    tarjetas = ''
    for n, (l, prods, subs) in enumerate(lineas_activas(), 1):
        s = l['slug']
        href = c.L(f'catalogo/{s}/')
        cuenta = pl(len(prods), 'producto', 'productos') if prods else 'Sin productos publicados'
        if prods:
            lista = ''.join(f'<li><a href="{href}">{E(x)}{ico("flecha")}</a></li>' for x in subs)
            extra = ''
            if s == 'construccion':
                extra = f'<div class="grupo fin">{boton_wa(wa("Hola, quiero cotizar materiales para obra:"), "Cotiza materiales para obra")}</div>'
            cuerpo = f'<ul>{lista}</ul>{extra}<a class="mas" href="{href}"><span>Ver {l["nombre"].lower()}</span>{ico("flecha")}</a>'
        else:
            cuerpo = f'<div class="grupo">{boton_wa(wa("Hola, quiero cotizar en papelería:"), "Cotiza por WhatsApp")}</div>'
        tarjetas += (f'<article class="linea{" principal" if s == "construccion" else ""}{"" if prods else " sin"}"><span class="num" aria-hidden="true">{n:02d}</span>'
                     f'<h3>{l["nombre"]}</h3><p class="cuenta" data-cuenta="{s}">{cuenta}</p><p>{DESC_LINEA[s]}</p>{cuerpo}</article>')
    # Índice estático (se vuelve a dibujar con los datos vigentes cuando hay JavaScript)
    grupos = []
    for i in ACTIVOS:
        g = next((x for x in grupos if x[0] == i['linea'] and x[1] == i['sub']), None)
        if not g:
            g = (i['linea'], i['sub'], [])
            grupos.append(g)
        g[2].append(i)
    indice = ''.join(f'<div><h3>{E(sb)}</h3><ul>' + ''.join(
        f'<li><a href="{c.L("catalogo/%s/" % ln)}">{E(p["nombre"])}{(" · " + E(p["pres"])) if p["pres"] else ""}</a></li>' for p in ps) + '</ul></div>' for ln, sb, ps in grupos)
    marcas = list(MARCAS_EXTRA)
    for i in ACTIVOS:
        if i['marca'] and i['marca'] not in marcas:
            marcas.append(i['marca'])
    marcas_html = ''.join(f'<li>{E(m)}</li>' for m in marcas)
    pasos = [('Elige o manda tu lista', 'Agrega productos del catálogo o escribe tu lista en WhatsApp.'),
             ('Pide tu precio', 'Revisamos tu lista y te respondemos por WhatsApp con el precio.'),
             ('Confirma con la tienda', 'Cuando todo esté claro, confirma tu pedido y paga en efectivo o por transferencia.')]
    pasos_html = ''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in pasos)
    rapido = ''.join(f'<li><a href="{c.L("catalogo/%s/" % l["slug"])}">{l["nombre"]}</a></li>' for l in LINEAS)
    return f'''<section class="heroe"><div class="wrap"><div>
<h1>Materiales de construcción, limpieza y papelería en {N["ciudad"]}</h1>
<p class="sub">Cotiza por WhatsApp: elige productos del catálogo o manda tu lista, y te respondemos con el precio.</p>
<div class="grupo">{boton_wa(WA_GENERAL, "Cotiza por WhatsApp")}<a class="btn borde-b" href="{c.L("catalogo/")}">Ver catálogo</a></div></div>
<div class="panel-busca"><h2>Busca un producto</h2><p>Escribe el nombre de lo que necesitas.</p>
{buscador_form(c, "busca-i", "Ejemplo: cloro, escobas, palas")}
<ul class="rapido">{rapido}</ul></div></div></section>
<div class="datos-b"><div class="wrap"><ul>
<li>{ico("pin")}<div><b>{N["calle"]}, Col. {N["colonia"]}</b><span>{N["ciudad"]}, {N["estado"]}</span></div></li>
<li>{ico("reloj")}<div><b>Lun a vie 9:00–14:00 y 16:00–18:30</b><span>Sábado 9:00–13:00</span></div></li>
<li>{ico("pago")}<div><b>Efectivo y transferencia</b><span>Los datos para pagar se piden a la tienda</span></div></li>
</ul></div></div>
<section class="sec"><div class="wrap">{encabezado_sec("Catálogo por línea", "Tres líneas en un solo lugar. Elige una o busca por producto.")}<div class="lineas{" con-sin" if "linea sin" in tarjetas or " sin\"" in tarjetas else ""}">{tarjetas}</div></div></section>
<section class="sec gris"><div class="wrap">{encabezado_sec("Lo que encuentras", "Productos que manejamos hoy. Si no ves el que buscas, pregúntanos por WhatsApp.")}
<div class="indice" data-indice {attrs_href(c)}>{indice}</div>
<div class="marcas"><h3>Marcas</h3><ul>{marcas_html}</ul></div></div></section>
<section class="sec"><div class="wrap">{encabezado_sec("Así cotizas")}<ol class="pasos">{pasos_html}</ol></div></section>
<section class="banda"><div class="wrap">{encabezado_sec("Manda tu lista", "Escríbela como la tengas. Se abre WhatsApp con tu lista lista para enviar; si tienes una foto, la adjuntas desde el chat.")}
<form class="form-lista solo-js" data-form-lista><label for="lista-t">Tu lista</label>
<textarea id="lista-t" name="lista" placeholder="Por ejemplo: 2 palas, 1 caja de herramienta, 6 rollos de papel higiénico"></textarea>
<div class="grupo"><a class="btn" data-lista-wa href="{wa("Hola, quiero cotizar esta lista:")}" target="_blank" rel="noopener noreferrer">{ico("wa")}Enviar lista por WhatsApp</a></div>
<p class="chico">WhatsApp solo abre el mensaje: tú decides si lo envías.</p></form>
<noscript><div>{boton_wa(wa("Hola, quiero cotizar esta lista:"), "Enviar mi lista por WhatsApp", "claro")}</div></noscript></div></section>
<section class="sec" id="tienda"><div class="wrap">{encabezado_sec("Visítanos")}<div class="tienda"><div>
<ul class="ficha"><li>{ico("pin")}<div><b>Dirección</b>{N["calle"]}, Col. {N["colonia"]}<br>{N["ciudad"]}, {N["estado"]}</div></li>
<li>{ico("tel")}<div><b>Teléfono y WhatsApp</b><a href="tel:{N["tel_href"]}">{N["tel"]}</a></div></li></ul>
<div class="grupo"><a class="btn" href="{MAPS}" target="_blank" rel="noopener noreferrer">{ico("pin")}Cómo llegar</a><a class="btn cont" href="{c.L("visitanos/")}">Más datos de la tienda</a></div></div>
<div><h3>Horario</h3>{horario_tabla()}</div></div></div></section>'''


AVISO_CAT = '<div class="aviso"><p><b>Estamos completando el catálogo.</b> Si no ves lo que buscas, pregúntanos por WhatsApp y te decimos si lo tenemos.</p><p>%s</p></div>'


def catalogo_layout(c, slug, con_busqueda=True):
    cid = 'cat-' + slug
    lateral = (f'<details class="lateral" data-lateral data-para="{cid}" {attrs_href(c).replace("data-href", "data-href")}>'
               f'<summary>Categorías{ico("chev")}</summary></details>')
    herr = ''
    if con_busqueda:
        herr = (f'<div class="herr"><div class="busca"><label class="sr" for="buscar-{slug}">Buscar en el catálogo</label>{ico("lupa")}'
                f'<input id="buscar-{slug}" type="search" placeholder="Buscar en el catálogo" autocomplete="off" data-en="{cid}"></div>'
                f'<p class="nota">{ico("wa")}<span data-nota>Los precios te los damos por WhatsApp. «Cotizar» abre WhatsApp con tu producto listo; tú decides si lo envías.</span></p></div>')
    modo = 'todos' if slug == 'todos' else slug
    aviso = '' if slug == 'papeleria' else AVISO_CAT % boton_wa(WA_GENERAL, 'Cotiza por WhatsApp', 'compacto')
    return f'<div class="wrap"><div class="cat">{lateral}<div>{herr}<div id="{cid}" data-catalogo="{modo}"></div>{aviso}</div></div></div>'


def p_catalogo(c):
    cab = cabecera_pagina(c, [('Inicio', ''), ('Catálogo', None)], 'Catálogo',
                          'Productos por línea. Busca por nombre, agrega a tu lista o cotiza directo por WhatsApp; el precio te lo damos en el chat.')
    return cab + catalogo_layout(c, 'todos')


def p_linea(slug):
    l = [x for x in LINEAS if x['slug'] == slug][0]

    def f(c):
        cab = cabecera_pagina(c, [('Inicio', ''), ('Catálogo', 'catalogo/'), (l['nombre'], None)], l['nombre'], DESC_LINEA[slug])
        return cab + catalogo_layout(c, slug, con_busqueda=(slug != 'papeleria'))
    return f


def p_como_comprar(c):
    sub = f'<ul class="subnav" aria-label="En esta página"><li>{c.ancla("solicitar-cotizacion", "Solicitar cotización")}</li><li>{c.ancla("formas-de-pago", "Formas de pago")}</li><li>{c.ancla("preguntas", "Preguntas")}</li></ul>'
    cab = cabecera_pagina(c, [('Inicio', ''), ('Cómo comprar', None)], 'Cómo comprar', 'Cotizas por WhatsApp, confirmas con la tienda y pagas en efectivo o por transferencia.', sub)
    pasos = [('Elige o manda tu lista', 'Agrega productos del catálogo a tu lista, o escribe tu lista directo en WhatsApp. Si tienes una foto de tu lista, adjúntala desde el chat.'),
             ('Pide tu precio', 'Te respondemos por WhatsApp con el precio de lo que pediste.'),
             ('Confirma con la tienda', 'Cuando todo esté claro, confirma tu pedido. WhatsApp solo abre un mensaje: tú decides si lo envías.')]
    pasos_html = ''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in pasos)
    faq = ''.join(f'<details><summary>{E(q)}{ico("chev")}</summary><p>{E(r)}</p></details>' for q, r in FAQ)
    return cab + f'''<section class="sec" id="solicitar-cotizacion"><div class="wrap">{encabezado_sec("Solicitar cotización", "Tres pasos, sin registrarte ni crear una cuenta.")}
<ol class="pasos">{pasos_html}</ol><div class="grupo" style="margin-top:32px">{boton_wa(wa("Hola, quiero cotizar esta lista:"), "Enviar mi lista por WhatsApp")}<a class="btn cont" href="{c.L("catalogo/")}">Ver catálogo</a></div></div></section>
<section class="sec gris compacta" id="formas-de-pago"><div class="wrap">{encabezado_sec("Formas de pago", "Aceptamos efectivo y transferencia. No publicamos datos bancarios en este sitio: pídelos a la tienda al confirmar tu pedido.")}
<ul class="pagos"><li>Efectivo</li><li>Transferencia</li></ul></div></section>
<section class="sec" id="preguntas"><div class="wrap">{encabezado_sec("Preguntas")}<div class="preguntas">{faq}</div>
<div class="aviso"><p>¿Tienes otra duda? Escríbenos por WhatsApp.</p><p>{boton_wa(WA_GENERAL, "Cotiza por WhatsApp", "compacto")}</p></div></div></section>'''


def p_visitanos(c):
    sub = f'<ul class="subnav" aria-label="En esta página"><li>{c.ancla("ubicacion", "Ubicación")}</li><li>{c.ancla("horario", "Horario")}</li><li>{c.ancla("contacto", "Contacto")}</li></ul>'
    cab = cabecera_pagina(c, [('Inicio', ''), ('Visítanos', None)], 'Visítanos', f'Estamos en el centro de {N["ciudad"]}. Aquí están la dirección, el horario y cómo escribirnos.', sub)
    return cab + f'''<section class="sec"><div class="wrap"><div class="dos"><div id="ubicacion"><h2>Ubicación</h2>
<ul class="ficha"><li>{ico("pin")}<div><b>Dirección</b>{N["calle"]}<br>Col. {N["colonia"]}, C.P. {N["cp"]}<br>{N["ciudad"]}, {N["estado"]}</div></li></ul>
<div class="grupo"><a class="btn" href="{MAPS}" target="_blank" rel="noopener noreferrer">{ico("pin")}Cómo llegar</a></div>
<p class="chico" style="margin-top:12px">El botón abre tu aplicación de mapas con esta dirección.</p></div>
<div id="horario"><h2>Horario</h2>{horario_tabla()}<p class="chico" style="margin-top:12px">Pago: efectivo y transferencia.</p></div></div></div></section>
<section class="sec gris" id="contacto"><div class="wrap"><h2>Contacto</h2><ul class="ficha">
<li>{ico("tel")}<div><b>Teléfono</b><a href="tel:{N["tel_href"]}">{N["tel"]}</a></div></li>
<li>{ico("wa")}<div><b>WhatsApp</b><a href="{WA_GENERAL}" target="_blank" rel="noopener noreferrer">{N["tel"]}</a></div></li>
<li>{ico("mail")}<div><b>Correo</b><a href="mailto:{N["correo"]}">{N["correo"]}</a></div></li></ul>
<div class="grupo">{boton_wa(WA_GENERAL, "Cotiza por WhatsApp")}</div></div></section>'''


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
    canon = '' if REVISION else f'<link rel="canonical" href="https://{N["dominio"]}/{ruta}">'
    og = (f'<meta property="og:type" content="website"><meta property="og:locale" content="es_MX"><meta property="og:site_name" content="{N["nombre"]}">'
          f'<meta property="og:title" content="{E(titulo)}"><meta property="og:description" content="{E(desc)}">')
    return (f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(titulo)}</title>'
            f'<meta name="description" content="{E(desc)}"><meta name="theme-color" content="#174F7C">{robots}{canon}{og}<link rel="icon" href="{FAVICON}">')


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
        pagina = f'''<!doctype html><html lang="es-MX"><head>{head(c, ruta, titulo, desc)}<link rel="stylesheet" href="{c.asset("css/site.css")}">{json_ld(c, ruta)}</head><body>
<a class="saltar" href="#contenido">Saltar al contenido</a>{SPRITE}{cabecera_sitio(c, ruta)}<main id="contenido">{fn(c)}</main>{pie_sitio(c)}{utilidades()}
<noscript><div class="wrap"><p class="aviso">Para ver y buscar el catálogo necesitas activar JavaScript. Mientras tanto, cotiza por WhatsApp: {boton_wa(WA_GENERAL, "abrir WhatsApp", "compacto")}</p></div></noscript>
<script src="{c.asset("js/catalogo.js")}"></script><script src="{c.asset("js/site.js")}"></script></body></html>'''
        escribir(dist / (ruta + 'index.html'), pagina)
    c = Ctx('dist', '')
    escribir(dist / '404.html', f'''<!doctype html><html lang="es-MX"><head>{head(c, '404', 'Página no encontrada · Comercializadora Robles', 'Página no encontrada.')}<link rel="stylesheet" href="assets/css/site.css"></head><body>{SPRITE}{cabecera_sitio(c, '404')}<main id="contenido"><section class="sec"><div class="wrap"><div class="enc-sec"><h1>No encontramos esta página</h1><p>Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos por WhatsApp.</p></div><div class="grupo"><a class="btn" href="index.html">Ir al inicio</a>{boton_wa(WA_GENERAL, "Cotiza por WhatsApp", "cont")}</div></div></section></main>{pie_sitio(c)}{utilidades()}<script src="assets/js/catalogo.js"></script><script src="assets/js/site.js"></script></body></html>''')
    escribir(dist / 'robots.txt', 'User-agent: *\nDisallow: /\n' if REVISION else f'User-agent: *\nAllow: /\nSitemap: https://{N["dominio"]}/sitemap.xml\n')
    if PUBLICAR:
        urls = ''.join(f'<url><loc>https://{N["dominio"]}/{r}</loc></url>' for r, *_ in PAGINAS if r != 'catalogo/papeleria/')
        escribir(dist / 'sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')


def construir_portatil():
    secciones = ''
    for ruta, titulo, desc, fn in PAGINAS:
        c = Ctx('portatil', ruta)
        secciones += f'<div class="pagina" data-ruta="{ruta}" data-titulo="{E(titulo)}" hidden>{fn(c)}</div>\n'
    c = Ctx('portatil', '')
    inicio = PAGINAS[0]
    doc = f'''<!doctype html><html lang="es-MX"><head>{head(c, '', inicio[1], inicio[2])}<style>{css_fuentes('portatil')}{CSS}</style>{json_ld(c, '')}</head><body>
<a class="saltar" href="#contenido" data-ancla="contenido">Saltar al contenido</a>{SPRITE}{cabecera_sitio(c, '')}<main id="contenido">
{secciones}</main>{pie_sitio(c)}{utilidades()}
<script>window.ROBLES_PORTATIL=true;</script><script>{CATALOGO_JS}</script><script>{JS}</script></body></html>'''
    escribir(RAIZ / 'robles-portatil.html', doc)


if __name__ == '__main__':
    construir_dist()
    construir_portatil()
    print('Listo: dist/ (%d páginas + 404) y robles-portatil.html (%d KB). Modo: %s. Productos: %d.' % (
        len(PAGINAS), (RAIZ / 'robles-portatil.html').stat().st_size // 1024, 'PUBLICAR' if PUBLICAR else 'revisión', len(CATALOGO)))
