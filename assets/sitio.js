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
    ['main', 'footer', '.skip'].forEach(function (s) { var n = $(s); if (n) n.inert = on; });
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

  /* --- Aparición al bajar: encabezados de sección y tarjetas (una tras otra), una sola vez.
     Lo que ya se ve al cargar no se esconde; sin JS o con movimiento reducido no se marca nada. --- */
  var rejillas = '.necesidades, .rejilla, .pasos, .ayuda, .voces, .lista2, .cat-col > ul, .cat-pie, .chips, .otros, .faq, .webs';
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
    $$('main section:not(.hero) .head, main .remate, main .mas, main .mide, main .persona, main .svc, main .cta-band h2, main .cierre h2, main .cierre .actions, ' +
       rejillas.split(', ').map(function (r) { return 'main ' + r + ' > *'; }).join(', ')).forEach(function (el) {
      if (el.getBoundingClientRect().top < alto) return;
      var p = el.parentNode;
      if (p.matches && p.matches(rejillas)) el.style.setProperty('--rv-d', (Array.prototype.indexOf.call(p.children, el) % 6) * 90 + 'ms');
      el.classList.add('rv');
      io.observe(el);
    });
  }

  /* --- Cinta «Trabajamos con:»: ~40 px por segundo y botón de pausa (WCAG 2.2.2) --- */
  var cinta = $('.cinta'), pausa = $('.cinta-pausa'), lista = $('.cinta-lista');
  if (cinta && pausa && lista && !reduce) {
    var velocidad = function () { cinta.style.setProperty('--cinta-dur', Math.min(70, Math.max(45, lista.scrollWidth / 40)).toFixed(1) + 's'); };
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(velocidad); else velocidad();
    pausa.addEventListener('click', function () {
      var on = pausa.getAttribute('aria-pressed') !== 'true';
      pausa.setAttribute('aria-pressed', String(on));
      pausa.setAttribute('aria-label', on ? 'Reanudar la cinta' : 'Pausar la cinta');
      cinta.classList.toggle('pausada', on);
    });
  }

  /* --- Contador (Umami Cloud): eventos sin datos de la persona; si Umami no cargó, no pasa nada --- */
  function evento(n, d) { try { if (window.umami && typeof window.umami.track === 'function') window.umami.track(n, d); } catch (e) {} }
  function lugar(a) {
    if (a.closest('.hero')) return 'portada';
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
