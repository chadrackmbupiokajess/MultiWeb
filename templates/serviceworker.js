const CACHE_NAME = 'portfolio-cache-v1';
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

// Étape de fetch : servir les fichiers depuis le cache ou le réseau
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Si la ressource est dans le cache, on la retourne
        if (response) {
          return response;
        }

        // Sinon, on la récupère sur le réseau
        return fetch(event.request);
      })
  );
});
