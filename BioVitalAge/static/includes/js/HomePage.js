/*  -----------------------------------------------------------------------------------------------
  GLOBAL FUNCTION
--------------------------------------------------------------------------------------------------- */
function showAlert(type, message) {
  // Controllo se esiste già un alert visibile
  let existingAlert = document.getElementById("global-alert");
  if (existingAlert) existingAlert.remove();

  // Creazione del div per l'alert Bootstrap
  let alertDiv = document.createElement("div");
  alertDiv.id = "global-alert";
  alertDiv.classList.add("alert", `alert-${type}`, "fade", "show");
  alertDiv.style.position = "fixed";
  alertDiv.style.top = "20px";
  alertDiv.style.left = "50%";
  alertDiv.style.transform = "translateX(-50%)";
  alertDiv.style.zIndex = "9999999999999";
  alertDiv.style.width = "auto";
  alertDiv.style.maxWidth = "400px";
  alertDiv.style.display = "flex";
  alertDiv.style.justifyContent = "space-between";
  alertDiv.style.alignItems = "center";
  alertDiv.style.padding = "10px 15px";
  alertDiv.style.borderRadius = "6px";
  alertDiv.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";
  alertDiv.style.opacity = "0"; // Inizialmente nascosto

  // Contenuto dell'alert
  alertDiv.innerHTML = `
      <span>${message}</span>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

  // Aggiunge l'alert al DOM
  document.body.appendChild(alertDiv);

  // Effetto di comparsa con GSAP
  gsap.to(alertDiv, { opacity: 1, duration: 0.3, ease: "power2.out" });

  // Rimuove automaticamente l'alert dopo 5 secondi con un fade-out
  setTimeout(() => {
    gsap.to(alertDiv, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => alertDiv.remove(),
    });
  }, 5000);
}

/*  -----------------------------------------------------------------------------------------------
  Disclaimer
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const disclaimerContainer = document.getElementById("disclaimerContainer");
  const overlay = document.getElementById("cookieOverlay");
  const initialMessage = document.getElementById("initialMessage");
  const customizeSection = document.getElementById("customizeSection");

  // Verifica la presenza del cookie
  const disclaimerAccepted = document.cookie.includes("disclaimer_accepted=true");
  console.log("Stato del cookie:", document.cookie); // Log per debug
  console.log("Disclaimer accettato?", disclaimerAccepted); // Log per debug

  // Mostra il disclaimer se il cookie non è stato accettato
  if (!disclaimerAccepted && disclaimerContainer) {
    showDisclaimer();
  }

  // Aggiungi i listener agli elementi solo se esistono
  const acceptCookiesButton = document.getElementById("acceptCookies");
  const rejectCookiesButton = document.getElementById("rejectCookies");
  const customizeCookiesButton = document.getElementById("customizeCookies");
  const saveCookiesButton = document.getElementById("saveCookies");

  if (acceptCookiesButton) {
    acceptCookiesButton.addEventListener("click", function () {
      sendCookieSettings({ functional: true, analytics: true, marketing: true });
      closeDisclaimer();
    });
  } else {
    console.warn("Pulsante 'Accetta tutti' non trovato nel DOM.");
  }

  if (rejectCookiesButton) {
    rejectCookiesButton.addEventListener("click", function () {
      sendCookieSettings({ functional: false, analytics: false, marketing: false });
      closeDisclaimer();
    });
  } else {
    console.warn("Pulsante 'Rifiuta tutti' non trovato nel DOM.");
  }

  if (customizeCookiesButton) {
    customizeCookiesButton.addEventListener("click", function () {
      if (initialMessage && customizeSection) {
        initialMessage.classList.add("hidden-disclaimer");
        customizeSection.classList.remove("hidden-disclaimer");
      }
    });
  } else {
    console.warn("Pulsante 'Personalizza' non trovato nel DOM.");
  }

  if (saveCookiesButton) {
    saveCookiesButton.addEventListener("click", function () {
      const functional = document.getElementById("functionalCookies")?.checked || false;
      const analytics = document.getElementById("analyticsCookies")?.checked || false;
      const marketing = document.getElementById("marketingCookies")?.checked || false;

      sendCookieSettings({ functional, analytics, marketing });
      closeDisclaimer();
    });
  } else {
    console.warn("Pulsante 'Salva impostazioni' non trovato nel DOM.");
  }

  // Mostra il disclaimer
  function showDisclaimer() {
    console.log("Mostro il disclaimer"); // Log per debug
    disclaimerContainer.classList.add("visible-disclaimer");
    overlay.classList.add("visible-disclaimer");
    disclaimerContainer.classList.remove("hidden-disclaimer");
    overlay.classList.remove("hidden-disclaimer");
    document.body.style.overflow = "hidden";
  }

  // Nascondi il disclaimer e imposta il cookie
  function closeDisclaimer() {
    console.log("Chiudo il disclaimer e imposto il cookie"); // Log per debug
    disclaimerContainer.classList.remove("visible-disclaimer");
    overlay.classList.remove("visible-disclaimer");
    document.body.style.overflow = "auto";
    document.cookie = "disclaimer_accepted=true; path=/; max-age=31536000"; // 1 anno
  }

  // Invia le impostazioni dei cookie al server
  function sendCookieSettings(settings) {
    console.log("Invio le impostazioni dei cookie al server:", settings); // Log per debug
    fetch("/accept-disclaimer/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(settings),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Errore durante il salvataggio dei cookie");
        return response.json();
      })
      .then((data) => console.log("Impostazioni salvate con successo:", data))
      .catch((error) => console.error("Errore nell'invio delle impostazioni:", error));
  }

  // Ottieni un cookie per nome
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split("; ");
      for (let cookie of cookies) {
        if (cookie.startsWith(name + "=")) {
          cookieValue = cookie.split("=")[1];
          break;
        }
      }
    }
    return cookieValue;
  }
});

/*  -----------------------------------------------------------------------------------------------
  JS SIDEBAR
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const sidebarTitle = document.getElementById("sidebar-title");
  const sidebarContent = document.getElementById("sidebar-content");
  const closeSidebar = document.getElementById("closeSidebar");
  const bgSidebar = document.querySelector(".bg-sidebar");
  
  document.querySelectorAll(".sidebar-trigger").forEach((trigger) => {
      trigger.addEventListener("click", (event) => {
          event.preventDefault();
          const section = trigger.getAttribute("data-section");
          sidebarTitle.textContent = section;
          
          switch (section) {
            case "Notifiche":
              sidebarContent.style.padding = "0px";
              sidebarContent.innerHTML = notifications
                .map(
                  (notifica) => `
                      <div class="alert alert-${notifica.type} notification">
                          ${notifica.message} <button type="button" class="btn-close" onclick="removeNotification(this.parentElement)"></button>
                      </div>
                  `
                )
                .join("");
              gsap.to(".notification", {
                opacity: 1,
                y: 0,
                duration: 0.5,
                ease: "power2.out",
                stagger: 0.2,
              });
              break;
            case "Email":
              sidebarContent.style.padding = "0px";
              sidebarContent.innerHTML = emails
                .map(
                  (email) => `
                      <div class="alert alert-info notification">
                          <a href="https://mail.google.com/mail/u/0/#inbox" target="_blank" style="text-decoration: none; color: inherit;">
                              ${email.subject} - ${email.sender}
                          </a>
                      </div>
                  `
                )
                .join("");
              gsap.to(".notification", {
                opacity: 1,
                y: 0,
                duration: 0.5,
                ease: "power2.out",
                stagger: 0.2,
              });
              break;
            case "Update":
              sidebarContent.style.padding = "0px";
              sidebarContent.innerHTML = updates
                .map(
                  (update) => `
                      <div class="alert alert-warning notification">
                          ${update.version} - ${update.description}
                      </div>
                  `
                )
                .join("");
              gsap.to(".notification", {
                opacity: 1,
                y: 0,
                duration: 0.5,
                ease: "power2.out",
                stagger: 0.2,
              });
              break;
            case "Configurazione":
              sidebarContent.style.padding = "0px";
              sidebarContent.innerHTML = configurations
                .map(
                  (config) => `
                        <div class="alert alert-secondary notification">
                            ${config.setting} - ${config.value}
                        </div>
                    `
                )
                .join("");
              gsap.to(".notification", {
                opacity: 1,
                y: 0,
                duration: 0.5,
                ease: "power2.out",
                stagger: 0.2,
              });
              break;
            case "Funzionalità":
              sidebarContent.style.padding = "0px";
              sidebarContent.innerHTML = features
                .map(
                  (feature) => `
                        <div class="alert alert-success notification">
                            ${feature.name} - ${feature.description}
                        </div>
                    `
                )
                .join("");
              gsap.to(".notification", {
                opacity: 1,
                y: 0,
                duration: 0.5,
                ease: "power2.out",
                stagger: 0.2,
              });
              break;
            default:
              sidebarContent.style.padding = "0px";
              sidebarContent.innerHTML = "<p>Contenuto non disponibile.</p>";
          }

          document.body.classList.add("visible");
      });
  });

  bgSidebar.addEventListener("click", () => {
      document.body.classList.remove("visible");
  });
  closeSidebar.addEventListener("click", () => {
      document.body.classList.remove("visible");
  });
});

const notifications = [
  { message: "Nuovo referto disponibile", type: "success" },
  { message: "Appuntamento aggiornato", type: "info" },
  { message: "Errore nella trasmissione dati", type: "danger" },
  { message: "Promemoria: visita in scadenza", type: "warning" }
];

const emails = [
  { subject: "Risultati laboratorio", sender: "Clinica Roma" },
  { subject: "Nuova richiesta prenotazione", sender: "Segreteria" }
];

const updates = [
  { version: "v1.2.3", description: "Correzione bug e miglioramenti UI" },
  { version: "v1.3.0", description: "Nuove funzionalità di gestione appuntamenti" }
];

const configurations = [
  { setting: "Lingua", value: "Italiano" },
  { setting: "Tema", value: "Chiaro" }
];

const features = [
  { name: "Gestione Appuntamenti", description: "Permette di pianificare e gestire appuntamenti con i pazienti." },
  { name: "Monitoraggio Referti", description: "Consente di tenere traccia dei referti e delle analisi di laboratorio." }
];

function removeNotification(notification) {
  gsap.to(notification, { opacity: 0, y: -20, duration: 0.5, ease: "power2.in", onComplete: () => notification.remove() });
}


/*  -----------------------------------------------------------------------------------------------
  Actions on appointments
--------------------------------------------------------------------------------------------------- */
function confirmDeleteAppointment(appointmentId) {
  // Controllo se c'è già un alert visibile
  let existingAlert = document.getElementById("delete-alert");
  if (existingAlert) existingAlert.remove();

  // 🔹 Creazione alert Bootstrap personalizzato
  let confirmAlert = document.createElement("div");
  confirmAlert.id = "delete-alert";
  confirmAlert.classList.add("alert", "alert-danger", "fade", "show");
  confirmAlert.style.position = "fixed";
  confirmAlert.style.top = "20px";
  confirmAlert.style.left = "50%";
  confirmAlert.style.transform = "translateX(-50%)";
  confirmAlert.style.zIndex = "1050";
  confirmAlert.style.width = "auto";
  confirmAlert.style.maxWidth = "420px";
  confirmAlert.style.display = "flex";
  confirmAlert.style.justifyContent = "space-between";
  confirmAlert.style.alignItems = "center";
  confirmAlert.style.padding = "10px 15px";
  confirmAlert.style.borderRadius = "6px";
  confirmAlert.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";
  confirmAlert.style.opacity = "0"; // 🔹 Opacità iniziale per GSAP

  confirmAlert.innerHTML = `
      <span>Sei sicuro di voler eliminare questo appuntamento?</span>
      <div class="d-flex gap-2">
          <button type="button" class="btn btn-sm btn-danger" id="confirmDelete">Elimina</button>
          <button type="button" class="btn btn-sm btn-secondary" id="cancelDelete">Annulla</button>
      </div>
  `;

  // 🔹 Aggiungo l'alert al DOM
  document.body.appendChild(confirmAlert);

  // 🔹 Effetto GSAP per far apparire l'alert con un fade-in
  gsap.to(confirmAlert, { opacity: 1, duration: 0.3, ease: "power2.out" });

  // 🔹 Eventi sui bottoni
  document.getElementById("confirmDelete").addEventListener("click", () => {
    deleteAppointment(appointmentId, confirmAlert);
  });

  document.getElementById("cancelDelete").addEventListener("click", () => {
    gsap.to(confirmAlert, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => confirmAlert.remove(),
    });
  });

  // 🔹 Rimuove automaticamente l'alert dopo 10 secondi con un fade-out GSAP
  setTimeout(() => {
    gsap.to(confirmAlert, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => confirmAlert.remove(),
    });
  }, 10000);
}

function deleteAppointment(appointmentId, confirmAlert) {
  fetch(`/delete-appointment/${appointmentId}/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Errore HTTP: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        // 🔹 Rimuove anche l'alert di conferma
        gsap.to(confirmAlert, {
          opacity: 0,
          duration: 0.3,
          ease: "power2.in",
          onComplete: () => confirmAlert.remove(),
        });

        // 🔹 Mostra l'alert di successo
        showAlert("success", "Appuntamento eliminato con successo!");
      } else {
        console.error("❌ Errore nella cancellazione:", data.error);
        showAlert("danger", "Errore nella cancellazione dell'appuntamento.");
      }
    })
    .catch((error) => {
      console.error("❌ Errore nella richiesta:", error);
      showAlert("danger", "Errore nella richiesta al server.");
    });
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".action-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const row = this.closest("tr"); // Trova la riga
      const appointmentId = row.getAttribute("data-id"); // Ottiene l'ID dall'attributo data-id
      const action = this.classList.contains("approve") ? "approve" : "delete";

      if (action === "approve") {
        fetch(`/api/appointments/${appointmentId}/approve/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              row.style.backgroundColor = "#d4edda"; // Verde per indicare confermato
              showAlert("success", "Appuntamento confermato!");
            } else {
              showAlert("danger", "Errore: " + data.error);
            }
          });
      } else if (action === "delete") {
        confirmDeleteAppointment(appointmentId);
      }
    });
  });

  function getCSRFToken() {
    let csrfToken = null;
    document.cookie.split(";").forEach((cookie) => {
      let [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") csrfToken = value;
    });
    return csrfToken;
  }
});