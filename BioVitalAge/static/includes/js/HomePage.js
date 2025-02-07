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