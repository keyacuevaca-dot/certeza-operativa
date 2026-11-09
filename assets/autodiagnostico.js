/* Certeza Operativa · autodiagnóstico de 7 pasos. Nada se guarda: sin cookies ni almacenamiento;
   las respuestas solo viven en la página mientras está abierta. */
(function () {
  var app = document.querySelector('.ad-app'), f = document.getElementById('ad-form'), datos = document.getElementById('ad-datos');
  if (!app || !f || !datos) return;
  var D = JSON.parse(datos.textContent);
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var pasos = $$('.ad-paso', f), res = app.querySelector('.ad-res'), atras = app.querySelector('.ad-atras');
  var sig = f.querySelector('.ad-sig'), avance = app.querySelector('.ad-avance'), segs = $$('i', avance);
  var actual = 0, empezado = false, toque = false;

  function evento(n, d) { try { if (window.umami && typeof window.umami.track === 'function') window.umami.track(n, d); } catch (e) {} }
  function valor(nombre) { var c = f.querySelector('input[name="' + nombre + '"]:checked'); return c ? c.value : ''; }
  function completo(p) { return $$('.ad-g', p).every(function (g) { return !!g.querySelector('input:checked'); }); }

  function pintar(n, final) {
    segs.forEach(function (s, j) { s.classList.toggle('hecho', final || j <= n); });
    avance.setAttribute('aria-valuenow', String(final ? 7 : n + 1));
    avance.setAttribute('aria-valuetext', final ? 'Resultado' : 'Paso ' + (n + 1) + ' de 7');
  }

  function ir(n, foco) {
    actual = n;
    pasos.forEach(function (p, j) { p.hidden = j !== n; });
    f.hidden = false; res.hidden = true;
    atras.hidden = n === 0;
    sig.disabled = !completo(pasos[n]);
    pintar(n, false);
    if (foco) pasos[n].querySelector('legend').focus();
  }

  function avanzar() {
    if (!completo(pasos[actual])) return;
    if (actual < pasos.length - 1) ir(actual + 1, true); else resultado();
  }

  function resultado() {
    var primero = valor('primero');
    var rapido = D.rapido.map(function (t, j) { return [t, valor('r' + j)]; });
    var lista = [];
    if (primero && primero !== D.no_se) lista.push(primero);
    ['No', 'A veces'].forEach(function (r) {
      rapido.forEach(function (x) { if (x[1] === r && lista.indexOf(x[0]) < 0) lista.push(x[0]); });
    });
    lista = lista.slice(0, 3);
    var bien = primero === D.no_se && rapido.every(function (x) { return x[1] === 'Sí'; });
    var mostrar = bien ? D.va_bien : lista;

    var cont = res.querySelector('.ad-tarjetas'), cards = $$('.necesidad', cont);
    cards.forEach(function (c) { c.hidden = true; });
    mostrar.forEach(function (t) {
      var c = cards.filter(function (x) { return x.getAttribute('data-titulo') === t; })[0];
      if (c) { c.hidden = false; cont.appendChild(c); }
    });
    res.querySelector('.ad-bien').hidden = !bien;

    var giro = valor('giro'), ind = res.querySelector('.ad-ind'), slug = D.cinta[giro];
    if (slug) {
      var a = ind.querySelector('a');
      a.textContent = D.ver_industria.replace('{categoria}', giro);
      a.href = D.base + 'industrias/' + slug + '.html';
      ind.hidden = false;
    } else { ind.hidden = true; }
    res.querySelector('.ad-aviso').hidden = valor('personas') !== D.mas_250;

    var tambien = mostrar.filter(function (t) { return t !== primero; });
    var v = { giro: giro, personas: valor('personas'), primero: primero, lista: tambien.length ? tambien.join(', ') : '—',
              cuando: valor('cuando'), presupuesto: valor('presupuesto'), contacto: valor('contacto') };
    var texto = D.mensaje.map(function (l) { return l.replace(/\{(\w+)\}/g, function (_, k) { return v[k]; }); }).join('\n');
    res.querySelector('[data-ad-wa]').href = 'https://wa.me/' + D.wa + '?text=' + encodeURIComponent(texto);

    f.hidden = true; res.hidden = false; atras.hidden = false;
    pintar(6, true);
    res.querySelector('h2').focus();
    evento('autodiagnostico-resultado');
  }

  // Un toque elige y pasa solo al siguiente paso; con teclado, las flechas eligen y Enter avanza.
  f.addEventListener('pointerdown', function () { toque = true; });
  f.addEventListener('keydown', function (e) {
    toque = false;
    if (e.key === 'Enter' && e.target.matches('input[type="radio"]')) { e.preventDefault(); avanzar(); }
  });
  f.addEventListener('click', function (e) {
    var r = e.target.closest('input[type="radio"]');
    if (r && toque && r.checked && pasos[actual].hasAttribute('data-unica')) { toque = false; setTimeout(avanzar, 160); }
  });
  f.addEventListener('change', function () {
    if (!empezado) { empezado = true; evento('autodiagnostico-inicio'); }
    sig.disabled = !completo(pasos[actual]);
  });
  f.addEventListener('submit', function (e) { e.preventDefault(); avanzar(); });
  atras.addEventListener('click', function () {
    if (!res.hidden) ir(pasos.length - 1, true); else if (actual > 0) ir(actual - 1, true);
  });
  res.querySelector('.ad-otra').addEventListener('click', function () { f.reset(); empezado = false; ir(0, true); });

  ir(0, false);
})();
