# Contenido del sitio. Todo lo que se publica sale de aquí: si cambia un texto, se cambia aquí
# y se vuelve a generar con `python _fuente/construir.py`.
# Reglas: sin cifras, clientes ni testimonios inventados; trato de usted; sin precios ni tarifa por hora;
# sin vocabulario interno (se escribe «primera visita sin costo», «plan en una hoja», «punto de partida medido»,
# «trabajo con precio cerrado» y «mejora medida antes y después»).
import json, os

WA_NUM = '523114469363'
TEL = '+52 311 446 9363'

# Catálogo de trabajos (datos de Kevin, oct-2026). Se usa tal cual: no se editan textos aquí.
CATALOGO = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catalogo.json'), encoding='utf-8'))
HORAS_ESCALA = 23  # 23 horas útiles = barra al 100 %

# Piezas con las que se arma un trabajo: (pilar, nombre, para qué sirve)
PIEZAS = [
    ('orden', 'Lista de precios o catálogo', 'Que todos vean el mismo producto y el mismo precio.'),
    ('orden', 'Cotizador', 'Decir qué se entrega, cuánto cuesta y hasta cuándo vale el precio.'),
    ('orden', 'Procedimiento escrito', 'Mostrar cómo hacer la tarea sin depender de la memoria.'),
    ('orden', 'Quién hace qué', 'Que cada pendiente tenga una persona responsable.'),
    ('orden', 'Expediente para el contador', 'Tener juntos los documentos que necesita su contador.'),
    ('visibilidad', 'Control de pedidos y cobros', 'Saber qué se pidió, qué se entregó y cuánto falta cobrar.'),
    ('visibilidad', 'Registro diario desde el celular', 'Guardar el dato antes de olvidarlo.'),
    ('visibilidad', 'Flujo a 30, 60 y 90 días', 'Ver si el dinero alcanzaría en las próximas fechas.'),
    ('visibilidad', 'Tablero semanal', 'Ver lo más urgente sin leer todos los registros.'),
    ('visibilidad', 'Inventario y reorden', 'Tener existencias visibles y pedir antes de quedarse sin producto.'),
    ('control', 'Agenda de cobranza', 'Saber a quién cobrar, cuánto y cuándo.'),
    ('control', 'Lo cobrado contra lo depositado', 'Comprobar que lo que cobró coincide con lo que entró al banco.'),
    ('control', 'Arqueo y cierre de caja', 'Cerrar el día con la caja contada y comparada.'),
]
PIEZA = {p[1]: p for p in PIEZAS}
PILAR_NOMBRE = {'orden': 'Orden', 'visibilidad': 'Visibilidad', 'control': 'Control', 'mejora': 'Mejora continua'}

# ---------------- Industrias ----------------
INDUSTRIAS = [
    dict(slug='alimentos-y-bebidas', corto='Restaurantes, cafeterías, panaderías y más.', nombre='Alimentos y bebidas',
         tipos='Restaurantes, cocinas económicas, cafeterías, panaderías, tortillerías y purificadoras.',
         lead='Vende todo el día, en efectivo y por transferencia, con insumos que caducan. Le ayudamos a que la caja cuadre, el inventario avise a tiempo y cada turno trabaje igual.',
         voces=['¿Por qué no me cuadra la caja al cierre?', '¿Qué tengo que comprar para mañana?', '¿Cómo hago que el turno de la tarde trabaje igual que el de la mañana?', '¿Cuánto vendí esta semana contra la pasada?'],
         piezas=['Arqueo y cierre de caja', 'Lo cobrado contra lo depositado', 'Inventario y reorden', 'Procedimiento escrito', 'Registro diario desde el celular', 'Lista de precios o catálogo'],
         herramientas=['Hojas de Google', 'Excel', 'WhatsApp Business', 'Canva', 'Mercado Pago', 'Google Maps']),
    dict(slug='comercio-y-tiendas', corto='Abarrotes, ferreterías, papelerías y farmacias.', nombre='Comercio y tiendas',
         tipos='Abarrotes, ferreterías, papelerías, farmacias, boutiques y materiales.',
         lead='Muchos productos, precios que cambian y clientes que piden fiado. Ordenamos su lista de precios, su inventario y su cobranza para que sepa qué tiene y quién le debe.',
         voces=['¿Qué tengo y qué necesito comprar?', '¿Quién me debe y desde cuándo?', '¿Todos mis empleados dan el mismo precio?', '¿Cuánto vendí esta semana contra la pasada?'],
         piezas=['Lista de precios o catálogo', 'Inventario y reorden', 'Agenda de cobranza', 'Tablero semanal', 'Arqueo y cierre de caja', 'Cotizador'],
         herramientas=['Excel', 'Hojas de Google', 'WhatsApp Business', 'Canva', 'Mercado Pago', 'CONTPAQi', 'Aspel']),
    dict(slug='distribucion-y-logistica', corto='Distribuidoras, repartidores y fleteras.', nombre='Distribución y logística',
         tipos='Distribuidoras, repartidores, fleteras y mensajería local.',
         lead='Pedidos, rutas y cobros que se cruzan. Hacemos visible qué falta entregar, a qué hora y qué falta cobrar, para que el dinero de la ruta llegue completo.',
         voces=['¿Qué falta entregar y a qué hora?', '¿Qué pedido ya se entregó y cuál no se ha cobrado?', '¿Quién trae el efectivo de la ruta?', '¿Me alcanza para pagar a proveedores este mes?'],
         piezas=['Control de pedidos y cobros', 'Agenda de cobranza', 'Lo cobrado contra lo depositado', 'Flujo a 30, 60 y 90 días', 'Quién hace qué', 'Tablero semanal'],
         herramientas=['Hojas de Google', 'Google Maps', 'WhatsApp Business', 'Google Forms', 'Excel', 'Odoo']),
    dict(slug='construccion-e-ingenieria', corto='Contratistas, herrerías y despachos de proyecto.', nombre='Construcción e ingeniería',
         tipos='Contratistas, constructoras pequeñas, herrerías, carpinterías y despachos de proyecto.',
         lead='Cada obra es un proyecto con material, cuadrillas y pagos por avance. Le ayudamos a saber quién hace qué, para cuándo, y si el dinero alcanza hasta el siguiente pago del cliente.',
         voces=['¿Quién hace qué y para cuándo?', '¿Cuánto material se fue en esta obra?', '¿Me alcanza el dinero hasta el próximo pago del cliente?', '¿Qué falta cobrar de cada obra?'],
         piezas=['Quién hace qué', 'Cotizador', 'Flujo a 30, 60 y 90 días', 'Control de pedidos y cobros', 'Expediente para el contador', 'Procedimiento escrito'],
         herramientas=['Excel', 'Hojas de Google', 'Google Drive', 'WhatsApp Business', 'Trello', 'Canva']),
    dict(slug='fabricacion-y-produccion', corto='Producción por lotes o por encargo.', nombre='Fabricación y producción',
         tipos='Talleres de producción, maquila, muebles, alimentos procesados y producción por lotes o por encargo.',
         lead='Producir bien y a tiempo depende de saber qué pedido sigue, cuánto material se va en cada lote y quién responde por cada paso.',
         voces=['¿Qué pedido toca entregar primero?', '¿Cuánto material se va en cada lote?', '¿Por qué sale distinto el mismo producto?', '¿Qué falta comprar para la producción de la semana?'],
         piezas=['Procedimiento escrito', 'Inventario y reorden', 'Control de pedidos y cobros', 'Tablero semanal', 'Quién hace qué', 'Cotizador'],
         herramientas=['Excel', 'Hojas de Google', 'Odoo', 'Google Forms', 'WhatsApp Business', 'Power BI']),
    dict(slug='automotriz', corto='Talleres, hojalatería y refaccionarias.', nombre='Automotriz',
         tipos='Talleres mecánicos, hojalatería y pintura, refaccionarias y lavado de autos.',
         lead='Autos que esperan una refacción, clientes que preguntan «¿ya está?» y presupuestos que cambian. Hacemos visible qué reparación sigue y qué la detiene.',
         voces=['¿Qué reparación sigue y qué la detiene?', '¿Cuánto cotizamos y cuánto se cobró al final?', '¿Qué refacciones tengo y cuáles hay que pedir?', '¿Qué auto se entrega hoy?'],
         piezas=['Cotizador', 'Control de pedidos y cobros', 'Inventario y reorden', 'Procedimiento escrito', 'Agenda de cobranza', 'Tablero semanal'],
         herramientas=['Excel', 'Hojas de Google', 'WhatsApp Business', 'Google Calendar', 'Canva', 'Mercado Pago']),
    dict(slug='turismo-y-hospitalidad', corto='Hoteles pequeños, rentas vacacionales y tours.', nombre='Turismo y hospitalidad',
         tipos='Hoteles pequeños, renta vacacional, tours y restaurantes de la costa y la sierra de Nayarit.',
         lead='Temporadas altas y bajas, reservaciones por WhatsApp y personal que cambia. Le ayudamos a ver reservaciones, cobros y pendientes en una sola vista, y a que cada temporada arranque con el mismo estándar.',
         voces=['¿Qué está reservado y qué falta cobrar?', '¿Me alcanza el dinero para la temporada baja?', '¿Cómo entreno rápido al personal nuevo?', '¿Qué se rentó y cuándo regresa?'],
         piezas=['Flujo a 30, 60 y 90 días', 'Control de pedidos y cobros', 'Procedimiento escrito', 'Tablero semanal', 'Agenda de cobranza', 'Lista de precios o catálogo'],
         herramientas=['Google Calendar', 'WhatsApp Business', 'Hojas de Google', 'Google Maps', 'Instagram', 'Facebook']),
    dict(slug='servicios-profesionales', corto='Consultorios, despachos y estéticas.', nombre='Servicios profesionales y de salud',
         tipos='Consultorios, despachos, estéticas, gimnasios, escuelas y servicios por cita.',
         lead='Su agenda es su inventario. Ordenamos citas, cobros y seguimientos para que no se crucen las citas ni se queden pagos sin cobrar.',
         voces=['¿Se me cruzan las citas?', '¿Qué servicio toca y qué falta cobrar?', '¿Quién da seguimiento a cada cliente?', '¿Cuántos clientes regresan?'],
         piezas=['Agenda de cobranza', 'Quién hace qué', 'Tablero semanal', 'Lista de precios o catálogo', 'Registro diario desde el celular', 'Expediente para el contador'],
         herramientas=['Google Calendar', 'WhatsApp Business', 'Hojas de Google', 'Google Forms', 'Notion', 'Zoom']),
    dict(slug='reparacion-y-mantenimiento', corto='Equipos, cómputo, lavanderías y mantenimiento.', nombre='Reparación y mantenimiento',
         tipos='Reparación de electrodomésticos, cómputo y celulares, refrigeración y aire acondicionado, lavanderías y tintorerías, cerrajerías y mantenimiento de inmuebles.',
         lead='Trabajos que entran a revisión, refacciones que hay que pedir y clientes que preguntan «¿ya quedó?». Le ayudamos a que cada trabajo tenga su orden, su presupuesto autorizado y su fecha de entrega, y a que nada se quede sin cobrar.',
         voces=['¿Qué trabajos tengo pendientes y desde cuándo?', '¿El cliente ya autorizó el presupuesto?', '¿Qué refacciones hay que pedir?', '¿Qué se entrega hoy y qué falta cobrar?'],
         piezas=['Control de pedidos y cobros', 'Cotizador', 'Inventario y reorden', 'Procedimiento escrito', 'Agenda de cobranza', 'Registro diario desde el celular'],
         herramientas=['Hojas de Google', 'Excel', 'WhatsApp Business', 'Google Calendar', 'Google Forms', 'Mercado Pago'],
         ver_tambien=('automotriz', '¿Tiene un taller de autos? Vea la página Automotriz.')),
    dict(slug='campo-y-pesca', corto='Huertas, ranchos, granjas y cooperativas pesqueras.', nombre='Campo y pesca',
         tipos='Productores de frutas y hortalizas, ranchos ganaderos, granjas avícolas y acuícolas, apicultores y cooperativas pesqueras.',
         lead='Cosechas y capturas que dependen de la temporada, jornales que se pagan cada semana e insumos que se compran por adelantado. Le ayudamos a registrar lo que produce, lo que gasta y lo que le pagan, para que sepa cuánto le dejó cada temporada.',
         voces=['¿Cuánto me costó producir este ciclo?', '¿Cuánto se pagó de jornales esta semana?', '¿Qué me falta cobrar de lo que entregué?', '¿Me alcanza el dinero hasta la siguiente temporada?'],
         piezas=['Registro diario desde el celular', 'Flujo a 30, 60 y 90 días', 'Control de pedidos y cobros', 'Inventario y reorden', 'Quién hace qué', 'Expediente para el contador'],
         herramientas=['Hojas de Google', 'Excel', 'WhatsApp Business', 'Google Forms', 'Google Drive', 'Mercado Pago']),
    dict(slug='limpieza-y-seguridad', corto='Limpieza, jardinería, fumigación y vigilancia.', nombre='Limpieza y seguridad',
         tipos='Empresas de limpieza, jardinería, control de plagas, recolección de residuos y vigilancia de instalaciones.',
         lead='Cuadrillas en varios lugares a la vez, turnos que hay que cubrir y clientes que pagan cada mes. Le ayudamos a ver quién está en cada servicio, qué material se usó y qué cliente falta por cobrar.',
         voces=['¿Quién cubre cada turno y cada servicio?', '¿Cuánto material se gasta con cada cliente?', '¿Qué cliente no ha pagado este mes?', '¿Cómo compruebo que el servicio se hizo?'],
         piezas=['Quién hace qué', 'Registro diario desde el celular', 'Agenda de cobranza', 'Inventario y reorden', 'Procedimiento escrito', 'Tablero semanal'],
         herramientas=['Hojas de Google', 'WhatsApp Business', 'Google Forms', 'Google Calendar', 'Google Maps', 'Excel']),
]

# Cinta «Trabajamos con:» de la página de inicio (nombre corto, slug de la página de industria)
CINTA = [
    ('Comercio', 'comercio-y-tiendas'),
    ('Alimentos y bebidas', 'alimentos-y-bebidas'),
    ('Reparación y mantenimiento', 'reparacion-y-mantenimiento'),
    ('Servicios personales', 'servicios-profesionales'),
    ('Servicios profesionales', 'servicios-profesionales'),
    ('Hospedaje y eventos', 'turismo-y-hospitalidad'),
    ('Construcción', 'construccion-e-ingenieria'),
    ('Manufactura', 'fabricacion-y-produccion'),
    ('Distribución y logística', 'distribucion-y-logistica'),
    ('Educación y membresías', 'servicios-profesionales'),
    ('Campo y pesca', 'campo-y-pesca'),
    ('Limpieza y seguridad', 'limpieza-y-seguridad'),
]

# ---------------- Soluciones ----------------
SOLUCIONES = [
    dict(slug='orden', nombre='Orden', tl='Cada cosa en su lugar.',
         lead='Que las cosas salgan igual aunque usted no esté: precios a la vista, tareas escritas y un responsable para cada pendiente.',
         voces=['Todo depende de mí: los precios están en mi cabeza.', 'Cuando falto, algo sale mal.', 'Me preguntan lo mismo varias veces al día.'],
         entregables=[('Lista de precios o catálogo', 'Con su marca, en PDF, para que todos den el mismo precio.'),
                      ('Cotizador', 'Decir qué se entrega, cuánto cuesta y hasta cuándo vale el precio.'),
                      ('Procedimiento escrito', 'Una tarea paso a paso, con lista de verificación.'),
                      ('Quién hace qué', 'Mapa de quién hace cada cosa y quién decide.'),
                      ('Expediente para el contador', 'Los documentos que pide su contador, juntos y a tiempo.')],
         mide=('Pendientes sin responsable', 'Contamos cuántos pendientes no tienen dueño antes de empezar y al entregar. La meta: ninguno.')),
    dict(slug='visibilidad', nombre='Visibilidad', tl='Saber qué pasa, a tiempo.',
         lead='Saber cada semana cómo va el negocio, en una sola vista, sin esperar a fin de mes ni leer todas las libretas.',
         voces=['No sé cómo va el negocio hasta fin de mes.', 'No sé si esta semana fue mejor que la pasada.', 'Los números están en varias libretas.'],
         entregables=[('Registro diario desde el celular', 'Una captura corta para guardar el dato antes de olvidarlo.'),
                      ('Tablero semanal', 'Cinco indicadores con gráficas que se actualizan solas.'),
                      ('Control de pedidos y cobros', 'Qué se pidió, qué se entregó y cuánto falta cobrar.'),
                      ('Flujo a 30, 60 y 90 días', 'Ver a tiempo si el dinero alcanzaría.'),
                      ('Inventario y reorden', 'Existencias visibles y aviso para pedir antes de quedarse sin producto.')],
         mide=('Dinero previsto a 30, 60 y 90 días', 'Al entregar comparamos con usted lo previsto contra lo que pasó; después usted lo revisa cada semana en su tablero.')),
    dict(slug='control', nombre='Control', tl='Que lo cobrado cuadre.',
         lead='Que no se le escape dinero sin darse cuenta: la caja cuadra al cierre y cada cliente que le debe tiene fecha de cobro.',
         voces=['Fío y se me olvida cobrar.', 'Al cerrar, la caja no coincide con las ventas.', 'No sé si lo que cobré llegó completo al banco.'],
         entregables=[('Arqueo y cierre de caja', 'Lista de apertura y cierre, con una hoja que suma sola.'),
                      ('Lo cobrado contra lo depositado', 'Comprobar que lo cobrado coincide con lo que entró al banco.'),
                      ('Agenda de cobranza', 'Calendario de cobro ordenado por monto y antigüedad.'),
                      ('Mensajes de cobranza', 'En tres tonos, listos para WhatsApp. Usted los envía.')],
         mide=('Lo cobrado contra lo depositado', 'Lo probamos con usted en un cierre real. Si algo no cuadra, se ve la diferencia y su causa.')),
    dict(slug='mejora-continua', nombre='Mejora continua', tl='Medir, resolver, comprobar y volver a empezar.',
         lead='Medimos su punto de partida con sus papeles. El trabajo termina cuando su equipo completa un ciclo sin nosotros. Después comparamos el número de antes con el de hoy.',
         voces=['Ya intenté ordenarme y a las dos semanas volvimos a lo mismo.', 'No sé si lo que cambié sirvió de algo.', 'Mi equipo deja de usar los formatos.'],
         entregables=[('Punto de partida medido', 'Elegimos un solo número que importe y lo medimos con sus papeles, no de memoria.'),
                      ('Prueba con un caso real', 'Una semana o un cierre real, y ajuste antes de darlo por entregado.'),
                      ('Su equipo lo usa solo', 'El trabajo termina cuando su equipo completa un ciclo sin nosotros.'),
                      ('Mejora medida antes y después', 'Comparamos el número de antes con el de hoy. Lo que funcionó queda escrito.'),
                      ('El siguiente problema', 'Si usted quiere, lo elegimos juntos, con su propio precio cerrado.'),
                      ('Capacitación', 'Capacitamos a quien lo va a usar, para que su equipo lo use sin nosotros.')],
         mide=('Mejora medida antes y después', 'La diferencia entre el número de antes y el de después. Usted la ve y usted la verifica.')),
    dict(slug='herramientas', nombre='Herramientas', tl='Sencillas y adaptadas a su negocio.',
         lead='No le vendemos software. Partimos de lo que ya usa, en papel o en el celular, y lo dejamos ordenado para que su equipo lo use solo.',
         voces=['Compré un sistema y nadie lo usa.', 'Tengo todo en Excel, pero nadie lo entiende.', 'Quiero usar inteligencia artificial, pero no sé para qué.'],
         entregables=[('Hojas de cálculo', 'Excel u Hojas de Google con registros que suman solos.'),
                      ('Documentos con su marca', 'Formatos, listas y tableros en la cuenta de Canva de su negocio.'),
                      ('WhatsApp Business', 'Mensajes listos, catálogos y recordatorios para sus clientes.'),
                      ('Formularios', 'Captura semanal de 5 minutos desde el celular, por ejemplo con Google Forms.'),
                      ('Sistemas que ya tiene', 'Si ya usa Odoo, CONTPAQi o Aspel, partimos de ahí.'),
                      ('Inteligencia artificial, fácil', 'Asistentes como Claude, ChatGPT o Gemini para redactar y resumir; usted revisa y decide.')],
         mide=('Uso real', 'Una herramienta sirve si su equipo la usa. Al entregar revisamos con usted si se captura y se consulta.')),
    dict(slug='metodos', nombre='Métodos', tl='Claros, cortos y en su idioma.',
         lead='Llevamos métodos de la mejora continua al tamaño de su negocio, sin siglas ni papeleo de más.',
         voces=['Los consultores me dejaron un documento que nunca leí.', 'Quiero saber qué hacer el lunes, no una teoría.', 'Necesito que mi equipo entienda el cambio.'],
         entregables=[('Primera visita sin costo', 'Doce preguntas y un caso real de su negocio, de punta a punta.'),
                      ('Plan en una hoja', 'Lo encontrado, una acción gratis para hoy y el siguiente paso con precio cerrado y fecha.'),
                      ('Punto de partida medido', 'Su número de hoy, medido con sus papeles. Es la base para comparar después.'),
                      ('Trabajo con precio cerrado', 'Se entrega cuando su equipo lo usa solo.'),
                      ('Mejora medida antes y después', 'Para decidir con datos el siguiente paso.'),
                      ('Listas de verificación', 'Para que una tarea salga igual sin depender de la memoria.'),
                      ('Tableros visuales', 'Pocos números, a la vista, revisados cada semana.')],
         mide=('Mejora medida antes y después', 'El número de cada trabajo, antes y después. Usted lo verifica.')),
    dict(slug='marketing-digital', nombre='Marketing digital', tl='Que lo conozcan y le escriban.',
         lead='Publicar sin plan cansa y no trae clientes. Le armamos una marca que se reconoce, publicaciones con un objetivo y campañas medidas, para que más personas lo encuentren y le escriban.',
         voces=['Publico cuando me acuerdo y no pasa nada.', 'Mi logo y mis colores cambian en cada publicación.', 'Pagué anuncios y no supe si sirvieron.'],
         entregables=[('Imagen de marca básica', 'Logo limpio, colores y letras, aplicados a todas sus piezas.'),
                      ('Piezas para redes', 'Publicaciones, historias, menús y flyers con su marca.'),
                      ('Calendario mensual', 'Qué se publica, cuándo y para qué. Usted lo aprueba antes de publicar.'),
                      ('Campañas en Facebook e Instagram', 'Las armamos y las medimos. Usted autoriza el monto y lo paga directo a Meta.'),
                      ('Que lo encuentren en Google', 'Ficha de Google Maps optimizada, reseñas y textos de su página pensados para su zona.'),
                      ('Seguimiento automático a clientes', 'Mensajes de WhatsApp Business para cotizaciones sin respuesta y clientes que no regresan.')],
         mide=('Clientes que le escriben', 'Contamos cuántos clientes le escriben por semana antes de empezar y después de un mes. La meta la fijamos con usted.'),
         no_incluye='No pagamos ni adelantamos publicidad, no publicamos nada sin su aprobación, no respondemos los mensajes del día a día y no prometemos seguidores ni ventas. Sus cuentas quedan a su nombre. La página web está en el catálogo, en «Que lo encuentren».'),
    dict(slug='ia-y-automatizacion', nombre='IA y automatización', tl='Menos trabajo a mano.',
         lead='Contestar lo mismo, pasar datos de un papel a otro y acordarse de cobrar quita horas. Configuramos herramientas que ya existen para que esas tareas salgan solas y usted solo revise.',
         voces=['Contesto las mismas preguntas todo el día.', 'Paso a la computadora lo que anotamos en papel.', 'Se me olvida cobrar o pedir a tiempo.'],
         entregables=[('Respuestas automáticas en WhatsApp', 'Bienvenida, horario, catálogo y mensajes listos para cobrar.'),
                      ('Asistente de IA en sus redes', 'El asistente de Meta para negocios, con sus productos, horarios y preguntas frecuentes, en WhatsApp, Instagram y Messenger, cuando Meta lo active en su cuenta.'),
                      ('Formularios y recordatorios', 'Lo que su equipo captura en el celular cae solo en una hoja, con avisos de cobro y de reorden.'),
                      ('Asistente de IA para su oficina', 'ChatGPT, Gemini o Claude con instrucciones escritas para cotizar, redactar y resumir. Usted revisa antes de enviar.'),
                      ('Excel con botones', 'Un libro de Excel donde cada tarea se hace con un botón.')],
         mide=('Horas en tareas repetidas', 'Medimos cuánto tiempo a la semana se va en contestar lo mismo, pasar datos y recordar cobros, antes y después. La meta la fijamos con usted.'),
         no_incluye='No desarrollamos programas propios ni programación a la medida: usamos herramientas que ya existen. La IA no decide sola: precios, descuentos y respuestas delicadas los revisa usted. Las cuentas y licencias quedan a su nombre.'),
]

# Sección «¿Qué necesita su negocio?» de inicio
NECESIDADES = [
    # (título, texto, enlace, ícono)
    ('Cobros y caja', 'Quién le debe, cuánto, y cierres que cuadran.', 'soluciones/control.html', 'monedas'),
    ('Equipo y procesos', 'Quién hace qué y cómo, aunque usted no esté.', 'catalogo.html#su-negocio-camina-sin-usted', 'organigrama'),
    ('Inventario y compras', 'Existencias a la vista y pedidos antes de que falte.', 'catalogo.html#inventario-bajo-control', 'caja'),
    ('Precios y cotizaciones', 'Lista de precios y cotizaciones sin errores.', 'catalogo.html#cotice-sin-errores', 'etiqueta'),
    ('Contador en orden', 'Ingresos, gastos y comprobantes de cada mes.', 'catalogo.html#llegue-ordenado-al-contador', 'carpeta'),
    ('Números del dueño', 'Cuánto entra, cuánto sale y si le alcanza.', 'soluciones/visibilidad.html', 'grafica'),
    ('Presencia digital', 'Página, Google Maps y redes, con WhatsApp a un toque.', 'catalogo.html#f2', 'navegador'),
    ('Marketing digital', 'Marca, publicaciones y campañas con un objetivo medible.', 'soluciones/marketing-digital.html', 'megafono'),
    ('IA y automatización', 'Respuestas, recordatorios y documentos con menos trabajo a mano.', 'soluciones/ia-y-automatizacion.html', 'chip'),
]

# Frase entre la cinta y «¿Qué necesita su negocio?» (sustituye a «¿Le pasa esto?»).
# Combinación elegida por Kevin en el configurador: J · T5 · R3 · C1 · A3 · F2 · S3 · íconos.
FRASE_J = dict(
    antes='Más',
    gira=['control', 'orden', 'visibilidad'],  # la palabra que cambia sola, cada 3 s y sin detenerse (decisión de Kevin)
    despues='menos sorpresas.',
    resultados=[
        # (título, texto, ícono)
        ('Tiempo', 'Deja de resolver lo mismo todos los días.', 'reloj'),
        ('Tranquilidad', 'La caja cuadra y sabe por qué.', 'check'),
        ('Claridad', 'Sabe qué pedir y a quién cobrar.', 'grafica'),
        ('Rumbo', 'Decide qué sigue con sus propios números.', 'brujula'),
    ],
)

# ---------------- Fase 4: sitio, contador y autodiagnóstico ----------------
# Dirección completa del sitio: si cambia el dominio, se cambia solo esta línea.
SITIO_URL = 'https://keyacuevaca-dot.github.io/certeza-operativa/'

# Identificador del sitio en Umami Cloud (plan gratuito). Vacío: no se carga el contador.
UMAMI_ID = ''

# Autodiagnóstico (autodiagnostico.html). Las opciones de los pasos 2 y 3 salen de CINTA y NECESIDADES.
AUTODIAGNOSTICO = dict(
    titulo='Autodiagnóstico',
    intro='7 pasos, 2 minutos. No guardamos sus respuestas.',
    pasos=[
        dict(clave='personas', pregunta='¿Cuántas personas trabajan en su negocio, contándolo a usted?', opciones=['1 a 10', '11 a 50', '51 a 250', 'Más de 250']),
        dict(clave='giro', pregunta='¿De qué es su negocio?', opciones='CINTA', extra='Otro'),
        dict(clave='primero', pregunta='¿Qué necesita resolver primero?', opciones='NECESIDADES', extra='Todavía no lo sé'),
        dict(clave='rapido', pregunta='Conteste rápido', respuestas=['Sí', 'A veces', 'No'], preguntas=[
            ('¿Sabe hoy quién le debe, cuánto y desde cuándo?', 'Cobros y caja'),
            ('¿Sabe cada semana cuánto entró, cuánto salió y si le alcanza?', 'Números del dueño'),
            ('¿Su negocio trabaja igual cuando usted no está?', 'Equipo y procesos'),
            ('¿Sabe qué se le va a acabar antes de que se acabe?', 'Inventario y compras'),
            ('¿Lo encuentran en Google Maps y le escriben por WhatsApp?', 'Presencia digital')]),
        dict(clave='cuando', pregunta='¿Para cuándo lo necesita?', opciones=['Lo antes posible', 'En menos de 3 meses', 'En 3 a 6 meses', 'Solo estoy viendo opciones']),
        dict(clave='presupuesto', pregunta='¿Ya tiene un presupuesto para resolverlo?', opciones=['Sí, ya lo tengo', 'Tengo una idea', 'Todavía no']),
        dict(clave='contacto', pregunta='¿Cómo prefiere que le contactemos?', opciones=['WhatsApp', 'Llamada', 'Correo']),
    ],
    siguiente='Siguiente',
    resultado='Esto es lo que vemos en su negocio',
    va_bien='Su negocio va bien en lo básico. Lo siguiente puede ser:',
    va_bien_sugeridas=['Marketing digital', 'IA y automatización'],
    ver_industria='Vea cómo trabajamos con negocios de {categoria}',
    mas_250='Trabajamos con negocios de hasta 250 personas. Escríbanos y vemos si podemos ayudarle.',
    boton_wa='Mandar mi resultado por WhatsApp',
    reiniciar='Volver a empezar',
    sin_js='Para hacer el autodiagnóstico, active JavaScript o escríbanos por WhatsApp.',
    mensaje=['Hola, hice el autodiagnóstico de su página.', 'Giro: {giro}', 'Personas: {personas}', 'Quiero resolver primero: {primero}',
             'También me salió: {lista}', 'Para cuándo: {cuando}', 'Presupuesto: {presupuesto}', 'Prefiero que me contacten por: {contacto}'],
    entrada_pregunta='¿No sabe por dónde empezar?',
    entrada_boton='Haga el autodiagnóstico',
    entrada_cierre='O haga el autodiagnóstico de 2 minutos',
)
