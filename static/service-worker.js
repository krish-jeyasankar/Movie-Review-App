const CACHE_NAME = "codynn-cinema-cache-v1";

const urlsToCache = [
    "/",
    "/static/style.css",
    "/static/script.js",
    "/static/icons/icon-192.png",
    "/static/icons/icon-512.png",
    "/offline.html"
];

// Install service worker
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(urlsToCache);
        })
    );
});

// Fetch handler
self.addEventListener("fetch", event => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
