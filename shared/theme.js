/* shared/theme.js — 亮/暗主题切换，所有页面共用 */
(function () {
  var KEY = 'docTheme';
  var html = document.documentElement;

  /* 立即应用（在 <head> 中执行，避免页面闪烁） */
  var saved = localStorage.getItem(KEY);
  if (!saved) {
    saved = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  html.setAttribute('data-theme', saved);

  /* DOMContentLoaded 后注入切换按钮 */
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.createElement('button');
    btn.className = 'theme-btn';
    btn.setAttribute('aria-label', '切换亮色/暗色主题');

    function sync() {
      var isDark = html.getAttribute('data-theme') === 'dark';
      btn.textContent = isDark ? '☀' : '◑';
      btn.title = isDark ? '切换亮色模式' : '切换暗色模式';
    }

    btn.addEventListener('click', function () {
      var next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem(KEY, next);
      sync();
    });

    sync();
    document.body.appendChild(btn);
  });
})();
