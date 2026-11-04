/* The first offline cache of Konfetti Deco lived at this address; the app is now in app/. This worker removes the old
   cache and itself, so nothing stale is served from here any more. */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const ks = await caches.keys(); await Promise.all(ks.filter((k) => k.startsWith('loulou-')).map((k) => caches.delete(k)));
    await self.registration.unregister();
    const cs = await self.clients.matchAll({ type: 'window' }); cs.forEach((c) => c.navigate(c.url));
  })());
});
self.addEventListener('fetch', () => {});
