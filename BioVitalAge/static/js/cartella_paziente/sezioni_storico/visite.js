import showAlert from "../../components/showAlert.js";

/*  -----------------------------------------------------------------------------------------------
   MAPPING TIPOLOGIE
--------------------------------------------------------------------------------------------------- */
const mappingTipologie = {
  Fisioestetica: [
    { value: "Crioterapia", text: "Crioterapia", duration: [30] },
    {
      value: "Radiofrequenza medica",
      text: "Radiofrequenza medica",
      duration: [20, 30, 45],
    },
    {
      value: "Mesoterapia transdermica",
      text: "Mesoterapia transdermica",
      duration: [20, 30, 45],
    },
    {
      value: "Mesoterapia intramedica",
      text: "Mesoterapia intramedica",
      duration: [30],
    },
    { value: "TECAR + massaggio", text: "TECAR + massaggio", duration: [20] },
    {
      value: "Massaggio linfodrenante",
      text: "Massaggio linfodrenante",
      duration: [30],
    },
    {
      value: "Massaggio tonificante volto",
      text: "Massaggio tonificante volto",
      duration: [20],
    },
    { value: "Onde d'urto", text: "Onde d'urto", duration: [10] },
  ],
  "Fisioterapia e Riabilitazione": [
    { value: "Visita fisiatrica", text: "Visita fisiatrica", duration: [30] },
    { value: "Visita ortopedica", text: "Visita ortopedica", duration: [30] },
    {
      value: "Visita neurologica",
      text: "Visita neurologica",
      duration: [30],
    },
    {
      value: "Visita reumatologica",
      text: "Visita reumatologica",
      duration: [30],
    },
    {
      value: "Chinesiterapia manuale/strumentale",
      text: "Chinesiterapia manuale/strumentale",
      duration: [30],
    },
    {
      value: "Elettrostimolazioni - diadinamica, ionoforesi o tens",
      text: "Elettrostimolazioni - diadinamica, ionoforesi o tens",
      duration: [20],
    },
    {
      value: "Infiltrazioni",
      text: "Infiltrazioni",
      duration: ["Da definire"],
    },
    { value: "Infrarossi", text: "Infrarossi", duration: [10] },
    { value: "Laserterapia", text: "Laserterapia", duration: [20] },
    { value: "Magnetoterapia", text: "Magnetoterapia", duration: [20] },
    {
      value: "Massaggio linfodrenante",
      text: "Massaggio linfodrenante",
      duration: [30],
    },
    { value: "Massoterapia", text: "Massoterapia", duration: [20] },
    {
      value: "Mesoterapia antalgica-antinfiammatoria",
      text: "Mesoterapia antalgica-antinfiammatoria",
      duration: [30],
    },
    {
      value: "Mobilizzazioni articolari",
      text: "Mobilizzazioni articolari",
      duration: [15],
    },
    {
      value: "Rieducazione motoria/rinforzo muscolare",
      text: "Rieducazione motoria/rinforzo muscolare",
      duration: [30],
    },
    { value: "TECAR", text: "TECAR", duration: [20] },
    { value: "Ultrasuonoterapia", text: "Ultrasuonoterapia", duration: [15] },
    { value: "Onde d'urto", text: "Onde d'urto", duration: [10] },
    {
      value: "Trattamento miofasciale",
      text: "Trattamento miofasciale",
      duration: [30],
    },
    {
      value: "Valutazione + Cervical ROM",
      text: "Valutazione + Cervical ROM",
      duration: [30],
    },
  ],
  "Fisioterapia Sportiva": [
    {
      value: "Rieducazione motoria/Rinforzo muscolare",
      text: "Rieducazione motoria/Rinforzo muscolare",
      duration: [30],
    },
    {
      value: "Prevenzione infotuni sport specifico",
      text: "Prevenzione infotuni sport specifico",
      duration: [30],
    },
    {
      value: "Massaggio decontratturante",
      text: "Massaggio decontratturante",
      duration: [30],
    },
  ],
};














/*  -----------------------------------------------------------------------------------------------
    MODALE NUOVA VISITA
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const apriBtn = document.getElementById("openModal"); // bottone per aprire modale
  const modale = document.getElementById("appointmentModal");
  const chiudiBtn1 = document.getElementById("closeModal");
  const chiudiBtn2 = document.getElementById("closeModalBtn");

  const tipologiaSelect = document.getElementById("tipologia_visita");
  const vocePrezzarioSelect = document.getElementById("voce-prezzario");
  const timeSelect = document.getElementById("time");

  if (
    !apriBtn ||
    !modale ||
    !chiudiBtn1 ||
    !chiudiBtn2 ||
    !tipologiaSelect ||
    !vocePrezzarioSelect ||
    !timeSelect
  ) {
    console.warn("Alcuni elementi della modale non sono stati trovati.");
    return;
  }

  // Reset voci e durata
  const resetDropdowns = () => {
    vocePrezzarioSelect.innerHTML = `<option>Seleziona una Voce</option>`;
    timeSelect.innerHTML = `<option>Seleziona una Durata</option>`;
  };

  // Popola voce prezzario e durata
  tipologiaSelect.addEventListener("change", () => {
    const selectedTipologia = tipologiaSelect.value;
    resetDropdowns();

    if (mappingTipologie[selectedTipologia]) {
      mappingTipologie[selectedTipologia].forEach((voce) => {
        const option = document.createElement("option");
        option.value = voce.value;
        option.text = voce.text;
        vocePrezzarioSelect.appendChild(option);
      });
    }
  });

  vocePrezzarioSelect.addEventListener("change", () => {
    const selectedTipologia = tipologiaSelect.value;
    const selectedVoce = vocePrezzarioSelect.value;
    timeSelect.innerHTML = `<option>Seleziona una Durata</option>`;

    if (mappingTipologie[selectedTipologia]) {
      const voce = mappingTipologie[selectedTipologia].find(
        (v) => v.value === selectedVoce
      );
      if (voce) {
        voce.duration.forEach((min) => {
          const opt = document.createElement("option");
          opt.value = min;
          opt.text = min === "Da definire" ? "Da definire" : `${min} minuti`;
          timeSelect.appendChild(opt);
        });
      }
    }
  });

  // Animazione apertura
  gsap.set(modale, { opacity: 0, display: "none", y: -50 });
  apriBtn.addEventListener("click", () => {
    gsap.set(modale, { display: "block" });
    gsap.to(modale, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" });
  });

  // Animazione chiusura
  const chiudiModale = () => {
    gsap.to(modale, {
      opacity: 0,
      y: -50,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => gsap.set(modale, { display: "none" }),
    });
  };

  chiudiBtn1.addEventListener("click", chiudiModale);
  chiudiBtn2.addEventListener("click", chiudiModale);
});




















/*  -----------------------------------------------------------------------------------------------
    MODALE AGGIUNGI UTENTE
--------------------------------------------------------------------------------------------------- */
// Selezioniamo il pulsante "add-user"
document.querySelectorAll('[title="add-user"]').forEach((btn) => {
  btn.addEventListener("click", function (e) {
    e.stopPropagation(); // Evita chiusure accidentali della modale principale

    // 1. Mostra l'overlay subito (senza animazioni)
    let addUserModal = document.getElementById("addUserModal");
    addUserModal.classList.remove("hidden-user-modal");

    // 2. Anima solo il contenuto interno con GSAP
    gsap.fromTo(
      ".modal-content-user",
      { opacity: 0, y: -50 },
      { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }
    );

    // Disabilita la modale principale finché è aperta la "seconda" modale
    document.getElementById("appointmentModal").style.pointerEvents = "none";
  });
});

// Chiudi la seconda modale senza chiudere la principale
document
  .getElementById("closeAddUserModal")
  .addEventListener("click", function () {
    gsap.to(".modal-content-user", {
      opacity: 0,
      y: -50,
      duration: 0.3,
      ease: "power2.out",
      onComplete: () => {
        let addUserModal = document.getElementById("addUserModal");
        addUserModal.classList.add("hidden-user-modal");
        document.getElementById("appointmentModal").style.pointerEvents =
          "auto";
        gsap.set(".modal-content-user", { opacity: 1, y: 0 });
      },
    });
  });

// Impedisce la chiusura della modale principale quando si clicca dentro la seconda
document.getElementById("addUserModal").addEventListener("click", function (e) {
  e.stopPropagation();
});

// gestione input prefissi
document.addEventListener("DOMContentLoaded", function () {
  // Lista di prefissi con bandiere
  const prefissi = [
    {
      value: "+39",
      flag: "/static/image/Bandiera-italia.png",
      country: "Italia",
      code: "IT",
    },
    {
      value: "+33",
      flag: "/static/image/Bandiera-francia.png",
      country: "Francia",
      code: "FR",
    },
    {
      value: "+44",
      flag: "/static/image/Bandiera-inghilterra.png",
      country: "Regno Unito",
      code: "GB",
    },
    {
      value: "+49",
      flag: "/static/image/Bandiera-germania.png",
      country: "Germania",
      code: "DE",
    },
    {
      value: "+34",
      flag: "/static/image/Bandiera-spagna.png",
      country: "Spagna",
      code: "ES",
    },
    {
      value: "+1",
      flag: "/static/image/Bandiera-usa.png",
      country: "Stati Uniti",
      code: "US",
    },
  ];

  const selectContainer = document.querySelector(".custom-select");
  const selectedOption = selectContainer.querySelector(".selected-option");
  const optionsList = selectContainer.querySelector(".options-list");
  const hiddenInput = document.getElementById("hidden-prefisso");

  // **1️⃣ Rileva la posizione dell'utente e imposta il prefisso corretto**
  async function setUserCountryPrefix() {
    try {
      const response = await fetch("https://ipapi.co/json/");
      const data = await response.json();

      // Trova il prefisso associato alla nazione
      const userPrefix = prefissi.find((p) => p.code === data.country);
      if (userPrefix) {
        updateSelectedPrefix(userPrefix);
      }
    } catch (error) {
      console.error("❌ Errore nel rilevare la posizione dell'utente:", error);
    }
  }

  // **2️⃣ Funzione per aggiornare il prefisso selezionato**
  function updateSelectedPrefix(prefisso) {
    selectedOption.innerHTML = `
            <img src="${prefisso.flag}" alt="${prefisso.country}" class="flag-icon">
            <span id="selected-prefix">${prefisso.value}</span>
        `;
    hiddenInput.value = prefisso.value;
  }

  // **3️⃣ Popola la lista delle opzioni dinamicamente**
  prefissi.forEach((prefisso) => {
    const li = document.createElement("li");
    li.innerHTML = `
            <img src="${prefisso.flag}" alt="${prefisso.country}" class="flag-icon">
            <span>${prefisso.value}</span>
        `;
    li.addEventListener("click", () => {
      updateSelectedPrefix(prefisso);
      optionsList.style.display = "none";
    });
    optionsList.appendChild(li);
  });

  // **4️⃣ Mostra/Nasconde il menu delle opzioni**
  selectedOption.addEventListener("click", () => {
    optionsList.style.display =
      optionsList.style.display === "block" ? "none" : "block";
    optionsList.paddingLeft = "0px";
  });

  // **5️⃣ Chiude il menu se si clicca fuori**
  document.addEventListener("click", (e) => {
    if (!selectContainer.contains(e.target)) {
      optionsList.style.display = "none";
    }
  });

  // **6️⃣ Imposta il prefisso predefinito in base alla nazione dell'utente**
  setUserCountryPrefix();
});

// Gestione input animati form
document.querySelectorAll(".input-container input").forEach((input) => {
  input.addEventListener("focus", function () {
    this.previousElementSibling.classList.add("active-label");
  });

  input.addEventListener("blur", function () {
    if (this.value === "") {
      this.previousElementSibling.classList.remove("active-label");
    }
  });
});

/*  -----------------------------------------------------------------------------------------------
   evento per aggiungere un paziente
--------------------------------------------------------------------------------------------------- */
document.getElementById("addUserForm").addEventListener("submit", function (e) {
  e.preventDefault();

  let newNameEl = document.getElementById("newName");
  let newSurnameEl = document.getElementById("newSurname");
  let newPhoneEl = document.getElementById("newCell");
  let newEmailEl = document.getElementById("newEmail");
  
  let newName = newNameEl.value.trim();
  let newSurname = newSurnameEl.value.trim();
  let newPhone = newPhoneEl.value.trim();
  let newEmail = newEmailEl.value.trim();
  

  // 🔹 Recupera il token CSRF
  function getCSRFToken() {
    let csrfTokenElement = document.querySelector(
      "input[name='csrfmiddlewaretoken']"
    );
    return csrfTokenElement ? csrfTokenElement.value : null;
  }

  if (!newName || !newSurname || !newPhone || !newEmail) {
    alert("Errore: Uno o più campi del form non sono stati trovati nel DOM.");
    return;
  }

  if (!newName || !newSurname) {
    showAlert({
      type: "danger",
      message: "Nome e cognome sono obbligatori!",
      extraMessage: "",
      borderColor: "#EF4444",
    });
    return;
  }

  let csrfToken = getCSRFToken();
  if (!csrfToken) {
    console.error("Errore: token CSRF non trovato nel DOM.");
    showAlert({
      type: "danger",
      message:
        "Errore di sicurezza: impossibile procedere. Ricarica la pagina e riprova.",
      extraMessage: "",
      borderColor: "#EF4444",
    });
    return;
  }

  fetch("/aggiungi-paziente/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      name: newName,
      surname: newSurname,
      email: newEmail,
      phone: newPhone,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        showAlert({
          type: "success",
          message: "Paziente aggiunto con successo!",
          extraMessage: "",
          borderColor: "var(--positive-color)",
        });
        // **AGGIORNAMENTO DINAMICO DEL SELECT**
        let selectPazienti = document.getElementById("paziente-select");
        if (selectPazienti) {
          let newOption = document.createElement("option");
          newOption.value = `${newName} ${newSurname}`;
          newOption.textContent = `${newName} ${newSurname}`;
          selectPazienti.appendChild(newOption);
        }
        // **Chiudi la modale senza ricaricare la pagina**
        let addUserModal = document.getElementById("addUserModal");
        addUserModal.classList.add("hidden-user-modal");
        document.getElementById("appointmentModal").style.pointerEvents =
          "auto";
        // **Svuota i campi del form**
        newNameEl.value = "";
        newSurnameEl.value = "";
        newPhoneEl.value = "";
        newEmailEl.value = "";
      } else {
        showAlert({
          type: "danger",
          message: "Errore: " + data.error,
          extraMessage: "",
          borderColor: "#EF4444",
        });
      }
    })
    .catch((error) =>
      showAlert({
        type: "danger",
        message: "Errore:",
        extraMessage: error,
        borderColor: "#EF4444",
      })
    );
});


























/*  -----------------------------------------------------------------------------------------------
   GESTIONE RENDERIZZAMENTO SU GOOGLE CALENDAR
--------------------------------------------------------------------------------------------------- */
// Converte una data dal formato "DD/MM/YYYY" a "YYYY-MM-DD"
function parseLocalDate(dateStr) {
  const parts = dateStr.split("/");
  if (parts.length === 3) {
    return `${parts[2]}-${parts[1].padStart(2, "0")}-${parts[0].padStart(
      2,
      "0"
    )}`;
  }
  return dateStr;
}

function addToGoogleCalendar(appointment) {
  let formattedDate = appointment.data;
  if (appointment.data.includes("/")) {
    formattedDate = parseLocalDate(appointment.data);
  }
  const startDateTime = new Date(`${formattedDate}T${appointment.orario}`);
  const duration = parseInt(appointment.durata) || 30;
  const endDateTime = new Date(startDateTime.getTime() + duration * 60000);
  function formatDateTime(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");
    return `${year}${month}${day}T${hours}${minutes}${seconds}`;
  }
  const startStr = formatDateTime(startDateTime);
  const endStr = formatDateTime(endDateTime);
  const title = encodeURIComponent(
    `${appointment.tipologia_visita} con ${appointment.nome_paziente || ""}`
  );
  const details = encodeURIComponent(appointment.note || "");
  const location = encodeURIComponent(
    "Via Nicola Tridente, 22, 70125 Bari BA, Italia"
  );
  const ctz = encodeURIComponent("Europe/Rome");
  const calendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${startStr}/${endStr}&details=${details}&location=${location}&ctz=${ctz}`;
  return calendarUrl;
}

document
  .getElementById("googleCalendarBtn")
  .addEventListener("click", function () {
    const dateElem = document.getElementById("date-appointment");
    let rawDate = dateElem.textContent.trim();
    rawDate = rawDate.replace(/,/g, "").trim();
    const appointment = {
      data: rawDate,
      orario: document.getElementById("time-appointment").textContent.trim(),
      tipologia_visita: document.getElementById("tipologia_visita").value,
      durata: document.getElementById("time").value,
      nome_paziente: document
        .getElementById("paziente-select")
        .value.split("|")[0],
      note: document.getElementById("note").value,
      numero_studio: document.getElementById("studio").value,
    };
    const calendarUrl = addToGoogleCalendar(appointment);
    window.open(calendarUrl, "_blank");
  });