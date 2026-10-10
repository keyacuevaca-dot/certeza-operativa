# C1 · Que lo encuentren

Documento interno. Al cliente se le muestra como **«Que lo encuentren»**, sin códigos ni horas por partida.

- **Para quién:** negocios que no aparecen o aparecen incompletos en Google.
- **Gancho:** ¿Aparece su negocio en Google Maps?
- **Promesa:** Que lo encuentren en Google y le escriban por WhatsApp con un toque.
- **Lo que incluye (para el cliente):**
  1. Su ficha de Google Maps completa y enviada a verificación, a su nombre.
  2. Una página con botón de WhatsApp, su ubicación y su horario, publicada y probada en celular.
  3. WhatsApp Business con mensaje de bienvenida, mensaje de ausencia, respuestas listas y una tarjeta con QR.
- **Lo que no incluye:** el pago del dominio (lo paga el cliente, a su nombre), Facebook e Instagram (otro combo),
  publicidad pagada, reseñas, ni un lugar garantizado en Google.

## Partidas y horas

1. Página de lanzamiento (`componentes/W1`): 5 h, fijas por nivel.
2. Google Maps y WhatsApp Business (`componentes/P1`): 2 h, fijas por nivel. Solo se vende dentro de un combo.

Total: 7 h útiles. Fuente: catálogo v4 del Evaluador (CERTEZA-CAT-INT-01, 9-oct-2026). Sin precios en este repositorio
(decisiones D1 y D2 del 10-oct).

## Orden de trabajo (ejemplo con 3 h útiles por día [P])

1. **Día 1 · 2:30 h.** Ficha de datos completa con el dueño (0:45), fotos (0:45), `negocio.json` (0:45), armar (0:15).
2. **Día 2 · 2:30 h.** Pruebas de la página (0:30), revisar textos y guía (0:15), sesión con el dueño: Google y video
   de verificación (0:45), WhatsApp Business (0:30), prueba del QR e impresión de la tarjeta (0:15), mandar la vista
   previa de la página (0:15).
3. **Revisión del cliente:** 1 día hábil para pedir su ronda de cambios.
4. **Día 3 · 2:00 h.** Ronda de cambios (1:00), publicar y conectar el dominio (0:45), cierre con evidencia (0:15).

Google puede tardar días en verificar la ficha; la entrega no depende de eso: se entrega la ficha completa y enviada.

## Cómo se arma

1. Una sola vez: `pip install -r componentes/requirements.txt`.
2. Cree la carpeta del cliente fuera de lo que se sube a GitHub: `clientes/<negocio>/` (está en `.gitignore`
   porque el repositorio es público). Dentro: `negocio.json` (copia de `componentes/negocio.plantilla.json`) y `fotos/`.
3. Arme todo: `python3 combos/C1-que-lo-encuentren/armar.py clientes/<negocio>/negocio.json`
4. Abra `clientes/<negocio>/salida/index.html`: enlaza la página, los textos, la guía, la tarjeta, los PDF y la lista de pendientes.
5. Siga los pasos de `componentes/W1/README.md` (5 h) y `componentes/P1/README.md` (2 h).

## Demo: Autolavado Gota Azul (inventado)

Nombre, teléfono (311 000 0000), dirección, precios, logo y fotos son inventados; las fotos son marcadores que dicen
«Foto de ejemplo». Datos en `demo/negocio.json`; resultado en `demo/salida/`.

1. Volver a armar: `python3 combos/C1-que-lo-encuentren/armar.py combos/C1-que-lo-encuentren/demo/negocio.json`
2. Ver: `demo/salida/index.html`, `demo/salida/pagina/index.html`, `demo/salida/perfil/guia.pdf` y `tarjeta.pdf`.

Probado el 10-oct-2026 (hora no especificada):
1. 360 px: sin desborde horizontal y sin errores en consola (página, textos, guía y tarjeta).
2. Lighthouse 13.5 en modo celular: con la configuración publicable (sin cinta, con dominio de ejemplo) 100 en rendimiento,
   accesibilidad, buenas prácticas y SEO; en vista previa, 100/100/100 y SEO 66 por el `noindex` puesto a propósito.
   Primera pintura 0.8 s, LCP 0.8–1.0 s, CLS 0.
3. QR leído con un lector (zxing): abre `https://wa.me/523110000000?text=Hola, escaneé su código. Quiero informes.`
4. Variantes: negocio a domicilio (oculta la dirección y muestra zonas), sin fotos, sin formas de pago, y datos
   faltantes (el armado se detiene y dice qué corregir).

## Lo que les falta a 3 fichas de autolavados en Tepic

No se pudo abrir Google Maps desde la sesión de trabajo. Lo que sigue sale de directorios que copian datos de Maps
(lavadosauto.com, autosyllantas.com y autolavadu.com.mx, consultados el 10-oct-2026). Los negocios van sin nombre porque el
repositorio es público; no se copiaron textos ni fotos.

1. **Autolavado A (col. San José):** calificación 4.4 con 18 opiniones; horario publicado; sin página propia; una reseña
   negativa visible (no se pudo ver si el negocio respondió). Le falta: página con botón de WhatsApp y más fotos del trabajo.
2. **Autolavado B (Lagos del Country):** opiniones mixtas con quejas de limpieza; abre los 7 días; sin página propia.
   Le falta: página con botón de WhatsApp y fotos del trabajo terminado que respondan a esas quejas.
3. **Autolavado C (av. Rey Nayar):** más de 200 opiniones (4.2), pero dos directorios muestran horarios distintos.
   Le falta: horario único y confirmado, y horario especial de días festivos.

Patrón: en 2 de 3 el horario no es confiable o no coincide entre fuentes, y ninguno de los 3 tiene página propia con botón de
WhatsApp. De 4 autolavados revisados, solo 1 (col. San Juan) tiene página propia.
Coincide con la nota del Evaluador: las 2 fichas que Kevin revisó en San Juan estaban sin reclamar.

**Pendiente (10 min por ficha, desde el celular):** confirmar en Google Maps, para cada uno: si está reclamada
(«¿Es el propietario?» visible = sin reclamar), número de fotos, si tiene descripción, servicios, sitio web, horario especial,
si responde reseñas y si tiene botón de mensajes o WhatsApp.

## Entrega al cliente (lista de cierre)

1. Página publicada en su dominio o en la dirección gratuita, abierta desde su celular.
2. Ficha de Google completa y con estado «en revisión» o «verificada» (captura con fecha).
3. WhatsApp Business con bienvenida, ausencia, 5 respuestas rápidas y catálogo (capturas).
4. Tarjeta impresa y QR probado.
5. Guía impresa o en PDF, a su nombre.
6. Cuentas y dominio a nombre del cliente; Certeza sin contraseñas.
