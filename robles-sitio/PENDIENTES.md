# Robles · qué falta y ruta para terminar

Actualizado el 8-oct-2026 con el inventario del cliente (4 capturas) y el chat de WhatsApp. El sitio está listo como **vista previa** (no publicado). Esta tabla sustituye a «Datos del negocio: conocidos y pendientes» de la propuesta.

Estados: **Rellenado** = lo puse yo porque era un detalle simple (revisar) · **Por decidir** = lo decide el responsable o el cliente · **Falta dato** = sin eso no se puede completar.

## Ruta más eficaz (orden y tiempo de trabajo, sin contar esperas)

| # | Paso | Quién | Tiempo | Desbloquea |
|---|---|---|---|---|
| 1 | Mandar al cliente el enlace de vista previa con el mensaje de `herramientas/mensaje-al-cliente.md` (pide solo precios, supuestos y fotos) | Responsable | 10 min | Respuesta del cliente |
| 2 | Cargar precios (monto, unidad, IVA y vigencia) en el CSV o el editor | IA | 30 min | Precios visibles |
| 3 | Fotos propias o autorizadas: `src/img/productos/<id>.webp`; logos de marca en `src/img/marcas/` | Cliente toma; IA coloca | 30 min + espera | Catálogo con fotos y marcas |
| 4 | Decidir lo de «Por decidir» (tabla de abajo) en una sola conversación | Responsable + cliente | 30 min | Textos finales |
| 5 | Probar en 2 celulares reales (Android y iPhone) y mandar el QR a imprimir | Responsable | 30 min | Cierre de pruebas |
| 6 | Verificar disponibilidad de dominio (`.com`, `.net`, `.mx`), registrar y publicar | Responsable autoriza; IA prepara | 1–2 h | Publicación |
| 7 | Abrir la página de Facebook con `herramientas/kit-facebook.md` | Cliente | 30 min | Redes (prioridad 1 del cliente) |
| 8 | Dar a la persona que atiende las respuestas rápidas y mostrar cómo actualizar el catálogo | Responsable | 30 min | Operación semanal |

Total aproximado: **4–5 h de trabajo** si el paso 1 se contesta completo. Es una estimación mía, no una medición.

## Tabla de estado

| Dato | Estado | Qué hay hoy | Qué falta o decidir |
|---|---|---|---|
| Nombre y líneas | Dato | Comercializadora Robles: construcción, limpieza y papelería | — |
| Logo | Rellenado | Logo real del cliente, con fondo transparente, en encabezado, pie y favicon | ¿Hay archivo vectorial original? Confirmar autoría y derechos de uso |
| Colores | Rellenado | Tomados del logo: azul `#044770`, naranja `#E97E1C` | Comparar con empaques de Truper y Pretul (no pude verificarlo) |
| Atención por WhatsApp | Rellenado | «Nuestro equipo atiende todas las consultas por WhatsApp» | ¿En qué horario responde? ¿Mensaje de bienvenida y de ausencia? |
| Dirección | Dato | Juárez 43, Col. Centro, CP 63830 (dato más reciente del cliente) | El archivo de diseño decía 63890; comprobar antes de publicar |
| Horario | Dato | Lun–vie 9:00–14:00 y 16:00–18:30; sáb 9:00–13:00 | Domingo: no se publica |
| Teléfono, WhatsApp y correo | Dato | 311 910 4468 (WhatsApp es el canal principal); correo aprobado | — |
| Peso visual de las líneas | Rellenado | Las tres líneas pesan igual; construcción va primero | — |
| Inventario (202 productos) | Rellenado | 185 de construcción y 17 de limpieza: 172 filas de las capturas del cliente (dos lecturas independientes, coinciden) más lo dicho por chat | Resto de limpieza y papelería; el sitio invita a preguntar lo que no aparece |
| Precios, unidades y vigencia | **Falta dato** | Las capturas **no traían la columna de precios**. Cada producto ya tiene su unidad de venta | Monto, IVA y vigencia; quién los actualiza (administradora, semanal) |
| Fotos de producto | **Falta dato** | Iconos por producto; el sitio ya carga fotos si existen | Fotos autorizadas |
| Logos de marca | **Falta dato** | 14 marcas en texto dentro de un recuadro | Archivos de logo o permiso para usarlos |
| Descripciones dudosas | Rellenado | Texto que toca el borde de la captura (marcado en `nota_interna`) y correcciones de ortografía hechas al transcribir | Confirmar con el original |
| Supuestos de chat | Rellenado | Cloralex «750 ml»; varilla en «pulgadas»; sellador «Del Toro» (el cliente escribió «marca del toro»); pegapiso «Ade1000» sin marca; Truper en picos y palas | Confirmar con la tienda |
| Sellador «Del Toro» | Por decidir | Aparece una vez por chat (cubeta) y una vez en la captura 4 («18 kg») | ¿Es el mismo producto? Si lo es, quitar uno |
| Años, historia y qué distingue al negocio | Falta dato | «Distinguen costos y materiales» sigue ambiguo y no se publica | Una ventaja concreta, o se omite |
| ¿Guardan mis datos? | Rellenado | El sitio no guarda cuentas ni formularios | Aviso de privacidad formal (ver nota legal) |
| Entregas, factura, garantías | Por decidir | El sitio no afirma nada y remite a WhatsApp | Qué se ofrece y con qué condiciones |
| Eslogan | Por decidir | No se usa | ¿Se quiere uno? |
| Redes sociales | Falta dato | No se muestran. Primera prioridad del cliente; abrirán Facebook | Enlace cuando exista (kit listo en `herramientas/kit-facebook.md`) |
| Ruta «Ya soy cliente» | Por decidir | No existe; el cliente no contestó | ¿Todo lo atiende la misma persona o se agrega esa opción? |
| Datos fiscales | Por decidir | No se publican. En Hacienda aparece Juárez 55 y el negocio usa Juárez 43 | Si algún día facturan, igualar el domicilio |
| Dominio | Por decidir | No depende del cliente, sino de si está disponible. Decisión previa: `.mx`; el cliente dijo `.com` y luego «tú dices cuál se ve más presentable». **Sin verificar ni registrar** | Revisar `.com`, `.net` y `.mx` y aclararlo con el cliente al mostrarle la página; titular y pago |
| Hosting | Por decidir | — | Un hosting estático alcanza (el sitio no usa base de datos) |
| Ficha de Google | Por decidir | — | Crearla o reclamarla: horario, mapa y WhatsApp en un solo lugar |
| Repositorio público | Por decidir | Un commit antiguo contiene dos nombres personales | Pasarlo a privado o reescribir el historial |

## Lo que simplifica la vida (competencia y chat)

No pude abrir los sitios de la competencia (Home Depot, Office Depot y otros) desde este entorno: el acceso está bloqueado. Tampoco serviría copiar sus precios ni sus fotos: no son del negocio y las fotos tienen derechos. De ellos se tomó solo la **estructura** (buscador al centro, cinta de productos, categorías con icono). Lo demás sale del documento de referencias, del HTML del chat y de guías generales.

**Para quien administra**
- Catálogo desde una hoja (CSV) y el editor: ya incluido. Ahí mismo se ve qué falta para que un precio se muestre.
- Respuestas rápidas listas para pegar en WhatsApp Business: `herramientas/respuestas-whatsapp.md`.
- QR que abre WhatsApp con el mensaje inicial, para mostrador, bolsas o cartel: `herramientas/qr-whatsapp.png` y `.svg`. Escanéalo con un teléfono antes de imprimir.
- Una guía de sitios para ferreterías apunta a combinar catálogo, sucursales con horarios y cotización, y señala que el maestro de obra cotiza antes por WhatsApp ([ejemplo de Perú](https://kom.pe/pagina-web-para-ferreterias-web-lima/)).

**Para el cliente**
- Mensaje listo para revisar, con botón «Copiar mensaje» por si WhatsApp no abre (idea tomada del HTML del chat): incluido.
- Mensaje para el cliente y kit de Facebook: `herramientas/mensaje-al-cliente.md` y `herramientas/kit-facebook.md`.
- Cotización con vigencia e IVA visibles: ya en la regla de precios.
- Horario, dirección y mapa en un solo lugar: ya en «Visítanos».

**Nota legal (no es asesoría)**: las fuentes que encontré dicen que quien recaba datos personales debe mostrar un aviso de privacidad, y que el formulario web y el alta por WhatsApp cuentan como ejemplo. Hay discrepancias sobre el texto vigente de la ley y sobre la autoridad. Este sitio no recaba datos, pero conviene que un asesor lo confirme ([Praxium](https://praxiumconsultores.com/blog/es-obligatorio-el-aviso-de-privacidad), [Legiscope](https://www.legiscope.com/blog/aviso-privacidad-mexico-lfpdppp.html)).
