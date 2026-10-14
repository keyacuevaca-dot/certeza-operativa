# Contenido del sitio. Todo lo que se publica sale de aquí: si cambia un texto, se cambia aquí
# y se vuelve a generar con `python3 _fuente/construir.py`.
# Regla: sin cifras, clientes ni testimonios inventados. Lo que no está confirmado lleva «POR CONFIRMAR» en el reporte.

WA_NUM = '523114469363'
TEL = '+52 311 446 9363'

# Piezas del estimador. Precio cerrado por solución: (micro, pequeña) en pesos, más IVA.
# El tercer dato marca las piezas que suman adopción en el estimador (assets/sitio.js). Fuente: Kevin, 14-oct-2026.
PIEZAS = [
    ('orden', (350, 1000), False, 'Lista de precios o catálogo', 'Que todos vean el mismo producto y el mismo precio.'),
    ('orden', (700, 2000), True, 'Cotizador', 'Decir qué se entrega, cuánto cuesta y hasta cuándo vale el precio.'),
    ('orden', (1400, 4000), True, 'Procedimiento escrito', 'Mostrar cómo hacer la tarea sin depender de la memoria.'),
    ('orden', (1050, 3000), False, 'Quién hace qué', 'Que cada pendiente tenga una persona responsable.'),
    ('orden', (1400, 4000), False, 'Expediente para el contador', 'Tener juntos los documentos que necesita tu contador.'),
    ('visibilidad', (700, 2000), True, 'Control de pedidos y cobros', 'Saber qué se pidió, qué se entregó y cuánto falta cobrar.'),
    ('visibilidad', (1400, 4000), True, 'Registro diario desde el celular', 'Guardar el dato antes de olvidarlo.'),
    ('visibilidad', (1400, 4000), True, 'Flujo a 30, 60 y 90 días', 'Ver si el dinero alcanzaría en las próximas fechas.'),
    ('visibilidad', (1750, 5000), True, 'Tablero semanal', 'Ver lo más urgente sin leer todos los registros.'),
    ('visibilidad', (1750, 5000), True, 'Inventario y reorden', 'Tener existencias visibles y pedir antes de quedarte sin producto.'),
    ('control', (700, 2000), True, 'Agenda de cobranza', 'Saber a quién cobrar, cuánto y cuándo.'),
    ('control', (1400, 4000), False, 'Lo cobrado contra lo depositado', 'Comprobar que lo que cobraste coincide con lo que entró al banco.'),
    ('control', (700, 2000), True, 'Arqueo y cierre de caja', 'Cerrar el día con la caja contada y comparada.'),
]
PIEZA = {p[3]: p for p in PIEZAS}
PILAR_NOMBRE = {'orden': 'Orden', 'visibilidad': 'Visibilidad', 'control': 'Control', 'mejora': 'Mejora continua'}

# ---------------- Soluciones listas (servicios.html#soluciones-listas) ----------------
# Una tarjeta por combo. Al cliente no se le muestran el código ni el precio; el código vive solo aquí, junto a su nombre.
# Textos adaptados a «tú». El ancla es la que Kevin definió para anuncios (servicios.html#<ancla>); no cambiarla.
# Fuente: Kevin, 14-oct-2026.
COMBOS = [
    dict(codigo='A1', nombre='Cobra lo que te deben', ancla='cobre-lo-que-le-deben',  # A1 · Cobre lo que le deben
         quien='Comercios, talleres y servicios que fían o dan crédito.',
         promesa='Ten claro quién te debe, cuánto y desde cuándo, y cobra sin pelearte.',
         puntos=['Lista de lo que te deben, con fechas', 'Agenda para cobrar a cada quien', 'Mensajes listos para cobrar con respeto']),
    dict(codigo='A2', nombre='Caja que cuadra', ancla='caja-que-cuadra',  # A2 · Caja que cuadra
         quien='Tiendas, comida y negocios con caja diaria.',
         promesa='Cierra la caja sin dudas y ten claro cuánto entró y salió cada día.',
         puntos=['Cierre de caja con lista de apertura', 'Registro diario desde el celular', 'Resumen semanal sin esperar al fin de mes']),
    dict(codigo='A3', nombre='Cotiza sin errores', ancla='cotice-sin-errores',  # A3 · Cotice sin errores
         quien='Talleres, servicios y comercios que cotizan seguido.',
         promesa='Precios claros y cotizaciones sin errores en minutos.',
         puntos=['Lista de precios con tu marca', 'Cotizador que no se equivoca en sumas', 'Menos mensajes de «¿cuánto cuesta?»']),
    dict(codigo='A4', nombre='Inventario bajo control', ancla='inventario-bajo-control',  # A4 · Inventario bajo control
         quien='Tiendas, refaccionarias y ferreterías.',
         promesa='Ten claro qué pedir y qué no mover, antes de que falte.',
         puntos=['Existencias con punto de reorden', 'Lo que no se mueve, a la vista', 'Borrador de pedido listo']),
    dict(codigo='A5', nombre='Tu negocio camina sin ti', ancla='su-negocio-camina-sin-usted',  # A5 · Su negocio camina sin usted
         quien='Dueños que no pueden faltar.',
         promesa='Cada quien sabe qué le toca y cómo hacerlo, aunque tú no estés.',
         puntos=['Quién hace qué y a quién se escala', 'La tarea clave escrita paso a paso', 'Lista de verificación para tu equipo']),
    dict(codigo='A6', nombre='Llega ordenado al contador', ancla='llegue-ordenado-al-contador',  # A6 · Llegue ordenado al contador
         quien='Negocios que empiezan a formalizarse.',
         promesa='Tus ingresos y gastos ordenados, mes por mes.',
         puntos=['Carpeta con comprobantes clasificados', 'Resumen por mes', 'Registro diario desde el celular']),
    dict(codigo='B1', nombre='Lo encuentran y le pagan', ancla='lo-encuentran-y-le-pagan',  # B1 · Lo encuentran y le pagan
         quien='Negocios con clientes de crédito que quieren más clientes.',
         promesa='Que te encuentren en Google, Facebook e Instagram, y que te paguen a tiempo.',
         puntos=['Página, ficha de Google Maps y redes listas', 'WhatsApp con respuestas automáticas', 'Control de lo que te deben y agenda de cobro']),
    dict(codigo='B2', nombre='Vitrina y ventas', ancla='vitrina-y-ventas',  # B2 · Vitrina y ventas
         quien='Comercios y talleres que cotizan por WhatsApp.',
         promesa='Que te encuentren en internet y cotices en minutos.',
         puntos=['Página, Google Maps y redes listas', 'Lista de precios para WhatsApp', 'Cotizador sin errores']),
    dict(codigo='B3', nombre='Comida en orden y en el mapa', ancla='comida-en-orden-y-en-el-mapa',  # B3 · Comida en orden y en el mapa
         quien='Restaurantes, cocinas y antojitos.',
         promesa='Tu negocio en el mapa, tu menú a la mano y la caja cuadrada cada noche.',
         puntos=['Página, Google Maps y redes listas', 'Menú o lista de precios con tu marca', 'Cierre de caja diario']),
    dict(codigo='B4', nombre='Negocio completo', ancla='negocio-completo',  # B4 · Negocio completo
         quien='Negocios pequeños listos para crecer.',
         promesa='Presencia completa, cotizaciones rápidas y cobranza al día.',
         puntos=['Sitio de hasta 5 secciones, Google Maps y redes', 'Cotizador sin errores', 'Control de cobros y agenda de cobranza']),
    dict(codigo='S1', nombre='Que lo encuentren', ancla='que-lo-encuentren',  # S1 · Que lo encuentren (kit: combos/S1-que-lo-encuentren)
         quien='Negocios que no aparecen o aparecen incompletos en Google.',
         promesa='Que te encuentren en Google y te escriban por WhatsApp con un toque.',
         puntos=['Tu ficha de Google Maps completa', 'Página con botón de WhatsApp', 'WhatsApp Business con respuestas listas']),
    dict(codigo='S2', nombre='Página y redes', ancla='pagina-y-redes',  # S2 · Página y redes
         quien='Negocios que venden por redes.',
         promesa='Google, Facebook, Instagram y WhatsApp conectados y listos.',
         puntos=['Página con botón de WhatsApp', 'Ficha de Google Maps completa', 'Facebook e Instagram conectados']),
    dict(codigo='S3', nombre='Sitio completo', ancla='sitio-completo',  # S3 · Sitio completo
         quien='Negocios con varios servicios.',
         promesa='Un sitio que responde las preguntas de siempre antes de que te las hagan.',
         puntos=['Sitio de hasta 5 secciones', 'Ficha de Google Maps completa', 'Facebook e Instagram conectados']),
    dict(codigo='S4', nombre='Catálogo en línea', ancla='catalogo-en-linea',  # S4 · Catálogo en línea
         quien='Negocios con productos que se cotizan.',
         promesa='Tus productos en línea y los pedidos de cotización ordenados.',
         puntos=['Hasta 30 productos con foto', 'Botón de cotización por WhatsApp', 'Ficha de Google Maps completa']),
]

# ---------------- Industrias ----------------
INDUSTRIAS = [
    dict(slug='alimentos-y-bebidas', corto='Restaurantes, cafeterías, panaderías y más.', nombre='Alimentos y bebidas',
         tipos='Restaurantes, cocinas económicas, cafeterías, panaderías, tortillerías y purificadoras.',
         lead='Vendes todo el día, en efectivo y por transferencia, con insumos que caducan. Te ayudamos a que la caja cuadre, el inventario avise a tiempo y cada turno trabaje igual.',
         voces=['¿Por qué no me cuadra la caja al cierre?', '¿Qué tengo que comprar para mañana?', '¿Cómo hago que el turno de la tarde trabaje igual que el de la mañana?', '¿Cuánto vendí esta semana contra la pasada?'],
         piezas=['Arqueo y cierre de caja', 'Lo cobrado contra lo depositado', 'Inventario y reorden', 'Procedimiento escrito', 'Registro diario desde el celular', 'Lista de precios o catálogo'],
         herramientas=['Hojas de Google', 'Excel', 'WhatsApp Business', 'Canva', 'Mercado Pago', 'Google Maps']),
    dict(slug='comercio-y-tiendas', corto='Abarrotes, ferreterías, papelerías y farmacias.', nombre='Comercio y tiendas',
         tipos='Abarrotes, ferreterías, papelerías, farmacias, boutiques y materiales.',
         lead='Muchos productos, precios que cambian y clientes que piden fiado. Ordenamos tu lista de precios, tu inventario y tu cobranza para que sepas qué tienes y quién te debe.',
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
         lead='Cada obra es un proyecto con material, cuadrillas y pagos por avance. Te ayudamos a saber quién hace qué, para cuándo, y si el dinero alcanza hasta el siguiente pago del cliente.',
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
         lead='Temporadas altas y bajas, reservaciones por WhatsApp y personal que cambia. Te ayudamos a ver reservaciones, cobros y pendientes en una sola vista, y a que cada temporada arranque con el mismo estándar.',
         voces=['¿Qué está reservado y qué falta cobrar?', '¿Me alcanza el dinero para la temporada baja?', '¿Cómo entreno rápido al personal nuevo?', '¿Qué se rentó y cuándo regresa?'],
         piezas=['Flujo a 30, 60 y 90 días', 'Control de pedidos y cobros', 'Procedimiento escrito', 'Tablero semanal', 'Agenda de cobranza', 'Lista de precios o catálogo'],
         herramientas=['Google Calendar', 'WhatsApp Business', 'Hojas de Google', 'Google Maps', 'Instagram', 'Facebook']),
    dict(slug='servicios-profesionales', corto='Consultorios, despachos y estéticas.', nombre='Servicios profesionales y de salud',
         tipos='Consultorios, despachos, estéticas, gimnasios, escuelas y servicios por cita.',
         lead='Tu agenda es tu inventario. Ordenamos citas, cobros y seguimientos para que no se crucen las citas ni se queden pagos sin cobrar.',
         voces=['¿Se me cruzan las citas?', '¿Qué servicio toca y qué falta cobrar?', '¿Quién da seguimiento a cada cliente?', '¿Cuántos clientes regresan?'],
         piezas=['Agenda de cobranza', 'Quién hace qué', 'Tablero semanal', 'Lista de precios o catálogo', 'Registro diario desde el celular', 'Expediente para el contador'],
         herramientas=['Google Calendar', 'WhatsApp Business', 'Hojas de Google', 'Google Forms', 'Notion', 'Zoom']),
]

# ---------------- Soluciones ----------------
SOLUCIONES = [
    dict(slug='orden', nombre='Orden', icono='i-orden', tl='Cada cosa en su lugar.',
         lead='Que las cosas salgan igual aunque tú no estés: precios a la vista, tareas escritas y un responsable para cada pendiente.',
         voces=['Todo depende de mí: los precios están en mi cabeza.', 'Cuando falto, algo sale mal.', 'Me preguntan lo mismo varias veces al día.'],
         entregables=[('Lista de precios o catálogo', 'Con tu marca, en PDF, para que todos den el mismo precio.'),
                      ('Cotizador', 'Decir qué se entrega, cuánto cuesta y hasta cuándo vale el precio.'),
                      ('Procedimiento escrito', 'Una tarea paso a paso, con lista de verificación.'),
                      ('Quién hace qué', 'Mapa de quién hace cada cosa y quién decide.'),
                      ('Expediente para el contador', 'Los documentos que pide tu contador, juntos y a tiempo.'),
                      ('Plantillas protegidas (con Plus)', 'Tu equipo solo cambia textos y precios; el formato no se rompe.')],
         mide=('Pendientes sin responsable', 'Contamos cuántos pendientes no tienen dueño antes de empezar y al entregar. La meta: ninguno.')),
    dict(slug='visibilidad', nombre='Visibilidad', icono='i-vis', tl='Saber qué pasa, a tiempo.',
         lead='Saber cada semana cómo va el negocio, en una sola vista, sin esperar a fin de mes ni leer todas las libretas.',
         voces=['No sé cómo va el negocio hasta fin de mes.', 'No sé si esta semana fue mejor que la pasada.', 'Los números están en varias libretas.'],
         entregables=[('Registro diario desde el celular', 'Una captura corta para guardar el dato antes de olvidarlo.'),
                      ('Tablero semanal', 'Cinco indicadores con gráficas que se actualizan solas.'),
                      ('Control de pedidos y cobros', 'Qué se pidió, qué se entregó y cuánto falta cobrar.'),
                      ('Flujo a 30, 60 y 90 días', 'Ver a tiempo si el dinero alcanzaría.'),
                      ('Inventario y reorden', 'Existencias visibles y aviso para pedir antes de quedarte sin producto.'),
                      ('Resumen de una página (con Plus)', 'Para imprimir o mandar por WhatsApp.')],
         mide=('Dinero previsto a 30, 60 y 90 días', 'Al entregar comparamos contigo lo previsto contra lo que pasó; después lo revisas tú cada semana en tu tablero.')),
    dict(slug='control', nombre='Control', icono='i-ctl', tl='Que lo cobrado cuadre.',
         lead='Que no se te escape dinero sin darte cuenta: la caja cuadra al cierre y cada cliente que te debe tiene fecha de cobro.',
         voces=['Fío y se me olvida cobrar.', 'Al cerrar, la caja no coincide con las ventas.', 'No sé si lo que cobré llegó completo al banco.'],
         entregables=[('Arqueo y cierre de caja', 'Lista de apertura y cierre, con una hoja que suma sola.'),
                      ('Lo cobrado contra lo depositado', 'Comprobar que lo cobrado coincide con lo que entró al banco.'),
                      ('Agenda de cobranza', 'Calendario de cobro ordenado por monto y antigüedad.'),
                      ('Mensajes de cobranza', 'En tres tonos, listos para WhatsApp. Los envías tú.'),
                      ('Formato de salidas y entregas (con Plus)', 'Para saber qué salió, quién lo llevó y quién lo recibió.'),
                      ('Capacitación a tu encargado de caja (con Plus)', 'Para que el cierre salga igual cualquier día.')],
         mide=('Lo cobrado contra lo depositado', 'Lo probamos contigo en un cierre real. Si algo no cuadra, se ve la diferencia y su causa.')),
    dict(slug='mejora-continua', nombre='Mejora continua', icono='i-mejora', tl='Medir, resolver, comprobar y volver a empezar.',
         lead='Medimos tu punto de partida con tus papeles. El trabajo termina cuando tu equipo completa un ciclo sin nosotros. Después comparamos el número de antes con el de hoy: eso es el Delta (Δ).',
         voces=['Ya intenté ordenarme y a las dos semanas volvimos a lo mismo.', 'No sé si lo que cambié sirvió de algo.', 'Mi equipo deja de usar los formatos.'],
         entregables=[('Tu punto de partida (Línea Cero)', 'Elegimos un solo número que importe y lo medimos con tus papeles, no de memoria.'),
                      ('Prueba con un caso real', 'Una semana o un cierre real, y ajuste antes de darlo por entregado.'),
                      ('Tu equipo lo usa solo (Prueba de salida)', 'El trabajo termina cuando tu equipo completa un ciclo sin nosotros.'),
                      ('Revisión a las cuatro semanas (con Plus)', 'En Visibilidad, para ajustar los indicadores.'),
                      ('Medimos la mejora (Delta)', 'Comparamos el número de antes con el de hoy. Lo que funcionó queda escrito.'),
                      ('El siguiente problema', 'Si quieres, lo elegimos juntos, con su propio precio.'),
                      ('Capacitación', 'Capacitamos a quien lo va a usar, para que tu equipo lo use sin nosotros.')],
         mide=('Delta (Δ)', 'La diferencia entre el número de antes y el de después. Tú la ves y tú la verificas.')),
    dict(slug='herramientas', nombre='Herramientas', icono='i-herr', tl='Sencillas y adaptadas a tu negocio.',
         lead='No te vendemos software. Partimos de lo que ya usas, en papel o en el celular, y lo dejamos ordenado para que tu equipo lo use solo.',
         voces=['Compré un sistema y nadie lo usa.', 'Tengo todo en Excel, pero nadie lo entiende.', 'Quiero usar inteligencia artificial, pero no sé para qué.'],
         entregables=[('Hojas de cálculo', 'Excel u Hojas de Google con registros que suman solos.'),
                      ('Documentos con tu marca', 'Formatos, listas y tableros en la cuenta de Canva de tu negocio.'),
                      ('WhatsApp Business', 'Mensajes listos, catálogos y recordatorios para tus clientes.'),
                      ('Formularios', 'Captura semanal de 5 minutos desde el celular, por ejemplo con Google Forms.'),
                      ('Sistemas que ya tienes', 'Si ya usas Odoo, CONTPAQi o Aspel, partimos de ahí.'),
                      ('Inteligencia artificial, fácil', 'Asistentes como Claude, ChatGPT o Gemini para redactar y resumir; tú revisas y decides.')],
         mide=('Uso real', 'Una herramienta sirve si tu equipo la usa. Al entregar revisamos contigo si se captura y se consulta.')),
    dict(slug='metodos', nombre='Métodos', icono='i-metodo', tl='Claros, cortos y en tu idioma.',
         lead='Llevamos métodos de la mejora continua al tamaño de tu negocio, sin siglas ni papeleo de más.',
         voces=['Los consultores me dejaron un documento que nunca leí.', 'Quiero saber qué hacer el lunes, no una teoría.', 'Necesito que mi equipo entienda el cambio.'],
         entregables=[('Triaje', 'Doce preguntas y un caso real de tu negocio, de punta a punta. Siempre sin costo.'),
                      ('Ficha', 'El plan en una hoja: lo encontrado, una acción gratis para hoy y el siguiente paso con precio y fecha.'),
                      ('Punto de partida (Línea Cero)', 'Tu número de hoy, medido con tus papeles. Es la base para comparar después.'),
                      ('Ticket', 'Un trabajo con precio cerrado. Se entrega cuando tu equipo lo usa solo.'),
                      ('Delta', 'La medición de antes y después, para decidir el siguiente paso.'),
                      ('Listas de verificación', 'Para que una tarea salga igual sin depender de la memoria.'),
                      ('Tableros visuales', 'Pocos números, a la vista, revisados cada semana.')],
         mide=('Delta (Δ)', 'El número de cada Ticket, antes y después. Tú lo verificas.')),
]
