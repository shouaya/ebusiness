window.addEventListener("load", function() {
    var el = document.querySelector(".js-push-button");
    if (el == null) {
        return;
    }
    el.addEventListener("click", function() {
        subscribeUser();
    });

    if ('serviceWorker' in navigator && 'PushManager' in window) {
        // 指定したスクリプトをServiceWorkerとしてインストール
        navigator.serviceWorker.register("/push.js").then(function(swReg) {
            console.log('Service Worker is registered', swReg);

            swRegistration = swReg;
            swRegistration.pushManager.getSubscription()
            .then(function(subscription) {
                isSubscribed = !(subscription === null);
                if (isSubscribed) {
                    console.log('User IS subscribed.');
                    el.disabled = true;
                    renderSubscription(subscription);
                } else {
                    console.log('User is NOT subscribed.');
                }
            })
//            navigator.serviceWorker.ready.then(function(serviceWorkerRegistration) {
//            serviceWorkerRegistration.pushManager
//                .getSubscription()
//                .then(function(subscription) {
//                    // subscribeされてなければnullになる
//                    if (!subscription) {
//                      return;
//                    }
//
//                    el.disabled = true;
//                    renderSubscription(subscription);
//                });
//            });
        }).catch(function(error) {
            console.error('Service Worker Error', error);
        });
    } else {
        console.warn('Push messaging is not supported');
    }
}, false);

function subscribeUser() {
    swRegistration.pushManager.subscribe({userVisibleOnly: true})
    .then(function(subscription) {
        console.log('User is subscribed.');
        renderSubscription(subscription);
        isSubscribed = true;
    })
    .catch(function(err) {
        console.log('Failed to subscribe the user: ', err);
    });
//  navigator.serviceWorker.ready.then(function(serviceWorkerRegistration) {
//    serviceWorkerRegistration.pushManager.subscribe({userVisibleOnly:true}).then(function(subscription) {
//      var el = document.querySelector(".js-push-button");
//      el.disabled = true;
//      renderSubscription(subscription);
//    });
//  });
}

function renderSubscription(subscription) {
  document.querySelector('#subscription').innerHTML = subscription.endpoint.split("/").pop();
}

function updateSubscriptionOnServer(subscription) {

}