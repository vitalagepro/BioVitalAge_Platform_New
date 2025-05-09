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
        Listener per la paginazione
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", function (event) {
    const target = event.target;

    // Se hai cliccato su un <a> dentro la paginazione
    if (target.closest(".pagination_tabella a")) {
      event.preventDefault();

      const link = target.closest("a");
      const url = link.href;

      fetch(url)
        .then((response) => response.text())
        .then((html) => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const newContent = doc.querySelector(".table-wrapper");
          document.querySelector(".table-wrapper").innerHTML =
            newContent.innerHTML;
        });
    }
  });
});



























/* -----------------------------------------------------------------------------------------------
   ATTIVA INPUT DATA/ORA PER VISITE (MODALE)
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const editBtn = document.getElementById("edit-date-btn");
  const dateInput = document.getElementById("editDate");
  const timeInput = document.getElementById("editTime");
  const form = document.getElementById("date-appointment-form");

  const daySpan = document.getElementById("day-appointment");
  const dateSpan = document.getElementById("date-appointment");
  const timeSpan = document.getElementById("time-appointment");

  const openBtn = document.getElementById("openModal"); // bottone "Aggiungi nuova visita"

  if (!editBtn || !dateInput || !timeInput || !form || !openBtn) return;

  // Al click su "Aggiungi nuova visita" => precompila data/orario
  openBtn.addEventListener("click", () => {
    const now = new Date();
    const giorno = 'Giorno, ';
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, "0");
    const dd = String(now.getDate()).padStart(2, "0");
    const formattedDate = `Data, `;
    const inputDateValue = `${yyyy}-${mm}-${dd}`;
    const formattedTime = "Orario";

    // aggiorna span
    daySpan.textContent = giorno;
    dateSpan.textContent = formattedDate;
    timeSpan.textContent = formattedTime;

    // aggiorna input
    dateInput.value = inputDateValue;
    timeInput.value = formattedTime;

    // nascondi input inizialmente
    dateInput.style.display = "none";
    timeInput.style.display = "none";
  });

  // Al click su "Edita" => mostra input e nascondi gli span
  editBtn.addEventListener("click", (e) => {
    e.preventDefault();
    dateInput.style.display = "inline-block";
    timeInput.style.display = "inline-block";
    daySpan.style.display = "none";
    dateSpan.style.display = "none";
    timeSpan.style.display = "none";
  });

  // Quando cambia data, aggiorna il giorno della settimana
  dateInput.addEventListener("change", () => {
    const selectedDate = new Date(dateInput.value);
    const giorni = ["Domenica", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"];
    const giorno = giorni[selectedDate.getDay()];
    daySpan.textContent = giorno;
    daySpan.style.display = "inline";
  });

  // Validazione al submit
  form.addEventListener("submit", (e) => {
    if (!dateInput.value || !timeInput.value) {
      e.preventDefault();
      showAlert({
        type: "danger",
        message: "Inserisci data e orario prima di salvare l'appuntamento.",
        extraMessage: "",
        borderColor: "#EF4444",
      });
    } else {
      // aggiorna gli span con i valori definitivi
      const [yyyy, mm, dd] = dateInput.value.split("-");
      dateSpan.textContent = `${dd}/${mm}/${yyyy}`;
      timeSpan.textContent = timeInput.value;
    }
  });
});












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




document.addEventListener("DOMContentLoaded", () => {
  const editBtn = document.getElementById("edit-date-btn");
  const dateInput = document.getElementById("editDate");
  const timeInput = document.getElementById("editTime");
  const container = document.getElementById("edit-date-container");

  const daySpan = document.getElementById("day-appointment");
  const dateSpan = document.getElementById("date-appointment");
  const timeSpan = document.getElementById("time-appointment");

  if (!editBtn || !dateInput || !timeInput || !container) return;

  editBtn.addEventListener("click", (e) => {
    e.preventDefault();

    // Mostra il container
    container.style.display = "flex"; // oppure "block" se preferisci in colonna
    dateInput.style.display = "inline-block";
    timeInput.style.display = "inline-block";

    // Nasconde gli span
    if (daySpan) daySpan.style.display = "none";
    if (dateSpan) dateSpan.style.display = "none";
    if (timeSpan) timeSpan.style.display = "none";
  });

  const saveBtn = document.getElementById("save-date-btn");
  
  editBtn.addEventListener("click", (e) => {
    e.preventDefault();
  
    container.style.display = "flex";
    dateInput.style.display = "inline-block";
    timeInput.style.display = "inline-block";
    saveBtn.style.display = "inline-block";
  
    daySpan.style.display = "none";
    dateSpan.style.display = "none";
    timeSpan.style.display = "none";
  });
  
  saveBtn.addEventListener("click", () => {
    const dateVal = dateInput.value;
    const timeVal = timeInput.value;
  
    if (!dateVal || !timeVal) {
      showAlert({
        type: "danger",
        message: "Inserisci data e ora prima di salvare.",
        extraMessage: "",
        borderColor: "#EF4444",
      });
      return;
    }
  
    const giorniSettimana = ["Domenica", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"];
    const dateObj = new Date(dateVal);
    const dayName = giorniSettimana[dateObj.getDay()];
  
    // Aggiorna gli span
    daySpan.textContent = dayName;
    dateSpan.textContent = dateVal.split("-").reverse().join("/");
    timeSpan.textContent = timeVal;
  
    // Mostra gli span
    daySpan.style.display = "inline";
    dateSpan.style.display = "inline";
    timeSpan.style.display = "inline";
  
    // Nascondi input e bottone
    dateInput.style.display = "none";
    timeInput.style.display = "none";
    saveBtn.style.display = "none";
    container.style.display = "none";
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const saveBtn = document.getElementById("saveAppointmentBtn");

  saveBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

    const date = document.getElementById("editDate").value;
    const time = document.getElementById("editTime").value;
    const day = document.getElementById("day-appointment").textContent.trim();
    const tipologia = document.getElementById("tipologia_visita").value;
    const vocePrezzario = document.getElementById("voce-prezzario").value;
    const durata = document.getElementById("time").value;
    const studio = document.getElementById("studio").value;
    const note = document.getElementById("note").value;
    const pazienteVal = document.getElementById("paziente-select").value;

    if (!date || !time || !tipologia || !vocePrezzario || !durata || !studio || !pazienteVal) {
      showAlert({
        type: "danger",
        message: "⚠️ Compila tutti i campi obbligatori prima di salvare.",
        borderColor: "#EF4444",
      });
      return;
    }

    const [nomeCompleto, pazienteId] = pazienteVal.split("|");
    const [nome, cognome] = nomeCompleto.trim().split(" ");

    const payload = {
      giorno: day,
      data: date,
      orario: time,
      tipologia_visita: tipologia,
      voce_prezzario: vocePrezzario,
      durata: durata,
      numero_studio: studio,
      note: note,
      nome_paziente: nome || "",
      cognome_paziente: cognome || "",
    };

    try {
      const response = await fetch("/salva-appuntamento/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (result.success) {
        showAlert({
          type: "success",
          message: "✅ Appuntamento salvato con successo!",
          extraMessage: "",
          borderColor: "var(--positive-color)",
        });

        // ✅ RESETTA I CAMPI DELLA MODALE
        document.getElementById("tipologia_visita").selectedIndex = 0;
        document.getElementById("voce-prezzario").innerHTML = `<option>Seleziona una Voce</option>`;
        document.getElementById("time").innerHTML = `<option>Seleziona una Durata</option>`;
        document.getElementById("studio").selectedIndex = 0;
        document.getElementById("paziente-select").selectedIndex = 0;
        document.getElementById("note").value = "";

        // ✅ RESET DATE/TIME
        const oggi = new Date();
        const yyyy = oggi.getFullYear();
        const mm = String(oggi.getMonth() + 1).padStart(2, "0");
        const dd = String(oggi.getDate()).padStart(2, "0");
        const defaultTime = "09:00";

        document.getElementById("editDate").value = `${yyyy}-${mm}-${dd}`;
        document.getElementById("editTime").value = defaultTime;
        document.getElementById("day-appointment").textContent = "";
        document.getElementById("date-appointment").textContent = "";
        document.getElementById("time-appointment").textContent = "";

        // ✅ RIPRISTINA visibilità SPAN e nasconde gli input
        document.getElementById("editDate").style.display = "none";
        document.getElementById("editTime").style.display = "none";
        document.getElementById("day-appointment").style.display = "inline";
        document.getElementById("date-appointment").style.display = "inline";
        document.getElementById("time-appointment").style.display = "inline";

        // ✅ CHIUDI MODALE
        gsap.to("#appointmentModal", {
          opacity: 0,
          y: -50,
          duration: 0.3,
          ease: "power2.in",
          onComplete: () => {
            document.getElementById("appointmentModal").style.display = "none";
            document.body.style.overflow = "auto";
          },
        });
      } else {
        showAlert({
          type: "danger",
          message: result.error || "Errore sconosciuto",
          borderColor: "#EF4444",
        });
      }
    } catch (err) {
      console.error("❌ Errore fetch:", err);
      showAlert({
        type: "danger",
        message: "Errore di rete: " + err.message,
        borderColor: "#EF4444",
      });
    }
  });
});