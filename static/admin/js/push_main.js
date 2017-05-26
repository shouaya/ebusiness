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
        }).catch(function(error) {
            console.error('Service Worker Error', error);
        });
    } else {
        console.warn('Push messaging is not supported');
    }
}, false);

function subscribeUser() {
//    var applicationServerPublicKey = "BAvstILXqJgYl_9_KTNwExG7Z9KcuEfXiBvSxKYqQnvFW9fNy2eFh5nqsNW0oPYFGg9c4sNqBVu5OkEN5YiWMWs";
//    applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
    swRegistration.pushManager.subscribe({userVisibleOnly: true})
    .then(function(subscription) {
        console.log('User is subscribed.');
        renderSubscription(subscription);
        isSubscribed = true;
    })
    .catch(function(err) {
        console.log('Failed to subscribe the user: ', err);
    });
}

function renderSubscription(subscription) {
    reg_id = subscription.endpoint.split("/").pop();
    console.log(reg_id);

    var rawKey = subscription.getKey ? subscription.getKey('p256dh') : '';
    var key = rawKey ? Base64EncodeUrl(btoa(String.fromCharCode.apply(null, new Uint8Array(rawKey)))) : '';
    var rawAuthSecret = subscription.getKey ? subscription.getKey('auth') : '';
    var authSecret = rawAuthSecret ? Base64EncodeUrl(btoa(String.fromCharCode.apply(null, new Uint8Array(rawAuthSecret)))) : '';
    console.log("Key: " + key);
    console.log("AuthSecret: " + authSecret);
    console.log('endpoint:', subscription.endpoint);
    console.log('subscription:' + JSON.stringify(subscription));
}

function Base64EncodeUrl(str){
    return str.replace(/\+/g, '-').replace(/\//g, '_').replace(/\=+$/, '');
}

function Base64DecodeUrl(str){
    str = (str + '===').slice(0, str.length + (str.length % 4));
    return str.replace(/-/g, '+').replace(/_/g, '/');
}

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}
