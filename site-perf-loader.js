/* 初回描画は core のみ。過去問・実践演習等は必要な画面で遅延読み込み */
(function () {
  var CDN = (window.__SITE_CDN_BASE__ || '').replace(/\/$/, '');

  function assetUrl(path) {
    return CDN ? CDN + '/' + path : path;
  }

  var BUNDLES = {
    config: ['site-config.js'],
    core: ['takken-master-data-core.js'],
    past: [assetUrl('takken-master-data-past.js')],
    orig: [assetUrl('takken-data-original.js')],
    glossary: [assetUrl('takken-data-glossary.js')],
    supabase: ['https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2'],
  };

  var loadedScripts = Object.create(null);
  var loadedBundles = Object.create(null);
  var loadingBundles = Object.create(null);

  function loadScript(src, fallback) {
    if (loadedScripts[src]) return loadedScripts[src];
    loadedScripts[src] = new Promise(function (resolve, reject) {
      var el = document.createElement('script');
      el.src = src;
      el.async = true;
      el.onload = function () { resolve(); };
      el.onerror = function () {
        if (fallback && fallback !== src) {
          delete loadedScripts[src];
          loadScript(fallback).then(resolve).catch(reject);
          return;
        }
        reject(new Error('Failed to load: ' + src));
      };
      document.head.appendChild(el);
    });
    return loadedScripts[src];
  }

  function loadScriptWithFallback(path) {
    var primary = assetUrl(path);
    var local = path;
    return primary === local ? loadScript(primary) : loadScript(primary, local);
  }

  function loadBundle(name) {
    if (loadedBundles[name]) return Promise.resolve();
    if (loadingBundles[name]) return loadingBundles[name];
    var files = BUNDLES[name];
    if (!files || !files.length) return Promise.resolve();
    loadingBundles[name] = Promise.all(files.map(function (src) {
      if (CDN && src.indexOf(CDN + '/') === 0) {
        return loadScriptWithFallback(src.slice(CDN.length + 1));
      }
      return loadScript(src);
    }))
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
