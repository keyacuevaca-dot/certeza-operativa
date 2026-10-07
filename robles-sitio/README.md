# Comercializadora Robles · sitio web

**Estado: construido para revisión. No está publicado.** No se registró ningún dominio, no se envió ningún mensaje y no se publicó nada. La página lleva una cinta de «vista previa» y `noindex`.

## Verlo

- **`robles-portatil.html`**: todo el sitio en **un solo archivo**. Se abre con doble clic en cualquier navegador, con o sin internet, y se puede mandar por WhatsApp o correo como archivo. Sin instalar nada.
- **`dist/`**: el mismo sitio, una carpeta por página (`dist/index.html`). Es lo que se subiría a un hosting de páginas estáticas.

En GitHub, estos archivos se ven como código; descárgalos (*Download raw file*) o clona la rama.

## Qué incluye

| Página | Contenido |
|---|---|
| Inicio | Qué vende y dónde, botón «Cotiza por WhatsApp», tres líneas (Construcción primero), productos, «¿Ya tienes tu lista?», cómo cotizar y tarjeta de la tienda |
| Catálogo | 24 productos con buscador, cantidad, «Cotizar por WhatsApp» y «Agregar a mi lista» |
| Construcción, Limpieza, Papelería | Una página por línea; Papelería aún sin productos |
| Cómo comprar | Solicitar cotización, formas de pago y preguntas |
| Visítanos | Ubicación, horario y contacto |

**Mi lista:** el visitante agrega productos y envía **toda la lista en un solo mensaje de WhatsApp**. Se guarda solo en su dispositivo. WhatsApp abre el mensaje listo; **enviarlo lo decide la persona**.

**Precios:** un precio solo se muestra si tiene monto, unidad, IVA y fecha de vigencia sin vencer. Si falta algo o venció, dice «Solicita precio». No se muestra existencia.

## Actualizar el catálogo cada semana (administradora)

1. Guarda una copia de `dist/assets/js/catalogo.js`.
2. Abre `herramientas/editor-catalogo.html` y carga ese archivo.
3. Cambia productos y precios (la tabla avisa qué falta para que un precio se muestre).
4. Pulsa **Descargar catalogo.js** y reemplaza con él `dist/assets/js/catalogo.js`.
5. Abre `dist/index.html` y revisa.

Para el archivo único, quien administre el repositorio ejecuta `python3 scripts/build.py`. Antes, copia el `catalogo.csv` que descargó el editor a `datos/catalogo.csv`. Todavía **falta comprobar que la administradora puede hacerlo sola**.

## Cambiar otros detalles

Datos del negocio, horario y textos: `scripts/build.py`. Colores y tamaños: `src/site.css`. Después, `python3 scripts/build.py` regenera todo (solo requiere Python 3; no usa la red).

## Publicarlo después (requiere autorización aparte)

`python3 scripts/build.py --publicar` quita la cinta y el `noindex`, agrega el dominio, `canonical` y `sitemap.xml`. Se sube **solo el contenido de `dist/`**, nunca la raíz de esta carpeta. El dominio elegido es `comercializadorarobles.mx`: **su disponibilidad no está verificada ni está registrado**.

## Decisiones

- **Diseño:** Ruta A (catálogo claro). Azul `#174F7C` y naranja `#F48F07` del archivo de diseño del negocio; el naranja solo rellena botones, con texto `#1A1A1A`.
- **Tipografía:** sin Arial. Bricolage Grotesque (títulos) e Instrument Sans (cuerpo), con licencia libre (OFL), incluidas en el sitio. Licencias en `licencias/`.
- **Que no se parezca a Truper ni a Pretul:** el azul domina, el naranja ocupa poca superficie y se evitó el amarillo con negro. **No pude comprobar sus colores reales** (sin acceso a sus sitios): conviene comparar con un empaque. Si el naranja resultara parecido, el botón pasa a celeste `#00A9E9` con texto oscuro.
- **Datos publicados:** dirección, teléfono y WhatsApp, horario de lunes a sábado y el correo aprobado. **No se publica** el domingo, el nombre del responsable ni datos bancarios o fiscales.
- **Sin fotos:** ilustraciones propias de línea, genéricas, no son inventario.
- **Marca:** la casa y el nombre en texto son provisionales y **no son el logo original**. Falta exportar la pieza correcta del archivo de diseño.

## Lo que falta o no se afirma

- **Materiales de obra:** la lista del negocio no los trae (cemento, varilla, block…), aunque son la línea principal. No se inventaron; el sitio invita a preguntar por WhatsApp.
- **Papelería:** sin productos en la lista, por eso no tiene catálogo.
- **Marcas:** Truper se mencionó pero no quedó asignada a ningún producto; solo Stanley, Cloralex, Fabuloso, Suavitel, Kleenex y Raid aparecen donde el negocio las indicó.
- No se afirman entregas, facturación, garantías, descuentos, testimonios, pago con tarjeta ni existencia.

## Pruebas realizadas

Móvil 360 y 390 px, tableta 768 y escritorio 1440 en las 7 páginas, tanto en `dist/` como en el archivo único: sin desbordes, sin errores de consola y sin peticiones externas. Contraste AA en todo el texto, objetivos táctiles de 44 px, foco visible, navegación por teclado, reflujo a 320 px, diálogo de «Mi lista» y las instrucciones del editor de punta a punta. **No se midieron** velocidad, SEO ni posicionamiento, y no se probó con lectores de pantalla reales.

## Privacidad

El repositorio es público. Este sitio contiene la dirección, el teléfono y el correo del negocio, cuya publicación fue aprobada. Revisa `../robles-propuesta/README.md` sobre nombres que quedaron en el historial.
