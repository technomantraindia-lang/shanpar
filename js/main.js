/* Shanpar website: shared behaviour. Each block only runs when its markup is on the page. */
(function () {
  'use strict';
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Header + mobile menu + mega menu ---------- */
  var header = $('.site-header');
  var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var toggle = $('#nav-toggle'), nav = $('#main-nav');
  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    toggle.classList.toggle('is-active', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
    document.documentElement.classList.toggle('menu-open', open);
  }
  if (toggle) {
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      setMenu(!nav.classList.contains('is-open'));
    });
  }

  var megaItem = $('.has-mega'), megaBtn = $('.mega-toggle');
  function setMega(open) {
    if (!megaItem) return;
    megaItem.classList.toggle('is-open', open);
    if (megaBtn) megaBtn.setAttribute('aria-expanded', String(open));
    header.classList.toggle('mega-open', open);
  }
  if (megaBtn) {
    megaBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      setMega(!megaItem.classList.contains('is-open'));
    });
  }
  document.addEventListener('click', function (e) {
    if (header && !header.contains(e.target)) {
      setMenu(false);
      setMega(false);
    }
  });
  if (megaItem) {
    megaItem.addEventListener('focusout', function (e) {
      if (!megaItem.contains(e.relatedTarget) && window.innerWidth > 900) setMega(false);
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (megaItem && megaItem.classList.contains('is-open') && window.innerWidth > 900) {
      setMega(false);
      if (megaBtn) megaBtn.focus();
    } else {
      setMenu(false);
    }
  });
  if (nav) {
    nav.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (a && !a.classList.contains('mega-toggle')) {
        setMenu(false);
        if (window.innerWidth <= 900) setMega(false);
      }
    });
  }

  /* ---------- Hero slider (wipe) ---------- */
  var media = $('.hero');
  if (media) {
    var slides = $$('.slide', media), dots = $$('.media-dots button', media);
    var countEl = $('.media-count', media), textEl = $('.media-text', media);
    var DURATION = 6000, current = 0, timer = null;
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    media.style.setProperty('--slide-ms', DURATION + 'ms');
    var show = function (i) {
      var next = (i + slides.length) % slides.length;
      if (next === current) return;
      slides.forEach(function (s) { s.classList.remove('is-prev'); });
      slides[current].classList.remove('is-active');
      slides[current].classList.add('is-prev');
      dots[current].setAttribute('aria-selected', 'false');
      current = next;
      var img = $('img', slides[current]);
      if (img.loading === 'lazy') img.loading = 'eager';
      slides[current].classList.add('is-active');
      dots[current].setAttribute('aria-selected', 'true');
      countEl.textContent = pad(current + 1) + ' / ' + pad(slides.length);
      textEl.textContent = slides[current].getAttribute('data-caption');
      var bar = $('i', dots[current]);
      bar.style.display = 'none'; void bar.offsetWidth; bar.style.display = '';
    };
    var start = function () {
      if (reduceMotion) return;
      clearInterval(timer);
      timer = setInterval(function () { show(current + 1); }, DURATION);
    };
    dots.forEach(function (d, i) { d.addEventListener('click', function () { show(i); start(); }); });
    document.addEventListener('visibilitychange', function () { if (document.hidden) clearInterval(timer); else start(); });
    var x0 = null;
    media.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    media.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) { show(current + (dx < 0 ? 1 : -1)); start(); }
      x0 = null;
    });
    window.addEventListener('load', function () {
      slides.forEach(function (s) { var im = $('img', s); if (im.loading === 'lazy') im.loading = 'eager'; });
    });
    start();
  }

  /* ---------- Scroll reveal animations (Trigger on Scroll Down & Scroll Up) ---------- */
  if (!reduceMotion && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('js-ready');
    var reveals = $$('[data-reveal]');
    if (reveals.length) {
      var revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add('is-revealed');
          } else {
            // When an element has completely scrolled out of the viewport
            // (either past the top or below the bottom), remove is-revealed
            // so when scrolling back up or down it smoothly animates into view again!
            var rect = en.boundingClientRect;
            if (rect.top > window.innerHeight || rect.bottom < 0) {
              en.target.classList.remove('is-revealed');
            }
          }
        });
      }, {
        threshold: 0.08,
        rootMargin: '0px 0px -30px 0px'
      });

      reveals.forEach(function (el) {
        revealObserver.observe(el);
      });
    }
  }

  /* ---------- Count-up numbers (Re-triggers on scroll into view) ---------- */
  var counters = $$('[data-count]');
  if (counters.length && !reduceMotion && 'IntersectionObserver' in window) {
    var countObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var el = en.target, end = +el.getAttribute('data-count');
        if (en.isIntersecting) {
          var t0 = null;
          var step = function (t) {
            if (!t0) t0 = t;
            var p = Math.min((t - t0) / 1200, 1);
            el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
            if (p < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
        } else {
          el.textContent = '0';
        }
      });
    }, { threshold: 0.25 });
    counters.forEach(function (c) { countObserver.observe(c); });
  }

  /* ---------- Periodic table (home) ---------- */
  var table = $('#ptable');
  if (table && window.SHANPAR) {
    var DATA = window.SHANPAR.elements;
    var ROWS = [
      'H,,,,,,,,,,,,,,,,,He', 'Li,Be,,,,,,,,,,,B,C,N,O,F,Ne', 'Na,Mg,,,,,,,,,,,Al,Si,P,S,Cl,Ar',
      'K,Ca,Sc,Ti,V,Cr,Mn,Fe,Co,Ni,Cu,Zn,Ga,Ge,As,Se,Br,Kr', 'Rb,Sr,Y,Zr,Nb,Mo,Tc,Ru,Rh,Pd,Ag,Cd,In,Sn,Sb,Te,I,Xe',
      'Cs,Ba,La,Hf,Ta,W,Re,Os,Ir,Pt,Au,Hg,Tl,Pb,Bi,Po,At,Rn'
    ];
    var Z = {};
    'H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La'
      .split(' ').forEach(function (s, i) { Z[s] = i + 1; });
    'Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn'.split(' ').forEach(function (s, i) { Z[s] = 72 + i; });
    var level = function (n) { return n >= 15 ? 5 : n >= 8 ? 4 : n >= 4 ? 3 : n >= 2 ? 2 : 1; };
    var panel = $('#ptable-panel'), buttons = {}, frag = document.createDocumentFragment();
    var canHover = window.matchMedia('(hover: hover)').matches;

    ROWS.forEach(function (row, r) {
      row.split(',').forEach(function (sym, c) {
        if (!sym) return;
        var d = DATA[sym];
        var el = document.createElement(d ? 'button' : 'div');
        el.className = 'el' + (d ? ' lv' + level(d.products.length) : '');
        el.style.setProperty('--c', c + 1);
        el.style.setProperty('--r', r + 1);
        el.innerHTML = '<small>' + Z[sym] + '</small>' + sym + (d ? '<b>' + d.products.length + '</b>' : '');
        if (d) {
          el.type = 'button';
          el.setAttribute('aria-label', d.name + ', ' + d.products.length + ' products');
          el.addEventListener('click', function () { select(sym); });
          el.addEventListener('focus', function () { select(sym); });
          if (canHover) el.addEventListener('mouseenter', function () { select(sym); });
          buttons[sym] = el;
        } else {
          el.setAttribute('aria-hidden', 'true');
        }
        frag.appendChild(el);
      });
    });
    table.insertBefore(frag, panel);

    var selected = null;
    var select = function (sym) {
      if (sym === selected) return;
      if (selected) buttons[selected].classList.remove('is-selected');
      selected = sym;
      buttons[sym].classList.add('is-selected');
      var d = DATA[sym], n = d.products.length, lv = level(n);
      panel.innerHTML =
        '<div class="pp-tile lv' + lv + (lv < 4 ? ' light' : '') + '">' +
          '<span class="pp-z">' + d.z + '</span><span class="pp-sym">' + sym + '</span><span class="pp-name">' + d.name + '</span>' +
        '</div><div class="pp-body"><h3>' + d.name + ' products</h3>' +
        '<p class="pp-meta">' + n + (n === 1 ? ' product' : ' products') + ' · Atomic number ' + d.z + '</p>' +
        '<ul class="pp-list">' + d.products.map(function (p) { return '<li>' + p + '</li>'; }).join('') + '</ul></div>';
    };
    select('Ca');
  }

  /* ---------- Catalogue filters (products page) ---------- */
  var filters = $('#filters');
  if (filters) {
    var rows = $$('.products-table tbody tr');
    var q = $('#f-q'), fam = $('#f-fam'), onlyNew = $('#f-new');
    var count = $('#f-count'), empty = $('#f-empty');
    var params = new URLSearchParams(location.search);
    if (params.get('grade')) { var r0 = filters.querySelector('input[name="grade"][value="' + params.get('grade') + '"]'); if (r0) r0.checked = true; }
    if (params.get('family')) fam.value = params.get('family');
    if (params.get('q')) q.value = params.get('q');
    if (params.get('new')) onlyNew.checked = true;

    var apply = function () {
      var text = q.value.trim().toLowerCase();
      var grade = (filters.querySelector('input[name="grade"]:checked') || {}).value || '';
      var f = fam.value, nw = onlyNew.checked, shown = 0;
      rows.forEach(function (tr) {
        var ok = (!text || tr.dataset.name.indexOf(text) !== -1) &&
                 (!grade || tr.dataset.grades.split(' ').indexOf(grade) !== -1) &&
                 (!f || tr.dataset.family === f) &&
                 (!nw || tr.dataset.new === '1');
        tr.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = 'Showing ' + shown + ' of ' + rows.length + ' products';
      empty.hidden = shown !== 0;
    };
    filters.addEventListener('input', apply);
    filters.addEventListener('change', apply);
    apply();
    if (params.toString()) { var cat = $('#catalogue'); if (cat) cat.scrollIntoView(); }
  }

  /* ---------- Staff chart tooltip (about page) ---------- */
  var chart = $('#staff-chart');
  if (chart) {
    var tip = $('#sc-tip');
    $$('.sc-bars li', chart).forEach(function (li) {
      li.addEventListener('mousemove', function (e) {
        var box = chart.getBoundingClientRect();
        tip.textContent = li.getAttribute('data-tip');
        tip.style.left = Math.min(Math.max(e.clientX - box.left, 120), box.width - 120) + 'px';
        tip.style.top = (e.clientY - box.top) + 'px';
        tip.hidden = false;
      });
      li.addEventListener('mouseleave', function () { tip.hidden = true; });
    });
  }

  /* ---------- Enquiry form (contact page) ----------
     There is no server yet, so the form opens the visitor's email app with the
     enquiry filled in. Swap this for a POST to your form handler when one exists. */
  var form = $('#enquiry-form');
  if (form) {
    var p = new URLSearchParams(location.search);
    if (p.get('product')) $('#e-product').value = p.get('product');
    var err = $('#form-error');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var missing = [];
      $$('[required]', form).forEach(function (f) {
        var bad = !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
        f.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad) missing.push(form.querySelector('label[for="' + f.id + '"]').textContent.toLowerCase());
      });
      if (missing.length) {
        err.textContent = 'Please add your ' + missing.join(', ') + ' so our team can reply.';
        err.hidden = false;
        return;
      }
      err.hidden = true;
      var v = function (id) { var el = $('#' + id); return el ? el.value.trim() : ''; };
      var lines = [
        'Product: ' + v('e-product'),
        'Grade: ' + (v('e-grade') || 'Not sure'),
        'Quantity: ' + v('e-qty'),
        'Name: ' + v('e-name'),
        'Email: ' + v('e-email'),
        'Phone: ' + v('e-phone'),
        '',
        v('e-msg')
      ].filter(function (l) { return l.length > 0; });
      window.location.href = 'mailto:info@shanpar.com?subject=' + encodeURIComponent('Enquiry: ' + v('e-product')) +
        '&body=' + encodeURIComponent(lines.join('\n'));
    });
  }
  /* ---------- Key personnel filter (About page) ---------- */
  var pFilter = $('#people-filter');
  if (pFilter) {
    var pBtns = $$('.pf-btn', pFilter);
    var pCards = $$('.people li');
    pBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var filter = btn.getAttribute('data-filter');
        pBtns.forEach(function (b) {
          b.classList.remove('is-active');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('is-active');
        btn.setAttribute('aria-selected', 'true');
        pCards.forEach(function (card) {
          var cat = card.getAttribute('data-cat') || '';
          var match = filter === 'all' || cat.indexOf(filter) !== -1;
          if (match) {
            card.hidden = false;
            card.style.display = '';
            card.classList.add('is-revealed');
          } else {
            card.hidden = true;
            card.style.display = 'none';
          }
        });
      });
    });
  }

  /* ---------- RFQ interactive chips & pills (Contact page) ---------- */
  var enquiryForm = $('#enquiry-form');
  if (enquiryForm) {
    // Grade pill selection
    var gradePills = $$('.grade-pill', enquiryForm);
    var gradeSelect = $('#e-grade');
    if (gradePills.length && gradeSelect) {
      gradePills.forEach(function (pill) {
        pill.addEventListener('click', function () {
          gradePills.forEach(function (p) { p.classList.remove('is-selected'); });
          pill.classList.add('is-selected');
          var val = pill.getAttribute('data-val') || '';
          gradeSelect.value = val;
        });
      });
      if (gradeSelect) {
        gradeSelect.addEventListener('change', function () {
          gradePills.forEach(function (p) {
            p.classList.toggle('is-selected', p.getAttribute('data-val') === gradeSelect.value);
          });
        });
      }
    }

    // Quick quantity chips
    var qtyChips = $$('.qty-chip', enquiryForm);
    var qtyInput = $('#e-qty');
    if (qtyChips.length && qtyInput) {
      qtyChips.forEach(function (chip) {
        chip.addEventListener('click', function () {
          qtyChips.forEach(function (c) { c.classList.remove('is-selected'); });
          chip.classList.add('is-selected');
          qtyInput.value = chip.getAttribute('data-val') || chip.textContent.trim();
        });
      });
    }

    // Document request checkboxes to auto-populate message
    var docChecks = $$('.doc-check input', enquiryForm);
    var msgArea = $('#e-msg');
    if (docChecks.length && msgArea) {
      var updateDocs = function () {
        var selectedDocs = [];
        docChecks.forEach(function (chk) {
          if (chk.checked) selectedDocs.push(chk.value);
        });
        var currentText = msgArea.value.replace(/\n*Requested documents:[^\n]+(\n|$)/g, '').trim();
        if (selectedDocs.length) {
          msgArea.value = (currentText ? currentText + '\n\n' : '') + 'Requested documents: ' + selectedDocs.join(', ');
        } else {
          msgArea.value = currentText;
        }
      };
      docChecks.forEach(function (chk) { chk.addEventListener('change', updateDocs); });
    }
  }

  /* ---------- Certificate Modal Lightbox (Quality page) ---------- */
  var certModal = $('#cert-modal');
  if (certModal) {
    var modalImg = $('#cert-modal-img');
    var modalTitle = $('#cert-modal-title');
    var modalMeta = $('#cert-modal-meta');
    var modalDl = $('#cert-modal-download');
    var closeBtn = $('#cert-modal-close');

    function openCert(src, title, meta) {
      if (!src) return;
      modalImg.src = src;
      modalImg.alt = title || 'Certificate';
      modalTitle.textContent = title || 'Certificate';
      modalMeta.textContent = meta || '';
      if (modalDl) modalDl.href = src;
      certModal.hidden = false;
      document.body.style.overflow = 'hidden';
      if (closeBtn) closeBtn.focus();
    }

    function closeCert() {
      certModal.hidden = true;
      document.body.style.overflow = '';
    }

    $$('[data-modal="cert"]').forEach(function (trigger) {
      function handleTrigger(e) {
        e.preventDefault();
        var src = trigger.getAttribute('data-img');
        var title = trigger.getAttribute('data-title');
        var meta = trigger.getAttribute('data-meta');
        openCert(src, title, meta);
      }
      trigger.addEventListener('click', handleTrigger);
      trigger.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          handleTrigger(e);
        }
      });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeCert);
    certModal.addEventListener('click', function (e) {
      if (e.target === certModal) closeCert();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !certModal.hidden) closeCert();
    });
  }
})();
