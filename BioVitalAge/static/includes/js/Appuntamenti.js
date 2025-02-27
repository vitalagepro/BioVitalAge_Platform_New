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
  const currentDateElement = document.getElementById("currentData");
  const monthLayout = document.getElementById("month-layout");
  const prevButton = document.querySelector(".prev");
  const nextButton = document.querySelector(".next");
  const todayButton = document.getElementById("currentBtn");
  const dateInput = document.getElementById("date");
  const modal = document.getElementById("appointmentModal");
  const modalContent = document.querySelector(".modal-content-appointments");
  const openModalBtn = document.getElementById("openModal");
  const closeModalBtn = document.getElementById("closeModal");
  const monthGrid = document.querySelector(".container-content-table");

  let currentDate = new Date();

  function updateCalendar() {
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
    currentDateElement.textContent = `${currentDate.getDate()} ${
      monthNames[currentDate.getMonth()]
    } ${currentDate.getFullYear()}`;
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

  prevButton.addEventListener("click", function () {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
  });

  nextButton.addEventListener("click", function () {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
  });

  todayButton.addEventListener("click", function () {
    currentDate = new Date();
    updateCalendar();
  });

  dateInput.addEventListener("change", function () {
    const selectedDate = new Date(this.value);
    if (!isNaN(selectedDate)) {
      currentDate = selectedDate;
      updateCalendar();
    }
  });

  // Gestione modale appuntamenti con GSAP solo sul contenuto
  openModalBtn.addEventListener("click", function () {
    modal.style.display = "block";
    gsap.fromTo(
      modalContent,
      { opacity: 0, scale: 0.8 },
      { opacity: 1, scale: 1, duration: 0.3 }
    );
  });

  closeModalBtn.addEventListener("click", function () {
    gsap.to(modalContent, {
      opacity: 0,
      scale: 0.8,
      duration: 0.3,
      onComplete: function () {
        modal.style.display = "none";
      },
    });
  });

  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      gsap.to(modalContent, {
        opacity: 0,
        scale: 0.8,
        duration: 0.3,
        onComplete: function () {
          modal.style.display = "none";
        },
      });
    }
  });

  updateCalendar();
});
