// Service worker: torna o app instalável e recebe as notificações do Sistema.
// Não guarda nada em cache, então toda atualização do app aparece na hora.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => {});

self.addEventListener('push', (e) => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { d = { title: '[SISTEMA]', body: e.data && e.data.text() }; }
  e.waitUntil(self.registration.showNotification(d.title || '[SISTEMA] Missão diária', {
    body: d.body || 'Chegou a hora do treino, jogador.',
    icon: '/app/icons/icon-192.png',
    badge: '/app/icons/icon-192.png',
    tag: d.tag || 'fh-treino',
    renotify: true,
    requireInteraction: true,
    vibrate: [200, 100, 200, 100, 300],
    data: { url: d.url || '/app/?tab=treinar' },
  }));
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || '/app/';
  e.waitUntil((async () => {
    const all = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    for (const c of all) { if (c.url.includes('/app/')) { await c.focus(); c.postMessage({ fh: 'tab', tab: 'treinar' }); return; } }
    await self.clients.openWindow(url);
  })());
});
