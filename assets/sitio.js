/* Certeza Operativa · comportamiento compartido (sin librerías) */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* --- Menú: cada pestaña despliega un panel informativo --- */
  var menu = $('.menu'), burger = $('.burger'), tops = $$('.mtop[aria-controls]');
  var desk = matchMedia('(min-width: 1081px)'), hover = matchMedia('(hover: hover) and (pointer: fine)'), t = null, porHover = null;
  function closeAll(except) {
    tops.forEach(function (b) { if (b !== except) { b.setAttribute('aria-expanded', 'false'); $('#' + b.getAttribute('aria-controls')).classList.remove('open'); } });
  }
  function setOpen(b, on) {
    closeAll(b);
    b.setAttribute('aria-expanded', String(on));
    $('#' + b.getAttribute('aria-controls')).classList.toggle('open', on);
  }
  tops.forEach(function (b) {
    var li = b.parentNode;
    b.addEventListener('click', function () {
      clearTimeout(t);
      if (porHover === b && b.getAttribute('aria-expanded') === 'true') { porHover = null; return; }
      porHover = null;
      setOpen(b, b.getAttribute('aria-expanded') !== 'true');
    });
    li.addEventListener('mouseenter', function () { if (desk.matches && hover.matches) { clearTimeout(t); t = setTimeout(function () { if (b.getAttribute('aria-expanded') !== 'true') porHover = b; setOpen(b, true); }, 90); } });
    li.addEventListener('mouseleave', function () { if (desk.matches && hover.matches) { clearTimeout(t); porHover = null; t = setTimeout(function () { setOpen(b, false); }, 160); } });
    li.addEventListener('focusout', function (e) { if (desk.matches && !li.contains(e.relatedTarget)) setOpen(b, false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = tops.filter(function (b) { return b.getAttribute('aria-expanded') === 'true'; })[0];
    if (open) { setOpen(open, false); open.focus(); }
    else if (menu && menu.classList.contains('open')) { toggleMenu(false); burger.focus(); }
  });
  document.addEventListener('click', function (e) { if (desk.matches && !e.target.closest('.menu')) closeAll(); });
  function toggleMenu(on) {
    menu.classList.toggle('open', on);
    burger.setAttribute('aria-expanded', String(on));
    burger.setAttribute('aria-label', on ? 'Cerrar menú' : 'Abrir menú');
    document.body.style.overflow = on ? 'hidden' : '';
    ['main', 'footer', '#float', '.skip'].forEach(function (s) { var n = $(s); if (n) n.inert = on; });
    if (!on) closeAll();
  }
  if (burger) burger.addEventListener('click', function () { toggleMenu(!menu.classList.contains('open')); });
  var alCambiar = function () { if (desk.matches && menu.classList.contains('open')) toggleMenu(false); closeAll(); };
  if (desk.addEventListener) desk.addEventListener('change', alCambiar); else if (desk.addListener) desk.addListener(alCambiar);
  $$('.menu a[href*="#"]').forEach(function (a) { a.addEventListener('click', function () { if (menu.classList.contains('open')) toggleMenu(false); closeAll(); }); });

  /* --- Botón flotante --- */
  var fl = $('#float');
  if (fl) {
    var ticking = false;
    addEventListener('scroll', function () {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () { fl.classList.toggle('on', scrollY > 700); ticking = false; });
    }, { passive: true });
  }

  if (reduce) document.documentElement.classList.add('rm');
})();
