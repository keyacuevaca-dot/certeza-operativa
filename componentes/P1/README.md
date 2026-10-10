# P1 · Google Maps y WhatsApp Business

Deja al negocio con su Perfil de Negocio de Google completo y enviado a verificación, y con WhatsApp Business
configurado (perfil, bienvenida, ausencia, 5 respuestas rápidas y catálogo), más una tarjeta con QR a su WhatsApp.
Se vende solo dentro de un combo (con la página W1 o con un Ticket), nunca suelto.
Uso interno: el cliente nunca ve el código P1.

**Regla fija:** el dueño da de alta todo desde su propia cuenta. Certeza lo acompaña y nunca pide ni usa su contraseña.
El perfil queda a nombre del cliente.

## Lo que hay en la carpeta

1. `ficha-de-datos.html`: ficha para llenar con el dueño (sirve también para W1). Se imprime en carta o se llena en pantalla.
2. `generar.py`: desde `negocio.json` escribe en `salida/perfil/`:
   - `textos.html` y `textos.txt`: todo lo que se pega en Google y en WhatsApp Business, con botón «Copiar» y conteo de caracteres.
     Google: nombre, categorías, ubicación o zona, horario, teléfono, sitio web, descripción (máx. 750), fecha de apertura,
     atributos, fotos para subir y servicios. WhatsApp: perfil de empresa, mensaje de bienvenida, mensaje de ausencia,
     5 respuestas rápidas (`/horario`, `/ubicacion` o `/zona`, `/servicios`, `/pago` o `/llamar`, `/gracias`), catálogo y enlace directo.
   - `guia.html`: guía paso a paso para el dueño, con el guion del video de verificación adaptado a su negocio.
   - `tarjeta.html`, `qr-whatsapp.svg` y `qr-whatsapp.png`: hoja carta con un letrero de mostrador y 4 tarjetas con QR.
   - `reporte.txt`: avisos y pendientes.
3. Para cambiar un texto generado sin tocar el código, escríbalo en `"textos"` de `negocio.json`
   (`descripcion_google`, `descripcion_whatsapp`, `bienvenida`, `ausencia` o `rapidas`).

Los mensajes de WhatsApp traen texto distinto según de dónde llegan: «vi su página» (página) y «escaneé su código» (tarjeta).
Así el dueño sabe qué canal le trae clientes; es la evidencia de toques a WhatsApp.

## Preparar la computadora (una sola vez)

1. Python 3.10 o más nuevo.
2. `pip install -r componentes/requirements.txt`.

## Personalizar para un cliente nuevo · 2 h

1. **(0:15)** Con el dueño, llenar la sección 5 de la ficha (correo de Google del negocio, si ya aparece en Maps,
   si ya usa WhatsApp Business, equipo de trabajo). Confirmar el nombre con la foto del letrero y elegir la categoría
   escribiendo el giro en Google (se elige de la lista, no se inventa). Pasarlo a `negocio.json`
   (si ya se hizo la página, es el mismo archivo).
2. **(0:15)** Generar: `python3 componentes/P1/generar.py clientes/<negocio>/negocio.json`. Leer `reporte.txt`,
   corregir lo que marque y abrir `guia.html` y `tarjeta.html` en Chrome > Imprimir > Guardar como PDF
   (el armado del combo hace los PDF solo).
3. **(0:45)** Sesión con el dueño, con su celular, siguiendo la Parte 1 de la guía: buscar el negocio en Maps,
   reclamarlo o agregarlo, nombre igual al letrero, categoría, ubicación o zona, teléfono, y grabar el video de
   verificación si Google lo pide. Abrir `textos.html` en el celular del dueño y pegar horario, descripción, servicios y fotos.
4. **(0:30)** Parte 2 de la guía: instalar o configurar WhatsApp Business, perfil de empresa, mensaje de bienvenida,
   mensaje de ausencia, las 5 respuestas rápidas y el catálogo.
5. **(0:15)** Probar: escanear la tarjeta desde otro celular y mandar un mensaje (debe llegar con el texto listo y responder
   la bienvenida); revisar que la ficha diga «en revisión» o «verificada». Imprimir la tarjeta. Guardar evidencia
   (capturas con fecha) y anotar los pendientes.

Total: 2:00 h. Si Google tarda en verificar, la entrega es la ficha completa y enviada a verificación; el enlace de la ficha
(`mapa_url`) se agrega después a la página y a la respuesta `/gracias`.

## Lo que pide Google (resumen para explicar al dueño)

1. **Nombre:** el que usa en el mundo real, igual al letrero, papelería y marca. No agregar ciudad, lemas ni palabras clave:
   puede causar la suspensión del perfil.
2. **Ubicación:** si los clientes van al local, dirección exacta y pin en la entrada. Si va a domicilio, se oculta la
   dirección y se muestran las zonas que atiende (negocio con área de servicio). Un solo perfil por negocio.
3. **Descripción:** hasta 750 caracteres, sin enlaces, precios ni promociones. Lo importante en los primeros ~250, que es lo que se ve sin tocar «Más».
4. **Video de verificación:** un solo video continuo, sin cortes ni edición, de al menos 30 segundos, grabado y subido desde la app
   en ese momento. Se muestra: la calle (letreros, número, negocios vecinos), el letrero permanente con el nombre exacto,
   prueba de que lo maneja (abrir con llave, caja, área de empleados) y el equipo de trabajo. Sin identificaciones, datos
   bancarios ni de clientes. Para negocios a domicilio: referencia fija de la calle, herramientas y vehículo o uniforme con el nombre.
5. **Tiempo:** la revisión la decide Google y puede tardar días. Mientras revisa, no cambiar nombre, dirección ni categoría.

## WhatsApp: enlace y números de México

- Formato: `https://wa.me/52` + los 10 dígitos, sin `+`, espacios, guiones ni el «1» que llevaban los celulares antes.
  El script lo arma solo desde los 10 dígitos.
- Mensaje listo: se agrega `?text=` con el texto codificado (el script lo hace).

## Lo que no se hace

1. No se crea el perfil con cuentas de Certeza ni se pide la contraseña.
2. No se compran reseñas, no se ofrecen descuentos a cambio de reseñas ni se escriben reseñas.
3. No se promete un lugar en los resultados de Google ni un tiempo de verificación.
