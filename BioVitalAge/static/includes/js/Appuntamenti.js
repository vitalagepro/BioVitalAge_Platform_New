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
                                            CALENDAR
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("appointmentModal");
  const modalContent = document.querySelector(".modal-content-appointments");
  const openModalBtn = document.getElementById("openModal");
  const closeModalIcon = document.getElementById("closeModal");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const saveAppointmentBtn = document.querySelector(".btn-primary");

  const alertContainer = document.createElement("div");
  alertContainer.classList.add("position-fixed", "top-0", "end-0", "p-3");
  document.body.appendChild(alertContainer);

  const dayAppointmentSpan = document.getElementById("day-appointment");
  const dateAppointmentSpan = document.getElementById("date-appointment");
  const timeAppointmentSpan = document.getElementById("time-appointment");
  const editTimeBtn = document.getElementById("edit-date-btn");

  const monthGrid = document.querySelector(".container-content-table");

  let currentDate = new Date();
  let isFromCalendar = false;

  function updateCalendar() {
    generateCalendar();
  }

  function generateCalendar() {
    monthGrid.innerHTML = "";
    let firstDay = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth(),
      1
    ).getDay();
    let daysInMonth = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth() + 1,
      0
    ).getDate();
    let prevMonthDays = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth(),
      0
    ).getDate();
    let startDay = firstDay === 0 ? 6 : firstDay - 1;

    for (let i = startDay; i > 0; i--) {
      let cell = document.createElement("div");
      cell.classList.add("cella", "prev");
      cell.innerHTML = `<p class="data prev">${prevMonthDays - i + 1}</p>`;
      monthGrid.appendChild(cell);
    }

    for (let i = 1; i <= daysInMonth; i++) {
      let cell = document.createElement("div");
      cell.classList.add("cella");
      if (i === currentDate.getDate()) {
        cell.classList.add("current");
      }
      cell.innerHTML = `<p class="data">${i}</p>`;
      monthGrid.appendChild(cell);
    }

    let remainingCells = 42 - monthGrid.children.length;
    for (let i = 1; i <= remainingCells; i++) {
      let cell = document.createElement("div");
      cell.classList.add("cella", "next");
      cell.innerHTML = `<p class="data next">${i}</p>`;
      monthGrid.appendChild(cell);
    }
  }

  function formatDate(date) {
    const giorniSettimana = [
      "Domenica",
      "Lunedì",
      "Martedì",
      "Mercoledì",
      "Giovedì",
      "Venerdì",
      "Sabato",
    ];
    let giornoSettimana = giorniSettimana[date.getDay()];
    let giorno = String(date.getDate()).padStart(2, "0");
    let mese = String(date.getMonth() + 1).padStart(2, "0");
    let anno = date.getFullYear();

    return { giornoSettimana, giorno, mese, anno };
  }

  function showAlert(message, type) {
    const alert = document.createElement("div");
    alert.classList.add("alert", `alert-${type}`, "fade", "show");
    alert.setAttribute("role", "alert");
    alert.innerHTML = message;

    alertContainer.appendChild(alert);

    setTimeout(() => {
      alert.classList.remove("show");
      setTimeout(() => alert.remove(), 200);
    }, 3000);
  }

  function openModalWithDate(date, fromCalendarClick = false) {
    isFromCalendar = fromCalendarClick;
    document.body.style.overflow = "hidden";
    modal.style.display = "block";

    gsap.fromTo(
      modalContent,
      { opacity: 0, scale: 0.8 },
      { opacity: 1, scale: 1, duration: 0.3 }
    );

    if (isFromCalendar) {
      let { giornoSettimana, giorno, mese, anno } = formatDate(date);
      dayAppointmentSpan.textContent = `${giornoSettimana}, `;
      dateAppointmentSpan.textContent = `${giorno}/${mese}/${anno}, `;
      timeAppointmentSpan.textContent = `Ora`;
    } else {
      dayAppointmentSpan.textContent = `Giorno, `;
      dateAppointmentSpan.textContent = `Data, `;
      timeAppointmentSpan.textContent = `Ora`;
    }
  }

  function closeModal() {
    document.body.style.overflow = "auto";
    gsap.to(modalContent, {
      opacity: 0,
      scale: 0.8,
      duration: 0.3,
      onComplete: function () {
        modal.style.display = "none";
        dayAppointmentSpan.textContent = "Giorno, ";
        dateAppointmentSpan.textContent = "Data, ";
        timeAppointmentSpan.textContent = "Ora";
        removeInputIfPresent(dateAppointmentSpan);
        removeInputIfPresent(timeAppointmentSpan);
      },
    });
  }

  editTimeBtn.addEventListener("click", function () {
    if (
      dateAppointmentSpan.querySelector("input") ||
      timeAppointmentSpan.querySelector("input")
    ) {
      return;
    }

    let dateInput = document.createElement("input");
    dateInput.type = "date";
    dateInput.classList.add("form-control");

    let timeInput = document.createElement("input");
    timeInput.type = "time";
    timeInput.classList.add("form-control");

    dateInput.addEventListener("change", function () {
      let selectedDate = new Date(this.value);
      let { giornoSettimana } = formatDate(selectedDate);
      dayAppointmentSpan.textContent = `${giornoSettimana}, `;
    });

    dateAppointmentSpan.innerHTML = "";
    dateAppointmentSpan.appendChild(dateInput);

    timeAppointmentSpan.innerHTML = "";
    timeAppointmentSpan.appendChild(timeInput);
  });

  function removeInputIfPresent(element) {
    let input = element.querySelector("input");
    if (input) {
      element.textContent = input.value || "Ora";
      element.removeChild(input);
    }
  }

  saveAppointmentBtn.addEventListener("click", function () {
    let dateInput = dateAppointmentSpan.querySelector("input[type='date']");
    let timeInput = timeAppointmentSpan.querySelector("input[type='time']");

    let finalDateValue = dateInput
      ? dateInput.value
      : dateAppointmentSpan.textContent.replace(",", "").trim();
    let finalTimeValue = timeInput
      ? timeInput.value
      : timeAppointmentSpan.textContent.replace(",", "").trim();

    let appointmentData = {
      date: finalDateValue,
      time: finalTimeValue,
    };

    fetch("/salva-appuntamento/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(appointmentData),
    })
      .then((response) => response.json())
      .then((data) => {
        showAlert("Appuntamento salvato con successo!", "success");
        closeModal();
      })
      .catch((error) => {
        showAlert("Errore nel salvataggio, riprova!", "danger");
      });
  });

  monthGrid.addEventListener("click", function (event) {
    let cell = event.target.closest(".cella");
    if (cell && cell.querySelector(".data")) {
      let dayNum = parseInt(cell.querySelector(".data").textContent);
      let selectedDate = new Date(
        currentDate.getFullYear(),
        currentDate.getMonth(),
        dayNum
      );
      openModalWithDate(selectedDate, true);
    }
  });

  openModalBtn.addEventListener("click", function () {
    openModalWithDate(new Date(), false);
  });

  closeModalIcon.addEventListener("click", closeModal);
  closeModalBtn.addEventListener("click", closeModal);

  updateCalendar();
});
