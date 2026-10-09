/* Comercializadora Robles · comportamiento del sitio. Sin dependencias.
   Los datos del catálogo vienen de assets/js/catalogo.js (window.ROBLES_CATALOGO). */
(function () {
  'use strict';
  var D = document, H = D.documentElement, NS = 'http://www.w3.org/2000/svg';
  H.classList.add('js');
  var WA = '523119104468';
  // Las fotos de producto con ruta relativa se resuelven desde la carpeta del sitio (la del script)
  var BASE = (function () { var s = D.currentScript; return s && s.src ? s.src.replace(/assets\/js\/site\.js.*$/, '') : ''; })();
  function fotoSrc(f) { return /^(data:|https?:|\/)/.test(f) ? f : BASE + f; }
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
  function pico(k) {
    var s = D.createElementNS(NS, 'svg'); s.setAttribute('class', 'ico'); s.setAttribute('aria-hidden', 'true');
    var u = D.createElementNS(NS, 'use'); u.setAttribute('href', '#p-' + k); s.appendChild(u); return s;
  }
  function tile(k) { return el('span', { 'class': 'ico-prod', 'aria-hidden': 'true' }, [pico(k)]); }
  var SUBICO = [[/cemento/, 'saco'], [/varilla/, 'varilla'], [/llaves, pinzas/, 'llave'], [/herramienta/, 'herramienta'], [/medicion/, 'regla'], [/brocas/, 'brocas'],
    [/pintura/, 'rodillo'], [/tubos/, 'tubo'], [/sanitarios/, 'taza'], [/interruptores/, 'rayo'], [/contactos/, 'enchufe'], [/tornill/, 'tuerca'],
    [/cerraj/, 'candado'], [/seguridad/, 'casco'], [/papel/, 'papel'], [/cloro/, 'gotas'], [/jabon/, 'jabon'], [/utensilios/, 'escoba'], [/insectic/, 'aerosol']];
  function iconoSub(nombre) { var n = norm(nombre); for (var i = 0; i < SUBICO.length; i++) if (SUBICO[i][0].test(n)) return SUBICO[i][1]; return 'caja'; }
  function corto(n) { var c = String(n).split(',')[0]; return c.length > 34 ? c.slice(0, 33).replace(/\s+\S*$/, '') + '…' : c; }
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
    if (it.unidad && !/^pieza$/i.test(it.unidad) && !precioCompleto(it)) p.push('por ' + it.unidad);
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
  /* Copiar texto al portapapeles; si el navegador lo niega, se avisa en lugar de fingir que funcionó */
  function copiar(txt, btn) {
    function fin(ok) {
      decir(ok ? 'Mensaje copiado.' : 'No se pudo copiar. Selecciona el texto y cópialo.');
      var n = btn.lastChild; if (!n || n.nodeType !== 3) return;
      var o = btn.getAttribute('data-txt') || n.nodeValue; btn.setAttribute('data-txt', o);
      n.nodeValue = ok ? 'Copiado' : 'No se pudo copiar'; clearTimeout(btn._tm); btn._tm = setTimeout(function () { n.nodeValue = o; }, 1800);
    }
    function viejo() {
      var ta = D.createElement('textarea'); ta.value = txt; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
      D.body.appendChild(ta); ta.select(); var ok = false; try { ok = D.execCommand('copy'); } catch (e) { ok = false; } D.body.removeChild(ta); fin(ok);
    }
    try { if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(txt).then(function () { fin(true); }, viejo); return; } } catch (e) { /* cae al método anterior */ }
    viejo();
  }
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
    borrar.hidden = lista.length === 0; var cop = $('#lista-copiar', dlg); if (cop) cop.hidden = lista.length === 0;
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
    var cop = $('#lista-copiar', dlg); if (cop) cop.addEventListener('click', function () { copiar(msgLista(), cop); });
  }

  /* ---------- Catálogo: filas ---------- */
  var cuenta = 0;
  function fila(it, nivel) {
    var uid = 'q-' + it.id + '-' + (cuenta++), m = meta(it), pc = precioCompleto(it);
    var c = cantidad(1, function () {}, etiq(it), uid);
    var add = el('button', { type: 'button', 'class': 'btn cont compacto', 'aria-label': 'Agregar ' + etiq(it) + ' a mi lista' }, [ico('mas'), 'Agregar']);
    add.addEventListener('click', function () {
      agregar(it.id, c.leer());
      var t = add.lastChild; t.nodeValue = 'Agregado'; clearTimeout(add._tm); add._tm = setTimeout(function () { t.nodeValue = 'Agregar'; }, 1600);
    });
    // Sin ningún precio publicado, el aviso va una sola vez arriba de la lista; con precios, cada fila sin precio lo indica.
    var precio = pc ? el('p', { 'class': 'precio' }, [pc.monto, el('small', { text: pc.detalle })])
                    : (HAY_PRECIOS ? el('p', { 'class': 'precio' }, ['Solicita precio', el('small', { text: 'Te lo damos por WhatsApp' })]) : null);
    var partes = [];
    partes.push(it.foto ? el('div', { 'class': 'foto' }, [el('img', { src: fotoSrc(it.foto), alt: it.nombre, loading: 'lazy' })]) : tile(it.icono || 'caja'));
    partes.push(el('div', { 'class': 'info' }, [el(nivel || 'h3', { text: it.nombre }), m ? el('p', { 'class': 'meta', text: m }) : null, precio]));
    partes.push(c.nodo, el('div', { 'class': 'acc' }, [add]));
    return el('article', { 'class': 'prod' + (it.foto ? ' con-foto' : ''), 'data-buscar': norm([it.nombre, it.marca, it.pres].join(' ')) }, partes);
  }
  function idSub(modo, linea, sub) { return (modo === 'todos' ? 't-' : 's-') + linea + '-' + slug(sub); }
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
          el('a', { 'class': 'btn', href: waUrl('Hola, quiero cotizar en ' + ln.nombre.toLowerCase() + ':'), target: '_blank', rel: 'noopener noreferrer' }, [ico('wa'), 'Preguntar por WhatsApp'])
        ]));
        cont.appendChild(cajaL); return;
      }
      var subs = []; prods.forEach(function (p) { if (subs.indexOf(p.sub) < 0) subs.push(p.sub); });
      subs.forEach(function (s) {
        var lst = prods.filter(function (p) { return p.sub === s; });
        cajaL.appendChild(el('div', { 'class': 'grupo-sub', id: idSub(modo, ln.slug, s), tabindex: '-1' }, [
          el(unica ? 'h2' : 'h3', {}, [s + ' ', el('span', { 'class': 'n', text: lst.length + (lst.length === 1 ? ' producto' : ' productos') })]),
          el('div', { 'class': 'filas' }, lst.map(function (p) { return fila(p, unica ? 'h3' : 'h4'); }))
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
        var a = enPagina ? el('a', { href: '#' + idSub(modo, ln.slug, s), 'data-ancla': idSub(modo, ln.slug, s) }, [s, el('span', { text: String(n) })])
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
  if (HAY_PRECIOS) $$('[data-nota]').forEach(function (e) { e.textContent = 'Agrega productos a tu lista y envíala por WhatsApp. Si un producto no muestra precio, pídelo en el chat.'; });
  $$('[data-cuenta]').forEach(function (e) {
    var n = ITEMS.filter(function (i) { return i.linea === e.getAttribute('data-cuenta'); }).length;
    e.textContent = n ? n + (n === 1 ? ' producto' : ' productos') : 'Sin productos publicados';
  });

  /* ---------- Portada: categorías y cinta de productos, desde el mismo archivo de datos ---------- */
  var PORTATIL = !!window.ROBLES_PORTATIL, pendienteSub = '';
  $$('[data-categorias]').forEach(function (cont) {
    var hay = false; cont.textContent = '';
    LINEAS.forEach(function (ln) {
      var prods = ITEMS.filter(function (i) { return i.linea === ln.slug; });
      var base = cont.getAttribute('data-href-' + ln.slug) || '#';
      var grupo = el('section', { 'class': 'cat-grupo', 'aria-label': ln.nombre });
      if (!prods.length) {
        grupo.appendChild(el('h3', {}, [ln.nombre]));
        grupo.appendChild(el('p', { 'class': 'cat-vacia', text: 'Todavía no hay productos publicados en esta línea.' }));
        cont.appendChild(grupo); return;
      }
      hay = true;
      var subs = []; prods.forEach(function (p) { var g = subs.filter(function (x) { return x.n === p.sub; })[0]; if (!g) { g = { n: p.sub, c: 0 }; subs.push(g); } g.c++; });
      grupo.appendChild(el('h3', {}, [ln.nombre + ' ', el('span', { 'class': 'n', text: prods.length + (prods.length === 1 ? ' producto' : ' productos') })]));
      grupo.appendChild(el('ul', { 'class': 'cat-grid' }, subs.map(function (g) {
        var id = idSub('linea', ln.slug, g.n);
        var a = el('a', { 'class': 'cat-tile', href: PORTATIL ? base : base + '#' + id, 'data-sub-id': id }, [tile(iconoSub(g.n)), el('span', {}, [el('b', { text: g.n }), el('small', { text: g.c + (g.c === 1 ? ' producto' : ' productos') })])]);
        return el('li', {}, [a]);
      })));
      cont.appendChild(grupo);
    });
    if (!hay) cont.appendChild(el('p', { 'class': 'cat-vacia', text: 'El catálogo se está actualizando.' }));
  });
  $$('[data-cinta]').forEach(function (sec) {
    var ul = $('.pista', sec); if (!ul) return;
    var ids = (sec.getAttribute('data-ids') || '').split(',').filter(Boolean);
    var elegidos = ids.map(function (id) { return BYID[id]; }).filter(Boolean);
    if (!elegidos.length) { sec.hidden = true; return; }
    var base = sec.getAttribute('data-href-catalogo') || '#';
    function copia(oculta) {
      return elegidos.map(function (it) {
        var a = el('a', { 'class': 'mini', href: PORTATIL ? base : base + '?q=' + encodeURIComponent(it.nombre), 'data-q': it.nombre }, [tile(it.icono || 'caja'), el('span', {}, [el('b', { text: corto(it.nombre) }), el('small', { text: it.sub })])]);
        var li = el('li', {}, [a]);
        if (oculta) { li.setAttribute('aria-hidden', 'true'); a.setAttribute('tabindex', '-1'); }
        return li;
      });
    }
    copia(false).concat(copia(true)).forEach(function (li) { ul.appendChild(li); });
    ul.style.setProperty('--dur', Math.max(40, elegidos.length * 5) + 's');
    var bp = $('.btn-pausa', sec);
    if (bp) bp.addEventListener('click', function () {
      var p = sec.classList.toggle('pausada'); bp.setAttribute('aria-pressed', p ? 'true' : 'false');
      bp.lastChild.nodeValue = p ? 'Reanudar' : 'Pausar'; var u = bp.querySelector('use'); if (u) u.setAttribute('href', p ? '#i-play' : '#i-pausa');
    });
  });
  // Enlaces que llevan al catálogo con un texto o a una subcategoría concreta
  D.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-q],a[data-sub-id]'); if (!a) return;
    if (a.hasAttribute('data-q') && PORTATIL) { pendienteQ = a.getAttribute('data-q'); limpiarQ = false; }
    if (a.hasAttribute('data-sub-id') && PORTATIL) {
      pendienteSub = a.getAttribute('data-sub-id');
      // ya estás en esa página: el hash no cambia, así que se baja directo a la sección
      if (a.getAttribute('href') === location.hash) { e.preventDefault(); irASub(); }
    }
  });
  function irASub() {
    var id = pendienteSub || (!PORTATIL && location.hash.length > 1 ? location.hash.slice(1) : ''); pendienteSub = '';
    var t = id && D.getElementById(id); if (t) { t.scrollIntoView({ behavior: 'instant', block: 'start' }); }
  }

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
    var cb = $('[data-copiar-lista]', f);
    if (cb) cb.addEventListener('click', function () { copiar(ta.value.trim() ? 'Hola, quiero cotizar esta lista:\n' + ta.value.trim() : 'Hola, quiero cotizar en Comercializadora Robles.', cb); });
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
      aplicarQ(); irASub();
    };
    window.addEventListener('hashchange', function () { ruta(false); });
    ruta(true);
  } else { aplicarQ(); irASub(); }

  pintarLista();
})();
