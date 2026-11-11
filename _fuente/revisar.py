# Revisa el sitio ya generado, sin cambiar ningún archivo. Se corre después de `python _fuente/construir.py`.
#   python _fuente/revisar.py                        → tabla de las 24 páginas del sitio principal y lista de problemas
#   python _fuente/revisar.py --detalle index.html   → además, cada coincidencia de esa página con su frase
#   python _fuente/revisar.py --todo                 → agrega alucard/, combos/ y componentes/ (no salen del generador)
# Errores (salida con código 1): archivo o ancla que no existe, WhatsApp o teléfono distinto del oficial, términos internos,
#   precios o montos, «POR LLENAR», imagen de más de 300 KB.
# Avisos (no detienen): trato (usted y tú), horas de trabajo, título o descripción repetidos, descripción de más de
#   155 caracteres, más o menos de un H1, saltos de encabezado y sitemap distinto de las páginas indexables.
# Trato: «usted» son formas seguras de usted; «dudosos» son formas que también pueden ser de tercera persona
#   («su propio precio», «le toca», «tiene»): se revisan con --detalle. «tú» son formas seguras de tú.
#   Lo que de verdad sea de tercera persona se anota en PERMITIDAS con su motivo, para que el conteo pueda llegar a 0.
# Solo usa la biblioteca estándar de Python, para que corra igual en cualquier computadora.
import bisect, json, os, re, sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from contenido import INDUSTRIAS, SOLUCIONES, WA_NUM, TEL, SITIO_URL

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGINAS = (['index.html', 'catalogo.html'] + [f"industrias/{i['slug']}.html" for i in INDUSTRIAS]
           + [f"soluciones/{s['slug']}.html" for s in SOLUCIONES] + ['servicios.html', 'nosotros.html', 'autodiagnostico.html'])
NO_PUBLICA = ('_fuente', '_capturas', '.git')
LIMITE_IMG = 300 * 1024
LIMITE_DESC = 155
TEL_NUM = re.sub(r'\D', '', TEL)
IMAGEN = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.avif')

# Frases que no cuentan como trato aunque coincidan: ('ruta o *', 'frase en minúsculas', 'motivo').
PERMITIDAS = [
    ('*', 'a un toque', 'sustantivo («WhatsApp a un toque»), no el imperativo «toque»'),
    ('*', 'con un toque', 'sustantivo, no el imperativo «toque»'),
    ('*', 'necesita tu negocio', 'tercera persona: quien necesita es el negocio'),
]


def rx(*partes):
    return re.compile('|'.join(partes), re.I)


USTED = rx(r'\busted(?:es)?\b',
           r'\b(?:escr[ií]banos|cu[eé]ntenos|ll[aá]menos|d[ií]ganos|m[aá]ndenos|perm[ií]tanos|plat[ií]quenos|preg[uú]ntenos)\b',
           r'\b(?:les?|se l[oa]s?) \w+(?:amos|emos|imos)\b',
           r'\ble (?:atiende|debe|deben|paga|pagan|paguen|escribe|escriben|escriban|pregunta|preguntan|pide|piden|quita|cuesta'
           r'|cuestan|alcanza|conviene|funciona|sirve|suena|pasa|interesa|falta|faltan|ahorra|dejó)\b',
           r'\b(?:agende|elija|haga|vea|empiece|ordene|cobre|cotice|sepa|anticipe|conozca|pida|revise|responda|conteste|mire|lea'
           r'|busque|compare|active|toque|descubra|evite|platique|pregunte|aproveche|solicite|escriba|llame|mande|cuente)\b',
           r'\bsus? (?:negocios?|equipo|empresa|caja|inventario|cobranza|contador|clientes?|agenda|marca|operación|cuentas?|página'
           r'|perspectiva|autorización|nombre|celular|whatsapp|giro|idioma|papeles|dinero|tiempo|crecimiento|ventas|gente|personal'
           r'|local|tienda|taller|zona|lista|cuenta|teléfono|correo)\b')
DUDOSO = rx(r'\bsus? \w+', r'\bles? \w+', r'\b(?:tiene|puede|quiere|necesita|sabe|vende|conoce|decide|llegue|tenga)\b')
TU = rx(r'\b(?:tú|tus?|te|ti|contigo)\b',
        r'\b(?:escríbenos|cuéntanos|llámanos|dinos|mándanos|platícanos|pregúntanos)\b',
        r'\b(?:quieres|tienes|puedes|sabes|necesitas|vendes|trabajas|transformas|conformas|haces|buscas|usas|pagas|debes|ganas'
        r'|pierdes|cierras|ves|llevas|empiezas|eliges|pides|cotizas|cobras|decides|piensas|eres|estás|vas|das|dices)\b',
        r'\bhaz\b', r'\bcotiza sin costo\b')
HORAS = rx(r'\bhoras? útiles\b', r'\b\d+(?:[.,]\d+)?\s*horas?\b', r'\bhoras? (?:de trabajo|autorizadas|como mínimo|mínimas)\b')
TERMINOS = rx(r'\bl[ií]neas? cero\b', r'\bdeltas?\b', r'\btriajes?\b', r'\bfichas?\b', r'\btickets?\b', r'\bvector(?:es)? de fuga\b',
              r'\bmontos? atascados?\b')
PRECIOS = rx(r'\$\s?\d[\d.,]*', r'\b\d[\d.,]*\s?(?:pesos|mxn)\b', r'\bmxn\b', r'\bpor hora\b', r'/\s?hora\b', r'\btarifas?\b', r'\biva\b')

VACIOS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr', 'param'}
ZONAS = {'header', 'nav', 'main', 'section', 'footer', 'aside', 'article', 'form', 'dialog'}


def cadenas(o):
    # Textos dentro de JSON (datos del autodiagnóstico y datos estructurados), sin direcciones ni números sueltos
    if isinstance(o, str):
        return [] if re.match(r'(https?:|/|#|\+?[\d\s:.-]+$)', o) else [o]
    if isinstance(o, dict):
        return [s for v in o.values() for s in cadenas(v)]
    if isinstance(o, list):
        return [s for v in o for s in cadenas(v)]
    return []


class Pagina(HTMLParser):
    def __init__(self, ruta):
        super().__init__(convert_charrefs=True)
        self.ruta, self.pila, self.trozos, self.atributos, self.datos, self.comentarios = ruta, [], [], [], [], []
        self.ids, self.refs, self.enlaces, self.encabezados = set(), [], [], []
        self.titulo, self.desc, self.robots, self.canonical, self.og = '', None, '', None, {}
        self._en, self._buf = None, []
        self.crudo = open(os.path.join(RAIZ, ruta), encoding='utf-8').read()
        self.feed(self.crudo)
        self.close()

    def _zona(self):
        return next((z for _, z, _ in reversed(self.pila) if z), 'página')

    def handle_starttag(self, tag, attrs):
        a = {k: (v or '') for k, v in attrs}
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a' and a.get('name'):
            self.ids.add(a['name'])
        zona = None
        if tag in ZONAS:
            zona = tag + ('#' + a['id'] if a.get('id') else ('.' + a['class'].split()[0] if a.get('class') else ''))
        for k in ('alt', 'aria-label', 'title', 'placeholder'):
            if a.get(k):
                self.atributos.append((a[k], zona or self._zona()))
        if tag == 'meta':
            n, c = (a.get('name') or a.get('property') or '').lower(), a.get('content', '')
            if n == 'description':
                self.desc = c
            elif n == 'robots':
                self.robots = c.lower()
            elif n.startswith('og:'):
                self.og[n] = c
            if n in ('description', 'og:title', 'og:description', 'og:image:alt'):
                self.atributos.append((c, 'head'))
        elif tag == 'link':
            rel = set(a.get('rel', '').lower().split())
            if 'canonical' in rel:
                self.canonical = a.get('href')
            if a.get('href') and rel & {'stylesheet', 'icon', 'preload', 'manifest', 'apple-touch-icon', 'modulepreload'}:
                self.refs.append(a['href'])
        elif tag in ('img', 'source', 'video', 'audio', 'iframe', 'embed'):
            self.refs += [a[k] for k in ('src', 'poster') if a.get(k)]
            self.refs += [p.strip().split(' ')[0] for p in a.get('srcset', '').split(',') if p.strip()]
        elif tag == 'script':
            if a.get('src'):
                self.refs.append(a['src'])
            self._en = 'json' if 'json' in a.get('type', '').lower() else 'script'
        elif tag == 'style':
            self._en = 'style'
        elif tag == 'title' and not any(t == 'svg' for t, _, _ in self.pila):
            self._en = 'title'
        if tag == 'a' and 'href' in a:
            self.enlaces.append((a['href'], self._zona()))
        if re.fullmatch(r'h[1-6]', tag):
            self.encabezados.append(int(tag[1]))
        if tag not in VACIOS:
            self.pila.append((tag, zona, 'hidden' in a))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VACIOS and self.pila and self.pila[-1][0] == tag:
            self.pila.pop()

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'title') and self._en:
            texto, self._buf = ''.join(self._buf), []
            if self._en == 'json':
                try:
                    self.datos += cadenas(json.loads(texto))
                except ValueError:
                    pass
            elif self._en == 'title':
                self.titulo = re.sub(r'\s+', ' ', texto).strip()
            self._en = None
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i][0] == tag:
                del self.pila[i:]
                break

    def handle_data(self, d):
        if self._en:
            self._buf.append(d)
        elif d.strip():
            self.trozos.append((re.sub(r'\s+', ' ', d).strip(), self._zona(), any(o for _, _, o in self.pila)))

    def handle_comment(self, d):
        self.comentarios.append(d)

    def textos(self):
        # (texto, zona, oculto) por bloque: el cuerpo se une en un solo texto para encontrar frases partidas en etiquetas
        cuerpo, inicios = '', []
        for t, _, _ in self.trozos:
            inicios.append(len(cuerpo))
            cuerpo += t + ' '
        return cuerpo, inicios, ([(t, 'atributo · ' + z) for t, z in self.atributos] + [(t, 'datos') for t in self.datos]
                                 + ([(self.titulo, 'title')] if self.titulo else []))


def buscar(p, patron, excluir=None):
    # Coincidencias del patrón en el cuerpo, los atributos y los datos: [(texto, zona, contexto, oculto)].
    # Si hay patrón de exclusión, se descartan las coincidencias que se enciman con él (los dudosos no repiten a usted).
    cuerpo, inicios, extras = p.textos()
    hits = []

    def libres(t):
        tramos = [m.span() for m in excluir.finditer(t)] if excluir else []
        return (m for m in patron.finditer(t) if not any(a < m.end() and m.start() < b for a, b in tramos))
    for m in libres(cuerpo):
        k = bisect.bisect_right(inicios, m.start()) - 1
        _, zona, oculto = p.trozos[k]
        hits.append((m.group(0), zona, cuerpo[max(0, m.start() - 45):m.end() + 45].strip(), oculto))
    vistos = set()
    for t, zona in extras:
        if t in vistos:
            continue
        vistos.add(t)
        for m in libres(t):
            hits.append((m.group(0), zona, t[max(0, m.start() - 45):m.end() + 45].strip(), False))
    return hits


def permitida(ruta, contexto):
    c = contexto.lower()
    return any((r == '*' or r == ruta) and f in c for r, f, _ in PERMITIDAS)


def resolver(ruta, url):
    # Ruta local a la que apunta una dirección, o None si es externa. Las direcciones completas del sitio oficial
    # (canonical, og:url, og:image) se leen desde la raíz del repositorio.
    base = os.path.dirname(ruta)
    if url.startswith(SITIO_URL):
        url, base = url[len(SITIO_URL):] or 'index.html', ''
    s = urlsplit(url)
    if s.scheme or url.startswith('//'):
        return None
    if not s.path:
        return ruta, s.fragment
    destino = os.path.normpath(os.path.join(base, unquote(s.path))).replace(os.sep, '/')
    if s.path.endswith('/') or os.path.isdir(os.path.join(RAIZ, destino)):
        destino = destino.rstrip('/') + '/index.html'
    return destino.lstrip('./') if not destino.startswith('..') else destino, s.fragment


CACHE = {}


def cargar(ruta):
    if ruta not in CACHE:
        CACHE[ruta] = Pagina(ruta)
    return CACHE[ruta]


def revisar(ruta, principal):
    p = cargar(ruta)
    err, av = [], []
    # Trato: primero las formas seguras; los dudosos no repiten lo que ya contó una forma segura
    usted = [h for h in buscar(p, USTED) if not permitida(ruta, h[2])]
    dudosos = [h for h in buscar(p, DUDOSO, USTED) if not permitida(ruta, h[2])]
    tu = [h for h in buscar(p, TU) if not permitida(ruta, h[2])]
    horas = buscar(p, HORAS)
    terminos = buscar(p, TERMINOS) + [(m.group(0), 'comentario del código', c[:90], False)
                                     for c in p.comentarios for m in TERMINOS.finditer(c)]
    precios = buscar(p, PRECIOS)
    for h in terminos:
        err.append(f'término interno «{h[0]}» ({h[1]}): …{h[2]}…')
    for h in precios:
        err.append(f'precio o tarifa «{h[0]}» ({h[1]}): …{h[2]}…')
    n = p.crudo.count('POR LLENAR')
    if n:
        err.append(f'«POR LLENAR» aparece {n} vez/veces en el HTML')
    if horas:
        av.append(f'{len(horas)} mención(es) de horas de trabajo: ' + ' · '.join(sorted({h[0] for h in horas})))
    # Enlaces, anclas y teléfonos
    for href, zona in p.enlaces:
        if 'wa.me/' in href:
            num = re.sub(r'\D', '', href.split('wa.me/')[1].split('?')[0])
            if principal and num != WA_NUM:
                err.append(f'WhatsApp {num} distinto de {WA_NUM} ({zona})')
            continue
        if href.startswith('tel:'):
            if principal and re.sub(r'\D', '', href) != TEL_NUM:
                err.append(f'teléfono {href} distinto de {TEL} ({zona})')
            continue
        if href.startswith(('mailto:', 'javascript:')):
            continue
        r = resolver(ruta, href)
        if r is None:
            continue
        destino, ancla = r
        if destino.startswith('..') or not os.path.isfile(os.path.join(RAIZ, destino)):
            err.append(f'enlace roto {href} ({zona})')
        elif ancla and destino.endswith('.html') and ancla not in cargar(destino).ids:
            err.append(f'ancla rota {href} ({zona})')
    # Recursos locales, peso e imágenes
    peso, vistos = len(p.crudo.encode('utf-8')), set()
    otros = [p.canonical] if p.canonical else []
    otros += [p.og[k] for k in ('og:image', 'og:url') if p.og.get(k)]
    for url in p.refs + otros:
        r = resolver(ruta, url)
        if r is None:
            continue
        destino = r[0]
        f = os.path.join(RAIZ, destino)
        if not os.path.isfile(f):
            err.append(f'archivo que no existe: {url}')
            continue
        if url in otros or destino in vistos:
            continue
        vistos.add(destino)
        tam = os.path.getsize(f)
        peso += tam
        if destino.lower().endswith(IMAGEN) and tam > LIMITE_IMG:
            err.append(f'imagen de {tam // 1024} KB (más de 300 KB): {destino}')
    for url in [p.og.get('og:image')] if p.og.get('og:image') else []:
        r = resolver(ruta, url)
        if r and os.path.isfile(os.path.join(RAIZ, r[0])) and os.path.getsize(os.path.join(RAIZ, r[0])) > LIMITE_IMG:
            err.append(f'imagen para compartir de más de 300 KB: {r[0]}')
    # Encabezados, título y descripción
    h1 = p.encabezados.count(1)
    if h1 != 1:
        av.append(f'{h1} H1 (debe haber 1)')
    saltos = [f'H{a}→H{b}' for a, b in zip(p.encabezados, p.encabezados[1:]) if b > a + 1]
    if saltos:
        av.append('saltos de encabezado: ' + ', '.join(saltos))
    if not p.titulo:
        av.append('sin título')
    if not p.desc:
        av.append('sin descripción')
    elif len(p.desc) > LIMITE_DESC:
        av.append(f'descripción de {len(p.desc)} caracteres (máximo {LIMITE_DESC})')
    return dict(ruta=ruta, usted=usted, dudosos=dudosos, tu=tu, horas=horas, terminos=terminos, precios=precios,
                err=err, av=av, kb=round(peso / 1024), titulo=p.titulo, desc=p.desc or '', noindex='noindex' in p.robots)


def sitemap(res):
    av, err = [], []
    f = os.path.join(RAIZ, 'sitemap.xml')
    locs = re.findall(r'<loc>([^<]+)</loc>', open(f, encoding='utf-8').read()) if os.path.isfile(f) else []
    rutas = set()
    for u in locs:
        r = resolver('index.html', u.strip())
        if r is None or not os.path.isfile(os.path.join(RAIZ, r[0])):
            err.append(f'sitemap: {u} no existe')
        else:
            rutas.add(r[0])
    for x in res:
        if x['ruta'] not in PAGINAS:
            continue
        if not x['noindex'] and x['ruta'] not in rutas:
            av.append(f"sitemap: falta {x['ruta']} (es indexable)")
        if x['noindex'] and x['ruta'] in rutas:
            av.append(f"sitemap: incluye {x['ruta']}, que tiene noindex")
    return err, av


def todas():
    extra = []
    for d, carpetas, archivos in os.walk(RAIZ):
        rel = os.path.relpath(d, RAIZ).replace(os.sep, '/')
        carpetas[:] = [c for c in carpetas if not (rel == '.' and c in NO_PUBLICA)]
        for a in archivos:
            r = (a if rel == '.' else f'{rel}/{a}')
            if a.endswith('.html') and r not in PAGINAS:
                extra.append(r)
    return sorted(extra)


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    args = sys.argv[1:]
    detalle = args[args.index('--detalle') + 1] if '--detalle' in args else None
    rutas = [(r, True) for r in PAGINAS] + ([(r, False) for r in todas()] if '--todo' in args else [])
    faltan = [r for r, _ in rutas if not os.path.isfile(os.path.join(RAIZ, r))]
    if faltan:
        print('Faltan páginas (corre primero python _fuente/construir.py):', ', '.join(faltan))
        return 1
    res = [revisar(r, pr) for r, pr in rutas]
    err_sm, av_sm = sitemap(res)
    for clave, nombre in (('titulo', 'título'), ('desc', 'descripción')):
        vistos = {}
        for x in res:
            if x['ruta'] in PAGINAS and x[clave]:
                vistos.setdefault(x[clave], []).append(x['ruta'])
        for v, rs in vistos.items():
            if len(rs) > 1:
                av_sm.append(f'{nombre} repetido en {", ".join(rs)}: «{v[:60]}»')
    print(f"{'página':<44}{'usted':>6}{'dudosos':>9}{'tú':>5}{'horas':>7}{'KB':>6}{'errores':>9}{'avisos':>8}")
    for x in res:
        print(f"{x['ruta']:<44}{len(x['usted']):>6}{len(x['dudosos']):>9}{len(x['tu']):>5}{len(x['horas']):>7}{x['kb']:>6}"
              f"{len(x['err']):>9}{len(x['av']):>8}")
    principales = [x for x in res if x['ruta'] in PAGINAS]
    n_err = sum(len(x['err']) for x in res) + len(err_sm)
    n_av = sum(len(x['av']) for x in res) + len(av_sm)
    us = [len(x['usted']) for x in principales]
    print(f"\n{len(res)} páginas · {n_err} errores · {n_av} avisos · usted: {sum(us)} en total (de {min(us)} a {max(us)} por página)"
          f" · tú: {sum(len(x['tu']) for x in principales)} · dudosos: {sum(len(x['dudosos']) for x in principales)}")
    if n_err:
        print('\nERRORES')
        for x in res:
            for e in x['err']:
                print(f"- {x['ruta']}: {e}")
        for e in err_sm:
            print(f'- {e}')
    if n_av:
        print('\nAVISOS')
        for x in res:
            for a in x['av']:
                print(f"- {x['ruta']}: {a}")
        for a in av_sm:
            print(f'- {a}')
    if detalle:
        x = next((x for x in res if x['ruta'] == detalle), None) or revisar(detalle, detalle in PAGINAS)
        print(f'\nDETALLE · {detalle}')
        for clave, nombre in (('usted', 'USTED'), ('dudosos', 'DUDOSOS (revisar a mano)'), ('tu', 'TÚ'), ('horas', 'HORAS'),
                              ('terminos', 'TÉRMINOS INTERNOS'), ('precios', 'PRECIOS')):
            if x[clave]:
                print(f'\n{nombre} ({len(x[clave])})')
                for t, zona, ctx, oculto in x[clave]:
                    print(f"  «{t}» · {zona}{' · oculto' if oculto else ''} · …{ctx}…")
    return 1 if n_err else 0


if __name__ == '__main__':
    sys.exit(main())
