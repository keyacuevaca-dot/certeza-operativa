# Robles · plan por fases hasta terminar la página

Hecho el 8-oct-2026. Parte del brief del cliente (`Brief_Profesional_Proyecto_Web.pdf`, 7 secciones) y del análisis de etapas de una web. **Los tiempos son míos** (con IA haciendo código y pruebas), no los del documento de horas; son estimaciones, no mediciones, y no cuentan esperas. Cada dato que sale del cliente se registra en `PENDIENTES.md`.

Quién: **P** = programador (yo, con IA) · **R** = responsable (tú) · **C** = cliente.

## Resumen

| Fase | Qué pasa | Quién | Tiempo de trabajo | Entregable |
|---|---|---|---|---|
| 1 | El cliente manda la información y lo que además quiere | C (R acompaña) | C 2–4 h · R 10 min + decisiones 30 min | Precios, confirmaciones, fotos, logos, decisiones, deseos |
| 2 | El programador crea su lista desde lo recibido e integra | P | 2:25–3:45 h (+ extras) | Versión corregida con datos reales |
| 3 | Se le entrega al cliente (una sola ronda) | R envía, C revisa | R 10 min · C 30–60 min | Lista de cambios del cliente |
| 4 | Cambios y pruebas en celulares reales | P y R | P 30–60 min · R 45 min | Versión final |
| 5 | Publicación (solo con autorización explícita) | P prepara, R autoriza | P 1:45–2:00 h · R 30 min | Sitio en su dominio |
| 6 | Operación semanal y crecimiento | R, C, P | R 1–1:30 h · C 30 min · P 20 min | Administradora autónoma, Facebook, ficha de Google |

**Totales (mis tiempos):** programador **5–7 h** (hasta publicar, 4:40–6:45 h), responsable ≈ 3–3:30 h, cliente ≈ 3–5:30 h. Antes dije 4–5 h de trabajo: sube porque ahora cuento carga y validación de precios, logos de marca, publicación y operación. Las 5 h solo caben si el cliente manda la fase 1 completa y no se agregan extras.

---

## Fase 1 · El cliente manda (y lo que además quiere)

**1.1 R:** envía el enlace de vista previa con `herramientas/mensaje-al-cliente.md` (10 min).

**1.2 C · Precios** (45–90 min; es lo que más pesa). Sub-pasos:
1. Poner un precio de venta en MXN a cada producto (son 202 en el sitio). Puede agregar una columna a su lista original o escribirlos en un mensaje.
2. Decir si el precio **incluye IVA** (igual para todos o por producto).
3. Confirmar la **unidad** del precio (pieza, kg, metro, bulto, litro, caja). Ya viene prellenada con la unidad de venta; solo corrige.
4. Decir **hasta cuándo vale** cada precio (por ejemplo, hasta el próximo sábado). Sin fecha de vigencia sin vencer, el sitio no lo muestra.
5. Marcar los productos que **no** quiere publicar con precio (los que cambian a diario); quedan como «Solicita precio».
6. Nombrar quién actualiza y qué día de la semana (dijo: la administradora, cada semana).

Regla del sitio: un precio se muestra solo con monto + unidad + IVA + vigencia sin vencer. Si no, aparece un solo aviso arriba, no uno por fila.

**1.3 C · Confirmar supuestos** (10–15 min): Cloralex «750 ml» · varilla en pulgadas · sellador Del Toro (¿es el mismo de «18 kg»? si sí, quitar uno) · pegapiso Ade1000 (¿marca o nombre?) · picos y palas Truper · descripciones que tocan el borde de la captura (`nota_interna`).

**1.4 C · Fotos** (30–60 min): primero los 10–20 productos que más vende (cemento, varilla, carretillas, herramienta). Propias, con luz de día, fondo liso, un producto por foto, de 800 px o más. Que confirme por escrito que son suyas.

**1.5 C · Logo y marcas** (15–30 min): archivo original del logo (vectorial) y quién tiene sus derechos; logos de las 14 marcas o permiso para usarlos (Truper, Stanley, Pretul, Tolteca, Moctezuma, Calidra, Del Toro, Phillips, Cloralex, Fabuloso, Suavitel, Kleenex, Raid, Lucek).

**1.6 R + C · Decidir** (30 min, una sola conversación): qué se ofrece sobre entregas, factura y garantías (hoy el sitio no afirma nada) · una ventaja concreta frente a la competencia, o se omite («distinguen costos y materiales» es ambiguo) · eslogan: sí o no · «Ya soy cliente»: sí o no · quién aprueba el sitio · horario de respuesta por WhatsApp · si habrá papelería y cuándo · aviso de privacidad con un asesor.

**1.7 C · Lo que además quiere** (10–15 min). Tabla para que él llene; yo la convierto en la lista del programador:

| Deseo | ¿Para lanzar o después? | Tiempo mío si entra |
|---|---|---|
| Facebook (su prioridad 1): enlace en pie y «Visítanos» | Lanzar | 10 min |
| «Ya soy cliente» (opción para quien ya pagó y manda su pedido) | Decidir | 45 min |
| Más productos de limpieza o papelería | Después, por tandas | 30–60 min por cada 50 |
| Foto para los 202 productos | Después, por tandas | 5–10 min por cada 10 fotos |
| Ficha de Google (horario, mapa y WhatsApp) | Después | 30 min (R) |
| Otro: ________ | | |

### Brief del PDF, ya prellenado (el cliente solo contesta lo que dice «Falta»)

| Sección | Ya sabemos | Falta |
|---|---|---|
| 01 Negocio | Comercializadora Robles; construcción, limpieza y papelería; Juárez 43, Col. Centro, CP 63830, Santa María del Oro; lun–vie 9–14 y 16–18:30, sáb 9–13; 311 910 4468; correo aprobado; sin sitio ni Facebook todavía (abrirán Facebook) | Persona que aprueba; redes actuales |
| 02 Objetivo | Cotizar por WhatsApp; público local y estatal; el 80% de las ganancias es construcción | Una ventaja concreta; medida de éxito (propuesta: listas recibidas por WhatsApp por mes) |
| 03 Alcance | 7 páginas, buscador, «Mi lista», WhatsApp; la administradora actualiza cada semana | Qué quiere para después (ver 1.7) |
| 04 Marca | Logo real y colores azul/naranja; estilo claro, sin parecerse a Truper ni Pretul; sin Arial | Logo vectorial, fotos, logos de marca |
| 05 Ventas | 202 productos; pago en efectivo y transferencia; el sitio no guarda datos | Precios; entregas, factura, garantías |
| 06 Operación | Hosting estático basta; el sitio no recaba datos | Dominio (se revisa `.com`, `.net`, `.mx` y se aclara cuando vea la página), titular y pago; aviso de privacidad |
| 07 Fechas | — | Fecha de lanzamiento; presupuesto de dominio y hosting; quién da comentarios y en cuántos días |

---

## Fase 2 · Lista del programador (se crea con lo recibido)

| # | Cambio en la página | Tiempo | Depende de |
|---|---|---|---|
| 2.1 | Cargar precios en `datos/catalogo.csv` con unidad, IVA y vigencia; validar que cada uno se muestre | 30–60 min | 1.2 |
| 2.2 | Corregir nombres y quitar notas internas confirmadas | 15–20 min | 1.3 |
| 2.3 | Fotos: pasar a `.webp`, nombrar `<id>.webp`, colocar en `src/img/productos/` | 30–45 min | 1.4 |
| 2.4 | Logos de marca en `src/img/marcas/` y logo vectorial en encabezado, pie y favicon | 20–30 min | 1.5 |
| 2.5 | Textos según las decisiones: ventaja, entregas/factura/garantías, aviso, eslogan | 20–30 min | 1.6 |
| 2.6 | Extras elegidos en 1.7 (tiempos de la tabla) | 10–55 min | 1.7 |
| 2.7 | Regenerar, correr las pruebas, actualizar el archivo único y la vista previa | 30–40 min | 2.1–2.6 |

Si los precios llegan en foto, 2.1 sube a 60 min por la transcripción.

## Fase 3 · Entrega al cliente
1. R manda el enlace de la versión corregida y le pide **una sola ronda** de cambios, con su lista junta (10 min).
2. C revisa en su celular y manda todos los cambios de una vez (30–60 min).

## Fase 4 · Cambios y pruebas finales
1. P aplica la ronda de cambios y vuelve a correr las pruebas (30–60 min).
2. R prueba en 2 celulares reales (Android y iPhone): buscar, agregar, enviar por WhatsApp (30 min).
3. R escanea el QR (`herramientas/qr-whatsapp.png`) antes de imprimirlo (15 min).

## Fase 5 · Publicación (requiere autorización explícita de R)
1. Revisar si `.com`, `.net` y `.mx` están disponibles en el buscador de un registrador (15 min; desde este entorno no tengo acceso). R lo aclara con el cliente.
2. R o C registra el dominio y paga; quedan a nombre del negocio (30 min).
3. P elige hosting estático, ejecuta `python3 scripts/build.py --publicar` (quita la cinta y el `noindex`, agrega dominio, `canonical` y `sitemap.xml`) y sube **solo** `dist/` (45–60 min).
4. P hace SEO básico y Search Console (30 min).
5. P prueba el sitio en vivo (15 min). Aparte queda la propagación del dominio.

## Fase 6 · Operación semanal y crecimiento
1. R enseña a la administradora a actualizar precios con el editor y a pasar `catalogo.js` (30–60 min). Todavía **no se probó** que lo haga sola.
2. C abre la página de Facebook con `herramientas/kit-facebook.md` (30 min); R le pasa el enlace y P lo agrega al sitio.
3. R crea o reclama la ficha de Google (30 min).
4. P revisa a los 7 días que los precios sigan vigentes y que no haya errores (20 min).

---

## Límites
- No hay precio del proyecto: no tengo tu tarifa. Multiplica mis horas por tu tarifa.
- Precios y fotos de Home Depot y Office Depot no se usan: el acceso está bloqueado y no son del negocio. Del tipo de sitio solo se tomó la estructura.
- Nada se publica, se paga ni se envía sin autorización explícita.
