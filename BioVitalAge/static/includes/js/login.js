// Carica la nuova libreria Google Identity Services
let isGoogleAuthInProgress = false;

function handleCredentialResponse(response) {
  if (isGoogleAuthInProgress) return;
  isGoogleAuthInProgress = true;

  // Invia il token al tuo backend Django
  fetch("/oauth2callback/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id_token: response.credential,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Inizializza GIS
function initGoogleAuth() {
  google.accounts.id.initialize({
    client_id: "",
    callback: handleCredentialResponse,
  });

  // Mostra il pulsante di login
  google.accounts.id.renderButton(
    document.getElementById("google-login-button"),
    { theme: "outline", size: "large" }
  );

  // Opzionale: Mostra anche l'One Tap login
  google.accounts.id.prompt();
}

// Carica la libreria GIS
function loadGoogleAuth() {
  const script = document.createElement("script");
  script.src = "https://accounts.google.com/gsi/client";
  script.async = true;
  script.defer = true;
  script.onload = initGoogleAuth;
  document.head.appendChild(script);
}

// Avvia tutto quando la pagina è pronta
document.addEventListener("DOMContentLoaded", loadGoogleAuth);
