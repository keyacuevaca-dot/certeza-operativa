# W1 · Página de lanzamiento

Una página de 5 bloques que se arma desde `negocio.json` y sale en HTML estático, rápida en celular.
Uso interno de Certeza: el cliente nunca ve el código W1.

1. **Presentación:** logo, nombre (igual al letrero), frase, «Abierto/Cerrado ahora», botón de WhatsApp y botón de llamar.
2. **Qué ofrece:** lo que lo distingue, servicios, precios solo si están completos y formas de pago.
3. **Fotos:** de 3 a 5, en WebP de 480 y 960 px, con carga diferida.
4. **Ubicación y horario:** dirección y «Cómo llegar» (o solo la zona si va a domicilio), horario y días cerrados.
5. **Contacto final:** botón de WhatsApp, teléfono y redes.

Además: título y descripción para Google, vista previa para Facebook y WhatsApp (1200 × 630), datos estructurados
LocalBusiness (schema.org) con horario, dirección o zona, y botón fijo de WhatsApp en celular.
Sin recursos externos (ni fuentes, ni mapas incrustados, ni librerías): por eso carga en menos de 1 s.

## Lo que hay en la carpeta

- `construir.py`: arma la página. Usa `../comun.py` y la plantilla `../negocio.plantilla.json`.
- La ficha de datos para llenar con el dueño está en `../P1/ficha-de-datos.html` (sirve para W1 y P1).

## Preparar la computadora (una sola vez)

1. Instale Python 3.10 o más nuevo.
2. En la carpeta del repositorio: `pip install -r componentes/requirements.txt` (Pillow y segno).

## Personalizar para un cliente nuevo · 5 h

1. **(0:30)** Llenar con el dueño las secciones 1 a 4 de la ficha de datos (`../P1/ficha-de-datos.html`, impresa o en pantalla). Tomar foto del letrero.
2. **(0:45)** Recibir o tomar las fotos (3 a 5, horizontales, desde 1200 px de ancho). Guardarlas en `clientes/<negocio>/fotos/` con nombres simples (`fachada.jpg`). La primera es la fachada con letrero.
3. **(0:45)** Copiar `componentes/negocio.plantilla.json` a `clientes/<negocio>/negocio.json` y llenarlo con la ficha. Lo que falte se deja vacío: no se inventa.
4. **(0:30)** Construir: `python3 componentes/W1/construir.py clientes/<negocio>/negocio.json`. Corregir los errores que marque, leer los avisos de `salida/pagina/reporte.txt` y ajustar textos y colores.
5. **(0:30)** Probar: abrir `salida/pagina/index.html` en el celular (360 px) y en la computadora; tocar el botón de WhatsApp desde un celular; confirmar que no hay desborde horizontal ni avisos de contraste.
6. **(1:00)** Mandar la vista previa al cliente (sale con cinta «Vista previa» y `noindex`) y aplicar una sola ronda de cambios.
7. **(0:45)** Con el sí del cliente: poner `"vista_previa": false` y `"dominio"`, reconstruir, publicar y conectar el dominio (abajo).
8. **(0:15)** Probar la dirección final desde el celular del cliente, pegarla en un chat de WhatsApp para ver la vista previa y guardar la evidencia (captura y fecha).

Total: 5:00 h.

Si el cliente también contrató el perfil de Google y WhatsApp, use el armado del combo
(`combos/C1-que-lo-encuentren/armar.py`), que hace W1 y P1 con el mismo `negocio.json`.

## Reglas que el script ya cuida

1. Precio solo con monto, unidad, IVA y vigencia sin vencer; si no, una sola nota «Pregunte el precio por WhatsApp».
2. Colores: el texto se elige solo (blanco o tinta) para pasar contraste AA; si un color no llega, avisa.
3. Número de WhatsApp: acepta 10 dígitos y arma `https://wa.me/52XXXXXXXXXX` (si viene con el «1» de antes, lo quita).
4. Atención a domicilio (`"atencion": "area"`): no publica la dirección, solo las zonas.
5. Vista previa: cinta y `noindex` hasta que el cliente autorice publicar.
6. Sin datos personales del dueño, sin formularios: la página no recoge datos, así que no necesita aviso de privacidad.
   Si algún día se agrega un formulario, el aviso de privacidad lo redacta el cliente o su asesor (LFPDPPP).

## Publicar gratis

La cuenta de alojamiento se abre con el correo del cliente: lo publicado queda a su nombre.
Se sube la carpeta completa `salida/pagina/` (con `img/`). Tres opciones sin costo para un sitio estático:

**A. Netlify Drop (la más simple, sin instalar nada)**
1. Con el correo del cliente, entre a app.netlify.com/drop.
2. Arrastre la carpeta `salida/pagina/` a la página.
3. Le da una dirección `algo.netlify.app`. En «Site configuration» cámbiele el nombre (por ejemplo `autolavado-gota-azul`).
4. Para actualizar: «Deploys» > arrastrar de nuevo la carpeta.

**B. Cloudflare Pages**
1. Con el correo del cliente, cree la cuenta en dash.cloudflare.com.
2. Workers y Pages > Crear > Pages > «Subir recursos» (subida directa).
3. Ponga el nombre del proyecto y suba la carpeta `salida/pagina/`. Queda en `nombre.pages.dev`.

**C. GitHub Pages** (si el cliente tiene o acepta una cuenta de GitHub)
1. Cree un repositorio público y suba el contenido de `salida/pagina/`.
2. Settings > Pages > «Deploy from a branch» > `main` y carpeta `/ (root)`.
3. Queda en `usuario.github.io/repositorio/`.

Las tres dan HTTPS sin costo. Las condiciones del plan gratuito cambian: revíselas el día que publique (no verificado hoy).

## Conectar el dominio que paga el cliente

El dominio (por ejemplo `autolavadogotaazul.mx`) se compra **a nombre del cliente**, con su correo y su pago.
Certeza no lo registra a su nombre.

1. En `negocio.json` ponga `"dominio": "https://www.sudominio.mx"` y reconstruya (actualiza la vista previa en redes,
   el `canonical`, el `sitemap.xml` y el archivo `CNAME`). Vuelva a subir la carpeta.
2. En el alojamiento, agregue el dominio:
   - Netlify: Domain management > Add a domain.
   - Cloudflare Pages: el proyecto > Custom domains > Set up a domain.
   - GitHub Pages: Settings > Pages > Custom domain (el archivo `CNAME` ya va en la carpeta).
3. En el panel donde se compró el dominio (DNS), cree los registros que le indique el alojamiento. Lo usual:
   - `www` → registro **CNAME** que apunta a la dirección gratuita (`algo.netlify.app`, `nombre.pages.dev` o `usuario.github.io`).
   - Dominio sin `www`: en GitHub Pages, cuatro registros **A** a `185.199.108.153`, `185.199.109.153`, `185.199.110.153` y `185.199.111.153`;
     en Netlify y Cloudflare, el registro que muestre su panel (o pase los DNS a Cloudflare).
4. Espere a que el alojamiento marque el dominio como verificado y active HTTPS (de minutos a unas horas).
5. Abra el dominio desde el celular, con y sin `www`, y confirme que carga con candado.
6. Pegue el dominio en el Perfil de Negocio de Google (campo Sitio web) y en WhatsApp Business.

## Probar la calidad

- Celular: abra la página y achique la ventana a 360 px; no debe haber desplazamiento horizontal.
- Lighthouse (Chrome > Inspeccionar > Lighthouse > Mobile) o pagespeed.web.dev con la dirección publicada.
  Con la demo, el 10-oct-2026: 100 en rendimiento, accesibilidad, buenas prácticas y SEO (en vista previa el SEO baja a 66 por el `noindex`, a propósito).
- Datos estructurados: pegue la dirección en search.google.com/test/rich-results.
