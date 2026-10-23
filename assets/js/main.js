/* Copyright (c) 2026 Ahmet Kaşif. MIT License (bkz. LICENSE).
   Küçük yardımcılar: tema düğmesi ve e-posta adreslerini tarayıcıda birleştirme.
   Bağımlılık yok (jQuery gerekmez). */
(function () {
  'use strict';

  /* 1) Koyu / açık tema */
  var root = document.documentElement;
  var button = document.getElementById('theme-toggle');

  function currentTheme() {
    return root.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
  }
  function reflect() {
    if (!button) return;
    var dark = currentTheme() === 'dark';
    button.setAttribute('aria-pressed', dark ? 'true' : 'false');
    var icon = button.querySelector('i');
    if (icon) icon.className = dark ? 'bi bi-sun' : 'bi bi-moon-stars';
  }
  if (button) {
    button.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-bs-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) { /* özel gezinme modu vb. */ }
      reflect();
    });
  }
  reflect();

  /* 2) Mobilde menüden bir bölüme dokununca menüyü kapat (başlığı örtmesin). */
  var menu = document.getElementById('nav-menu');
  if (menu) {
    menu.addEventListener('click', function (e) {
      var link = e.target.closest ? e.target.closest('a.nav-link') : null;
      if (link && menu.classList.contains('show') && window.bootstrap) {
        window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
      }
    });
  }

  /* 3) Menüde geçerli bölümü vurgula (kaydırmaya göre). Sayfa sonuna gelince son bölüm aktif olur. */
  var navLinks = [].slice.call(document.querySelectorAll('#site-nav a.nav-link[href^="#"]'));
  var navSections = navLinks.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var ticking = false;
  function updateNav() {
    ticking = false;
    var line = window.innerHeight * 0.3, current = 0;
    for (var i = 0; i < navSections.length; i++) {
      if (navSections[i] && navSections[i].getBoundingClientRect().top <= line) current = i;
    }
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) current = navLinks.length - 1;
    for (var j = 0; j < navLinks.length; j++) {
      var on = j === current;
      navLinks[j].classList.toggle('active', on);
      if (on) navLinks[j].setAttribute('aria-current', 'true'); else navLinks[j].removeAttribute('aria-current');
    }
  }
  function requestNavUpdate() { if (!ticking) { ticking = true; window.requestAnimationFrame(updateNav); } }
  window.addEventListener('scroll', requestNavUpdate, { passive: true });
  window.addEventListener('resize', requestNavUpdate);
  updateNav();

  /* 4) İpucu balonları (data-bs-toggle="tooltip"): fareyle üzerine gelince veya klavyeyle odaklanınca görünür. */
  if (window.bootstrap && window.bootstrap.Tooltip) {
    var tips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    for (var t = 0; t < tips.length; t++) new window.bootstrap.Tooltip(tips[t]);
  }

  /* 5) E-posta: data-user + data-domain → mailto bağlantısı.
        Adres HTML kaynağında bir arada bulunmadığı için basit botlar toplayamaz. */
  var mails = document.querySelectorAll('a.js-mail');
  for (var i = 0; i < mails.length; i++) {
    var a = mails[i];
    var addr = a.getAttribute('data-user') + '@' + a.getAttribute('data-domain');
    a.setAttribute('href', 'mailto:' + addr);
    if (a.classList.contains('js-mail-text')) a.textContent = addr;
  }
})();
