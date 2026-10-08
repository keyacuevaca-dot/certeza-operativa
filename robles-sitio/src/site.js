/* Comercializadora Robles · comportamiento del sitio. Sin dependencias.
   Los datos del catálogo vienen de assets/js/catalogo.js (window.ROBLES_CATALOGO). */
(function () {
  'use strict';
  var D = document, H = D.documentElement, NS = 'http://www.w3.org/2000/svg';
  H.classList.add('js');
  var WA = '523119104468';
  var $ = function (s, r) { return (r || D).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || D).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var LINEAS = window.ROBLES_LINEAS || [];
  var ITEMS = (window.ROBLES_CATALOGO || []).filter(function (i) { return String(i.activo).toLowerCase() !== 'no'; })
    .sort(function (a, b) { return (a.orden || 0) - (b.orden || 0); });
  var BYID = {}; ITEMS.forEach(function (i) { BYID[i.id] = i; });

  function norm(t) { return String(t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function waUrl(msg) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg); }
  function slug(t) { return norm(t).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
  function el(tag, attrs, kids) {
    var e = D.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { if (k === 'text') e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); });
    (kids || []).forEach(function (c) { if (c) e.appendChild(typeof c === 'string' ? D.createTextNode(c) : c); });
    return e;
  }
  function ico(id) {
    var s = D.createElementNS(NS, 'svg'); s.setAttribute('class', 'ico'); s.setAttribute('aria-hidden', 'true');
    var u = D.createElementNS(NS, 'use'); u.setAttribute('href', '#i-' + id); s.appendChild(u); return s;
  }

  /* ---------- Almacenamiento (puede fallar: modo privado, bloqueo) ---------- */
  var KEY = 'robles-lista-v1', memoria = null;
  function cargar() {
    try { var a = JSON.parse(localStorage.getItem(KEY) || '[]'); if (Array.isArray(a)) return a; } catch (e) {}
    return memoria || [];
  }
  var lista = cargar().filter(function (x) { return x && BYID[x.id] && x.qty > 0; });
  function guardar() { memoria = lista; try { localStorage.setItem(KEY, JSON.stringify(lista)); } catch (e) {} }

  /* ---------- Producto: texto, precio y mensajes ---------- */
  function etiq(it) { return it.nombre + (it.pres ? ' (' + it.pres + ')' : ''); }
  function nombreCompleto(it) {
    var n = it.nombre;
    if (it.marca && norm(n).indexOf(norm(it.marca)) < 0) n += ' ' + it.marca;
    return n;
  }
  function meta(it) {
    var p = [];
    if (it.marca && norm(it.nombre).indexOf(norm(it.marca)) < 0) p.push(it.marca);
    if (it.pres) p.push(it.pres);
    return p.join(' · ');
  }
  // Un precio solo se muestra completo: monto, unidad, IVA y fecha de vigencia sin vencer.
  function precioCompleto(it) {
    var p = parseFloat(String(it.precio).replace(',', '.'));
    if (!(p > 0) || !it.unidad || !/^(sí|si|no)$/i.test(String(it.iva || '')) || !it.vigencia) return null;
    var v = new Date(it.vigencia + 'T23:59:59');
    if (isNaN(v.getTime()) || v < new Date()) return null;
    var iva = /^(sí|si)$/i.test(it.iva) ? 'IVA incluido' : 'IVA no incluido';
    var fecha = v.toLocaleDateString('es-MX', { day: 'numeric', month: 'long' });
    return { monto: '$' + p.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' MXN',
             detalle: 'por ' + it.unidad + ' · ' + iva + ' · vigente hasta el ' + fecha };
  }
  var HAY_PRECIOS = ITEMS.some(function (i) { return !!precioCompleto(i); });
  function lineaMsg(it, qty) { return nombreCompleto(it) + (it.pres ? ' (' + it.pres + ')' : '') + ' · cantidad: ' + qty; }
  function msgProducto(it, qty) { return 'Hola, quiero cotizar: ' + lineaMsg(it, qty); }
  function msgLista() {
    var l = ['Hola, quiero cotizar esta lista:'];
    lista.forEach(function (x, i) { l.push((i + 1) + '. ' + lineaMsg(BYID[x.id], x.qty)); });
    return l.join('\n');
  }

  /* ---------- Control de cantidad ---------- */
  function cantidad(valor, alCambiar, etiqueta, uid) {
    var inp = el('input', { type: 'number', min: '1', max: '999', value: String(valor), inputmode: 'numeric', id: uid, 'aria-label': 'Cantidad de ' + etiqueta });
    function poner(n) { n = Math.max(1, Math.min(999, parseInt(n, 10) || 1)); inp.value = n; alCambiar(n); }
    var menos = el('button', { type: 'button', 'aria-label': 'Quitar una unidad de ' + etiqueta }, [ico('menos')]);
    var mas = el('button', { type: 'button', 'aria-label': 'Agregar una unidad de ' + etiqueta }, [ico('mas')]);
    menos.addEventListener('click', function () { poner((parseInt(inp.value, 10) || 1) - 1); });
    mas.addEventListener('click', function () { poner((parseInt(inp.value, 10) || 1) + 1); });
    inp.addEventListener('change', function () { poner(inp.value); });
    return { nodo: el('div', { 'class': 'cant' }, [el('label', { 'for': uid, text: 'Cantidad' }), menos, inp, mas]), leer: function () { return parseInt(inp.value, 10) || 1; } };
  }

  /* ---------- Lista del visitante ---------- */
  var dlg = $('#lista'), anuncio = $('#anuncio');
  function decir(t) { if (anuncio) { anuncio.textContent = ''; setTimeout(function () { anuncio.textContent = t; }, 30); } }
  function agregar(id, qty) {
    var f = lista.filter(function (x) { return x.id === id; })[0];
    if (f) f.qty = Math.min(999, f.qty + qty); else lista.push({ id: id, qty: qty });
    guardar(); pintarLista();
    decir(nombreCompleto(BYID[id]) + ' agregado. Tu lista tiene ' + lista.length + (lista.length === 1 ? ' producto.' : ' productos.'));
  }
  function pintarLista() {
    $$('[data-n-lista]').forEach(function (n) { n.textContent = lista.length; n.hidden = lista.length === 0; });
    if (!dlg) return;
    var ul = $('.items', dlg), vacio = $('.lista-vacia', dlg), enviar = $('#lista-wa', dlg), borrar = $('#lista-vaciar', dlg);
    var foco = null;
    if (dlg.open && D.activeElement && ul.contains(D.activeElement)) {
      var li0 = D.activeElement.closest('li');
      foco = { i: Array.prototype.indexOf.call(ul.children, li0), j: $$('button,input', li0).indexOf(D.activeElement) };
    }
    ul.textContent = '';
    lista.forEach(function (x) {
      var it = BYID[x.id], m = meta(it);
      var c = cantidad(x.qty, function (n) { x.qty = n; guardar(); pintarLista(); }, etiq(it), 'lq-' + it.id);
      var q = el('button', { type: 'button', 'class': 'quitar', 'aria-label': 'Quitar ' + etiq(it) + ' de mi lista' }, ['Quitar ' + it.nombre]);
      q.addEventListener('click', function () { lista = lista.filter(function (y) { return y !== x; }); guardar(); pintarLista(); decir(it.nombre + ' quitado de tu lista.'); });
      ul.appendChild(el('li', {}, [el('b', { text: nombreCompleto(it) }), c.nodo, m ? el('span', { 'class': 'meta', text: m }) : null, q]));
    });
    vacio.hidden = lista.length > 0; ul.hidden = lista.length === 0;
    enviar.setAttribute('href', lista.length ? waUrl(msgLista()) : '#');
    enviar.setAttribute('aria-disabled', lista.length ? 'false' : 'true');
    borrar.hidden = lista.length === 0;
    if (foco) {
      var li1 = ul.children[Math.min(foco.i, ul.children.length - 1)];
      if (li1) { var cs = $$('button,input', li1); (cs[foco.j] || cs[cs.length - 1]).focus(); } else $('.cerrar', dlg).focus();
    }
  }
  if (dlg) {
    $$('[data-abrir-lista]').forEach(function (b) { b.addEventListener('click', function () { pintarLista(); if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); }); });
    $('.cerrar', dlg).addEventListener('click', function () { if (dlg.close) dlg.close(); else dlg.removeAttribute('open'); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg && dlg.close) dlg.close(); });
    $('#lista-vaciar', dlg).addEventListener('click', function () { lista = []; guardar(); pintarLista(); decir('Tu lista quedó vacía.'); $('.cerrar', dlg).focus(); });
    $('#lista-wa', dlg).addEventListener('click', function (e) { if (!lista.length) e.preventDefault(); });
  }

  /* ---------- Catálogo: filas ---------- */
  var cuenta = 0;
  function fila(it) {
    var qty = 1, uid = 'q-' + it.id + '-' + (cuenta++), m = meta(it), pc = precioCompleto(it);
    var wa = el('a', { 'class': 'btn compacto', href: waUrl(msgProducto(it, qty)), target: '_blank', rel: 'noopener noreferrer', 'aria-label': 'Cotizar ' + etiq(it) + ' por WhatsApp' }, [ico('wa'), 'Cotizar']);
    var c = cantidad(1, function (n) { qty = n; wa.setAttribute('href', waUrl(msgProducto(it, n))); }, etiq(it), uid);
    var add = el('button', { type: 'button', 'class': 'btn cont compacto', 'aria-label': 'Agregar ' + etiq(it) + ' a mi lista' }, [ico('mas'), 'Agregar']);
    add.addEventListener('click', function () {
      agregar(it.id, c.leer());
      var t = add.lastChild; t.nodeValue = 'Agregado'; clearTimeout(add._tm); add._tm = setTimeout(function () { t.nodeValue = 'Agregar'; }, 1600);
    });
    // Sin ningún precio publicado, el aviso va una sola vez arriba de la lista; con precios, cada fila sin precio lo indica.
    var precio = pc ? el('p', { 'class': 'precio' }, [pc.monto, el('small', { text: pc.detalle })])
                    : (HAY_PRECIOS ? el('p', { 'class': 'precio' }, ['Solicita precio', el('small', { text: 'Te lo damos por WhatsApp' })]) : null);
    var partes = [];
    if (it.foto) partes.push(el('div', { 'class': 'foto' }, [el('img', { src: it.foto, alt: it.nombre, loading: 'lazy' })]));
    partes.push(el('div', { 'class': 'info' }, [el('h3', { text: it.nombre }), m ? el('p', { 'class': 'meta', text: m }) : null, precio]));
    partes.push(c.nodo, el('div', { 'class': 'acc' }, [wa, add]));
    return el('article', { 'class': 'prod' + (it.foto ? ' con-foto' : ''), 'data-buscar': norm([it.nombre, it.marca, it.pres].join(' ')) }, partes);
  }
  function idSub(idx, linea, sub) { return 's' + idx + '-' + linea + '-' + slug(sub); }
  function pintarCatalogo(cont, idx) {
    var modo = cont.getAttribute('data-catalogo'), unica = modo !== 'todos';
    var lineas = unica ? LINEAS.filter(function (l) { return l.slug === modo; }) : LINEAS;
    cont._idx = idx; cont.textContent = '';
    lineas.forEach(function (ln) {
      var prods = ITEMS.filter(function (i) { return i.linea === ln.slug; });
      var cajaL = el('section', { 'class': 'grupo-linea', 'aria-label': ln.nombre });
      if (!unica) cajaL.appendChild(el('h2', { text: ln.nombre }));
      if (!prods.length) {
        cajaL.appendChild(el('div', { 'class': 'vacio' }, [
          el(unica ? 'h2' : 'h3', { text: 'Aún no publicamos productos de ' + ln.nombre.toLowerCase() }),
          el('p', { text: 'Escríbenos qué necesitas y te decimos si lo tenemos.' }),
          el('a', { 'class': 'btn', href: waUrl('Hola, quiero cotizar en ' + ln.nombre.toLowerCase() + ':'), target: '_blank', rel: 'noopener noreferrer' }, [ico('wa'), 'Cotizar por WhatsApp'])
        ]));
        cont.appendChild(cajaL); return;
      }
      var subs = []; prods.forEach(function (p) { if (subs.indexOf(p.sub) < 0) subs.push(p.sub); });
      subs.forEach(function (s) {
        var lst = prods.filter(function (p) { return p.sub === s; });
        cajaL.appendChild(el('div', { 'class': 'grupo-sub', id: idSub(idx, ln.slug, s), tabindex: '-1' }, [
          el(unica ? 'h2' : 'h3', {}, [s + ' ', el('span', { 'class': 'n', text: lst.length + (lst.length === 1 ? ' producto' : ' productos') })]),
          el('div', { 'class': 'filas' }, lst.map(fila))
        ]));
      });
      cont.appendChild(cajaL);
    });
    cont.appendChild(el('div', { 'class': 'vacio sin-resultados', hidden: '' }));
  }
  $$('[data-catalogo]').forEach(pintarCatalogo);

  /* Menú lateral del catálogo: líneas y subcategorías con su conteo */
  $$('[data-lateral]').forEach(function (box) {
    var cont = D.getElementById(box.getAttribute('data-para')); if (!cont) return;
    var modo = cont.getAttribute('data-catalogo'), nav = el('nav', { 'aria-label': 'Categorías del catálogo' });
    LINEAS.forEach(function (ln) {
      var prods = ITEMS.filter(function (i) { return i.linea === ln.slug; });
      var enPagina = modo === 'todos' || modo === ln.slug;
      nav.appendChild(el('p', { 'class': 't', text: ln.nombre }));
      var ul = el('ul'), subs = []; prods.forEach(function (p) { if (subs.indexOf(p.sub) < 0) subs.push(p.sub); });
      if (!subs.length) ul.appendChild(el('li', {}, [el('a', { href: waUrl('Hola, quiero cotizar en ' + ln.nombre.toLowerCase() + ':'), target: '_blank', rel: 'noopener noreferrer' }, ['Pregunta por WhatsApp'])]));
      subs.forEach(function (s) {
        var n = prods.filter(function (p) { return p.sub === s; }).length;
        var a = enPagina ? el('a', { href: '#' + idSub(cont._idx, ln.slug, s), 'data-ancla': idSub(cont._idx, ln.slug, s) }, [s, el('span', { text: String(n) })])
                         : el('a', { href: box.getAttribute('data-href-' + ln.slug) || '#' }, [s, el('span', { text: String(n) })]);
        ul.appendChild(el('li', {}, [a]));
      });
      nav.appendChild(ul);
    });
    box.appendChild(nav);
    if (window.matchMedia) {
      var mq = matchMedia('(min-width:980px)');
      var ajusta = function () { if (mq.matches) box.setAttribute('open', ''); };
      ajusta(); if (mq.addEventListener) mq.addEventListener('change', ajusta);
    }
  });

  /* Conteo por línea en la portada, con los datos vigentes */
  if (HAY_PRECIOS) $$('[data-nota]').forEach(function (e) { e.textContent = '«Cotizar» abre WhatsApp con tu producto listo; tú decides si lo envías. Si un producto no muestra precio, pídelo por WhatsApp.'; });
  $$('[data-cuenta]').forEach(function (e) {
    var n = ITEMS.filter(function (i) { return i.linea === e.getAttribute('data-cuenta'); }).length;
    e.textContent = n ? n + (n === 1 ? ' producto' : ' productos') : 'Sin productos publicados';
  });

  /* Índice de la portada, desde el mismo archivo de datos */
  $$('[data-indice]').forEach(function (cont) {
    var grupos = [];
    ITEMS.forEach(function (i) { var g = grupos.filter(function (x) { return x.l === i.linea && x.s === i.sub; })[0]; if (!g) { g = { l: i.linea, s: i.sub, p: [] }; grupos.push(g); } g.p.push(i); });
    if (!grupos.length) return;
    cont.textContent = '';
    grupos.forEach(function (g) {
      var href = cont.getAttribute('data-href-' + g.l) || '#';
      cont.appendChild(el('div', {}, [el('h3', { text: g.s }), el('ul', {}, g.p.map(function (p) { return el('li', {}, [el('a', { href: href }, [p.nombre + (p.pres ? ' · ' + p.pres : '')])]); }))]));
    });
  });

  /* ---------- Buscador ---------- */
  function filtrar(cont, q0) {
    var q = norm(q0).trim(), hay = 0;
    $$('.prod', cont).forEach(function (c) { var ok = !q || c.getAttribute('data-buscar').indexOf(q) >= 0; c.hidden = !ok; if (ok) hay++; });
    $$('.grupo-sub', cont).forEach(function (g) {
      var v = $$('.prod', g).filter(function (c) { return !c.hidden; }).length;
      g.hidden = v === 0; var n = $('.n', g); if (n) n.textContent = v + (v === 1 ? ' producto' : ' productos');
    });
    $$('.grupo-linea', cont).forEach(function (l) { l.hidden = !!q && !$$('.prod', l).some(function (c) { return !c.hidden; }); });
    var sr = $('.sin-resultados', cont);
    if (q && !hay) {
      var t = q0.trim();
      sr.hidden = false; sr.textContent = '';
      sr.appendChild(el('h3', { text: 'No encontramos «' + t + '»' }));
      sr.appendChild(el('p', { text: 'Puede que no lo tengamos publicado todavía. Pregúntanos por WhatsApp.' }));
      sr.appendChild(el('a', { 'class': 'btn', href: waUrl('Hola, busco: ' + t), target: '_blank', rel: 'noopener noreferrer' }, [ico('wa'), 'Preguntar por WhatsApp']));
    } else { sr.hidden = true; }
  }
  $$('input[data-en]').forEach(function (inp) {
    var cont = D.getElementById(inp.getAttribute('data-en')); if (!cont) return;
    inp.addEventListener('input', function () { filtrar(cont, inp.value); });
  });
  // Búsqueda desde el encabezado o el inicio: lleva al catálogo con el texto ya escrito
  var pendienteQ = '', limpiarQ = false;
  function aplicarQ() {
    var q = pendienteQ;
    if (!q) { try { q = new URLSearchParams(location.search).get('q') || ''; } catch (e) { q = ''; } }
    if (!q && !limpiarQ) return;
    var inp = $$('input[data-en]').filter(function (i) { var c = D.getElementById(i.getAttribute('data-en')); return c && c.getAttribute('data-catalogo') === 'todos' && i.offsetParent !== null; })[0];
    if (inp) { inp.value = q; inp.dispatchEvent(new Event('input')); pendienteQ = ''; limpiarQ = false; }
  }
  $$('form[data-busqueda]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = $('input[name="q"]', f).value.trim(), dest = f.getAttribute('data-destino') || '#';
      if (dest.charAt(0) === '#') { pendienteQ = q; limpiarQ = !q; cerrarMovil(); if (location.hash === dest) aplicarQ(); else location.hash = dest; }
      else location.href = dest + (q ? '?q=' + encodeURIComponent(q) : '');
    });
  });

  /* Lista escrita: el botón es un enlace de WhatsApp que se actualiza con lo que escribes; la persona decide si lo envía */
  $$('form[data-form-lista]').forEach(function (f) {
    var ta = $('textarea', f), enlace = $('a[data-lista-wa]', f);
    function armar() { if (enlace) enlace.setAttribute('href', waUrl(ta.value.trim() ? 'Hola, quiero cotizar esta lista:\n' + ta.value.trim() : 'Hola, quiero cotizar en Comercializadora Robles.')); }
    ta.addEventListener('input', armar); armar();
    f.addEventListener('submit', function (e) { e.preventDefault(); });
  });

  /* ---------- Anclas dentro de la página (también en el archivo único) ---------- */
  D.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-ancla]'); if (!a) return;
    var t = D.getElementById(a.getAttribute('data-ancla')); if (!t) return;
    e.preventDefault();
    t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    if (!t.hasAttribute('tabindex')) t.setAttribute('tabindex', '-1');
    t.focus({ preventScroll: true });
  });

  /* ---------- Menús ---------- */
  var btnMenu = $('#btn-menu'), movil = $('#movil');
  function pintaMenu(ab) {
    if (!btnMenu) return;
    btnMenu.setAttribute('aria-expanded', ab ? 'true' : 'false'); btnMenu.lastChild.nodeValue = ab ? 'Cerrar' : 'Menú';
    var u = btnMenu.querySelector('use'); if (u) u.setAttribute('href', ab ? '#i-x' : '#i-menu');
    D.documentElement.classList.toggle('menu-ab', ab);
  }
  function cerrarMovil() { if (movil) movil.classList.remove('abierto'); pintaMenu(false); }
  if (btnMenu && movil) {
    btnMenu.addEventListener('click', function () { pintaMenu(movil.classList.toggle('abierto')); });
    movil.addEventListener('click', function (e) { if (e.target.closest('a')) cerrarMovil(); });
  }
  function cerrarMenus() { $$('.menu-d.abierto').forEach(function (m) { m.classList.remove('abierto'); var b = $('button.sub', m); if (b) b.setAttribute('aria-expanded', 'false'); }); }
  $$('.menu-d').forEach(function (m) {
    var b = $('button.sub', m);
    b.addEventListener('click', function () { var ab = !m.classList.contains('abierto'); cerrarMenus(); if (ab) { m.classList.add('abierto'); b.setAttribute('aria-expanded', 'true'); } });
    m.addEventListener('focusout', function (e) { if (!m.contains(e.relatedTarget)) { m.classList.remove('abierto'); b.setAttribute('aria-expanded', 'false'); } });
  });
  D.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var ab = $('.menu-d.abierto'); if (ab) { var b = $('button.sub', ab); cerrarMenus(); if (b) b.focus(); }
    else if (movil && movil.classList.contains('abierto')) { cerrarMovil(); btnMenu.focus(); }
  });
  D.addEventListener('click', function (e) { if (!e.target.closest('.menu-d')) cerrarMenus(); });

  /* ---------- Archivo único: una "página" por ruta, sin recargar ---------- */
  if (window.ROBLES_PORTATIL) {
    var paginas = $$('.pagina');
    var ruta = function (inicial) {
      var h = (location.hash || '').replace(/^#\/?/, ''), r = h === 'inicio' ? '' : h.replace(/~/g, '/');
      if (r && r.slice(-1) !== '/') r += '/';
      var pg = paginas.filter(function (p) { return p.getAttribute('data-ruta') === r; })[0] || paginas.filter(function (p) { return p.getAttribute('data-ruta') === ''; })[0];
      paginas.forEach(function (p) { p.hidden = p !== pg; });
      D.title = pg.getAttribute('data-titulo');
      var actual = pg.getAttribute('data-ruta');
      $$('[data-nav]').forEach(function (a) {
        var n = a.getAttribute('data-nav'), on = n === '' ? actual === '' : actual.indexOf(n) === 0;
        if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
      });
      var tok = actual === '' ? '#inicio' : '#' + actual.replace(/\/$/, '').replace(/\//g, '~');
      $$('#movil a').forEach(function (a) { if (a.getAttribute('href') === tok) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
      cerrarMenus(); cerrarMovil();
      if (!inicial) { window.scrollTo(0, 0); var h1 = $('h1', pg); if (h1) { h1.setAttribute('tabindex', '-1'); h1.focus({ preventScroll: true }); } }
      aplicarQ();
    };
    window.addEventListener('hashchange', function () { ruta(false); });
    ruta(true);
  } else { aplicarQ(); }

  pintarLista();
})();
