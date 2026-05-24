/* 初回描画を優先し、Supabase・設定・問題データを順次読み込む */
(function () {
  var SCRIPTS = [
    'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2',
    'site-config.js',
    'takken-master-data-core.js',
    'takken-master-data-past.js',
    'takken-data-glossary.js',
    'takken-data-original.js',
    'exam-site-data-ichimondou.js',
  ];

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var el = document.createElement('script');
      el.src = src;
      el.async = false;
      el.onload = function () { resolve(); };
      el.onerror = function () { reject(new Error('Failed to load: ' + src)); };
      document.head.appendChild(el);
    });
  }

  function loadAll() {
  return SCRIPTS.reduce(function (chain, src) {
    return chain.then(function () { return loadScript(src); });
  }, Promise.resolve());
  }

  window.__SITE_DATA_READY__ = loadAll().catch(function (err) {
    console.warn('Some site scripts failed to load', err);
  });
})();
