self.addEventListener("push", function(event) {
    console.log('[Service Worker] Push Received.');

    if (!(self.Notification && self.Notification.permission === 'granted')) {
        return;
    }

    const title = 'Push Codelab';
    const options = {
        body: 'Yay it works.',
        icon: '/static/logo.gif'
    };

    event.waitUntil(self.registration.showNotification(title, options));
});
