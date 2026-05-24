/* 初回描画は core のみ。過去問・実践演習等は必要な画面で遅延読み込み */
(function () {
  var BUNDLES = {
    config: ['site-config.js'],
    core: ['takken-master-data-core.js'],
    past: ['takken-master-data-past.js'],
    orig: ['takken-data-original.js'],
    glossary: ['takken-data-glossary.js'],
    supabase: ['https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2'],
  };

  var loadedScripts = Object.create(null);
  var loadedBundles = Object.create(null);
  var loadingBundles = Object.create(null);

  function loadScript(src) {
    if (loadedScripts[src]) return loadedScripts[src];
    loadedScripts[src] = new Promise(function (resolve, reject) {
      var el = document.createElement('script');
      el.src = src;
      el.async = true;
      el.onload = function () { resolve(); };
      el.onerror = function () { reject(new Error('Failed to load: ' + src)); };
      document.head.appendChild(el);
    });
    return loadedScripts[src];
  }

  function loadBundle(name) {
    if (loadedBundles[name]) return Promise.resolve();
    if (loadingBundles[name]) return loadingBundles[name];
    var files = BUNDLES[name];
    if (!files || !files.length) return Promise.resolve();
    loadingBundles[name] = Promise.all(files.map(loadScript))
      .then(function () { loadedBundles[name] = true; })
      .catch(function (err) {
        delete loadingBundles[name];
        throw err;
      });
    return loadingBundles[name];
  }

  window.__SITE_LOAD_BUNDLE__ = loadBundle;
  window.__SITE_LOAD_BUNDLES__ = function (names) {
    var uniq = [];
    (names || []).forEach(function (n) {
      if (n && uniq.indexOf(n) === -1) uniq.push(n);
    });
    return Promise.all(uniq.map(loadBundle));
  };

  window.__SITE_DATA_READY__ = Promise.all([
    loadBundle('config'),
    loadBundle('core'),
  ]).catch(function (err) {
    console.warn('Core site scripts failed to load', err);
  });
})();
