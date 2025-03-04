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
  function renderMonthCalendar() {
    // Svuoto container
    monthLayoutContainer.innerHTML = "";

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    // Prima e ultima data del mese
    const firstDayOfMonth = new Date(year, month, 1);
    const lastDayOfMonth = new Date(year, month + 1, 0);

    // In JS la settimana parte da domenica=0
    let startIndex = firstDayOfMonth.getDay();
    // Forzo la domenica a 7 per avere lun->dom
    if (startIndex === 0) startIndex = 7;

    const totalDaysInMonth = lastDayOfMonth.getDate();

    // Giorno di "oggi" con ore/min/sec azzerate per confronti
    const todayMidnight = new Date();
    todayMidnight.setHours(0, 0, 0, 0);

    // Celle vuote prima del 1° giorno (se non è lunedì)
    for (let i = 1; i < startIndex; i++) {
      const emptyCell = document.createElement("div");
      emptyCell.classList.add("cella", "empty-cell");
      monthLayoutContainer.appendChild(emptyCell);
    }

    // Celle con i giorni
    for (let day = 1; day <= totalDaysInMonth; day++) {
      const cella = document.createElement("div");
      cella.classList.add("cella");

      const dayParagraph = document.createElement("p");
      dayParagraph.classList.add("data");
      dayParagraph.textContent = day;

      // Se è oggi, evidenzia
      if (checkIfToday(year, month, day)) {
        cella.classList.add("today");
      }

      // Controllo se il giorno è già passato
      const cellDate = new Date(year, month, day);
      cellDate.setHours(0, 0, 0, 0);

      if (cellDate < todayMidnight) {
        // Giorno passato: classe "past-day" e nessun listener
        cella.classList.add("past-day");
      } else {
        // Giorno presente/futuro: aggiungo listener
        cella.addEventListener("click", () => {
          selectedDayCell = cella;

          // Calcolo la data corrispondente
          const selectedDate = new Date(year, month, day);

          // 1) Compilo i <span> con la data effettiva
          fillFormForCalendar(selectedDate);

          // 2) (Opzionale) Mostro anteprima nella cella
          showAppointmentPreview(cella);

          // 3) Apro modale
          openModalWithGSAP();
        });
      }

      cella.appendChild(dayParagraph);
      monthLayoutContainer.appendChild(cella);
    }

    // Aggiorno label "Mese Anno"
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
    // Rimuovo anteprima se c'era
    if (selectedDayCell) {
      removeAppointmentPreview(selectedDayCell);
      selectedDayCell = null;
    }

    // Compilo i campi <span> con placeholder
    fillFormForNewAppointment();

    // Apro modale
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
  function fillFormForNewAppointment() {
    fromCalendar = false;
    daySpan.textContent = "Giorno,";
    dateSpan.textContent = "Data,";
    timeSpan.textContent = "Orario";

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
                              FORM HOURS & DATE
--------------------------------------------------------------------------------------------------- */
