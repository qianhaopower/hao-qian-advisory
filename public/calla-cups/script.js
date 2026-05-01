/* Calla & Cups — small JS for tabs + mobile menu. No deps. */
(function () {
  'use strict';

  /* ─── Mobile menu toggle ─── */
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('mobileMenu');

  function setMenu(open) {
    if (!toggle || !menu) return;
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      menu.hidden = false;
      // next frame so the transition runs
      requestAnimationFrame(function () { menu.classList.add('open'); });
      document.body.style.overflow = 'hidden';
    } else {
      menu.classList.remove('open');
      document.body.style.overflow = '';
      // wait for transition before hiding
      setTimeout(function () { if (!menu.classList.contains('open')) menu.hidden = true; }, 260);
    }
  }

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      setMenu(!open);
    });

    // close on link click
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });

    // close on Esc
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        toggle.focus();
      }
    });

    // close when resizing up to desktop
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 960) setMenu(false);
    });
  }

  /* ─── Menu tabs ─── */
  var tabs = document.querySelectorAll('.tab');
  var panels = document.querySelectorAll('.menu-panel');

  function activate(name) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-tab') === name;
      t.classList.toggle('active', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
    });
    panels.forEach(function (p) {
      var on = p.getAttribute('data-panel') === name;
      p.classList.toggle('active', on);
      p.hidden = !on;
    });
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      activate(t.getAttribute('data-tab'));
    });
    t.addEventListener('keydown', function (e) {
      var list = Array.prototype.slice.call(tabs);
      var i = list.indexOf(t);
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        var next = e.key === 'ArrowRight' ? (i + 1) % list.length : (i - 1 + list.length) % list.length;
        list[next].focus();
        activate(list[next].getAttribute('data-tab'));
      }
    });
  });

  /* ─── "Open now" status (rough hours: weekdays 7–15:30, weekends 8–15) ─── */
  (function () {
    var pillDot = document.querySelector('.pill-dot');
    var statusDot = document.querySelector('.status-dot');
    if (!pillDot && !statusDot) return;

    var now = new Date();
    var day = now.getDay(); // 0 Sun … 6 Sat
    var minutes = now.getHours() * 60 + now.getMinutes();
    var weekend = day === 0 || day === 6;
    var open = weekend ? 8 * 60 : 7 * 60;
    var close = weekend ? 15 * 60 : 15 * 60 + 30;
    var isOpen = minutes >= open && minutes < close;

    if (!isOpen) {
      [pillDot, statusDot].forEach(function (el) {
        if (!el) return;
        el.style.background = '#9ca3af';
        el.style.boxShadow = '0 0 0 3px rgba(156,163,175,0.2)';
      });
      var pill = document.querySelector('.pill');
      if (pill) pill.lastChild.textContent = ' Closed now';
      var cardH = document.querySelector('.card-h');
      if (cardH && cardH.textContent.indexOf('Open') !== -1) {
        cardH.innerHTML = '<span class="status-dot"></span> Closed · opens ' + (weekend ? '8:00' : '7:00');
        var sd = cardH.querySelector('.status-dot');
        if (sd) { sd.style.background = '#9ca3af'; sd.style.boxShadow = '0 0 0 3px rgba(156,163,175,0.2)'; }
      }
    }

    // highlight today's row
    var rows = document.querySelectorAll('.hours li');
    if (rows.length === 7) {
      // our list is Mon=0 … Sun=6; JS day Sun=0 … Sat=6
      var idx = (day + 6) % 7;
      rows.forEach(function (r) { r.classList.remove('today'); });
      rows[idx].classList.add('today');
    }
  })();

})();
