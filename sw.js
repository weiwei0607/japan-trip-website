// 日本神社之旅 — Service Worker (離線快取)
const CACHE = 'japan-trip-v23';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './favicon.png',
  './og-image.png',
  'https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE)
      .then(function (c) { return Promise.all(ASSETS.map(function (u) { return c.add(u).catch(function () {}); })); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys()
      .then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); })); })
      .then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  var isHTML = e.request.mode === 'navigate' || e.request.destination === 'document';
  if (isHTML) {
    // network-first：有網路拿最新，沒網路用快取
    e.respondWith(
      fetch(e.request).then(function (resp) {
        var copy = resp.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, copy); }).catch(function () {});
        return resp;
      }).catch(function () {
        return caches.match(e.request).then(function (r) { return r || caches.match('./index.html'); });
      })
    );
  } else {
    // 靜態資源：cache-first
    e.respondWith(
      caches.match(e.request).then(function (r) {
        return r || fetch(e.request).then(function (resp) {
          var copy = resp.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, copy); }).catch(function () {});
          return resp;
        }).catch(function () { return caches.match('./index.html'); });
      })
    );
  }
});
