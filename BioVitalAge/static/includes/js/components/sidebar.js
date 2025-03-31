/*  -----------------------------------------------------------------------------------------------
  GLOBAL VARIABLES
--------------------------------------------------------------------------------------------------- */
let notifications = [];
let storedNotifications =
  JSON.parse(localStorage.getItem("notifications")) || [];
let dismissedNotifications =
  JSON.parse(localStorage.getItem("dismissedNotifications")) || [];
let emails = [
  { subject: "Risultati laboratorio", sender: "Clinica Roma" },
  { subject: "Nuova richiesta prenotazione", sender: "Segreteria" },
];

const updates = [
  {
    version: "v3.15.2",
    description: "Correzione bug e miglioramenti UI Home Page",
  },
  {
    version: "v3.15.2",
    description:
      "Abilitate le notifiche nella Home Page per gli appuntamenti in arrivo e quelli del giorno stesso.",
  },
  {
    version: "v3.15.2",
    description:
      "Abilitate le notifiche nella Home Page ache per le news del mondo medico.",
  },
  {
    version: "v3.15.2",
    description:
      "Impostato un layou adatto alle news con link che porta a quella news.",
  },
  {
    version: "v3.15.2",
    description: "Debug sezione appuntamenti completato con esito positivo",
  },
  { version: "v3.15.2", description: "..." },
];

const configurations = [
  { setting: "Lingua", value: "Italiano" },
  {
    setting: "Account",
    value: typeof currentUser !== "undefined" ? currentUser : "N/A",
  },
];

const features = [
  {
    name: "Sezione Appuntamenti",
    description:
      "Permette di pianificare e gestire appuntamenti con i pazienti e anche di aggiungere, eventualmente, l'appuntamento su Google Calendar",
  },
  {
    name: "Sezione Promemoria",
    description:
      "Permette di aggiungere dei promemoria e ti consente di visualizzare tutti gli appuntamenti in scadenza e quelli più importanti",
  },
  {
    name: "Sezione Pazienti",
    description:
      "Mostra una barra di ricerca che ti consente di ricercare il paziente per Nome, Cognome, Dottore Associato e Codice Fiscale",
  },
  {
    name: "Sezione Aggiungi Pazienti",
    description:
      "Ti consente di aggiungere dei pazienti completando i campi con i dati necessari",
  },
];

/*  -----------------------------------------------------------------------------------------------
  SIDEBAR HANDLER
--------------------------------------------------------------------------------------------------- */
async function fetchNotifications() {
  // Esegui il fetch delle notifiche da API (sia appuntamenti che news)
  await fetchAppointmentNotifications();
  await fetchMedicalNewsNotifications();

  // Dopo averle ottenute, salva l'array in localStorage
  localStorage.setItem("notifications", JSON.stringify(notifications));
}

// Se ci sono notifiche memorizzate, le usi, altrimenti fai il fetch
if (storedNotifications.length > 0) {
  // Usa solo le notifiche non eliminate (filtrando per id)
  notifications = storedNotifications.filter(
    (n) => !dismissedNotifications.includes(n.id)
  );
  updateNotificationsBadge();
} else {
  fetchNotifications();
}

document.addEventListener("DOMContentLoaded", () => {
  const sidebarTitle = document.getElementById("sidebar-title");
  const sidebarContent = document.getElementById("sidebar-content");
  const closeSidebar = document.getElementById("closeSidebar");
  const bgSidebar = document.querySelector(".bg-sidebar");

  document.querySelectorAll(".sidebar-trigger").forEach((trigger) => {
    const section = trigger.getAttribute("data-section");
    if (section === "Notifiche") {
      let badge = document.createElement("span");
      badge.classList.add("badge-count");
      badge.textContent = notifications.length;
      trigger.appendChild(badge);
    } else if (section === "Email") {
      let badge = document.createElement("span");
      badge.classList.add("badge-count");
      badge.textContent = emails.length;
      trigger.appendChild(badge);
    }

    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      const section = trigger.getAttribute("data-section");
      sidebarTitle.textContent = section;

      switch (section) {
        case "Notifiche":
          renderNotifications();
          break;
        case "Email":
          // Richiama il fetch per aggiornare le email dal back-end
          fetchEmails().then((fetchedEmails) => {
            sidebarContent.innerHTML = fetchedEmails
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
          });
          break;
        case "Update":
          sidebarContent.innerHTML = updates
            .map(
              (update, index) => `
              <div class="alert alert-warning notification" data-index="${index}">
                  ${update.version} - ${update.description}
              </div>
            `
            )
            .join("");
          break;
        case "Configurazione":
          sidebarContent.innerHTML = configurations
            .map(
              (config, index) => `
              <div class="alert alert-secondary notification" data-index="${index}">
                  ${config.setting} - ${config.value}
              </div>
            `
            )
            .join("");
          break;
        case "Funzionalità":
          sidebarContent.innerHTML = features
            .map(
              (feature, index) => `
              <div class="alert alert-success notification" data-index="${index}">
                  ${feature.name} - ${feature.description}
              </div>
            `
            )
            .join("");
          break;
        default:
          sidebarContent.innerHTML = "<p>Contenuto non disponibile.</p>";
      }

      document.body.classList.add("visible");

      requestAnimationFrame(() => {
        const elements = document.querySelectorAll(".notification");
        if (elements.length > 0) {
          gsap.to(elements, {
            opacity: 1,
            y: 0,
            duration: 0.5,
            ease: "power2.out",
            stagger: 0.2,
          });
        } else {
          console.warn("⚠️ Nessuna notifica trovata per GSAP.");
        }
      });
    });
  });

  bgSidebar.addEventListener("click", () => {
    document.body.classList.remove("visible");
  });
  closeSidebar.addEventListener("click", () => {
    document.body.classList.remove("visible");
  });

  const logoutBtn = document.getElementById("nav-bar-user-modal-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      // Al logout, se vuoi resettare le notifiche eliminate, rimuovi questa riga
      // localStorage.removeItem("dismissedNotifications");
    });
  }

  // Avvia i fetch
  fetchAppointmentNotifications();
  fetchMedicalNewsNotifications();

  setInterval(() => {
    console.log("Aggiorno le notifiche...");
    fetchAppointmentNotifications();
    fetchMedicalNewsNotifications();
  }, 60000);
});

/*  -----------------------------------------------------------------------------------------------
  EMAIL MANAGEMENT
--------------------------------------------------------------------------------------------------- */
// Funzione per il fetch delle email
async function fetchEmails() {
  try {
    const response = await fetch("/fetch_emails/");
    const data = await response.json();
    if (data.success && data.emails) {
      // Aggiorna la variabile globale "emails"
      emails = data.emails;

      // Aggiorna il badge della sezione Email
      const emailTrigger = document.querySelector(
        '.sidebar-trigger[data-section="Email"]'
      );
      if (emailTrigger) {
        let badge = emailTrigger.querySelector(".badge-count");
        if (!badge) {
          badge = document.createElement("span");
          badge.classList.add("badge-count");
          emailTrigger.appendChild(badge);
        }
        badge.textContent = emails.length;
      }

      return emails;
    } else {
      console.error("Errore nel recupero delle email:", data.error);
      return [];
    }
  } catch (error) {
    console.error("Errore nel fetch delle email:", error);
    return [];
  }
}

/*  -----------------------------------------------------------------------------------------------
  NOTIFICATION MANAGEMENT - VERSIONE CORRETTA
--------------------------------------------------------------------------------------------------- */

// Inizializzazione con pulizia
function initNotifications() {
  notifications = JSON.parse(localStorage.getItem("notifications")) || [];
  dismissedNotifications =
    JSON.parse(localStorage.getItem("dismissedNotifications")) || [];

  // Pulizia degli ID undefined
  dismissedNotifications = dismissedNotifications.filter(
    (id) => id && id !== "undefined"
  );
  localStorage.setItem(
    "dismissedNotifications",
    JSON.stringify(dismissedNotifications)
  );

  // Assegna ID univoci alle notifiche che non ne hanno
  notifications.forEach((notifica) => {
    if (!notifica.id) {
      notifica.id = `gen-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
    }
  });
  localStorage.setItem("notifications", JSON.stringify(notifications));
}

// Chiama all'inizio
initNotifications();

// Funzione di rimozione robusta
function removeNotification(notificationElement) {
  const id = notificationElement.getAttribute("data-id");
  if (!id) {
    console.error("ID notifica non valido");
    return;
  }

  // Aggiungi agli eliminati (senza duplicati)
  if (!dismissedNotifications.includes(id)) {
    dismissedNotifications = [...new Set([...dismissedNotifications, id])];
    localStorage.setItem(
      "dismissedNotifications",
      JSON.stringify(dismissedNotifications)
    );
  }

  // Rimuovi dalle notifiche attive
  notifications = notifications.filter((n) => n.id !== id);
  localStorage.setItem("notifications", JSON.stringify(notifications));

  // Animazione e rimozione
  gsap.to(notificationElement, {
    opacity: 0,
    y: -20,
    duration: 0.3,
    onComplete: () => {
      notificationElement.remove();
      updateNotificationsBadge();
      console.log("Notifica rimossa con successo");
    },
  });
}

// Aggiornamento badge garantito
function updateNotificationsBadge() {
  const trigger = document.querySelector(
    '.sidebar-trigger[data-section="Notifiche"]'
  );
  if (!trigger) return;

  let badge =
    trigger.querySelector(".badge-count") || document.createElement("span");
  badge.className = "badge-count";

  const activeNotifications = notifications.filter(
    (n) => n.id && !dismissedNotifications.includes(n.id)
  );

  badge.textContent =
    activeNotifications.length > 0 ? activeNotifications.length : "";
  badge.style.display = activeNotifications.length > 0 ? "flex" : "none";

  if (!trigger.contains(badge)) {
    trigger.appendChild(badge);
  }
}

// Modifica la funzione fetchMedicalNewsNotifications
async function fetchMedicalNewsNotifications() {
  try {
    const response = await fetch("/api/medical-news-notifications/");
    const data = await response.json();
    if (data.success) {
      // Filtra le news escludendo quelle eliminate
      const filteredNews = data.news.filter((news) => {
        const hasId = news.id && news.id !== "undefined";
        return hasId && !dismissedNotifications.includes(news.id);
      });

      // Prendi solo le prime 2 notifiche
      const newsToShow = filteredNews.slice(0, 2);

      // Sostituisci le notifiche news esistenti
      notifications = [
        ...notifications.filter((n) => n.origin !== "news"),
        ...newsToShow.map((news) => ({
          id:
            news.id ||
            `news-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          type: news.type || "info",
          message: `
              <div class="news-notification" data-id="${news.id}">
                <div class="news-date text-muted mb-1">${news.published_at}</div>
                <div class="news-title fw-bold">${news.title}</div>
                <div class="news-description text-muted text-truncate-3">${news.description}</div>
                <a href="${news.link}" target="_blank" class="btn btn-sm btn-outline-primary mt-2">Leggi di più</a>
              </div>
            `,
          origin: "news",
        })),
      ];

      updateNotificationsBadge();
      localStorage.setItem("notifications", JSON.stringify(notifications));
    }
  } catch (error) {
    console.error("Errore nel recupero notizie mediche:", error);
  }
}

async function fetchAppointmentNotifications() {
  try {
    const response = await fetch("/api/appointment-notifications/");
    const data = await response.json();
    if (data.success) {
      // Filtra le notifiche degli appuntamenti: usa n.message come id se n.id non esiste
      const filtered = data.notifications.filter(
        (n) => !dismissedNotifications.includes(n.message)
      );
      // Rimuovi le notifiche di appuntamenti già presenti
      notifications = notifications.filter((n) => n.origin !== "appointments");
      // Per ogni notifica, se non esiste un id, usalo dal message; assegna l'origine
      filtered.forEach((n) => {
        if (!n.id) {
          n.id = n.message;
        }
        n.origin = "appointments";
      });
      notifications = notifications.concat(filtered);
      updateNotificationsBadge();
    }
  } catch (error) {
    console.error("Errore nel recupero notifiche appuntamenti:", error);
  }
}

// Modifica renderNotifications per usare data-id corretti
function renderNotifications() {
  const sidebarContent = document.getElementById("sidebar-content");
  const activeNotifications = notifications.filter(
    (n) => n.id && !dismissedNotifications.includes(n.id)
  );

  sidebarContent.innerHTML = activeNotifications
    .map(
      (notifica) => `
        <div class="alert alert-${notifica.type} notification" 
             data-id="${notifica.id}">
          ${notifica.message}
          <button type="button" class="btn-close" 
                  onclick="removeNotification(this.parentElement)"></button>
        </div>
      `
    )
    .join("");

  // Animazione
  gsap.to(".notification", {
    opacity: 1,
    y: 0,
    duration: 0.5,
    stagger: 0.1,
  });
}
