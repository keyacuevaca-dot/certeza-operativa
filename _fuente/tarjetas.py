# Imagen para compartir (1200×630) de cada página interna: marca, título con su palabra en turquesa, frase corta y la
# escena propia de la página. Es la que se ve al mandar el enlace por WhatsApp o Facebook.
# Uso, desde la raíz del sitio y con el servidor local encendido (python3 -m http.server 8765 --bind 127.0.0.1):
#   python _fuente/tarjetas.py        → escribe assets/compartir/<página>.jpg; después correr python _fuente/construir.py
import json, os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import construir as C
from escenas import escena, acento

TEMP = os.path.join(C.RAIZ, '_fuente', '_tarjetas')
SALIDA = os.path.join(C.RAIZ, 'assets', 'compartir')
SERVIDOR = 'http://127.0.0.1:8765/'

ESTILO = '''html, body { margin: 0; background: #1E2328; }
.t { position: relative; width: 1200px; height: 630px; overflow: hidden; background: var(--petroleo); font-family: var(--sans); color: var(--texto-claro-2); }
.t-izq { position: absolute; left: 72px; top: 60px; bottom: 58px; width: 540px; display: flex; flex-direction: column; }
.t-marca { display: flex; align-items: center; gap: 16px; }
.t-marca .m-logo { width: 62px; height: 47px; }
.t-marca .m-nombre { display: block; width: 168px; height: auto; color: var(--texto-claro); overflow: visible; }
.t-marca .m-nombre text { font-family: var(--sans); font-size: 30px; fill: var(--texto-claro-2); }
.t-cuerpo { margin: auto 0; }
.t-pastilla { display: inline-flex; align-items: center; height: 36px; margin-bottom: 22px; padding: 0 18px; border: 1px solid var(--caja-borde); border-radius: 999px; font-size: 18px; font-weight: 600; color: var(--texto-claro-2); }
.t h1 { max-width: 500px; margin: 0 0 18px; font-family: var(--sans); font-weight: 700; font-size: 70px; line-height: .98; letter-spacing: -.025em; color: var(--texto-claro); }
.t h1 .acento { color: var(--acento-encabezado); }
.t p { margin: 0; font-size: 26px; line-height: 1.32; color: var(--texto-claro-2); }
.t-pie { font-size: 20px; color: var(--nota-oscura); }
.t .escena { position: absolute; right: 16px; top: 30px; width: 608px; height: 570px; }'''

MARCA = ('<div class="t-marca"><svg class="m-logo" viewBox="0 0 175 133" aria-hidden="true"><use href="#mark"/></svg>'
         '<svg class="m-nombre" viewBox="0 0 433.6 118" aria-hidden="true"><use href="#certeza" width="433.6" height="72.8"/>'
         '<text x="0" y="114" textLength="433.6" lengthAdjust="spacing">OPERATIVA</text></svg></div>')


def html_tarjeta(slug):
    pastilla, titulo, frase = C.datos_tarjeta(slug)
    partes = acento(slug, titulo)
    h1 = f'{C.esc(partes[0])}<span class="acento">{C.esc(partes[1])}</span>{C.esc(partes[2])}' if partes else C.esc(titulo)
    return (f'<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><link rel="stylesheet" href="/assets/estilo.css"><style>{ESTILO}</style></head>'
            f'<body>{C.sprite()}<div class="t"><div class="t-izq">{MARCA}<div class="t-cuerpo"><span class="t-pastilla">{pastilla}</span>'
            f'<h1>{h1}</h1><p>{C.esc(frase)}</p></div><div class="t-pie">Diagnóstico breve sin costo · Tepic, Nayarit</div></div>{escena(slug)}</div></body></html>')


if __name__ == '__main__':
    slugs = [i['slug'] for i in C.INDUSTRIAS] + [s['slug'] for s in C.SOLUCIONES] + ['nosotros']
    os.makedirs(TEMP, exist_ok=True)
    os.makedirs(SALIDA, exist_ok=True)
    try:
        for s in slugs:
            open(os.path.join(TEMP, f'{s}.html'), 'w', encoding='utf-8').write(html_tarjeta(s))
        lista = os.path.join(TEMP, 'lista.json')
        json.dump(slugs, open(lista, 'w'))
        subprocess.run(['node', os.path.join(C.RAIZ, '_fuente', 'tarjetas.js'), SERVIDOR + '_fuente/_tarjetas/', lista, SALIDA], check=True)
    finally:
        shutil.rmtree(TEMP, ignore_errors=True)
    print('\n'.join(f'assets/compartir/{s}.jpg' for s in slugs))
