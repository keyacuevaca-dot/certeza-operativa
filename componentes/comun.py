# Piezas que comparten W1 (página) y P1 (Google Maps y WhatsApp Business).
# Todo sale de negocio.json; aquí no hay datos de ningún cliente.
import datetime as dt
import json
import os
import re
from urllib.parse import quote

DIAS = ['lun', 'mar', 'mie', 'jue', 'vie', 'sab', 'dom']
DIA_NOMBRE = {'lun': 'Lunes', 'mar': 'Martes', 'mie': 'Miércoles', 'jue': 'Jueves',
              'vie': 'Viernes', 'sab': 'Sábado', 'dom': 'Domingo'}
DIA_SCHEMA = {'lun': 'Monday', 'mar': 'Tuesday', 'mie': 'Wednesday', 'jue': 'Thursday',
              'vie': 'Friday', 'sab': 'Saturday', 'dom': 'Sunday'}


class Avisos:
    """Junta errores (detienen la construcción) y avisos (se entregan como pendientes)."""

    def __init__(self):
        self.errores, self.avisos = [], []

    def error(self, t):
        self.errores.append(t)

    def aviso(self, t):
        self.avisos.append(t)


def cargar(ruta):
    with open(ruta, encoding='utf-8') as f:
        n = json.load(f)
    n['_carpeta'] = os.path.dirname(os.path.abspath(ruta))
    return n


def solo_digitos(s):
    return re.sub(r'\D', '', str(s or ''))


def numero_wa(n, av=None):
    """Número para wa.me: 52 + 10 dígitos, sin el 1 de los celulares de antes de 2020."""
    d = solo_digitos(n.get('whatsapp'))
    if d.startswith('521') and len(d) == 13:
        d = '52' + d[3:]
    elif d.startswith('52') and len(d) == 12:
        pass
    elif len(d) == 10:
        d = '52' + d
    else:
        if av:
            av.error('WhatsApp: escriba los 10 dígitos del número (ejemplo 3111234567).')
        return ''
    return d


def wa(n, msg=None):
    num = numero_wa(n)
    msg = n.get('mensaje_whatsapp') if msg is None else msg
    return f'https://wa.me/{num}' + (f'?text={quote(msg)}' if msg else '')


def tel_bonito(n, clave='telefono'):
    d = solo_digitos(n.get(clave))[-10:]
    return f'{d[:3]} {d[3:6]} {d[6:]}' if len(d) == 10 else ''


def tel_e164(n, clave='telefono'):
    d = solo_digitos(n.get(clave))[-10:]
    return f'+52{d}' if len(d) == 10 else ''


def hora(h):
    """'08:00' -> '8:00'."""
    hh, mm = h.split(':')
    return f'{int(hh)}:{mm}'


def tramos(n, dia):
    out = []
    for t in (n.get('horario') or {}).get(dia) or []:
        if len(t) == 2 and all(re.fullmatch(r'\d{2}:\d{2}', x or '') for x in t):
            out.append((t[0], t[1]))
    return out


def validar_horario(n, av):
    h = n.get('horario') or {}
    for d in DIAS:
        for t in h.get(d) or []:
            if t and any(t) and not (len(t) == 2 and all(re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d', x or '') for x in t)):
                av.error(f'Horario de {DIA_NOMBRE[d]}: use HH:MM en 24 h, por ejemplo ["08:00","18:00"].')
    if not any(tramos(n, d) for d in DIAS):
        av.error('Horario vacío: se necesita al menos un día con horario.')


def grupos_horario(n):
    """Agrupa días seguidos con el mismo horario: [(['lun',...,'sab'], [('08:00','18:00')]), ...]."""
    out = []
    for d in DIAS:
        t = tramos(n, d)
        if out and out[-1][1] == t:
            out[-1][0].append(d)
        else:
            out.append(([d], t))
    return out


def texto_dias(dias):
    if len(dias) == 1:
        return DIA_NOMBRE[dias[0]]
    if len(dias) == 2:
        return f'{DIA_NOMBRE[dias[0]]} y {DIA_NOMBRE[dias[1]].lower()}'
    return f'{DIA_NOMBRE[dias[0]]} a {DIA_NOMBRE[dias[-1]].lower()}'


def texto_tramos(t):
    return ' y '.join(f'{hora(a)} a {hora(b)}' for a, b in t) if t else 'Cerrado'


def horario_lineas(n):
    """['Lunes a sábado: 8:00 a 18:00', 'Domingo: 8:00 a 14:00']"""
    return [f'{texto_dias(d)}: {texto_tramos(t)}' for d, t in grupos_horario(n)]


def horario_frase(n):
    """'de lunes a sábado de 8:00 a 18:00 y el domingo de 8:00 a 14:00' (sin días cerrados)."""
    partes = []
    for d, t in grupos_horario(n):
        if not t:
            continue
        dias = texto_dias(d).lower()
        dias = f'el {dias}' if len(d) == 1 else (f'de {dias}' if len(d) > 2 else f'los {dias}')
        partes.append(dias + ' ' + ' y '.join(f'de {hora(a)} a {hora(b)}' for a, b in t))
    return lista_y(partes)


def minuscula(s):
    """Primera letra en minúscula, salvo siglas (SUV, IVA)."""
    return s if s[1:2].isupper() else s[:1].lower() + s[1:]


def mayuscula(s):
    return s[:1].upper() + s[1:]


def horario_corto(n):
    return ' · '.join(horario_lineas(n))


def precio_valido(s, hoy=None):
    """Un precio se publica solo con monto, unidad, IVA y vigencia sin vencer."""
    p = s.get('precio') or {}
    hoy = hoy or dt.date.today()
    try:
        vig = dt.date.fromisoformat(str(p.get('vigencia') or ''))
    except ValueError:
        return None
    if p.get('monto') in (None, '') or not p.get('unidad') or not p.get('iva') or vig < hoy:
        return None
    monto = float(p['monto'])
    m = f'${monto:,.0f}' if monto == int(monto) else f'${monto:,.2f}'
    iva = 'IVA incluido' if 'incl' in str(p['iva']).lower() else 'más IVA'
    return f'{m} {p["unidad"]}, {iva}. Vigente hasta el {vig.day} de {MESES[vig.month - 1]} de {vig.year}.'


MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
         'septiembre', 'octubre', 'noviembre', 'diciembre']


def direccion_linea(n):
    d = n.get('direccion') or {}
    partes = [d.get('calle'), d.get('colonia') and f'Col. {d["colonia"]}',
              ' '.join(x for x in [d.get('cp'), n.get('ciudad')] if x), n.get('estado')]
    return ', '.join(p for p in partes if p)


def muestra_direccion(n):
    return n.get('atencion', 'local') in ('local', 'ambos')


def mapa(n):
    """Enlace para ver el negocio en Google Maps (la ficha si ya existe; si no, el pin)."""
    if n.get('mapa_url'):
        return n['mapa_url']
    g = n.get('geo') or {}
    if g.get('lat') is not None and g.get('lng') is not None:
        return f'https://www.google.com/maps/search/?api=1&query={g["lat"]}%2C{g["lng"]}'
    return 'https://www.google.com/maps/search/?api=1&query=' + quote(f'{n.get("nombre", "")} {direccion_linea(n)}')


def como_llegar(n):
    g = n.get('geo') or {}
    if g.get('lat') is not None and g.get('lng') is not None:
        return f'https://www.google.com/maps/dir/?api=1&destination={g["lat"]}%2C{g["lng"]}'
    return mapa(n)


def lista_y(xs):
    xs = [x for x in xs if x]
    if len(xs) <= 1:
        return ''.join(xs)
    return ', '.join(xs[:-1]) + ' y ' + xs[-1]


def slug(s):
    s = s.lower()
    for a, b in zip('áéíóúüñ', 'aeiouun'):
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def validar_basico(n, av):
    for k, t in [('nombre', 'el nombre como dice el letrero'), ('giro', 'el giro'),
                 ('frase', 'la frase de presentación'), ('ciudad', 'la ciudad')]:
        if not str(n.get(k) or '').strip():
            av.error(f'Falta {t} ({k}).')
    numero_wa(n, av)
    validar_horario(n, av)
    if muestra_direccion(n) and not (n.get('direccion') or {}).get('calle'):
        av.error('Atiende en local: falta la calle y número (direccion.calle).')
    if n.get('atencion') == 'area' and not n.get('areas_servicio'):
        av.error('Atiende a domicilio: falta la lista de zonas que cubre (areas_servicio).')
    if not [s for s in n.get('servicios') or [] if s.get('nombre')]:
        av.error('Falta al menos un servicio con nombre.')
    nombre = str(n.get('nombre') or '')
    if re.search(r'\b(mejor|barato|económico|tepic|nayarit)\b', nombre, re.I):
        av.aviso(f'El nombre «{nombre}» trae ciudad o adjetivos: Google pide el nombre tal como dice el letrero. Confírmelo con una foto del letrero.')
