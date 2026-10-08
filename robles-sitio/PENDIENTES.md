# Robles · qué falta y ruta para terminar

Actualizado el 8-oct-2026. El sitio está listo como **vista previa** (no publicado). Esta tabla sustituye a «Datos del negocio: conocidos y pendientes» de la propuesta.

Estados: **Rellenado** = lo puse yo porque era un detalle simple (revisar) · **Por decidir** = lo decide el responsable o el cliente · **Falta dato** = sin eso no se puede completar.

## Ruta más eficaz (orden y tiempo de trabajo, sin contar esperas)

| # | Paso | Quién | Tiempo | Desbloquea |
|---|---|---|---|---|
| 1 | Juntar lo que el cliente mandó por WhatsApp (materiales de obra, precios, fotos) y pasármelo como texto o capturas | Responsable | 30–60 min | Todo lo demás |
| 2 | Cargar productos y precios (con unidad, IVA y vigencia) en el CSV o el editor | IA | 30–45 min | Línea de Construcción, que es el 80% de las ventas |
| 3 | Fotos con autorización y comprobar que el logo no tiene dueño de derechos distinto | Responsable | 30 min + espera | Catálogo con fotos |
| 4 | Decidir lo de «Por decidir» (tabla de abajo) en una sola conversación | Responsable + cliente | 30 min | Textos finales |
| 5 | Probar en 2 celulares reales (Android y iPhone) y mandar el QR a imprimir | Responsable | 30 min | Cierre de pruebas |
| 6 | Registrar dominio, elegir hosting estático y publicar | Responsable autoriza; IA prepara | 1–2 h | Publicación |
| 7 | Dar a la persona que atiende las respuestas rápidas y mostrar cómo actualizar el catálogo | Responsable | 30 min | Operación semanal |

Total aproximado: **4–5 h de trabajo** si el paso 1 llega completo. Es una estimación mía, no una medición.

## Tabla de estado

| Dato | Estado | Qué hay hoy | Qué falta o decidir |
|---|---|---|---|
| Nombre y líneas | Dato | Comercializadora Robles: construcción, limpieza y papelería | — |
| Logo | Rellenado | Logo real del cliente, con fondo transparente, en encabezado, pie y favicon | ¿Hay archivo vectorial original? Confirmar autoría y derechos de uso |
| Colores | Rellenado | Tomados del logo: azul `#044770`, naranja `#E97E1C` | Comparar con empaques de Truper y Pretul (no pude verificarlo) |
| Atención por WhatsApp | Rellenado | «Nuestro equipo atiende todas las consultas por WhatsApp» (el cliente dijo que una persona atiende) | Por decidir: ¿en qué horario responde? ¿mensaje de bienvenida y de ausencia? |
| Dirección | Dato | Juárez 43, Col. Centro | Código postal 63830 por confirmar (el archivo de diseño decía 63890) |
| Horario | Dato | Lun–vie 9:00–14:00 y 16:00–18:30; sáb 9:00–13:00 | Domingo: no se publica |
| Teléfono y WhatsApp | Dato | 311 910 4468; WhatsApp es el canal principal | — |
| Correo | Dato | Aprobado para publicar | — |
| Cloro Cloralex | Rellenado | «750 ml» (el negocio dijo «de 750») | Confirmar la unidad |
| ¿Guardan mis datos? | Rellenado | Respuesta en preguntas: el sitio no guarda cuentas ni formularios | Por decidir: aviso de privacidad formal (ver nota legal abajo) |
| Materiales de obra | **Falta dato** | Solo herramienta, corte y selladores | Lista completa (cemento, varilla, block, etc.); es lo que más vende |
| Papelería | **Falta dato** | Franja «sin productos publicados» | Productos |
| Precios, unidades y vigencia | **Falta dato** | «Los precios te los damos por WhatsApp» | Quién y cada cuánto los actualiza (administradora, semanal) |
| Fotos de producto | **Falta dato** | Catálogo en texto | Fotos autorizadas |
| Marca Truper | Por decidir | Aparece en «Marcas», sin producto asignado | ¿A qué productos aplica? |
| Entregas, factura, garantías | Por decidir | El sitio no afirma nada y remite a WhatsApp | Qué se ofrece y con qué condiciones |
| Eslogan | Por decidir | No se usa. La versión del chat proponía «Construye. Cuida. Crea.» | ¿Se quiere uno? |
| Redes sociales | Falta dato | No se muestran | Enlaces confirmados |
| Dominio `.mx` | Por decidir | `comercializadorarobles.mx`, sin verificar ni registrar | Registro, titular y pago |
| Hosting | Por decidir | — | Un hosting estático alcanza (el sitio no usa base de datos) |
| Ficha de Google | Por decidir | — | Crearla o reclamarla: horario, mapa y WhatsApp en un solo lugar |
| Repositorio público | Por decidir | Un commit antiguo contiene dos nombres personales | Pasarlo a privado o reescribir el historial |

## Lo que simplifica la vida (competencia y chat)

No pude abrir los sitios de la competencia desde este entorno (el acceso está bloqueado) y las búsquedas no devolvieron esas páginas. Lo que sigue sale del documento de referencias que diste, del HTML del chat y de guías generales.

**Para quien administra**
- Catálogo desde una hoja (CSV) y el editor: ya incluido. Ahí mismo se ve qué falta para que un precio se muestre.
- Respuestas rápidas listas para pegar en WhatsApp Business: `herramientas/respuestas-whatsapp.md`.
- QR que abre WhatsApp con el mensaje inicial, para mostrador, bolsas o cartel: `herramientas/qr-whatsapp.png` y `.svg`. Escanéalo con un teléfono antes de imprimir.
- Una guía de sitios para ferreterías apunta a combinar catálogo, sucursales con horarios y cotización, y señala que el maestro de obra cotiza antes por WhatsApp ([ejemplo de Perú](https://kom.pe/pagina-web-para-ferreterias-web-lima/)).

**Para el cliente**
- Mensaje listo para revisar, con botón «Copiar mensaje» por si WhatsApp no abre (idea tomada del HTML del chat): incluido.
- Cotización con vigencia e IVA visibles: ya en la regla de precios.
- Horario, dirección y mapa en un solo lugar: ya en «Visítanos».

**Nota legal (no es asesoría)**: las fuentes que encontré dicen que quien recaba datos personales debe mostrar un aviso de privacidad, y que el formulario web y el alta por WhatsApp cuentan como ejemplo. Hay discrepancias sobre el texto vigente de la ley y sobre la autoridad. Este sitio no recaba datos, pero conviene que un asesor lo confirme ([Praxium](https://praxiumconsultores.com/blog/es-obligatorio-el-aviso-de-privacidad), [Legiscope](https://www.legiscope.com/blog/aviso-privacidad-mexico-lfpdppp.html)).
