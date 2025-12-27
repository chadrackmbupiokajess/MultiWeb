const CACHE_NAME = 'portfolio-cache-v3'; // Incrémentez la version à chaque modification du SW
const OFFLINE_URL = '{% url "offline" %}';
const DYNAMIC_CACHE_URLS = [
    // La liste des URLs à mettre en cache sera injectée ici par Django
    {% for url in cache_urls %}'{{ url }}',{% endfor %}
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[Service Worker] Installation - Mise en cache des ressources statiques et de la page hors ligne.');
                return cache.addAll(DYNAMIC_CACHE_URLS.concat([OFFLINE_URL]));
            })
            .catch(error => {
                console.error('[Service Worker] Erreur lors de la mise en cache initiale :', error);
            })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Activation - Suppression de l\'ancien cache :', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    // Assurez-vous que le Service Worker prend le contrôle immédiatement
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
    // Ne pas intercepter les requêtes non-GET ou les requêtes vers des origines externes
    if (event.request.method !== 'GET' || !event.request.url.startsWith(self.location.origin)) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            // Si la ressource est dans le cache, la servir immédiatement
            if (cachedResponse) {
                return cachedResponse;
            }

            // Sinon, tenter de récupérer la ressource via le réseau
            return fetch(event.request)
                .then(networkResponse => {
                    // Si la requête réseau réussit, mettre à jour le cache et servir la réponse
                    if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(event.request, responseToCache);
                        });
                    }
                    return networkResponse;
                })
                .catch(() => {
                    // Si le réseau échoue, et que la ressource n'était pas dans le cache,
                    // servir la page hors ligne pour les requêtes de navigation
                    if (event.request.mode === 'navigate') {
                        return caches.match(OFFLINE_URL);
                    }
                    // Pour les autres types de requêtes (images, scripts, etc.), on peut retourner une réponse vide ou une image de remplacement
                    return new Response(null, { status: 503, statusText: 'Service Unavailable' });
                });
        })
    );
});
