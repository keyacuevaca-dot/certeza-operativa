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

  if (reduce) document.documentElement.classList.add('rm');
})();
