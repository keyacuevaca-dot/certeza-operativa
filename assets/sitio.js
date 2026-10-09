/* Certeza Operativa · comportamiento compartido (sin librerías) */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fmt = function (n) { return '$' + Math.round(n).toLocaleString('es-MX'); };

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

  /* --- Barra de herramientas: se puede pausar --- */
  var pausa = $('.pausa'), marquee = $('.marquee');
  if (pausa && marquee) pausa.addEventListener('click', function () {
    var on = !marquee.classList.contains('quieta');
    marquee.classList.toggle('quieta', on);
    pausa.setAttribute('aria-pressed', String(on));
    pausa.textContent = on ? 'Reanudar' : 'Pausar';
  });

  /* --- Botón flotante --- */
  var fl = $('#float');
  if (fl) {
    var ticking = false;
    addEventListener('scroll', function () {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () { fl.classList.toggle('on', scrollY > 700); ticking = false; });
    }, { passive: true });
  }

  /* --- Compartir --- */
  var share = $('#share');
  if (share) share.addEventListener('click', function (e) {
    e.preventDefault();
    var url = location.href.split('#')[0].split('?')[0], text = 'Certeza Operativa: consultoría para MiPyMEs en Nayarit. Empezar no cuesta.';
    if (navigator.share) navigator.share({ title: 'Certeza Operativa', text: text, url: url }).catch(function () {});
    else open('https://wa.me/?text=' + encodeURIComponent(text + ' ' + url), '_blank', 'noopener');
  });

  /* --- Catálogo + estimador (solo en el inicio) --- */
  var rng = $('#ventas');
  if (!rng) return;
  var RATE = { micro: 700, pequena: 1400, mediana: 0 }, NAME = { micro: 'Micro', pequena: 'Pequeña', mediana: 'Mediana' }, IVA = 0.16;
  var WA = 'https://wa.me/523114469363?text=';
  var pieces = $$('.piece'), FL0 = fl ? { href: fl.href, text: fl.textContent } : null;
  function size(v) { return v < 100000 ? 'micro' : (v <= 250000 ? 'pequena' : 'mediana'); }
  function range(v) { return v < 100000 ? 'menos de $100,000' : (v <= 250000 ? '$100,000 a $250,000' : 'más de $250,000'); }
  function calc() {
    var v = +rng.value, sz = size(v), r = RATE[sz], per = { orden: 0, visibilidad: 0, control: 0 }, adopt = false, sel = [];
    $('#ventasOut').textContent = fmt(v); rng.setAttribute('aria-valuetext', fmt(v) + ' al mes');
    $('#tam').textContent = NAME[sz]; $('#tar').textContent = r ? fmt(r) + ' + IVA por hora' : 'próximamente';
    if (!r) {
      ['h1', 'h2', 'h3'].forEach(function (id) { $('#' + id).textContent = '—'; });
      ['s1', 's2', 's3'].forEach(function (id) { $('#' + id).style.width = '0'; });
      $('#hrs').textContent = '—'; $('#monto').textContent = '—'; $('#tot').textContent = '';
      $('#msg').textContent = 'Por ahora atendemos negocios micro y pequeños, hasta $250,000 de ventas al mes. Escríbenos y te avisamos cuando abramos para empresas medianas.';
      var lk = WA + encodeURIComponent('Hola, mi negocio vende más de $250,000 al mes. Avísenme cuando atiendan empresas medianas.');
      $('#wa').href = lk; if (fl) { fl.href = lk; fl.textContent = FL0.text; }
      return;
    }
    pieces.forEach(function (p) { if ($('input', p).checked) { per[p.dataset.p] += +p.dataset.h; if (p.dataset.a) adopt = true; sel.push(p.dataset.n); } });
    var base = per.orden + per.visibilidad + per.control, tot = Math.round((base + (adopt ? .5 : 0)) * 4) / 4, billed = Math.max(5, tot), n = sel.length;
    var show = function (x) { return (Math.round(x * 4) / 4).toString().replace('.', ',') + ' h'; };
    ['orden', 'visibilidad', 'control'].forEach(function (k, i) { $('#h' + (i + 1)).textContent = show(per[k]); $('#s' + (i + 1)).style.width = (base > 0 ? per[k] / base * 100 : 0) + '%'; });
    $('#hrs').textContent = n ? show(billed) + (adopt ? ' (incluye 0,5 h de adopción)' : '') : '0 h';
    $('#monto').textContent = n ? fmt(billed * r) : '$0';
    $('#tot').textContent = n ? 'Total con IVA (16%): ' + fmt(billed * r * (1 + IVA)) : '';
    $('#msg').textContent = !n ? 'Elige al menos una pieza.' : (tot < 5 ? 'El mínimo por Ticket es de 5 h: súmale otra pieza y aprovechas mejor el trabajo.' : 'Listo. Este es un estimado; el precio cerrado llega después del Triaje.');
    var txt = 'Hola, quiero cotizar un trabajo con Certeza Operativa. Ventas al mes: ' + range(v) + '. ' + (n ? 'Piezas: ' + sel.join(', ') + '. Estimado orientativo: ' + fmt(billed * r) + ' + IVA (' + show(billed) + ').' : 'Quiero empezar con un Triaje sin costo.');
    var link = WA + encodeURIComponent(txt);
    $('#wa').href = link;
    if (fl) { fl.href = n ? link : FL0.href; fl.textContent = n ? 'Estimado ' + fmt(billed * r) + ' · Enviar por WhatsApp' : FL0.text; }
  }
  rng.addEventListener('input', calc);
  $$('input', $('#pieces')).forEach(function (i) { i.addEventListener('change', calc); });
  calc();

  /* Pilares: tocar uno abre sus piezas; tocarlo otra vez las cierra */
  var openP = null;
  function openPillar(p) {
    openP = p;
    $$('.pillar').forEach(function (b) { b.setAttribute('aria-pressed', String(!!p && b.dataset.p === p)); });
    pieces.forEach(function (x) { x.hidden = !p || x.dataset.p !== p; });
    $('#phint').hidden = !!p;
    if (p) $('#pieces').setAttribute('aria-labelledby', 'tab-' + p); else $('#pieces').removeAttribute('aria-labelledby');
  }
  $$('.pillar').forEach(function (b) { b.addEventListener('click', function () { openPillar(openP === b.dataset.p ? null : b.dataset.p); }); });
  $$('[data-open]').forEach(function (a) { a.addEventListener('click', function () { openPillar(a.dataset.open); }); });
  var h = location.hash.replace('#', '');
  openPillar(['orden', 'visibilidad', 'control'].indexOf(h) > -1 ? h : 'orden');
  if (reduce) document.documentElement.classList.add('rm');
})();
