# Reglas para crear sitios web en este repositorio

Aplican a `robles-sitio/` y a cualquier sitio nuevo. Salen de lo aprendido en el proyecto de Comercializadora Robles.

## Secuencia (no saltar pasos)
1. **Datos y decisiones del negocio** antes de diseñar: productos, logo, fotos autorizadas, horario, qué datos se publican, dominio y quién actualiza el catálogo. Si falta algo, pedir solo el dato indispensable y dejar el resto como pendiente a la vista; no inventarlo.
2. **Estructura y sistema de diseño**: mapa de páginas y flujos; colores, tipografías con licencia libre, un solo radio, un solo grosor de línea y una escala de espaciado. El CSS nace de estos valores, no al final.
3. **Prototipo con datos reales** (el HTML es el mockup; no usar imágenes de IA como diseño a aprobar).
4. **Construcción** desde plantilla y datos (en Robles: `scripts/build.py` + `datos/catalogo.csv`).
5. **Pruebas automáticas** antes de mostrar nada al cliente (ver abajo).
6. **Revisión cruzada** con pocos revisores, corregir lo confirmado.
7. **Vista previa con enlace** para el cliente, con una cinta de «vista previa» y `noindex`.
8. **Publicación** solo con autorización explícita.

## Nunca sin autorización explícita del usuario
Publicar, registrar dominio, enviar mensajes o correos, abrir PR, reescribir historial, subir datos personales. El repositorio es público.

## Contenido
- No afirmar entregas, factura, garantías, descuentos, testimonios, existencia, pago con tarjeta ni «mejor precio». Desconocido no es cero ni agotado.
- Un precio se muestra solo con monto, unidad, IVA y vigencia sin vencer; si no, «Solicita precio» (una sola vez arriba mientras ninguno tenga precio).
- No publicar nombres de personas, datos bancarios ni fiscales. Lo que se publica lo aprueba el responsable.
- Si hay datos que se contradicen (p. ej. código postal), usar el más reciente del usuario y dejar la discrepancia anotada.

## Diseño
- Sin Arial salvo que el usuario lo pida. Sin siluetas ni ilustraciones de objetos sin pulir: preferir texto limpio o fotos reales.
- Contraste AA, objetivos táctiles de 44 px, foco visible, orden de encabezados, un h1 por página.
- Diseñar primero para celular (la gente cotiza por WhatsApp).

## Pruebas mínimas antes de enviar un enlace
Sin desborde horizontal a 320, 390, 768, 980–1180 y 1440 px; consola sin errores; ningún recurso externo; enlaces internos y de WhatsApp correctos; contraste; teclado y foco; búsqueda, cantidades y «Mi lista». Si va como artefacto, probar dentro de un marco con sandbox (sin `localStorage`, sin `window.open`, rutas de hash simples).

## Uso de agentes y costo
- Para revisar: como máximo 4 revisores (funcional, contenido y privacidad, visual, reglas del visor) y un escéptico solo por hallazgo de severidad media o alta.
- Revisar resultados parciales y detener el proceso en cuanto haya suficiente; no lanzar decenas de agentes sin avisar el costo.
- Con presupuesto de ~5 h, el trabajo humano se limita a aportar datos, aprobar una sola ronda de cambios y autorizar la publicación.

## Entrega
Enlace de vista previa, README actualizado, lista honesta de lo que falta (datos, fotos, logo, dominio) y de lo que no se probó.
