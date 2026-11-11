/* Certeza Operativa · comportamiento compartido (sin librerías) */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* --- Menú: las tres líneas abren el panel; se cierra con Escape, con un enlace o tocando fuera --- */
  var burger = $('.burger'), panel = $('#menu-panel'), velo = $('.menu-velo');
  function abrir(on) {
    burger.setAttribute('aria-expanded', String(on));
    burger.setAttribute('aria-label', on ? 'Cerrar menú' : 'Abrir menú');
    panel.classList.toggle('open', on);
    document.documentElement.classList.toggle('menu-abierto', on);
    ['main', 'footer', '.skip', '.wa-fija'].forEach(function (s) { var n = $(s); if (n) n.inert = on; });
    if (on) { var a = $('a', panel); if (a) a.focus({ preventScroll: true }); }
  }
  if (burger && panel) {
    burger.addEventListener('click', function () { abrir(burger.getAttribute('aria-expanded') !== 'true'); });
    if (velo) velo.addEventListener('click', function () { abrir(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('open')) { abrir(false); burger.focus(); }
    });
    $$('a', panel).forEach(function (a) { a.addEventListener('click', function () { abrir(false); }); });
  }

  /* A6: al llegar al pie, los contactos normales quedan libres del botón fijo. */
  var pie = $('footer');
  if (pie && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      document.documentElement.classList.toggle('pie-visible', entries[0].isIntersecting);
    }).observe(pie);
  }

  /* --- Aparición al bajar: encabezados de sección y tarjetas (una tras otra), una sola vez.
     Lo que ya se ve al cargar no se esconde; sin JS o con movimiento reducido no se marca nada. --- */
  var rejillas = '.necesidades, .fj-items, .rejilla, .pasos, .ayuda, .voces, .lista2, .cat-rejilla, .cat-info, .chips, .otros, .faq, .webs';
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (vistos) {
      vistos.forEach(function (v) {
        if (!v.isIntersecting) return;
        var el = v.target, d = parseInt(el.style.getPropertyValue('--rv-d'), 10) || 0;
        io.unobserve(el);
        el.classList.add('rv-in');
        setTimeout(function () { el.classList.remove('rv', 'rv-in'); el.style.removeProperty('--rv-d'); }, 700 + d);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    var alto = innerHeight;
    $$('main section:not(.hero) .head, main .fj-frase, main .mas, main .mide, main .persona, main .svc, main .cta-band h2, main .cierre h2, main .cierre .actions, ' +
       rejillas.split(', ').map(function (r) { return 'main ' + r + ' > *'; }).join(', ')).forEach(function (el) {
      if (el.getBoundingClientRect().top < alto) return;
      var p = el.parentNode;
      if (p.matches && p.matches(rejillas)) el.style.setProperty('--rv-d', (Array.prototype.indexOf.call(p.children, el) % 6) * 90 + 'ms');
      el.classList.add('rv');
      io.observe(el);
    });
  }

  /* --- Frase «Más control, menos sorpresas.»: cada 3 s la palabra se desvanece y cambia a «orden» y «visibilidad»,
     sin detenerse (decisión de Kevin). Es un cambio de opacidad, sin desplazamiento. Sin JS se queda en «control». --- */
  var gira = $('.fj-gira');
  var palabras = gira ? (gira.getAttribute('data-gira') || '').split('|').filter(Boolean) : [];
  if (gira && palabras.length > 1) {
    gira.innerHTML = palabras.map(function (p, k) { return '<span' + (k ? ' class="fuera"' : '') + '>' + p.replace(/[&<>"]/g, '') + '</span>'; }).join('');
    var piezas = $$('span', gira), anchos = [], actual = 0;
    var medir = function () { anchos = piezas.map(function (s) { return Math.ceil(s.getBoundingClientRect().width); }); gira.style.width = anchos[actual] + 'px'; };
    var cambiar = function () {
      if (document.hidden) return;
      var sig = (actual + 1) % piezas.length;
      piezas[actual].classList.add('fuera');
      setTimeout(function () { gira.style.width = anchos[sig] + 'px'; piezas[sig].classList.remove('fuera'); actual = sig; }, 300);
    };
    var arrancar = function () {
      medir();
      /* Si la letra termina de cargar después (o cambia el tamaño), cada palabra cambia de ancho y se vuelve a medir */
      if ('ResizeObserver' in window) { var ro = new ResizeObserver(medir); piezas.forEach(function (s) { ro.observe(s); }); }
      else addEventListener('resize', medir);
      setInterval(cambiar, 3000);
    };
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(arrancar); else arrancar();
  }

  /* --- Catálogo: en celular «Qué incluye» se pliega; la tarjeta a la que se llega por enlace queda abierta.
     En escritorio siempre está abierto. Sin JS se ve todo. --- */
  var incluye = $$('.tr-incluye');
  if (incluye.length) {
    var cel = matchMedia('(max-width: 760px)');
    var ajustar = function () {
      var destino = location.hash ? document.getElementById(location.hash.slice(1)) : null;
      incluye.forEach(function (d) { d.open = !cel.matches || !!(destino && destino.contains(d)); });
    };
    ajustar();
    if (cel.addEventListener) cel.addEventListener('change', ajustar); else if (cel.addListener) cel.addListener(ajustar);
    addEventListener('hashchange', function () {
      var t = location.hash ? document.getElementById(location.hash.slice(1)) : null, d = t && $('.tr-incluye', t);
      if (d) d.open = true;
    });
  }

  /* --- Cinta de giros: una sola línea que corre de derecha a izquierda a 32 px por segundo, sin etiqueta ni botón
     (decisión de Kevin). Se detiene mientras el cursor está encima o un giro tiene el foco del teclado. --- */
  var cinta = $('.cinta'), lista = $('.cinta-lista');
  if (cinta && lista && !reduce) {
    var velocidad = function () { cinta.style.setProperty('--cinta-dur', Math.max(30, lista.scrollWidth / 32).toFixed(1) + 's'); };
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(velocidad); else velocidad();
  }

  /* --- Escenas de los encabezados: su movimiento continuo se pausa cuando no están a la vista (ahorra batería) --- */
  var escenas = $$('.ph .escena');
  if (escenas.length && !reduce && 'IntersectionObserver' in window) {
    var vigia = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('e-pausa', !e.isIntersecting); }); });
    escenas.forEach(function (s) { vigia.observe(s); });
  }

  /* --- Contador (Umami Cloud): eventos sin datos de la persona; si Umami no cargó, no pasa nada --- */
  function evento(n, d) { try { if (window.umami && typeof window.umami.track === 'function') window.umami.track(n, d); } catch (e) {} }
  function lugar(a) {
    if (a.closest('.hero')) return 'portada';
    if (a.closest('.ph')) return 'encabezado';
    if (a.closest('header.site')) return 'barra';
    if (a.closest('.cinta')) return 'cinta';
    if (a.closest('#que')) return 'tarjetas';
    if (a.closest('.ad')) return 'autodiagnostico';
    if (a.closest('.float')) return 'boton-flotante';
    if (a.closest('footer')) return 'pie';
    if (location.pathname.indexOf('/industrias/') > -1) return 'industria';
    if (location.pathname.indexOf('/soluciones/') > -1) return 'solucion';
    return 'cierre';
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    if ((a.getAttribute('href') || '').indexOf('wa.me/') > -1) {
      evento('whatsapp', { lugar: lugar(a) });
      if (a.hasAttribute('data-ad-wa')) evento('autodiagnostico-whatsapp');
    } else if (a.classList.contains('necesidad') && a.closest('#que')) {
      evento('tarjeta-necesidad', { titulo: a.getAttribute('data-titulo') });
    } else if (a.closest('.cinta-lista')) {
      evento('cinta', { nombre: a.textContent.trim() });
    }
  });

  if (reduce) document.documentElement.classList.add('rm');
})();
