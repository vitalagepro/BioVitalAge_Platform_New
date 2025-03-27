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
  { version: "v3.15.1", description: "Correzione bug e miglioramenti UI Home Page" },
  { version: "v3.15.1", description: "Aggiunta numeri dinamici nelle caselle oppurtune della Home Page" },
  { version: "v3.15.1", description: "Sezione appuntamenti completata" }
];

const configurations = [
  { setting: "Lingua", value: "Italiano" },
  { setting: "Account", value: "Segreteria" }
];

const features = [
  { name: "Gestione Appuntamenti", description: "Permette di pianificare e gestire appuntamenti con i pazienti." },
  { name: "Monitoraggio Referti", description: "Consente di tenere traccia dei referti e delle analisi di laboratorio." }
];

function removeNotification(notification) {
  gsap.to(notification, { opacity: 0, y: -20, duration: 0.5, ease: "power2.in", onComplete: () => notification.remove() });
}


/*  -----------------------------------------------------------------------------------------------
  Graphs and Charts
--------------------------------------------------------------------------------------------------- */

// Chart: Patients by Age
const ctx1 = document.getElementById("patientsByAge").getContext("2d");
new Chart(ctx1, {
  type: "bar",
  data: {
    labels: [
      "Gen",
      "Feb",
      "Mar",
      "Apr",
      "Mag",
      "Giu",
      "Lug",
      "Ago",
      "Set",
      "Ott",
      "Nov",
      "Dic",
    ],
    datasets: [
      {
        label: "0-5",
        data: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
        backgroundColor: "#6a2dcc",
      },
      {
        label: "6-15",
        data: [7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57, 62],
        backgroundColor: "#8041e0",
      },
      {
        label: "16-25",
        data: [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
        backgroundColor: "#9666e4",
      },
      {
        label: "26-45",
        data: [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
        backgroundColor: "#ad8be8",
      },
      {
        label: "46+",
        data: [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75],
        backgroundColor: "#c3b0ec",
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "bottom",
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  },
});

// Chart: Patients
const ctx2 = document.getElementById("patients").getContext("2d");
new Chart(ctx2, {
  type: "line",
  data: {
    labels: [
      "Gen",
      "Feb",
      "Mar",
      "Apr",
      "Mag",
      "Giu",
      "Lug",
      "Ago",
      "Set",
      "Ott",
      "Nov",
      "Dic",
    ],
    datasets: [
      {
        label: "Nuovo",
        data: [50, 60, 55, 70, 75, 80, 90, 85, 95, 100, 105, 110],
        borderColor: "#6a2dcc",
        backgroundColor: "#3b255d2c",
        fill: true,
      },
      {
        label: "Ritorno",
        data: [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85],
        borderColor: "#9666e4",
        backgroundColor: "#c3b0ec",
        fill: true,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "bottom",
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  },
});

// Chart: Income by Department
const ctx3 = document.getElementById("incomeByDepartment").getContext("2d");
new Chart(ctx3, {
  type: "bar",
  data: {
    labels: [
      "Gen",
      "Feb",
      "Mar",
      "Apr",
      "Mag",
      "Giu",
      "Lug",
      "Ago",
      "Set",
      "Ott",
      "Nov",
      "Dic",
    ],

    datasets: [
      {
        label: "Neurologia",
        data: [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32],
        backgroundColor: "#6a2dcc",
      },
      {
        label: "Cura dei denti",
        data: [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        backgroundColor: "#8041e0",
      },
      {
        label: "Ginecologia",
        data: [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
        backgroundColor: "#9666e4",
      },
      {
        label: "Ortopedia",
        data: [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26],
        backgroundColor: "#ad8be8",
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "bottom",
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  },
});

const weeklyCtx = document.getElementById("weeklyPatientsChart");
new Chart(weeklyCtx, {
  type: "line",
  data: {
    labels: ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"],
    datasets: [
      {
        label: "Pazienti Visitati",
        data: [5, 10, 8, 12, 15, 20, 5],
        borderColor: "#fff",
        backgroundColor: "rgba(255,255,255,0.3)",
        fill: true,
        tension: 0.3,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      x: {
        ticks: { color: "#fff" },
        grid: { color: "rgba(255,255,255,0.2)" },
      },
      y: {
        ticks: { color: "#fff" },
        grid: { color: "rgba(255,255,255,0.2)" },
      },
    },
    plugins: {
      legend: { display: false },
    },
  },
});

const patientsCtx = document.getElementById("patientsChart");
new Chart(patientsCtx, {
  type: "bar",
  data: {
    labels: [
      "Gen",
      "Feb",
      "Mar",
      "Apr",
      "Mag",
      "Giu",
      "Lug",
      "Ago",
      "Set",
      "Ott",
      "Nov",
      "Dic",
    ],
    datasets: [
      {
        label: "Pazienti Inseriti",
        data: [30, 45, 60, 50, 41, 66, 30, 50, 70, 90, 100, 120],
        backgroundColor: "#6a2dcc",
        categoryPercentage: 2.8, // Maggior spazio tra le categorie
        barPercentage: 0.1, // Barre più sottili
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: {
        ticks: {
          autoSkip: false, // Mostra tutte le etichette
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  },
});

const monthlyCtx = document.getElementById("monthlyPatientsChart");
const monthlyData = {
  labels: [
    "Gen",
    "Feb",
    "Mar",
    "Apr",
    "Mag",
    "Giu",
    "Lug",
    "Ago",
    "Set",
    "Ott",
    "Nov",
    "Dic",
  ],
  datasets: [
    {
      label: "Pazienti Mensili",
      data: [40, 60, 55, 70, 80, 90, 100, 85, 75, 95, 110, 120],
      backgroundColor: "#c3b0ec",
      borderColor: "#6a2dcc",
      borderWidth: 2,
      fill: true,
    },
  ],
};

let monthlyPatientsChart = new Chart(monthlyCtx, {
  type: "line",
  data: monthlyData,
  options: {
    responsive: true,
    interaction: {
      mode: "index",
      intersect: false,
    },
    plugins: {
      legend: { display: false },
    },
    scales: {
      y: { beginAtZero: true },
    },
    onHover: (event, chartElement) => {
      const tooltip = document.getElementById("monthlyTooltip");
      if (chartElement.length > 0) {
        const index = chartElement[0].index;
        const monthLabel = monthlyData.labels[index];
        const patientCount = monthlyData.datasets[0].data[index];
        const calcCount = Math.floor(patientCount * 0.6);

        tooltip.innerHTML = `
                      <strong>${monthLabel}</strong><br>
                      Pazienti: ${patientCount}<br>
                      Con calcolo età bio: ${calcCount}
                  `;
        const canvasPos = monthlyCtx.getBoundingClientRect();
        tooltip.style.opacity = 1;
        tooltip.style.left = event.clientX - canvasPos.left + "px";
        tooltip.style.top = event.clientY - canvasPos.top + "px";
      } else {
        const tooltip = document.getElementById("monthlyTooltip");
        tooltip.style.opacity = 0;
      }
    },
  },
});
