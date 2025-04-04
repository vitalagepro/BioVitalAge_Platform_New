/*  -----------------------------------------------------------------------------------------------
    FUNZIONE TOGGLE PASSWORD
--------------------------------------------------------------------------------------------------- */
function togglePasswordVisibility() {
  const passwordInput = document.getElementById("password");
  const toggleIconContainer = document.querySelector(".toggle-password");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleIconContainer.classList.add("active");
  } else {
    passwordInput.type = "password";
    toggleIconContainer.classList.remove("active");
  }
}

/*  -----------------------------------------------------------------------------------------------
    FUNZIONE SHOW ALERT
--------------------------------------------------------------------------------------------------- */
function showAlert(type, message) {
  // Rimuovi alert esistenti
  const existing = document.getElementById("global-alert");
  if (existing) existing.remove();

  // Crea l'alert
  const alertDiv = document.createElement("div");
  alertDiv.id = "global-alert";
  alertDiv.classList.add("alert", `alert-${type}`, "fade", "show");
  alertDiv.style.position = "fixed";
  alertDiv.style.top = "20px";
  alertDiv.style.left = "50%";
  alertDiv.style.transform = "translateX(-50%)";
  alertDiv.style.zIndex = "1050";
  alertDiv.style.padding = "12px 18px";
  alertDiv.style.borderRadius = "8px";
  alertDiv.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
  alertDiv.style.maxWidth = "400px";
  alertDiv.style.textAlign = "center";
  alertDiv.style.opacity = "0";

  // Inserisci messaggio
  alertDiv.innerHTML = `<span class="fw-semibold">${message}</span>`;

  document.body.appendChild(alertDiv);

  // Animazione di entrata
  gsap.to(alertDiv, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" });

  // Rimozione automatica
  setTimeout(() => {
    gsap.to(alertDiv, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => alertDiv.remove()
    });
  }, 4000);
}

/*  -----------------------------------------------------------------------------------------------
    FUNZIONE PER AGGIORNARE IL PROFILO    
-----------------------------------------------------------------------------------------------   */

document.addEventListener("DOMContentLoaded", function () {
  // Funzione per ottenere il CSRF token dalle cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Gestione della submission del form (nome, email, password e checkbox)
  const profileForm = document.querySelector("#content-user-profile form");
  if (profileForm) {
    profileForm.addEventListener("submit", function (e) {
      e.preventDefault(); // previene il submit classico
      if (!window.currentUser || window.currentUser === "guest") {
        console.warn("Utente non autenticato, annullo richiesta");
        return; // blocca la fetch
      }
      const formData = new FormData(profileForm);

      // Invia la richiesta POST via fetch
      fetch(window.location.href, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            showAlert("success", "Profilo aggiornato con successo");
            // Puoi mostrare un messaggio all'utente, es.:
            // document.getElementById("feedback").innerText = "Modifiche salvate!";
          } else {
            showAlert("danger", "Errore nell'aggiornamento del profilo");
          }
        })
        .catch((error) => console.error("Errore:", error));
    });
  }

  // Gestione separata del cambiamento della checkbox (aggiornamento in tempo reale)
  const gmailCheckbox = document.querySelector('input[name="check"]');
  if (gmailCheckbox) {
    gmailCheckbox.addEventListener("change", function () {
      const formData = new FormData();
      // Imposta il valore "SI" se spuntata, altrimenti stringa vuota
      formData.append("check", this.checked ? "SI" : "");

      fetch(window.location.href, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            showAlert("info", "Renderizzamento in corso...");
            // Se la checkbox è spuntata, dopo 400ms reindirizza al flusso OAuth di Google
            if (gmailCheckbox.checked) {
              setTimeout(function () {
                window.location.href =
                  "/auth/login/google-oauth2/?prompt=consent&access_type=offline";
              }, 400);
            }
          } else if (data.status === "disconnected") {
            showAlert("info", "Account Gmail disconnesso con successo");
          } else {
            showAlert("danger", "Errore nell'aggiornamento dello stato Gmail");
          }
        })
        .catch((error) => console.error("Errore:", error));
    });
  }
});
