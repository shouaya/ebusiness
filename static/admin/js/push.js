self.addEventListener("push", function(event) {
    console.log('[Service Worker] Push Received.');
    console.log(JSON.stringify(event.data));

    if (!(self.Notification && self.Notification.permission === 'granted')) {
        return;
    }

    var data = {};
    if (event.data) {
        data = event.data.json();
    }
    var title = data.title || 'Push title';
    var body = data.body || 'Push body!';
    var icon = '/static/logo.gif';

    var options = {
        body: body,
        icon: icon
    };

    event.waitUntil(self.registration.showNotification(title, options));
});
