// Service worker mínimo: torna o app instalável. Não guarda nada em cache,
// então toda atualização do app aparece na hora.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => {});
