self.addEventListener("install", function() {
  console.log("install");
}, false);

self.addEventListener("push", function(event) {
  event.waitUntil(
    self.registration.showNotification(
      "title",
      {
        "body": "body"
      }
    )
  );
}, false);
