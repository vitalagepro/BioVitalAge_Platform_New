/*  -----------------------------------------------------------------------------------------------
  LAYOUT
--------------------------------------------------------------------------------------------------- */
const monthLayoutBtn = document.getElementById("monthLayout");
const weekLayoutBtn = document.getElementById("weekLayout");

const headWeek = document.getElementById("week-head");
const weekLayout = document.getElementById("week-layout");

const monthWeek = document.getElementById("month-head");
const monthLayout = document.getElementById("month-layout");

/* RESET FUNCTION */
function resetMonthLayout() {
  monthLayout.style.display = "grid";
  monthWeek.style.display = "flex";
  document.querySelectorAll(".cella").forEach((cella) => {
    cella.style.display = "block";
  });
}

/* SETTING WEEK LAYOUT */
weekLayoutBtn.addEventListener("click", () => {
  monthLayoutBtn.classList.remove("active");
  weekLayoutBtn.classList.add("active");

  monthWeek.style.display = "none";
  monthLayout.style.display = "none";

  headWeek.style.display = "block";
  weekLayout.style.display = "block";
});

/* SETTING MONTH LAYOUT */
monthLayoutBtn.addEventListener("click", () => {
  weekLayoutBtn.classList.remove("active");
  monthLayoutBtn.classList.add("active");

  headWeek.style.display = "none";
  weekLayout.style.display = "none";

  resetMonthLayout();
});

/*  -----------------------------------------------------------------------------------------------
                                    DYNAMIC CALENDAR & MODAL APPEARS
--------------------------------------------------------------------------------------------------- */
let currentDate = new Date(); // Definisci la variabile globalmente
let selectedAppointment = null;

/* LOAD APPOINTMENTS */
function loadAppointments() {
  fetch("/get-appointments/")
    .then((response) => response.json())
    .then((appointmentsByDate) => {
      console.log("📢 Appuntamenti ricevuti dal backend:", appointmentsByDate);

      document.querySelectorAll(".cella").forEach((cell) => {
        const cellDay = cell.dataset.day;
        const cellMonth = cell.dataset.month;
        const cellYear = cell.dataset.year;

        if (!cellDay || !cellMonth || !cellYear) return;

        const formattedDate = `${cellYear}-${String(cellMonth).padStart(
          2,
          "0"
        )}-${String(cellDay).padStart(2, "0")}`;

        const appointmentsContainer = cell.querySelector(
          ".appointments-container"
        );
        appointmentsContainer.innerHTML = "";

        if (appointmentsByDate.appointments[formattedDate]) {
          appointmentsByDate.appointments[formattedDate].forEach(
            (appointment) => {
              if (!appointment.id || appointment.id === "") {
                console.error("❌ Errore: Appuntamento senza ID!", appointment);
              } else {
                addAppointmentToCell(
                  cell,
                  appointment.tipologia_visita,
                  appointment.orario,
                  appointment.id
                );
              }
            }
          );
        }
      });
    })
    .catch((error) =>
      console.error("❌ Errore nel caricamento appuntamenti:", error)
    );
}

// Funzione per formattare la data in YYYY-MM-DD per il backend
function formatDateForBackend(date, day) {
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Mese in due cifre
  const year = date.getFullYear();
  const dayFormatted = String(day).padStart(2, "0"); // Giorno in due cifre
  return `${year}-${month}-${dayFormatted}`;
}

// Aggiorna la data di un appuntamento nel backend
function updateAppointmentDate(appointmentId, newDate) {
  if (!appointmentId || !newDate) {
    console.error("❌ Errore: appointmentId o newDate non valido!", { appointmentId, newDate });
    return;
  }

  // Recupera il token CSRF dal campo hidden (assicurati che l'input esista nel DOM)
  const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']")?.value || '';

  fetch(`/update-appointment/${appointmentId}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken, // Includi il token CSRF
    },
    body: JSON.stringify({ new_date: newDate }),
  })
    .then((response) => {
      console.log(`📢 Risposta HTTP: ${response.status}`);
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        console.log("✅ Appuntamento spostato con successo!"); // Debug
      } else {
        showAlert("danger", `Errore nello spostamento dell'appuntamento: ${data.error}`);
      }
    })
    .catch((error) => console.error("❌ Errore nella richiesta:", error));
}

// Funzione per aggiungere un appuntamento alla cella
function addAppointmentToCell(cella, tipologia, orario, appointmentId) {
  const appointmentsContainer = cella.querySelector(".appointments-container");

  let appointmentBox = document.createElement("div");
  appointmentBox.classList.add("appointment-box");
  appointmentBox.setAttribute("draggable", "true");

  // Assicurati che l'ID sia una stringa valida
  appointmentId = appointmentId ? String(appointmentId) : "";
  if (!appointmentId.trim()) {
    console.error("❌ Errore: appointmentId non valido durante la creazione!", { appointmentId });
    return;
  }
  appointmentBox.dataset.id = appointmentId;

  let formattedTime = orario ? orario.slice(0, 5) : "00:00";
  let textSpan = document.createElement("span");
  textSpan.textContent = `${tipologia} - ${formattedTime}`;
  textSpan.style.flex = "1";

  let deleteButton = document.createElement("button");
  deleteButton.innerHTML = "&times;";
  deleteButton.classList.add("delete-appointment");
  deleteButton.setAttribute("data-id", appointmentId);
  deleteButton.addEventListener("click", (event) => {
    event.stopPropagation();
    confirmDeleteAppointment(appointmentId, appointmentBox);
  });

  appointmentBox.appendChild(textSpan);
  appointmentBox.appendChild(deleteButton);
  appointmentsContainer.appendChild(appointmentBox);

  // Event listener per il drag
  appointmentBox.addEventListener("dragstart", (e) => {
    selectedAppointment = e.target;
  });

  // Event listener per il click sull'appointment-box
  appointmentBox.addEventListener("click", (e) => {
    e.stopPropagation(); // Impedisce il bubble verso la cella
    const appointmentId = appointmentBox.dataset.id;
    if (appointmentId) {
      openAppointmentModal(appointmentId);
    }
  });
}

// Funzione per aprire la modale
function openAppointmentModal(appointmentId) {
  fetch(`/get-appointment/${appointmentId}/`)
    .then((response) => response.json())
    .then((data) => {
      console.log("📢 DEBUG: Dati ricevuti dal backend:", data); // 🔍 Debug per vedere i valori

      if (data.success) {
        // 🔹 Popoliamo i campi della modale con i dati ricevuti dal backend
        document.getElementById("day-appointment").textContent = data.giorno;
        const dateParts = data.data.split("-");
        const formattedDate = `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
        document.getElementById("date-appointment").textContent =
          formattedDate + ", ";
        document.getElementById("time-appointment").textContent =
          data.orario.slice(0, 5);
        document.getElementById("tipologia_visita").value =
          data.tipologia_visita || "";

        // 🔹 GESTIONE SELEZIONE PAZIENTE
        let pazienteSelect = document.getElementById("paziente-select");
        function normalizeName(name) {
          return name.trim().toLowerCase();
        }

        let nomeCompletoBackend = normalizeName(
          `${data.nome_paziente} ${data.cognome_paziente}`
        );

        let pazienteOption = [...pazienteSelect.options].find(
          (option) => normalizeName(option.value) === nomeCompletoBackend
        );

        if (pazienteOption) {
          pazienteSelect.value = pazienteOption.value; // ✅ Se esiste, lo selezioniamo
        } else {
          // ❗ Se non esiste, creiamo una nuova option con stile diverso
          let newOption = document.createElement("option");
          newOption.value = nomeCompletoBackend;
          newOption.textContent = `${data.nome_paziente} ${data.cognome_paziente} (Non in elenco)`;
          newOption.style.color = "red";
          pazienteSelect.appendChild(newOption);
          pazienteSelect.value = nomeCompletoBackend;
        }

        // 🔹 GESTIONE SELEZIONE VOCE PREZZARIO
        let vocePrezzarioSelect = document.getElementById("voce-prezzario");
        let voceOption = [...vocePrezzarioSelect.options].find(
          (option) =>
            option.value.trim().toLowerCase() ===
            data.voce_prezzario?.toLowerCase()
        );

        if (voceOption) {
          vocePrezzarioSelect.value = voceOption.value;
        } else if (data.voce_prezzario) {
          let newVoceOption = document.createElement("option");
          newVoceOption.value = data.voce_prezzario;
          newVoceOption.textContent = data.voce_prezzario + " (Non in elenco)";
          newVoceOption.style.color = "red";
          vocePrezzarioSelect.appendChild(newVoceOption);
          vocePrezzarioSelect.value = data.voce_prezzario;
        }

        // 🔹 GESTIONE SELEZIONE DURATA
        let durataSelect = document.getElementById("time");
        let durataOption = [...durataSelect.options].find(
          (option) =>
            option.value.trim().toLowerCase() === data.durata?.toLowerCase()
        );

        if (durataOption) {
          durataSelect.value = durataOption.value;
        } else if (data.durata) {
          let newDurataOption = document.createElement("option");
          newDurataOption.value = data.durata;
          newDurataOption.textContent = data.durata + " (Non in elenco)";
          newDurataOption.style.color = "red";
          durataSelect.appendChild(newDurataOption);
          durataSelect.value = data.durata;
        }

        // 🔹 GESTIONE SELEZIONE NUMERO STUDIO
        let studioSelect = document.getElementById("studio");
        if (
          [...studioSelect.options].some(
            (option) => option.value === data.numero_studio
          )
        ) {
          studioSelect.value = data.numero_studio;
        } else {
          studioSelect.selectedIndex = 0; // Se non esiste, seleziona la prima opzione
        }

        // 🔹 ASSEGNA NOTE SE PRESENTI
        document.getElementById("note").value = data.note || "";

        // 🔹 Salviamo l'ID dell'appuntamento per la modifica
        document
          .getElementById("date-appointment-form")
          .setAttribute("data-id", appointmentId);

        // 🔹 Apriamo la modale con GSAP
        document.getElementById("appointmentModal").style.display = "block";
        document.body.style.overflow = "hidden";
        gsap.fromTo(
          document.querySelector(".modal-content-appointments"),
          { opacity: 0, scale: 0.8 },
          { opacity: 1, scale: 1, duration: 0.3, ease: "power2.out" }
        );
      } else {
        console.error("❌ Errore nel recupero dati appuntamento:", data.error);
      }
    })
    .catch((error) => console.error("❌ Errore nella richiesta:", error));
}

// Funzione per salvare le modifiche all'appuntamento
function saveAppointmentChanges() {
  const appointmentId = document
    .getElementById("date-appointment-form")
    .getAttribute("data-id");
  const updatedTipologia = document.getElementById("tipologia_visita").value;
  const updatedOrario = document
    .getElementById("time-appointment")
    .textContent.trim();
  const updatedPaziente = document.getElementById("paziente-select").value;
  const updatedVocePrezzario = document.getElementById("voce-prezzario").value;
  const updatedDurata = document.getElementById("time").value;
  const updatedStudio = document.getElementById("studio").value;
  const updatedNote = document.getElementById("note").value;

  fetch(`/update-appointment/${appointmentId}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      tipologia_visita: updatedTipologia,
      orario: updatedOrario,
      paziente_id: updatedPaziente,
      voce_prezzario: updatedVocePrezzario,
      durata: updatedDurata,
      numero_studio: updatedStudio,
      note: updatedNote,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log("Appuntamento aggiornato con successo!");
        location.reload(); // Ricarica la pagina per aggiornare il calendario
      } else {
        console.error("Errore aggiornamento appuntamento:", data.error);
      }
    })
    .catch((error) => console.error("Errore nella richiesta:", error));
}

// Funzione per eliminare un appuntamento
function deleteAppointment(appointmentId, appointmentBox, confirmAlert) {
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
        // 🔹 Effetto GSAP per la rimozione fluida del box appuntamento
        gsap.to(appointmentBox, {
          opacity: 0,
          duration: 0.3,
          ease: "power2.in",
          onComplete: () => appointmentBox.remove(),
        });

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

// Funzione per confermare l'eliminazione di un appuntamento tramite modale bootstrap// Funzione per confermare l'eliminazione di un appuntamento tramite modale bootstrap con GSAP
function confirmDeleteAppointment(appointmentId, appointmentBox) {
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
  confirmAlert.style.maxWidth = "400px";
  confirmAlert.style.display = "flex";
  confirmAlert.style.justifyContent = "space-between";
  confirmAlert.style.alignItems = "center";
  confirmAlert.style.padding = "10px 15px";
  confirmAlert.style.borderRadius = "6px";
  confirmAlert.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";
  confirmAlert.style.opacity = "0"; // 🔹 Opacità iniziale per GSAP

  confirmAlert.innerHTML = `
      <span>Sei sicuro di voler eliminare questo appuntamento?</span>
      <div>
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
    deleteAppointment(appointmentId, appointmentBox, confirmAlert);
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
  alertDiv.style.zIndex = "1050";
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

// Funzione principale
document.addEventListener("DOMContentLoaded", () => {
  /***********************************************************************
   * SEZIONE 1: LOGICA DEL CALENDARIO
   ***********************************************************************/
  // -----------------------------
  // RIFERIMENTI ELEMENTI CALENDARIO
  // -----------------------------
  const monthLayoutBtn = document.getElementById("monthLayout");
  const weekLayoutBtn = document.getElementById("weekLayout");
  const dayLayoutBtn = document.getElementById("dayLayout");

  const monthLayoutContainer = document.getElementById("month-layout");
  const weekLayoutContainer = document.getElementById("week-layout");
  // const dayLayoutContainer = document.getElementById("day-layout"); // se esiste

  const monthHead = document.getElementById("month-head");
  const weekHead = document.getElementById("week-head");
  // const dayHead = document.getElementById("day-head");

  const btnPrev = document.querySelector(".prev");
  const btnNext = document.querySelector(".next");
  const btnToday = document.getElementById("currentBtn");
  const datePicker = document.getElementById("date");
  const currentDataLabel = document.getElementById("currentData");

  // Modale
  const appointmentModal = document.getElementById("appointmentModal"); // overlay
  const modalContent = document.querySelector(".modal-content-appointments"); // contenuto modale
  const btnCloseModal = document.getElementById("closeModalBtn");
  const iconCloseModal = document.getElementById("closeModal");

  // Pulsante "Appuntamento"
  const btnOpenModal = document.getElementById("openModal");

  // Variabili data
  let currentDate = new Date();
  let selectedDayCell = null; // cella cliccata

  // -----------------------------
  // FUNZIONI UTILI CALENDARIO
  // -----------------------------
  function formatDateLabel(date) {
    const monthNames = [
      "Gennaio",
      "Febbraio",
      "Marzo",
      "Aprile",
      "Maggio",
      "Giugno",
      "Luglio",
      "Agosto",
      "Settembre",
      "Ottobre",
      "Novembre",
      "Dicembre",
    ];
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear();
    return `${month} ${year}`;
  }

  function checkIfToday(year, month, day) {
    const today = new Date();
    return (
      year === today.getFullYear() &&
      month === today.getMonth() &&
      day === today.getDate()
    );
  }

  // -----------------------------
  // GENERAZIONE CALENDARIO MENSILE
  // -----------------------------
// Durante la generazione del calendario mensile, aggiungi la classe "past-day" se la data è passata
function renderMonthCalendar() {
  monthLayoutContainer.innerHTML = "";

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const firstDayOfMonth = new Date(year, month, 1);
  const lastDayOfMonth = new Date(year, month + 1, 0);

  let startIndex = firstDayOfMonth.getDay();
  if (startIndex === 0) startIndex = 7;

  const totalDaysInMonth = lastDayOfMonth.getDate();

  // Data di oggi (senza ore, minuti, secondi)
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Celle vuote prima del 1° giorno
  for (let i = 1; i < startIndex; i++) {
    const emptyCell = document.createElement("div");
    emptyCell.classList.add("cella", "empty-cell");
    monthLayoutContainer.appendChild(emptyCell);
  }

  // Genera le celle dei giorni
// Durante la generazione delle celle nel calendario:
for (let day = 1; day <= totalDaysInMonth; day++) {
  const cella = document.createElement("div");
  cella.classList.add("cella");

  // Imposta i dataset per giorno, mese e anno
  cella.dataset.day = day;
  cella.dataset.month = month + 1; // Mese in base 1
  cella.dataset.year = year;

  const dayParagraph = document.createElement("p");
  dayParagraph.classList.add("data");
  dayParagraph.textContent = day;

  const appointmentsContainer = document.createElement("div");
  appointmentsContainer.classList.add("appointments-container");

  // Controlla se la data della cella è passata
  const cellDate = new Date(year, month, day);
  cellDate.setHours(0, 0, 0, 0);
  if (cellDate < today) {
    cella.classList.add("past-day");
  }

  // Aggiungi listener per drag & drop e per il click solo se la cella non è passata
  if (!cella.classList.contains("past-day")) {
    cella.addEventListener("dragover", (e) => {
      e.preventDefault();
    });

    cella.addEventListener("drop", (e) => {
      e.preventDefault();
      if (selectedAppointment) {
        const appointmentsContainer = cella.querySelector(".appointments-container");
        if (!appointmentsContainer.contains(selectedAppointment)) {
          appointmentsContainer.appendChild(selectedAppointment);

          // Recupera la nuova data dalla cella e aggiorna l'appuntamento
          const newDay = cella.dataset.day;
          const newMonth = cella.dataset.month;
          const newYear = cella.dataset.year;
          if (newDay && newMonth && newYear) {
            const newDate = `${newYear}-${String(newMonth).padStart(2, "0")}-${String(newDay).padStart(2, "0")}`;
            updateAppointmentDate(selectedAppointment.dataset.id, newDate);
          }
          selectedAppointment = null;
        }
      }
    });

    cella.addEventListener("click", (e) => {
      if (e.target.closest('.appointment-box')) return; // Se il click è sull'appointment-box, non aprire la modale per un nuovo appuntamento
      selectedDayCell = cella;
      // Crea l'oggetto Date basandoti sui dataset della cella
      const selectedDate = new Date(
        parseInt(cella.dataset.year),
        parseInt(cella.dataset.month) - 1, // il mese in Date è 0-indexed
        parseInt(cella.dataset.day)
      );
      fillFormForNewAppointment(selectedDate);
      openModalWithGSAP();
    });      
  } else {
    // Se la cella rappresenta un giorno passato, disabilita l'interazione
    cella.style.pointerEvents = "none";
  }

  cella.appendChild(dayParagraph);
  cella.appendChild(appointmentsContainer);
  monthLayoutContainer.appendChild(cella);
}


  // Carica gli appuntamenti dopo aver generato il calendario
  loadAppointments();
  currentDataLabel.textContent = formatDateLabel(currentDate);
}


  // -----------------------------
  // NAVIGAZIONE CALENDARIO
  // -----------------------------
  btnPrev.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderMonthCalendar();
  });
  btnNext.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderMonthCalendar();
  });
  btnToday.addEventListener("click", () => {
    currentDate = new Date();
    renderMonthCalendar();
  });
  datePicker.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val) {
      const [yyyy, mm, dd] = val.split("-");
      currentDate = new Date(parseInt(yyyy), parseInt(mm) - 1, parseInt(dd));
      renderMonthCalendar();
    }
  });

  // -----------------------------
  // SWITCH LAYOUT
  // -----------------------------
  monthLayoutBtn.addEventListener("click", () => {
    monthLayoutBtn.classList.add("active");
    weekLayoutBtn.classList.remove("active");
    dayLayoutBtn.classList.remove("active");

    monthHead.style.display = "flex";
    monthLayoutContainer.style.display = "grid";
    weekHead.style.display = "none";
    weekLayoutContainer.style.display = "none";
    // dayHead.style.display = "none";
    // dayLayoutContainer.style.display = "none";

    renderMonthCalendar();
  });
  weekLayoutBtn.addEventListener("click", () => {
    weekLayoutBtn.classList.add("active");
    monthLayoutBtn.classList.remove("active");
    dayLayoutBtn.classList.remove("active");

    weekHead.style.display = "block";
    weekLayoutContainer.style.display = "block";
    monthHead.style.display = "none";
    monthLayoutContainer.style.display = "none";
    // dayHead.style.display = "none";
    // dayLayoutContainer.style.display = "none";
  });
  dayLayoutBtn.addEventListener("click", () => {
    dayLayoutBtn.classList.add("active");
    monthLayoutBtn.classList.remove("active");
    weekLayoutBtn.classList.remove("active");

    // dayHead.style.display = "block";
    // dayLayoutContainer.style.display = "block";
    monthHead.style.display = "none";
    monthLayoutContainer.style.display = "none";
    weekHead.style.display = "none";
    weekLayoutContainer.style.display = "none";
  });

  // -----------------------------
  // APERTURA / CHIUSURA MODALE
  // -----------------------------
  function openModalWithGSAP() {
    appointmentModal.style.display = "block"; // overlay
    document.body.style.overflow = "hidden";
    gsap.fromTo(
      modalContent,
      { opacity: 0, scale: 0.8 },
      { opacity: 1, scale: 1, duration: 0.3, ease: "power2.out" }
    );
  }

  function closeModalWithGSAP() {
    document.body.style.overflow = "auto";
    gsap.to(modalContent, {
      opacity: 0,
      scale: 0.8,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => {
        appointmentModal.style.display = "none";
        // Se avevo cliccato su una cella e ho aggiunto anteprima
        if (selectedDayCell) {
          removeAppointmentPreview(selectedDayCell);
          selectedDayCell = null;
        }
      },
    });
  }

  btnCloseModal.addEventListener("click", closeModalWithGSAP);
  iconCloseModal.addEventListener("click", closeModalWithGSAP);

  // Se clicco sul pulsante "Appuntamento"
  btnOpenModal.addEventListener("click", () => {
    // Rimuovo eventuale anteprima e resetto la cella selezionata
    if (selectedDayCell) {
      removeAppointmentPreview(selectedDayCell);
      selectedDayCell = null;
    }
    
    // Resetta il form per un nuovo appuntamento
    fillFormForNewAppointment();
  
    // Se necessario, resetta anche gli input del form (oltre agli span)
    document.getElementById("tipologia_visita").selectedIndex = 0;
    document.getElementById("paziente-select").selectedIndex = 0;
    document.getElementById("voce-prezzario").selectedIndex = 0;
    document.getElementById("time").selectedIndex = 0;
    document.getElementById("studio").selectedIndex = 0;
    document.getElementById("note").value = "";
    
    // Apri la modale con l'animazione
    openModalWithGSAP();
  });  

  // -----------------------------
  // ANTEPRIMA APPUNTAMENTO NELLA CELLA
  // -----------------------------
  function showAppointmentPreview(cella) {
    let preview = document.createElement("div");
    preview.classList.add("appointment-preview");
    preview.textContent = "Anteprima";
    // Stili minimi, poi gestiscili nel tuo CSS
    preview.style.border = "1px solid #3a255d";
    preview.style.marginTop = "5px";
    preview.style.padding = "2px 4px";
    preview.style.fontSize = "0.7rem";
    preview.style.borderRadius = "4px";
    cella.appendChild(preview);
  }
  function removeAppointmentPreview(cella) {
    let preview = cella.querySelector(".appointment-preview");
    if (preview) {
      cella.removeChild(preview);
    }
  }

  // Avvio di default sulla vista Mese
  monthLayoutBtn.click();

  /***********************************************************************
   * SEZIONE 2: LOGICA DEL FORM (autocompletamento <span>, edit, salvataggio)
   ***********************************************************************/
  // Riferimenti ai <span> e agli input nascosti
  const daySpan = document.getElementById("day-appointment");
  const dateSpan = document.getElementById("date-appointment");
  const timeSpan = document.getElementById("time-appointment");

  const editDateBtn = document.getElementById("edit-date-btn");
  const editDateContainer = document.getElementById("edit-date-container");
  const editDateInput = document.getElementById("editDate");
  const editTimeInput = document.getElementById("editTime");

  // Flag: ci dice se abbiamo aperto la modale da un giorno del calendario (true) o dal pulsante "Appuntamento" (false)
  let fromCalendar = false;

  // Array dei giorni in italiano
  const giorniSettimana = [
    "Domenica",
    "Lunedì",
    "Martedì",
    "Mercoledì",
    "Giovedì",
    "Venerdì",
    "Sabato",
  ];

  // Formatta data in DD/MM/YYYY
  function formatItalianDate(dateObj) {
    const dd = String(dateObj.getDate()).padStart(2, "0");
    const mm = String(dateObj.getMonth() + 1).padStart(2, "0");
    const yyyy = dateObj.getFullYear();
    return `${dd}/${mm}/${yyyy}`;
  }
  function getItalianDayName(dateObj) {
    return giorniSettimana[dateObj.getDay()];
  }

  /**
   * Se ho cliccato sul calendario, compilo i <span> con data e orario
   */
  function fillFormForCalendar(selectedDate) {
    fromCalendar = true;
    daySpan.textContent = getItalianDayName(selectedDate) + ",";
    dateSpan.textContent = formatItalianDate(selectedDate) + ",";
    timeSpan.textContent = "09:00"; // orario di default

    // Nascosti gli input
    editDateContainer.style.display = "none";
    editDateInput.style.display = "none";
    editTimeInput.style.display = "none";
  }

  /**
   * Se ho cliccato su "Appuntamento", metto placeholder
   */
  function fillFormForNewAppointment(selectedDate) {
    fromCalendar = false;
    // Se è stata passata una data, usala per compilare i <span> dinamicamente
    if (selectedDate instanceof Date) {
      daySpan.textContent = getItalianDayName(selectedDate) + ",";
      dateSpan.textContent = formatItalianDate(selectedDate) + ",";
    } else {
      daySpan.textContent = "Giorno,";
      dateSpan.textContent = "Data,";
    }
    timeSpan.textContent = "Orario"; // placeholder per l'orario
  
    // Nascondi i campi per l'editing (se non servono all'apertura)
    editDateContainer.style.display = "none";
    editDateInput.style.display = "none";
    editTimeInput.style.display = "none";
  }  

  /***********************************************************************
   * TOGGLE EDIT ↔ SALVA
   * Al primo click su "Edita" → mostro input, passo a "Salva"
   * Al secondo click → salvo, nascondo input, passo a "Edita"
   ***********************************************************************/
  let isEditing = false;

  // HTML da mostrare quando siamo in modalità "Edita"
  // (cioè la tua icona e testo)
  const editHTML = `
  <svg class="svg" viewBox="0 0 512 512">
    <path d="M410.3 231l11.3-11.3-33.9-33.9-62.1-62.1L291.7 89.8l-11.3 11.3-22.6 22.6L58.6 322.9c-10.4 10.4-18 23.3-22.2 37.4L1 480.7c-2.5 8.4-.2 17.5 6.1 23.7s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L387.7 253.7 410.3 231zM160 399.4l-9.1 22.7c-4 3.1-8.5 5.4-13.3 6.9L59.4 452l23-78.1c1.4-4.9 3.8-9.4 6.9-13.3l22.7-9.1v32c0 8.8 7.2 16 16 16h32zM362.7 18.7L348.3 33.2 325.7 55.8 314.3 67.1l33.9 33.9 62.1 62.1 33.9 33.9 11.3-11.3 22.6-22.6 14.5-14.5c25-25 25-65.5 0-90.5L453.3 18.7c-25-25-65.5-25-90.5 0zm-47.4 168l-144 144c-6.2 6.2-16.4 6.2-22.6 0s-6.2-16.4 0-22.6l144-144c6.2-6.2 16.4-6.2 22.6 0s6.2 16.4 0 22.6z"></path>
  </svg>
`;

  // HTML da mostrare quando siamo in modalità "Salva" (icona a tua scelta)
  const saveHTML = ` 
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              width="30"
              height="30"
              class="svg save-icon"
            >
              <path
                d="M22,15.04C22,17.23 20.24,19 18.07,19H5.93C3.76,19 2,17.23 2,15.04C2,13.07 3.43,11.44 5.31,11.14C5.28,11 5.27,10.86 5.27,10.71C5.27,9.33 6.38,8.2 7.76,8.2C8.37,8.2 8.94,8.43 9.37,8.8C10.14,7.05 11.13,5.44 13.91,5.44C17.28,5.44 18.87,8.06 18.87,10.83C18.87,10.94 18.87,11.06 18.86,11.17C20.65,11.54 22,13.13 22,15.04Z"
              ></path>
            </svg>
`;

  editDateBtn.innerHTML = editHTML; // di default è la modalità "Edita"

  // Listener sul link "Edita/Salva"
  editDateBtn.addEventListener("click", (e) => {
    e.preventDefault(); // evita eventuali comportamenti di <a>

    if (!isEditing) {
      // PRIMO CLICK -> ENTRO IN MODALITÀ EDIT
      isEditing = true;
      editDateBtn.innerHTML = saveHTML;

      // Mostro i campi input
      editDateContainer.style.display = "block";

      if (fromCalendar) {
        // Se la modale viene dal calendario -> SOLO time
        editDateInput.style.display = "none";
        editTimeInput.style.display = "inline-block";

        if (timeSpan.textContent.includes(":")) {
          const [hh, mm] = timeSpan.textContent.split(":");
          if (hh && mm) {
            editTimeInput.value =
              hh.padStart(2, "0") + ":" + mm.padStart(2, "0");
          }
        }
      } else {
        // Se vengo dal pulsante "Appuntamento" -> date + time
        editDateInput.style.display = "inline-block";
        editTimeInput.style.display = "inline-block";

        // Valori di default (oppure puoi parzialmente leggere dagli span)
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, "0");
        const dd = String(today.getDate()).padStart(2, "0");
        editDateInput.value = `${yyyy}-${mm}-${dd}`;
        editTimeInput.value = "09:00";
      }
    } else {
      // SECONDO CLICK -> SALVO MODIFICHE E TORNO A MODALITÀ VIEW
      isEditing = false;
      editDateBtn.innerHTML = editHTML;

      if (fromCalendar) {
        // Aggiorno solo orario
        const newTime = editTimeInput.value;
        if (newTime) {
          timeSpan.textContent = newTime;
        }
      } else {
        // Aggiorno data e orario
        const newDate = editDateInput.value;
        const newTime = editTimeInput.value;

        // Se c'è una data, la formatto e aggiorno i <span>
        if (newDate) {
          const parts = newDate.split("-");
          if (parts.length === 3) {
            const y = parseInt(parts[0]);
            const m = parseInt(parts[1]) - 1;
            const d = parseInt(parts[2]);
            const tmpDate = new Date(y, m, d);
            daySpan.textContent = getItalianDayName(tmpDate) + ",";
            dateSpan.textContent = formatItalianDate(tmpDate) + ",";
          }
        }
        if (newTime) {
          timeSpan.textContent = newTime;
        }
      }

      // Nascondo di nuovo i campi input
      editDateContainer.style.display = "none";
      editDateInput.style.display = "none";
      editTimeInput.style.display = "none";
    }
  });
});

/*  -----------------------------------------------------------------------------------------------
                              Saving form data
--------------------------------------------------------------------------------------------------- */
function convertDateFormat(dateString) {
  if (!dateString) return "";
  const parts = dateString.replace(/[^0-9\/]/g, "").split("/"); // Rimuove caratteri extra e split su "/"
  if (parts.length === 3) {
    return `${parts[2]}-${parts[1].padStart(2, "0")}-${parts[0].padStart(
      2,
      "0"
    )}`; // Converte DD/MM/YYYY → YYYY-MM-DD
  }
  return dateString; // Ritorna la stringa originale se il formato è già corretto
}

// Listener sul pulsante "Salva"
document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector(".btn-primary")
    .addEventListener("click", function (event) {
      event.preventDefault(); // 🔹 Evita il comportamento predefinito del pulsante

      // 🔹 Ottieni il nome completo dal <select>
      const pazienteSelect = document.getElementById("paziente-select");
      const nomeCompleto = pazienteSelect.selectedOptions[0]?.text.trim() || "";

      // 🔹 Dividiamo nome e cognome senza troncare i cognomi composti
      const nomeArray = nomeCompleto.split(" ");
      const nome_paziente = nomeArray[0]; // Il primo elemento è il nome
      const cognome_paziente = nomeArray.slice(1).join(" "); // Tutto il resto è il cognome intero

      // 🔹 Recupera voce prezzario e durata
      const vocePrezzarioElement = document.getElementById("voce-prezzario");
      const voce_prezzario = vocePrezzarioElement
        ? vocePrezzarioElement.options[
            vocePrezzarioElement.selectedIndex
          ].value.trim()
        : "";

      const durataElement = document.getElementById("time");
      const durata = durataElement
        ? durataElement.options[durataElement.selectedIndex].value.trim()
        : "";

      // 🔹 Recupera altri dati
      const tipologia_visita =
        document.getElementById("tipologia_visita")?.value.trim() || "";
      const numero_studio =
        document.getElementById("studio")?.value.trim() || "";
      const note = document.getElementById("note")?.value.trim() || "";

      const raw_data_appointment =
        document.getElementById("date-appointment")?.textContent.trim() || "";
      const data_appointment = convertDateFormat(raw_data_appointment);
      const time_appointment =
        document.getElementById("time-appointment")?.textContent.trim() || "";

      const appointmentData = {
        tipologia_visita,
        nome_paziente,
        cognome_paziente,
        numero_studio,
        note,
        voce_prezzario,
        durata,
        data: data_appointment,
        orario: time_appointment,
        csrfmiddlewaretoken:
          document.querySelector("input[name='csrfmiddlewaretoken']")?.value ||
          "",
      };

      console.log("📢 Dati inviati:", appointmentData); // Debug

      // 🔹 Invia i dati al backend Django
      fetch("/salva-appuntamento/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": appointmentData.csrfmiddlewaretoken,
        },
        body: JSON.stringify(appointmentData),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("📢 Risposta dal server:", data); // Debug
          if (data.success) {
            showAlert("success", "Appuntamento salvato con successo!");
            location.reload();
          } else {
            showAlert(
              "danger",
              "Errore nel salvataggio dell'appuntamento: " + data.error
            );
          }
        })
        .catch((error) => {
          console.error("❌ Errore durante il salvataggio:", error);
          showAlert("danger", "Si è verificato un errore inaspettato.");
        });
    });
});
