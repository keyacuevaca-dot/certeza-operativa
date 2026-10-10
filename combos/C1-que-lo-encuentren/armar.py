# «Que lo encuentren»: arma en un solo paso la página (W1) y el perfil de Google y WhatsApp (P1).
# Uso:   python3 combos/C1-que-lo-encuentren/armar.py ruta/a/negocio.json [--sin-pdf]
# Resultado en <carpeta del json>/salida/:
#   pagina/   la página lista para publicar
#   perfil/   textos, guía, tarjeta con QR (y sus PDF si hay Chrome o Chromium en la computadora)
#   index.html  índice para revisar todo antes de enseñárselo al cliente
import argparse
import glob
import os
import shutil
import subprocess
import sys
from html import escape as esc

AQUI = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(os.path.dirname(os.path.dirname(AQUI)), 'componentes')
sys.path[:0] = [COMP, os.path.join(COMP, 'W1'), os.path.join(COMP, 'P1')]
import construir as w1  # noqa: E402
import generar as p1  # noqa: E402

CHROMES = ['chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable',
           '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
           r'C:\Program Files\Google\Chrome\Application\chrome.exe',
           r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe']


def buscar_chrome():
    if os.environ.get('CHROME'):
        return os.environ['CHROME']
    for ch in CHROMES + sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome')):
        ruta = shutil.which(ch) or (ch if os.path.exists(ch) else None)
        if ruta:
            return ruta
    return None


def pdf(chrome, html, destino):
    url = 'file://' + os.path.abspath(html).replace('\\', '/')
    subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--no-pdf-header-footer',
                    f'--print-to-pdf={destino}', url], check=True, capture_output=True, timeout=120)


def indice(n, salida, avisos):
    items = [('pagina/index.html', 'Página de lanzamiento (vista en celular y computadora)'),
             ('perfil/textos.html', 'Textos para Google y WhatsApp Business (con botón Copiar)'),
             ('perfil/guia.html', 'Guía para el dueño, paso a paso'),
             ('perfil/tarjeta.html', 'Tarjeta y letrero con QR a su WhatsApp')]
    for x in ('guia.pdf', 'tarjeta.pdf', 'textos.pdf'):
        if os.path.exists(os.path.join(salida, 'perfil', x)):
            items.append((f'perfil/{x}', f'{x} para imprimir o mandar'))
    lis = ''.join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in items)
    pend = ''.join(f'<li>{esc(a)}</li>' for a in avisos) or '<li>Sin avisos.</li>'
    html = f'''<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Entrega · {esc(n["nombre"])}</title><meta name="robots" content="noindex, nofollow">
<style>body{{margin:0;font:16px/1.5 system-ui,sans-serif;color:#EAF2F4;background:#0D3441}}main{{max-width:760px;margin:0 auto;padding:20px 16px}}
a{{color:#7FE0DE}}li{{margin:8px 0}}h1{{line-height:1.2}}h2{{color:#28B7B5;font-size:1.1rem;margin-top:28px}}</style></head>
<body><main><h1>{esc(n["nombre"])}: que lo encuentren</h1><p>Revise todo antes de enseñárselo al cliente.</p>
<h2>Entregables</h2><ol>{lis}</ol><h2>Pendientes y avisos</h2><ol>{pend}</ol></main></body></html>
'''
    with open(os.path.join(salida, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    ap = argparse.ArgumentParser(description='Arma la página y el perfil de Google y WhatsApp desde negocio.json')
    ap.add_argument('negocio')
    ap.add_argument('--sin-pdf', action='store_true')
    a = ap.parse_args()

    dest_w, av_w = w1.construir(a.negocio)
    if w1.imprimir(av_w, dest_w, 'Página'):
        return 1
    dest_p, av_p = p1.generar(a.negocio)
    if av_p.errores:
        return 1
    print(f'Perfil: listo en {dest_p}')
    for i, t in enumerate(av_p.avisos, 1):
        print(f'  aviso {i}. {t}')

    if not a.sin_pdf:
        chrome = buscar_chrome()
        if chrome:
            for x in ('guia', 'tarjeta', 'textos'):
                try:
                    pdf(chrome, os.path.join(dest_p, f'{x}.html'), os.path.join(dest_p, f'{x}.pdf'))
                except (subprocess.SubprocessError, OSError) as e:
                    print(f'  No pude hacer {x}.pdf ({e}). Ábralo en Chrome y use Imprimir > Guardar como PDF.')
            print('PDF: guia.pdf, tarjeta.pdf y textos.pdf en perfil/')
        else:
            print('PDF: no encontré Chrome. Abra guia.html y tarjeta.html en Chrome y use Imprimir > Guardar como PDF.')

    n = w1.c.cargar(a.negocio)
    salida = os.path.dirname(dest_w)
    vistos, avisos = set(), []
    for t in av_w.avisos + av_p.avisos:
        if t not in vistos:
            vistos.add(t)
            avisos.append(t)
    indice(n, salida, avisos)
    print(f'Índice para revisar: {os.path.join(salida, "index.html")}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
