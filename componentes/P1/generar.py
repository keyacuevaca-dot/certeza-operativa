# Google Maps y WhatsApp Business: textos listos para copiar, guía para el dueño y tarjeta con QR.
# Uso:   python3 componentes/P1/generar.py ruta/a/negocio.json [--salida carpeta]
# Escribe en <carpeta del json>/salida/perfil/ (o en --salida):
#   textos.html   textos para pegar en el Perfil de Negocio de Google y en WhatsApp Business, con botón «Copiar»
#   textos.txt    lo mismo en texto plano
#   guia.html     guía paso a paso para que el dueño dé de alta su negocio desde su cuenta (se imprime o se guarda en PDF)
#   tarjeta.html  hoja carta con un letrero de mostrador y 4 tarjetas con QR a su WhatsApp
#   qr-whatsapp.svg / qr-whatsapp.png
# Requiere segno (pip install -r componentes/requirements.txt).
import argparse
import datetime as dt
import io
import os
import sys
from html import escape as esc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comun as c  # noqa: E402

try:
    import segno
except ImportError:
    sys.exit('Falta segno. Instálelo con: pip install -r componentes/requirements.txt')

LIM_GOOGLE = 750   # caracteres de la descripción del Perfil de Negocio
VISIBLE = 250      # lo que se ve antes de «Más»; aquí va lo importante
MSG_QR = 'Hola, escaneé su código. Quiero informes.'  # distinto al de la página para saber de dónde llegó el mensaje
CONTACTO_CERTEZA = 'Certeza Operativa · WhatsApp 311 446 9363 · Tepic, Nayarit'


# ---------- Textos ----------
def servicios(n):
    return [s for s in n.get('servicios') or [] if s.get('nombre')]


def _art(giro):
    g = giro.lower()
    return ('una ' if g.endswith(('a', 'ería', 'ión', 'dad')) and not g.endswith(('ma',)) else 'un ') + g


def descripcion_google(n, av):
    if n.get('textos', {}).get('descripcion_google'):
        t = n['textos']['descripcion_google']
    else:
        donde = n['ciudad'] if not c.muestra_direccion(n) else ', '.join(
            x for x in [(n.get('direccion') or {}).get('colonia') and f'la colonia {n["direccion"]["colonia"]}', n['ciudad']] if x)
        nombres = [c.minuscula(s['nombre']) for s in servicios(n)]
        t = f'{n["nombre"]} es {_art(n["giro"])} en {donde}, {n["estado"]}. Ofrecemos {c.lista_y(nombres[:5])}.'
        if n.get('diferenciadores'):
            t += f' Lo que nos distingue: {c.lista_y([c.minuscula(x) for x in n["diferenciadores"]])}.'
        if n.get('atencion') in ('area', 'ambos') and n.get('areas_servicio'):
            t += f' Vamos a {c.lista_y(n["areas_servicio"])}.'
        if n.get('desde'):
            t += f' Atendemos desde {n["desde"]}.'
        t += f' Abrimos {c.horario_frase(n)}.'
        if n.get('formas_pago'):
            t += f' Aceptamos {c.lista_y(n["formas_pago"])}.'
        t += ' Escríbanos por WhatsApp para preguntar por un servicio.'
    if len(t) > LIM_GOOGLE:
        av.aviso(f'La descripción para Google tiene {len(t)} caracteres; el máximo es {LIM_GOOGLE}. Acórtela en "textos".')
    for mal in ('http', 'www.', '$', '%'):
        if mal in t:
            av.aviso(f'La descripción para Google trae «{mal}»: Google no permite enlaces, precios ni promociones ahí.')
    return t


def descripcion_whatsapp(n):
    if n.get('textos', {}).get('descripcion_whatsapp'):
        return n['textos']['descripcion_whatsapp']
    nombres = c.lista_y([c.minuscula(s['nombre']) for s in servicios(n)][:3])
    return f'{n["giro"]} en {n["ciudad"]}. {c.mayuscula(nombres)}. Abrimos {c.horario_frase(n)}.'


def bienvenida(n):
    if n.get('textos', {}).get('bienvenida'):
        return n['textos']['bienvenida']
    return (f'¡Hola! Gracias por escribir a {n["nombre"]}. ¿Qué servicio le interesa? '
            f'Díganos y le respondemos con precio y disponibilidad.\n'
            f'Abrimos {c.horario_frase(n)}.')


def ausencia(n):
    if n.get('textos', {}).get('ausencia'):
        return n['textos']['ausencia']
    return (f'Gracias por escribir a {n["nombre"]}. En este momento estamos cerrados.\n'
            f'Abrimos {c.horario_frase(n)}.\n'
            f'Déjenos su mensaje y le respondemos en cuanto abramos.')


def rapidas(n, av):
    if n.get('textos', {}).get('rapidas'):
        return [tuple(x) for x in n['textos']['rapidas']]
    hor = '\n'.join(c.horario_lineas(n)) + (f'\n{n["horario_especial"]}' if n.get('horario_especial') else '')
    out = [('/horario', f'Nuestro horario:\n{hor}')]
    if c.muestra_direccion(n):
        ref = (n.get('direccion') or {}).get('referencia')
        out.append(('/ubicacion', f'Estamos en {c.direccion_linea(n)}.' + (f' {ref}' if ref else '') +
                    f'\nCómo llegar: {c.como_llegar(n)}'))
    else:
        out.append(('/zona', f'Vamos a {c.lista_y(n.get("areas_servicio") or [])}. Díganos su colonia y le confirmamos.'))
    lineas = []
    for s in servicios(n):
        p = c.precio_valido(s)
        lineas.append(f'• {s["nombre"]}' + (f': {p}' if p else ''))
    falta_precio = any(c.precio_valido(s) is None for s in servicios(n))
    out.append(('/servicios', 'Estos son nuestros servicios:\n' + '\n'.join(lineas) +
                ('\nDíganos cuál le interesa y le confirmamos el precio.' if falta_precio else '')))
    if n.get('formas_pago'):
        out.append(('/pago', f'Aceptamos {c.lista_y(n["formas_pago"])}.'))
    else:
        av.aviso('Sin formas de pago confirmadas: la respuesta /pago se cambió por /llamar.')
        out.append(('/llamar', f'Si prefiere, llámenos al {c.tel_bonito(n)} en horario de atención.'))
    resena = n.get('mapa_url') or '[enlace para dejar reseña: Perfil de Negocio > «Pedir reseñas»]'
    if not n.get('mapa_url'):
        av.aviso('La respuesta /gracias lleva un espacio para el enlace de reseñas: péguelo cuando Google verifique la ficha.')
    out.append(('/gracias', f'Gracias por su preferencia. Si quedó contento, nos ayuda mucho una reseña en Google: {resena}'))
    return out


def ficha_google(n, av):
    """Campos del Perfil de Negocio en el orden en que los pide Google."""
    g = n.get('google') or {}
    if not g.get('categoria_principal'):
        av.aviso('Falta la categoría principal de Google: elíjala en la lista al escribir el giro.')
    ubic = (f'Dirección: {c.direccion_linea(n)}. Mueva el pin a la entrada.' if c.muestra_direccion(n) else
            'No muestre la dirección: elija «No, solo atiendo a domicilio» (o similar).')
    if n.get('atencion') in ('area', 'ambos'):
        ubic += f' Zonas que cubre: {c.lista_y(n.get("areas_servicio") or [])}.'
    web = n.get('dominio') or 'Déjelo en blanco hasta que se publique la página.'
    fotos = ['Logo (cuadrado)', 'Portada: la mejor foto de la fachada'] + [f.get('alt') or f.get('archivo') for f in n.get('fotos') or [] if f.get('archivo')]
    campos = [
        ('Nombre', n['nombre'], 'Exactamente como dice el letrero. Sin ciudad ni lema.'),
        ('Categoría principal', g.get('categoria_principal') or '(por elegir)', 'Elíjala en la lista; no se escribe a mano.'),
        ('Categorías adicionales', ', '.join(g.get('categorias_adicionales') or []) or '(ninguna)', ''),
        ('Ubicación', ubic, ''),
        ('Horario', '\n'.join(c.horario_lineas(n)), n.get('horario_especial') and f'Horario especial: {n["horario_especial"]}' or ''),
        ('Teléfono', c.tel_bonito(n), ''),
        ('Sitio web', web, ''),
        ('Descripción', descripcion_google(n, av), f'Máximo {LIM_GOOGLE} caracteres; lo primero que se ve son unos {VISIBLE}.'),
        ('Fecha de apertura', str(n.get('desde') or '(opcional)'), ''),
        ('Atributos', ', '.join(g.get('atributos') or []) or '(los que apliquen)', 'Solo los que sean ciertos.'),
        ('Fotos para subir', '\n'.join(fotos), 'Fotos reales, con buena luz, sin texto encima.'),
    ]
    return campos


def servicios_google(n):
    return [(s['nombre'], s.get('descripcion') or '') for s in servicios(n)]


def catalogo_wa(n):
    out = []
    for s in servicios(n):
        p = c.precio_valido(s)
        out.append((s['nombre'], (s.get('descripcion') or '') + (f' {p}' if p else '')))
    return out


def perfil_wa(n):
    w = n.get('whatsapp_business') or {}
    return [
        ('Nombre de la empresa', n['nombre']),
        ('Categoría', w.get('categoria') or '(la más cercana al giro)'),
        ('Descripción', descripcion_whatsapp(n)),
        ('Dirección', c.direccion_linea(n) if c.muestra_direccion(n) else f'Servicio a domicilio en {n["ciudad"]}'),
        ('Horario', '\n'.join(c.horario_lineas(n))),
        ('Correo', w.get('correo') or '(opcional)'),
        ('Sitio web', n.get('dominio') or '(cuando se publique la página)'),
        ('Foto de perfil', 'El logo, cuadrado y sin texto pequeño'),
    ]


# ---------- HTML ----------
CSS_PAPEL = '''*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#14212B;background:#FFFFFF}
.banda{background:#0D3441;color:#EAF2F4;padding:18px 16px}.banda h1{margin:0;font-size:1.5rem;line-height:1.2}.banda p{margin:4px 0 0;color:#B9D3DA}
main{max-width:820px;margin:0 auto;padding:16px}h2{font-size:1.25rem;margin:28px 0 8px;color:#0D3441;border-bottom:2px solid #28B7B5;padding-bottom:4px}
h3{font-size:1.05rem;margin:18px 0 6px}p{margin:0 0 .7em}ol,ul{padding-left:22px}li{margin:4px 0}
.nota{color:#4A5866;font-size:.95rem}.pie{color:#4A5866;font-size:.9rem;border-top:1px solid #D9DFE5;margin-top:28px;padding-top:10px}
@media print{body{font-size:11.5pt}.no-imp{display:none}h2,h3{break-after:avoid}li,.campo{break-inside:avoid}@page{size:letter;margin:14mm}}'''


def pagina(titulo, sub, cuerpo, extra_css='', script='', preview=True):
    robots = '<meta name="robots" content="noindex, nofollow">'
    return f'''<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>{robots}<style>{CSS_PAPEL}{extra_css}</style></head>
<body><header class="banda"><h1>{esc(titulo)}</h1><p>{esc(sub)}</p></header>
<main>{cuerpo}</main>{f"<script>{script}</script>" if script else ""}</body></html>
'''


def caja(etiqueta, texto, nota='', limite=None):
    cnt = f'<span class="cnt">{len(texto)}{f" / {limite}" if limite else ""} caracteres</span>' if limite else ''
    nota = f'<p class="nota">{esc(nota)}</p>' if nota else ''
    return (f'<div class="campo"><div class="cab"><b>{esc(etiqueta)}</b>{cnt}'
            f'<button type="button" class="copiar no-imp">Copiar</button></div>'
            f'<pre>{esc(texto)}</pre>{nota}</div>')


CSS_TEXTOS = '''.campo{border:1px solid #D9DFE5;border-radius:10px;padding:10px 12px;margin:10px 0}
.cab{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.cab b{flex:1}.cnt{color:#4A5866;font-size:.85rem}
pre{white-space:pre-wrap;font:inherit;margin:8px 0 0;background:#F3F5F7;border-radius:8px;padding:8px 10px}
.copiar{min-height:44px;min-width:88px;border:0;border-radius:8px;background:#0D3441;color:#fff;font:600 15px system-ui,sans-serif;cursor:pointer}
.copiar:focus-visible{outline:3px solid #28B7B5;outline-offset:2px}'''

JS_COPIAR = '''document.querySelectorAll(".copiar").forEach(function(b){b.addEventListener("click",function(){
var t=b.closest(".campo").querySelector("pre").textContent,ok=function(){b.textContent="Copiado";setTimeout(function(){b.textContent="Copiar"},1500)};
if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(ok,f)}else f();
function f(){var a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();try{document.execCommand("copy");ok()}catch(e){}a.remove()}})});'''


def textos_html(n, av):
    partes = ['<p class="nota no-imp">Abra esta página en el celular del dueño, toque «Copiar» y pegue en la app. '
              'Nada se manda solo: el dueño revisa y guarda.</p>',
              '<h2>Perfil de Negocio de Google</h2>']
    for et, tx, nota in ficha_google(n, av):
        partes.append(caja(et, tx, nota, LIM_GOOGLE if et == 'Descripción' else None))
    partes.append('<h3>Servicios (uno por uno)</h3>')
    for nom, d in servicios_google(n):
        partes.append(caja(nom, d or nom))
    partes.append('<h2>WhatsApp Business: perfil de empresa</h2>')
    for et, tx in perfil_wa(n):
        partes.append(caja(et, tx))
    partes.append('<h2>WhatsApp Business: mensajes automáticos</h2>')
    partes.append(caja('Mensaje de bienvenida', bienvenida(n), 'Herramientas para la empresa > Mensaje de bienvenida. Enviar a: todos.'))
    partes.append(caja('Mensaje de ausencia', ausencia(n), 'Herramientas para la empresa > Mensaje de ausencia. Horario: fuera del horario comercial.'))
    partes.append('<h3>Respuestas rápidas</h3><p class="nota">Herramientas para la empresa > Respuestas rápidas. '
                  'El atajo se escribe en el chat y aparece el texto completo.</p>')
    for atajo, tx in rapidas(n, av):
        partes.append(caja(f'Atajo {atajo}', tx))
    partes.append('<h2>WhatsApp Business: catálogo</h2><p class="nota">Herramientas para la empresa > Catálogo > Agregar artículo. '
                  'Un artículo por servicio, con su foto.</p>')
    for nom, d in catalogo_wa(n):
        partes.append(caja(nom, d or nom))
    partes.append('<h2>Enlace directo a su WhatsApp</h2>')
    partes.append(caja('Enlace para redes y estados', c.wa(n, ''), 'Lleva directo al chat del negocio, sin guardar el número.'))
    return pagina(f'Textos para Google y WhatsApp · {n["nombre"]}', 'Listos para copiar y pegar en el celular del dueño',
                  ''.join(partes), CSS_TEXTOS, JS_COPIAR)


def textos_txt(n, av):
    L = [f'TEXTOS PARA GOOGLE Y WHATSAPP · {n["nombre"]}', '', '== PERFIL DE NEGOCIO DE GOOGLE ==']
    for et, tx, _ in ficha_google(n, c.Avisos()):
        L += [f'-- {et}', tx, '']
    L.append('-- Servicios')
    L += [f'• {a}: {b}' for a, b in servicios_google(n)] + ['', '== WHATSAPP BUSINESS ==']
    for et, tx in perfil_wa(n):
        L += [f'-- {et}', tx, '']
    L += ['-- Mensaje de bienvenida', bienvenida(n), '', '-- Mensaje de ausencia', ausencia(n), '', '-- Respuestas rápidas']
    for a, t in rapidas(n, c.Avisos()):
        L += [a, t, '']
    L.append('-- Catálogo')
    L += [f'• {a}: {b}' for a, b in catalogo_wa(n)]
    L += ['', '-- Enlace directo', c.wa(n, '')]
    return '\n'.join(L) + '\n'


def guia_html(n):
    nom = esc(n['nombre'])
    g = n.get('google') or {}
    ref = esc((n.get('direccion') or {}).get('referencia') or '')
    equipo = esc(n.get('equipo_trabajo') or 'las herramientas, el equipo y los productos con que trabaja')
    if c.muestra_direccion(n):
        paso_ubic = (f'<li><b>¿Sus clientes van a su local?</b> Responda <b>Sí</b> y escriba: «{esc(c.direccion_linea(n))}». '
                     'Mueva el pin hasta la entrada del negocio.' +
                     (f' Si también va a domicilio, agregue las zonas: {esc(c.lista_y(n.get("areas_servicio") or []))}.' if n.get('atencion') == 'ambos' else '') + '</li>')
        video = f'''<li>Empiece afuera, en la calle: grabe el letrero con el nombre de la calle o el número exterior, y los negocios de al lado. {("Referencia: " + ref) if ref else ""}</li>
<li>Gire hacia su letrero y grábelo completo, que se lea «{nom}». Debe ser un letrero fijo; uno de papel o escrito a mano no sirve.</li>
<li>Demuestre que usted lo maneja: abra el portón o la cortina con su llave, la caja o el área de empleados.</li>
<li>Termine adentro mostrando {equipo}.</li>'''
    else:
        paso_ubic = (f'<li><b>¿Sus clientes van a su local?</b> Responda <b>No</b>. Agregue las zonas que cubre: '
                     f'{esc(c.lista_y(n.get("areas_servicio") or []))}. Su dirección se pide para verificar, pero no se publica.</li>')
        video = f'''<li>Empiece en la calle de la dirección que dio: grabe el letrero de la calle o una referencia fija (no un terreno vacío).</li>
<li>Muestre {equipo} y, si tiene, el vehículo o el uniforme con el nombre «{nom}».</li>
<li>Demuestre que usted lo maneja: abra el vehículo o la bodega con su llave, o haga una parte del servicio.</li>'''
    cat = esc(g.get('categoria_principal') or 'la que corresponda a su giro')
    web = esc(n.get('dominio') or 'déjelo en blanco; lo agregamos cuando su página esté publicada')
    cuerpo = f'''
<p>Esta guía es para usted, dueño de <b>{nom}</b>. Usted da de alta su negocio desde su propia cuenta: el perfil queda a su nombre
y nadie más necesita su contraseña. Lo acompañamos en cada paso.</p>
<h2>Antes de empezar</h2>
<ul>
<li>Su celular con la cuenta de Google (Gmail) que usará para el negocio, con la sesión abierta.</li>
<li>El celular con el número de WhatsApp del negocio: {esc(c.tel_bonito(n, "whatsapp"))}.</li>
<li>Las llaves del local y 30 minutos con luz de día; el letrero tiene que verse bien.</li>
<li>La hoja de textos que le preparamos (la abrimos en su celular para copiar y pegar).</li>
</ul>

<h2>Parte 1. Su negocio en Google Maps</h2>
<ol>
<li>Abra Google Maps y busque «{nom}». Si ya aparece, toque la ficha y elija <b>«Reclamar este negocio»</b> (o «¿Es el propietario?»).
Si no aparece, en Maps toque su foto o el menú y elija <b>«Agregar su negocio»</b>. Los nombres de los botones pueden cambiar un poco.</li>
<li><b>Nombre:</b> escriba exactamente «{nom}», igual que el letrero. No agregue la ciudad, frases ni palabras como «el mejor»: Google puede suspender el perfil.</li>
<li><b>Categoría:</b> empiece a escribir y elija «{cat}» de la lista.</li>
{paso_ubic}
<li><b>Teléfono:</b> {esc(c.tel_bonito(n))}. <b>Sitio web:</b> {web}.</li>
<li><b>Verificación.</b> Google elige cómo comprobar que el negocio es suyo; con frecuencia pide un video grabado desde la app. Siga el guion de abajo.</li>
<li>Mientras Google revisa, llene desde la hoja de textos: horario, descripción, servicios y fotos. No cambie el nombre, la dirección ni la categoría mientras revisan.</li>
<li>Cuando Google lo apruebe (puede tardar varios días), toque <b>«Compartir perfil»</b> y mándenos el enlace para ponerlo en su página.</li>
</ol>
<h3>Guion del video de verificación</h3>
<p class="nota">Lo que pide Google: un solo video continuo, sin cortes ni edición, de al menos 30 segundos, grabado y subido desde la app en ese momento.
No se puede grabar antes y subirlo después. No hace falta hablar.</p>
<ol>
{video}
</ol>
<p class="nota">No muestre identificaciones, tarjetas, estados de cuenta, caras de clientes ni placas de autos de clientes.
Si Google rechaza el video, le dice por qué y puede volver a intentarlo.</p>

<h2>Parte 2. WhatsApp Business</h2>
<ol>
<li>Si va a pasar a WhatsApp Business el número que hoy usa en WhatsApp normal, primero respalde sus chats: Ajustes &gt; Chats &gt; Copia de seguridad.</li>
<li>Instale <b>WhatsApp Business</b> desde la tienda de su celular (es gratis) y regístrelo con el número {esc(c.tel_bonito(n, "whatsapp"))}.</li>
<li><b>Perfil de empresa:</b> en Ajustes &gt; Herramientas para la empresa &gt; Perfil de empresa, pegue nombre, categoría, descripción, dirección y horario desde la hoja de textos. Ponga su logo como foto.</li>
<li><b>Mensaje de bienvenida:</b> actívelo y pegue el texto. Así nadie se queda sin respuesta la primera vez que escribe.</li>
<li><b>Mensaje de ausencia:</b> actívelo, elija «Fuera del horario comercial» y pegue el texto.</li>
<li><b>Respuestas rápidas:</b> agregue las 5 respuestas con su atajo (por ejemplo /horario). En un chat, escriba / y elija la respuesta.</li>
<li><b>Catálogo:</b> agregue cada servicio con su foto.</li>
<li><b>Prueba:</b> desde otro celular, escanee el código de su tarjeta y mande un mensaje. Debe llegarle con el texto ya escrito.</li>
</ol>

<h2>Parte 3. Su tarjeta con código QR</h2>
<ol>
<li>Imprima la hoja de la tarjeta en tamaño carta. Arriba viene un letrero para el mostrador; abajo, 4 tarjetas para recortar.</li>
<li>Ponga el letrero donde el cliente espera o paga. Quien lo escanea con la cámara abre su WhatsApp con un mensaje listo.</li>
<li>Los mensajes que llegan con «escaneé su código» vienen de la tarjeta; los que dicen «vi su página», de la página. Así sabe qué funciona.</li>
</ol>

<h2>Qué hacemos nosotros y qué no</h2>
<ul>
<li>Le preparamos los textos, las fotos ordenadas, la tarjeta y lo acompañamos paso a paso.</li>
<li>No usamos su contraseña ni damos de alta nada a nuestro nombre. Todo queda a su nombre.</li>
<li>La aprobación y los tiempos los decide Google. Entregamos su ficha completa y enviada a verificación.</li>
</ul>
<p class="pie">{esc(CONTACTO_CERTEZA)} · {dt.date.today():%d/%m/%Y}</p>'''
    return pagina(f'Guía para dar de alta {n["nombre"]} en Google y WhatsApp', 'Paso a paso, desde su propia cuenta', cuerpo)


# ---------- QR y tarjeta ----------
def qr(n, dest):
    url = c.wa(n, MSG_QR)
    q = segno.make(url, error='m')
    q.save(os.path.join(dest, 'qr-whatsapp.svg'), scale=10, border=2, dark='#000000')
    q.save(os.path.join(dest, 'qr-whatsapp.png'), scale=16, border=2)
    buf = io.BytesIO()
    q.save(buf, kind='svg', scale=10, border=2, xmldecl=False, svgns=True, nl=False, svgclass='qr', omitsize=True)
    return buf.getvalue().decode('utf-8'), url


def tarjeta_html(n, svg):
    col = (n.get('colores') or {}).get('principal') or '#1D4E6B'
    nom, tel = esc(n['nombre']), esc(c.tel_bonito(n, 'whatsapp'))
    hor = '<br>'.join(esc(x) for x in c.horario_lineas(n))
    dirl = esc(c.direccion_linea(n)) if c.muestra_direccion(n) else esc('Servicio a domicilio en ' + c.lista_y(n.get('areas_servicio') or [n['ciudad']]))
    tarjeta = f'''<div class="tj"><div class="tq">{svg}</div><div class="tt"><b>{nom}</b><span>WhatsApp <i>{tel}</i></span><small>{esc(c.horario_corto(n))}</small><small>{dirl}</small></div></div>'''
    css = f'''@page{{size:letter;margin:10mm}}*{{box-sizing:border-box}}body{{margin:0;font:12pt/1.35 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#14212B}}
.hoja{{width:195.9mm;margin:0 auto}}.qr{{width:100%;height:auto;display:block}}
.letrero{{border:1.5mm solid {col};border-radius:6mm;height:118mm;display:grid;grid-template-columns:85mm 1fr;gap:8mm;align-items:center;padding:8mm}}
.letrero h1{{font-size:24pt;line-height:1.1;margin:0 0 3mm;color:{col}}}.letrero .g{{font-size:17pt;font-weight:700;margin:0 0 3mm}}.letrero p{{margin:0 0 3mm}}
.corte{{border-top:.3mm dashed #888;margin:7mm 0 5mm;text-align:center;font-size:8pt;color:#666}}
.tjs{{display:grid;grid-template-columns:90mm 90mm;gap:6mm 10mm;justify-content:center}}
.tj{{width:90mm;height:50mm;border:.3mm solid #999;border-radius:3mm;display:grid;grid-template-columns:34mm 1fr;gap:3mm;align-items:center;padding:3mm;border-left:3mm solid {col}}}
.tt{{display:grid;gap:1mm}}.tt b{{font-size:12pt;line-height:1.15}}.tt span{{font-weight:700;font-size:10.5pt}}.tt small{{font-size:7.5pt;color:#333}}.tt i{{font-style:normal;white-space:nowrap}}
@media screen{{body{{background:#E9ECEF;padding:16px 0}}.hoja{{background:#fff;padding:10mm;width:215.9mm;max-width:100%}}}}
@media screen and (max-width:700px){{.letrero{{grid-template-columns:1fr;height:auto}}.tjs{{grid-template-columns:1fr}}.tj{{width:100%;max-width:90mm;margin:0 auto}}}}'''
    return f'''<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tarjeta con QR · {nom}</title><meta name="robots" content="noindex, nofollow"><style>{css}</style></head>
<body><div class="hoja">
<section class="letrero" aria-label="Letrero de mostrador">
<div>{svg}</div>
<div><h1>{nom}</h1><p class="g">Escríbanos por WhatsApp</p><p>Abra la cámara de su celular y apunte al código.<br>Se abre el chat con el mensaje listo.</p>
<p><b>WhatsApp {tel}</b></p><p>{hor}</p></div>
</section>
<p class="corte">recorte por la línea</p>
<section class="tjs" aria-label="Tarjetas para recortar">{tarjeta * 4}</section>
</div></body></html>
'''


def generar(ruta_json, salida=None):
    n = c.cargar(ruta_json)
    av = c.Avisos()
    c.validar_basico(n, av)
    dest = salida or os.path.join(n['_carpeta'], 'salida', 'perfil')
    if av.errores:
        return None, av
    os.makedirs(dest, exist_ok=True)
    escribir = lambda nombre, txt: open(os.path.join(dest, nombre), 'w', encoding='utf-8').write(txt)
    escribir('textos.html', textos_html(n, av))
    escribir('textos.txt', textos_txt(n, av))
    escribir('guia.html', guia_html(n))
    svg, url = qr(n, dest)
    escribir('tarjeta.html', tarjeta_html(n, svg))
    if not n.get('equipo_trabajo'):
        av.aviso('Falta equipo_trabajo: la guía del video dirá «herramientas y equipo» en general.')
    lineas = [f'Google Maps y WhatsApp Business · {n["nombre"]} · {dt.datetime.now():%Y-%m-%d %H:%M}', f'QR apunta a: {url}', '']
    lineas += (['Pendientes y avisos:'] + [f'{i}. {t}' for i, t in enumerate(av.avisos, 1)]) if av.avisos else ['Sin avisos.']
    escribir('reporte.txt', '\n'.join(lineas) + '\n')
    return dest, av


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Textos de Google y WhatsApp Business, guía y tarjeta con QR desde negocio.json')
    ap.add_argument('negocio')
    ap.add_argument('--salida')
    a = ap.parse_args()
    dest, av = generar(a.negocio, a.salida)
    if av.errores:
        print('Perfil: no se generó. Corrija en negocio.json:')
        for i, t in enumerate(av.errores, 1):
            print(f'  {i}. {t}')
        sys.exit(1)
    print(f'Perfil: listo en {dest}')
    for i, t in enumerate(av.avisos, 1):
        print(f'  aviso {i}. {t}')
