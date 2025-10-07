const CACHE_NAME = 'portfolio-cache-v2'; // Version du cache incrémentée
const urlsToCache = [
  '/',
  '/about/',
  '/services/',
  '/contact/'
];

// Étape d'installation : mise en cache des fichiers de l'application
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache ouvert');
        return cache.addAll(urlsToCache);
      })
  );
});

// Étape d'activation : nettoyage des anciens caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Étape de fetch : stratégie "Network Falling Back to Cache"
self.addEventListener('fetch', event => {
  // On ne met en cache que les requêtes GET
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        // Si la requête réseau réussit, on met à jour le cache
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME)
          .then(cache => {
            cache.put(event.request, responseToCache);
          });
        return networkResponse;
      })
      .catch(() => {
        // Si la requête réseau échoue (hors ligne), on cherche dans le cache
        return caches.match(event.request);
      })
  );
});
