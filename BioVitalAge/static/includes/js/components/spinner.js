// Funzione che imposta "opacity: 0" e "z-index: -1" dopo 3 secondi
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    document.getElementById("loading-wrapper").style.opacity = "0";
    document.getElementById("loading-wrapper").style.zIndex = "-1";
  }, 400);
});

function initClient() {
  gapi.client
    .init({
      clientId:
        "596437252615-hne0f5om42kv8blauergn54t42iqrqp2.apps.googleusercontent.com", // Inserisci qui la tua Client ID
      scope: "https://www.googleapis.com/auth/gmail.readonly",
    })
    .then(
      () => {
        // Se l'utente non è autenticato, effettua il login
        if (!gapi.auth2.getAuthInstance().isSignedIn.get()) {
          gapi.auth2
            .getAuthInstance()
            .signIn()
            .then(() => {
              console.log(
                "Utente autenticato",
                gapi.auth2.getAuthInstance().currentUser.get().getId()
              );
              // Procedi con il fetch delle email o altre operazioni
            });
        } else {
          console.log("Utente già autenticato");
          // Procedi con il fetch delle email o altre operazioni
        }
      },
      (error) => {
        console.error("Errore nell'inizializzazione del client:", error);
      }
    );
}

console.log("Origin rilevato:", location.origin);

gapi.load("client:auth2", initClient);