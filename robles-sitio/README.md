# Comercializadora Robles · sitio web

**Estado: construido para revisión. No está publicado.** No se registró ningún dominio, no se envió ningún mensaje y no se publicó nada. La página lleva una cinta de «vista previa» y `noindex`.

## Verlo

- **`robles-portatil.html`**: todo el sitio en **un solo archivo**. Se abre con doble clic en cualquier navegador, con o sin internet, y se puede mandar por WhatsApp o correo como archivo. Sin instalar nada.
- **`dist/`**: el mismo sitio, una carpeta por página (`dist/index.html`). Es lo que se subiría a un hosting de páginas estáticas.

En GitHub, estos archivos se ven como código; descárgalos (*Download raw file*) o clona la rama.

## Qué incluye

| Página | Contenido |
|---|---|
| Inicio | Encabezado con buscador, héroe con panel «Busca un producto» y búsquedas frecuentes, cinta de productos que se mueve (con botón Pausar), categorías con icono, marcas, «Manda tu lista» y pie con tienda y contacto |
| Catálogo | 202 productos del inventario del cliente, en filas con icono, menú lateral de categorías, buscador, cantidad y «Agregar» a mi lista |
| Construcción, Limpieza, Papelería | Una página por línea; Papelería aún sin productos |
| Cómo comprar | Cómo se compra (3 pasos con icono), formas de pago y preguntas |
| Visítanos | Ubicación, horario y contacto |

Solo hay dos llamadas a cotizar: «Cotiza por WhatsApp» arriba y «Enviar por WhatsApp» con la lista. Los productos solo tienen «Agregar».

**Copiar mensaje:** la lista escrita y «Mi lista» tienen un botón para copiar el texto por si WhatsApp no abre.

**Mi lista:** el visitante agrega productos y envía **toda la lista en un solo mensaje de WhatsApp**. Se guarda solo en su dispositivo. WhatsApp abre el mensaje listo; **enviarlo lo decide la persona**.

**Precios:** un precio solo se muestra si tiene monto, unidad, IVA y fecha de vigencia sin vencer. Mientras ningún producto tenga precio publicado, el aviso «Los precios te los damos por WhatsApp» sale una sola vez arriba de la lista; en cuanto haya algún precio, los productos sin precio indican «Solicita precio». No se muestra existencia.

## Actualizar el catálogo cada semana (administradora)

1. Guarda una copia de `dist/assets/js/catalogo.js`.
2. Abre `herramientas/editor-catalogo.html` y carga ese archivo.
3. Cambia productos y precios (la tabla avisa qué falta para que un precio se muestre).
4. Pulsa **Descargar catalogo.js** y reemplaza con él `dist/assets/js/catalogo.js`.
5. Abre `dist/index.html` y revisa.

Para el archivo único, quien administre el repositorio ejecuta `python3 scripts/build.py`. Antes, copia el `catalogo.csv` que descargó el editor a `datos/catalogo.csv`. Todavía **falta comprobar que la administradora puede hacerlo sola**.

## Fotos de producto y logos de marca

- **Fotos:** guarda una por producto como `src/img/productos/<id>.webp` (o `.jpg`/`.png`; el `id` está en `datos/catalogo.csv`, por ejemplo `C101.webp`) y ejecuta `python3 scripts/build.py`. Sin foto, el producto muestra su icono. Solo fotos propias o autorizadas.
- **Logos de marca:** `src/img/marcas/<marca>.png|.webp|.svg` (minúsculas, sin acentos: `truper.png`). Sin archivo, la marca sale como texto en un recuadro. Hoy **todas** salen como texto: no hay archivos de logos.

## Cambiar otros detalles

Datos del negocio, horario y textos: `scripts/build.py`. Colores y tamaños: `src/site.css`. Después, `python3 scripts/build.py` regenera todo (solo requiere Python 3; no usa la red).

## Publicarlo después (requiere autorización aparte)

`python3 scripts/build.py --publicar` quita la cinta y el `noindex`, agrega el dominio, `canonical` y `sitemap.xml`. Se sube **solo el contenido de `dist/`**, nunca la raíz de esta carpeta. El dominio elegido es `comercializadorarobles.mx`: **su disponibilidad no está verificada ni está registrado**.

## Decisiones

- **Diseño (v3):** Ruta A (catálogo claro). Sistema único: radio de 8 px, líneas de 1 px, escala de espacios de 8 px. Azul `#044770` y naranja `#E97E1C`, tomados del logo real; el naranja solo rellena botones, con texto `#1A1A1A`. El botón «Menú» lleva marco azul de 2 px y fondo celeste claro para que destaque.
- **Iconos:** uno por producto y subcategoría, de trazo simple y un solo grosor. Salen de Lucide (licencia ISC, en `licencias/Lucide-ISC.txt`) más unos pocos dibujados a mano en `src/sprite-prod.svg`. No son fotos: se sustituyen por fotos reales cuando existan.
- **Tipografía:** sin Arial. Bricolage Grotesque (títulos) e Instrument Sans (cuerpo), con licencia libre (OFL), incluidas en el sitio. Licencias en `licencias/`.
- **Que no se parezca a Truper ni a Pretul:** el azul domina y el naranja ocupa poca superficie. **No pude comprobar sus colores reales** (sin acceso a sus sitios): conviene comparar con un empaque. Si el naranja resultara parecido, el botón pasa a celeste `#00A9E9` con texto oscuro.
- **Datos publicados:** dirección, teléfono y WhatsApp, horario de lunes a sábado y el correo aprobado. **No se publica** el domingo, el nombre del responsable ni datos bancarios o fiscales.
- **Inventario:** salió de 4 capturas del cliente, leídas por dos lectores independientes que coincidieron en las 172 filas (respaldo en `datos/inventario-capturas.csv`: texto original y nombre en el sitio). Las capturas **no traían la columna de precios**; por eso ningún producto muestra precio.
- **Competencia:** no pude abrir Home Depot ni Office Depot (acceso bloqueado desde este entorno). Además, sus precios y fotos no son del negocio y las fotos tienen derechos. Se tomó de ellos solo la **estructura** (buscador al centro, cinta de productos, categorías con icono), a partir de lo que ya se conoce de ese tipo de sitios.
- **Marca:** logo real del cliente (imagen con fondo transparente en `src/img/`). Falta confirmar si existe el archivo vectorial original y quién tiene los derechos de uso.

## Qué falta y ruta para terminar

Ver **`PENDIENTES.md`**: ruta ordenada, tabla de estado (rellenado · por decidir · falta dato) y lo que simplifica la operación.

Herramientas para quien atiende: `herramientas/respuestas-whatsapp.md` (respuestas rápidas), `herramientas/qr-whatsapp.png` y `.svg` (QR a WhatsApp) y `herramientas/editor-catalogo.html`.

## Lo que falta o no se afirma

- **Precios:** el cliente no los incluyó en las capturas. El campo `unidad_del_precio` ya trae la unidad de venta; falta monto, IVA y vigencia.
- **Fotos y logos de marca:** ver la sección de arriba. Hoy se usan iconos y texto.
- **Papelería:** sin productos en la lista, por eso no tiene catálogo.
- **Por confirmar con la tienda:** Cloralex «750 ml», varilla en pulgadas, marca «Del Toro», pegapiso «Ade1000», Truper en picos y palas, y las descripciones que tocan el borde de la captura (marcadas en `nota_interna`). Ver `PENDIENTES.md`.
- No se afirman entregas, facturación, garantías, descuentos, testimonios, pago con tarjeta ni existencia.

## Pruebas realizadas

Móvil 320, 360 y 390 px, tableta 768, 980–1180 y escritorio 1440 en las 7 páginas, en `dist/` y en el archivo único: sin desbordes, sin errores de consola y sin peticiones externas. Contraste AA, objetivos táctiles de 44 px, foco visible, orden de encabezados, navegación por teclado, diálogo de «Mi lista», búsqueda, chips de búsqueda frecuente, cantidades, enlaces de WhatsApp, cinta (mueve, pausa y enlaces), categorías que llevan a su subcategoría, foto de producto, editor de punta a punta y el archivo dentro de un marco con sandbox. **No se probó** en celulares reales ni con lectores de pantalla, y no se midieron velocidad ni SEO.

## Privacidad

El repositorio es público. Este sitio contiene la dirección, el teléfono y el correo del negocio, cuya publicación fue aprobada. Revisa `../robles-propuesta/README.md` sobre nombres que quedaron en el historial.
