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

  /* --- Catálogo + estimador (solo en el inicio) ---
     Precio cerrado por solución: cada pieza trae su precio por tamaño (data-micro, data-peq), en pesos más IVA.
     Estimado = suma de las piezas + adopción si alguna marcada lleva data-a; nunca menos del mínimo del tamaño. */
  var rng = $('#ventas');
  if (!rng) return;
  var NAME = { micro: 'Micro', pequena: 'Pequeña', mediana: 'Mediana' }, IVA = 0.16;
  var ADOP = { micro: 200, pequena: 350 }, MIN = { micro: 1750, pequena: 3500 }, MICRO = 100000, TOPE = 1000000;
  var PASOS = rng.dataset.pasos.split(',').map(Number);
  var WA = 'https://wa.me/523114469363?text=';
  var pieces = $$('.piece'), btn = $('#wa'), BTN0 = btn.textContent, FL0 = fl ? { href: fl.href, text: fl.textContent } : null;
  function size(v) { return v <= MICRO ? 'micro' : (v <= TOPE ? 'pequena' : 'mediana'); }
  function range(v) { return v <= MICRO ? 'hasta $100,000' : (v <= TOPE ? '$100,001 a $1,000,000' : 'más de $1,000,000'); }
  function precio(p, sz) { return +(sz === 'micro' ? p.dataset.micro : p.dataset.peq); }
  function calc() {
    var v = PASOS[+rng.value], sz = size(v), per = { orden: 0, visibilidad: 0, control: 0 }, adopt = false, sel = [];
    var vt = v > TOPE ? 'Más de ' + fmt(TOPE) : fmt(v);
    $('#ventasOut').textContent = vt; rng.setAttribute('aria-valuetext', vt + ' al mes');
    $('#tam').textContent = NAME[sz];
    if (sz === 'mediana') {
      pieces.forEach(function (p) { $('.k', p).textContent = '—'; });
      ['m1', 'm2', 'm3'].forEach(function (id) { $('#' + id).textContent = '—'; });
      ['s1', 's2', 's3'].forEach(function (id) { $('#' + id).style.width = '0'; });
      $('#det').textContent = ''; $('#monto').textContent = '—'; $('#tot').textContent = '';
      $('#msg').textContent = 'Por ahora atendemos negocios micro y pequeños, hasta $1,000,000 de ventas al mes.';
      var lk = WA + encodeURIComponent('Hola, mi negocio vende más de $1,000,000 al mes. Avísenme cuando atiendan empresas medianas.');
      btn.href = lk; btn.textContent = 'Escríbenos por WhatsApp';
      if (fl) { fl.href = lk; fl.textContent = FL0.text; }
      return;
    }
    pieces.forEach(function (p) {
      var x = precio(p, sz);
      $('.k', p).textContent = fmt(x);
      if ($('input', p).checked) { per[p.dataset.p] += x; if (p.dataset.a) adopt = true; sel.push(p.dataset.n); }
    });
    var base = per.orden + per.visibilidad + per.control, n = sel.length;
    var suma = base + (adopt ? ADOP[sz] : 0), est = n ? Math.max(MIN[sz], suma) : 0, minimo = n && suma < MIN[sz];
    ['orden', 'visibilidad', 'control'].forEach(function (k, i) { $('#m' + (i + 1)).textContent = fmt(per[k]); $('#s' + (i + 1)).style.width = (base > 0 ? per[k] / base * 100 : 0) + '%'; });
    $('#det').textContent = !n ? 'Sin piezas' : n + (n === 1 ? ' pieza' : ' piezas') + (minimo ? ' · mínimo por trabajo' : (adopt ? ' · incluye ' + fmt(ADOP[sz]) + ' de adopción' : ''));
    $('#monto').innerHTML = fmt(est) + '<small> + IVA</small>';
    $('#tot').textContent = n ? 'Total con IVA (16\u00a0%): ' + fmt(est * (1 + IVA)) : '';
    $('#msg').textContent = !n ? 'Elige al menos una pieza.' : (minimo ? 'El mínimo por trabajo es de ' + fmt(MIN[sz]) + ' + IVA: súmale otra pieza y aprovechas mejor el trabajo.' : 'Listo. Este es un estimado; el precio cerrado llega después del Triaje.');
    var txt = 'Hola, quiero cotizar un trabajo con Certeza Operativa. Ventas al mes: ' + range(v) + '. ' + (n ? 'Piezas: ' + sel.join(', ') + '. Estimado: ' + fmt(est) + ' + IVA.' : 'Quiero empezar con un Triaje sin costo.');
    var link = WA + encodeURIComponent(txt);
    btn.href = link; btn.textContent = BTN0;
    if (fl) { fl.href = n ? link : FL0.href; fl.textContent = n ? 'Estimado ' + fmt(est) + ' + IVA · Enviar por WhatsApp' : FL0.text; }
  }
  rng.addEventListener('input', calc);
  $$('input', $('#pieces')).forEach(function (i) { i.addEventListener('change', calc); });
  calc();

  if (reduce) document.documentElement.classList.add('rm');
})();
