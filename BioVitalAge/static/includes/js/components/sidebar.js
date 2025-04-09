/*  -----------------------------------------------------------------------------------------------
   GLOBAL VARIABLES
--------------------------------------------------------------------------------------------------- */
let emails = [];
let notifications = [];
let appUser = window.currentUser || 'guest'; // Usiamo appUser invece di currentUser per evitare conflitti
let previousUser = null;
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
      "Abilitate le notifiche nella Home Page anche per le news del mondo medico.",
  },
  {
    version: "v3.15.2",
    description:
      "Impostato un layout adatto alle news con link che porta a quella news.",
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
   USER MANAGEMENT
--------------------------------------------------------------------------------------------------- */
let userCheckInProgress = false;

function checkUserChange() {
  if (userCheckInProgress) return;
  userCheckInProgress = true;
  
  const templateUser = window.currentUser || 'guest';
  const storedUser = localStorage.getItem('appUser') || 'guest';

  if (templateUser !== storedUser) {
    console.log(`Cambio utente rilevato: ${storedUser} → ${templateUser}`);
    handleUserChange(templateUser);
  }

  localStorage.setItem('appUser', templateUser);
  appUser = templateUser;
  userCheckInProgress = false;
}

async function handleUserChange(newUser) {
  if (newUser === appUser) return;

  previousUser = appUser;
  appUser = newUser || 'guest';
  
  console.log(`Gestione cambio utente: ${previousUser} → ${appUser}`);
  
  // Resetta solo lo stato frontend
  notifications = [];
  dismissedNotifications = [];
  
  // Carica i dati per il nuovo utente
  try {
    await Promise.all([
      initUserNotifications(),
      fetchNotifications(),
    ]);
    updateAllBadges();
  } catch (error) {
    console.error("Errore durante il cambio utente:", error);
  }
}

/*  -----------------------------------------------------------------------------------------------
   EMAIL FETCHING
--------------------------------------------------------------------------------------------------- */


/*  -----------------------------------------------------------------------------------------------
   INITIALIZATION
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  // 1. Verifica il cambio utente
  checkUserChange();

  // 2. Configura intervallo di aggiornamento  
  // 3. Configura intervallo di aggiornamento
  setInterval(fetchNotifications, 3600000);

  updateAllBadges();
  // 4. Listener per logout
  document.getElementById('logout-btn')?.addEventListener('click', () => {
    localStorage.setItem('pendingLogout', 'true');
    // Pulisci solo i dati sensibili mantenendo le preferenze
    localStorage.removeItem('appUser');
  });
});


/*  -----------------------------------------------------------------------------------------------
   SIDEBAR HANDLER
--------------------------------------------------------------------------------------------------- */
// Funzione per il fetch delle notifiche
async function fetchNotifications() {
  await fetchAppointmentNotifications();
  await fetchMedicalNewsNotifications();
  updateNotificationsBadge();
  updateAllBadges(); // <--- QUI
  localStorage.setItem(`notifications_${appUser}`, JSON.stringify(notifications));
  console.log("Notifiche aggiornate...");
}

// // Se ci sono notifiche memorizzate, le usi, altrimenti fai il fetch
// if (storedNotifications.length > 0) {
//   // Usa solo le notifiche non eliminate (filtrando per id)
//   notifications = storedNotifications.filter(
//     (n) => !dismissedNotifications.includes(n.id)
//   );
//   updateNotificationsBadge();
// } else {
// }
updateAllBadges();
initUserNotifications();
fetchNotifications();

// Funzione per renderizzare le notifiche
document.addEventListener("DOMContentLoaded", () => {
  const sidebarTitle = document.getElementById("sidebar-title");
  const sidebarContent = document.getElementById("sidebar-content");
  const closeSidebar = document.getElementById("closeSidebar");
  const bgSidebar = document.querySelector(".bg-sidebar");

  // Inizializza con l'utente corrente
  handleUserChange(typeof currentUser !== 'undefined' ? currentUser : 'guest');

  // Listener per le notifiche
  document.querySelectorAll(".sidebar-trigger").forEach((trigger) => {
    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      const section = trigger.getAttribute("data-section");
      sidebarTitle.textContent = section;

      switch (section) {
        case "Notifiche":
          renderNotifications();
          break;
        case "Email":
          const emailsDataElement = document.getElementById("emails-data");

          if (emailsDataElement) {
            try {
              const emails = JSON.parse(emailsDataElement.textContent);
        
              if (Array.isArray(emails) && emails.length > 0) {
                sidebarContent.innerHTML = emails.map((email, index) => `
                  <a href="${email.link}" target="_blank" class="alert alert-warning notification d-block text-decoration-none" data-index="${index}">
                    <strong>${email.subject}</strong> - ${email.from}
                  </a>
                `).join("");
              } else {
                sidebarContent.innerHTML = `<p class="default-text-notification">Nessuna email disponibile.</p>`;
              }
            } catch (error) {
              console.error("Errore nel parsing JSON delle email:", error);
              sidebarContent.innerHTML = `<p class="default-text-notification">Errore nel caricamento email.</p>`;
            }
          } else {
            sidebarContent.innerHTML = `<p class="default-text-notification">Nessun dato email trovato.</p>`;
          }
          break;
        case "Appuntamenti":
          break;
        case "Update":
          sidebarContent.innerHTML = updates
            .map((update, index) => `
              <div class="alert alert-warning notification" data-index="${index}">
                  ${update.version} - ${update.description}
              </div>
            `)
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

  // Listener per chiudere lo sfondo della sidebar
  bgSidebar.addEventListener("click", () => {
    document.body.classList.remove("visible");
  });

  // Listener per chiudere la sidebar
  closeSidebar.addEventListener("click", () => {
    document.body.classList.remove("visible");
  });

  // Listener per il pulsante di logout
  const logoutBtn = document.getElementById("nav-bar-user-modal-btn");

  // Listener per il pulsante di logout
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      // Al logout (esempio)
      handleUserChange('guest');
    });
  }

  // Listener per il pulsante di login
  document.getElementById('login-btn')?.addEventListener('click', () => {
    handleUserChange(currentUser); // Sostituisci con l'utente reale

    console.log("Login effettuato: attendo 500ms per la propagazione dei cookie...");
  });

  // Avvia i fetch
  fetchAppointmentNotifications();
  fetchMedicalNewsNotifications();

  // 1. Verifica il cambio utente ad ogni caricamento
  checkUserChange();

  setInterval(() => {
    console.log("Aggiorno le notifiche...");
    fetchAppointmentNotifications();
    fetchMedicalNewsNotifications();
  }, 60000);
});


/*  -----------------------------------------------------------------------------------------------
   NOTIFICATION MANAGEMENT
--------------------------------------------------------------------------------------------------- */
// Inizializzazione con pulizia
function initUserNotifications() {
  const userKey = `notifications_${appUser}`;
  const dismissedKey = `dismissedNotifications_${appUser}`;

  notifications = JSON.parse(localStorage.getItem(userKey)) || [];
  dismissedNotifications = JSON.parse(localStorage.getItem(dismissedKey)) || [];

  // Filtra ID non validi
  dismissedNotifications = dismissedNotifications.filter(id => id && id !== 'undefined');

  console.log(`Notifiche caricate per ${appUser}: ${notifications.length}`);
  updateNotificationsBadge();
}

function saveUserNotifications() {
  const userKey = `notifications_${appUser}`;
  const dismissedKey = `dismissedNotifications_${appUser}`;

  localStorage.setItem(userKey, JSON.stringify(notifications));
  localStorage.setItem(dismissedKey, JSON.stringify(dismissedNotifications));
}

// Chiama all'inizio
initUserNotifications();

// Funzione di rimozione robusta
function removeNotification(notificationElement) {
  const id = notificationElement.getAttribute('data-id');
  if (!id) return;

  const dismissedKey = `dismissedNotifications_${appUser}`;

  if (!dismissedNotifications.includes(id)) {
    dismissedNotifications.push(id);
    localStorage.setItem(dismissedKey, JSON.stringify(dismissedNotifications));
  }

  notifications = notifications.filter(n => n.id !== id);
  localStorage.setItem(`notifications_${appUser}`, JSON.stringify(notifications));

  gsap.to(notificationElement, {
    opacity: 0,
    y: -20,
    duration: 0.3,
    onComplete: () => {
      notificationElement.remove();
      updateNotificationsBadge();
    }
  });
}

// Aggiornamento badge garantito
function updateNotificationsBadge() {
  const trigger = document.querySelector('.sidebar-trigger[data-section="Notifiche"]');
  if (!trigger) return;

  let badge = trigger.querySelector(".badge-count") || document.createElement("span");
  badge.className = "badge-count";

  const activeNotifications = notifications.filter(
    (n) => n.id && !dismissedNotifications.includes(n.id)
  );

  badge.textContent = activeNotifications.length > 0 ? activeNotifications.length : "";
  badge.style.display = activeNotifications.length > 0 ? "flex" : "none";

  if (!trigger.contains(badge)) {
    trigger.appendChild(badge);
  }
}

// Aggiorna tutti i badge
function updateAllBadges() {
  // Badge Notifiche
  const notifTrigger = document.querySelector('.sidebar-trigger[data-section="Notifiche"]');
  if (notifTrigger) {
    let badge = notifTrigger.querySelector(".badge-count");
    const activeNotifications = notifications.filter(n => n.id && !dismissedNotifications.includes(n.id));
    if (!badge) {
      badge = document.createElement("span");
      badge.className = "badge-count";
      notifTrigger.appendChild(badge);
    }
    badge.textContent = activeNotifications.length;
    badge.style.display = activeNotifications.length > 0 ? "flex" : "none";
  }

  // Badge Email
  const emailTrigger = document.querySelector('.sidebar-trigger[data-section="Email"]');
  if (emailTrigger) {
    let badge = emailTrigger.querySelector(".badge-count");
    if (!badge) {
      badge = document.createElement("span");
      badge.className = "badge-count";
      emailTrigger.appendChild(badge);
    }
    badge.textContent = emails.length;
    badge.style.display = emails.length > 0 ? "flex" : "none";
  }
}

// Modifica la funzione fetchMedicalNewsNotifications
// Funzione per generare l'HTML delle news
function generateNewsHTML(news) {
  // Crea un oggetto Date a partire dalla stringa ricevuta
  const date = new Date(news.published_at);
  // Format della data in italiano, puoi personalizzare le opzioni se necessario
  const formattedDate = new Intl.DateTimeFormat('it-IT', { dateStyle: 'long' }).format(date);

  return `
    <div class="news-notification">
      <div class="news-date text-muted mb-1">${formattedDate}</div>
      <div class="news-title fw-bold">${news.title}</div>
      <div class="news-description text-muted text-truncate-3">${news.description}</div>
      <a href="${news.link}" target="_blank" class="btn btn-sm btn-outline-primary mt-2">Leggi di più</a>
    </div>
  `;
}

// Funzione per il fetch delle news
async function fetchMedicalNewsNotifications() {
  try {
    const response = await fetch("/api/medical-news-notifications/");
    const data = await response.json();
    console.log(data);
    if (data.success) {
      const freshNews = (appUser === 'guest'
        ? data.news.slice(0, 2)
        : data.news.filter(news => news.id && !dismissedNotifications.includes(news.id)).slice(0, 2)
      );

      const newsNotifications = freshNews.map(news => ({
        id: news.id,
        type: 'info',
        message: generateNewsHTML(news),
        origin: 'news'
      }));

      // Confronta gli ID attuali delle notifiche di news con quelli delle nuove notifiche
      const currentNewsIds = notifications.filter(n => n.origin === 'news').map(n => n.id);
      const newNewsIds = newsNotifications.map(n => n.id);
      if (JSON.stringify(currentNewsIds) !== JSON.stringify(newNewsIds)) {
        notifications = notifications.filter(n => n.origin !== 'news');
        notifications = notifications.concat(newsNotifications);
        saveUserNotifications();
        updateNotificationsBadge();
      }
    }
  } catch (error) {
    console.error("Fetch news error:", error);
  }
}

// Funzione per il fetch delle notifiche di appuntamenti
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

// Funzione per il fetch delle email
/* EMAIL FETCHING */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Verifica se questo cookie inizia con il nome cercato
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Modifica renderNotifications per usare data-id corretti
function renderNotifications() {
  const sidebarContent = document.getElementById("sidebar-content");
  const activeNotifications = notifications.filter(
    (n) => !dismissedNotifications.includes(n.id)
  );

  sidebarContent.innerHTML = activeNotifications.length > 0 
    ? activeNotifications.map(notifica => `
        <div class="alert alert-${notifica.type} notification" data-id="${notifica.id}">
          ${notifica.message}
          <button type="button" class="btn-close" onclick="removeNotification(this.parentElement)"></button>
        </div>
      `).join("")
    : `<p class="default-text-notification">Attualmente non hai notifiche.</p>`;

  gsap.to(".notification", { opacity: 1, y: 0, duration: 0.5, stagger: 0.1 });
}
