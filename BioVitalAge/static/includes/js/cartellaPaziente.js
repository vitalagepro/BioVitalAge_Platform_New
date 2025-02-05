/*  -----------------------------------------------------------------------------------------------
  Funzione di paginazione con controllo di tabelle con la stessa classe
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const tables = document.querySelectorAll(".table-content");

  tables.forEach((table) => {
    const rows = table.querySelectorAll(".riga-container");
    const rowsPerPage = 5;
    let currentPage = 1;
    const totalPages = Math.ceil(rows.length / rowsPerPage);

    function showPage(page, filteredRows = rows) {
      rows.forEach((row) =>
        gsap.to(row, {
          opacity: 0,
          height: 0,
          duration: 0.3,
          onComplete: () => (row.style.display = "none"),
        })
      );

      filteredRows.forEach((row, index) => {
        if (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage) {
          gsap.to(row, {
            opacity: 1,
            height: "5rem",
            duration: 0.3,
            display: "flex",
            onStart: () => (row.style.display = "flex"),
          });
        }
      });
    }

    function updatePaginationControls() {
      let existingControls = table.querySelector(".pagination-controls");

 
      if (existingControls) existingControls.remove();


      if (rows.length > rowsPerPage) {
        const controls = document.createElement("div");
        controls.classList.add("pagination-controls");

        const range = 10;
        let startPage = Math.max(1, currentPage - Math.floor(range / 2));
        let endPage = Math.min(totalPages, startPage + range - 1);


        if (endPage - startPage < range - 1) {
          startPage = Math.max(1, endPage - range + 1);
        }

        if (startPage > 1) {
          const firstPageBtn = document.createElement("button");
          firstPageBtn.classList.add("button-style-pagination");
          firstPageBtn.textContent = "1";
          firstPageBtn.addEventListener("click", () => {
            currentPage = 1;
            showPage(currentPage);
            updatePaginationControls();
          });
          controls.appendChild(firstPageBtn);

          // Aggiungi i dots
          const dots = document.createElement("span");
          dots.textContent = "...";
          controls.appendChild(dots);
        }

        for (let i = startPage; i <= endPage; i++) {
          const btn = document.createElement("button");
          btn.classList.add("button-style-pagination");
          btn.textContent = i;
          if (i === currentPage) {
            btn.classList.add("active");
          }
          btn.addEventListener("click", () => {
            currentPage = i;
            showPage(currentPage);
            updatePaginationControls();
          });
          controls.appendChild(btn);
        }

        if (endPage < totalPages) {
          const dots = document.createElement("span");
          dots.textContent = "...";
          controls.appendChild(dots);

          const lastPageBtn = document.createElement("button");
          lastPageBtn.classList.add("button-style-pagination");
          lastPageBtn.textContent = totalPages;
          lastPageBtn.addEventListener("click", () => {
            currentPage = totalPages;
            showPage(currentPage);
            updatePaginationControls();
          });
          controls.appendChild(lastPageBtn);
        }

        table.appendChild(controls);
      }
    }

    // Mostra la prima pagina e controlla se la paginazione è necessaria
    showPage(currentPage);
    updatePaginationControls();
  });
});

/*  -----------------------------------------------------------------------------------------------
  Funzione di formattazione del telefono
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  function formatItalianPhoneNumber(phoneNumber) {
      const digits = phoneNumber.replace(/\D/g, ""); // Rimuove caratteri non numerici
      
      if (digits.length < 10) {
          return phoneNumber; // Restituisce il numero originale se non è valido
      }

      // Se il numero inizia con 39 (senza il "+"), assume che abbia già il prefisso internazionale
      if (digits.startsWith("39") && digits.length > 10) {
          return `+${digits.slice(0, 2)} ${digits.slice(2, 5)} ${digits.slice(5, 8)} ${digits.slice(8)}`;
      } 
      
      // Se il numero è lungo 10 cifre (formato italiano senza prefisso), aggiunge +39
      return `+39 ${digits.slice(0, 3)} ${digits.slice(3, 6)} ${digits.slice(6)}`;
  }

  let phoneElement = document.getElementById("phone");
  if (phoneElement) {
      let formattedPhone = formatItalianPhoneNumber(phoneElement.innerText.trim());
      phoneElement.innerText = formattedPhone;
  }
});

/*  -----------------------------------------------------------------------------------------------
  Funzione di modifica dati
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");

  const editButton = document.querySelector('a[title="Modifica"]');
  if (!editButton) {
    console.error('Il pulsante "Modifica" non è stato trovato.');
    return;
  }

  const emailSpan = document.getElementById("email");
  const phoneSpan = document.getElementById("phone");
  const associateStaffSpan = document.getElementById("associate_staff");
  const lastVisitSpan = document.getElementById("lastVisit");
  const upcomingVisitSpan = document.getElementById("upcomingVisit");
  const bloodGroupSpan = document.getElementById("blood_group");
  const successAlert = document.getElementById("successAlert");
  const successMessage = document.getElementById("successMessage");
  const errorAlert = document.getElementById("errorAlert");
  const errorMessage = document.getElementById("errorMessage");

  let isEditing = false; // Stato per determinare se siamo in modalità modifica

  // Funzione per mostrare una notifica
  function showAlert(alertElement, message) {
    const messageElement = alertElement.querySelector("span");
    messageElement.textContent = message;
    alertElement.style.display = "block";
    alertElement.classList.add("show");

    // Nascondi la notifica dopo 3 secondi
    setTimeout(() => {
      alertElement.classList.remove("show");
      setTimeout(() => (alertElement.style.display = "none"), 500);
    }, 3000);
  }

  // Funzione per convertire la data da "DD/MM/YYYY" a "YYYY-MM-DD" per input[type="date"]
  function formatDateForInput(dateString) {
    if (!dateString) return ""; // Se è vuoto, restituisci stringa vuota

    // Controlla se è già in formato YYYY-MM-DD
    if (dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
      return dateString;
    }

    // Prova a convertire una data in formato testuale ("June 25, 2024", "Jan. 31, 2025")
    const parsedDate = new Date(dateString);
    if (!isNaN(parsedDate.getTime())) {
      // Aggiunge l'offset del fuso orario locale per evitare lo shift di un giorno
      parsedDate.setMinutes(
        parsedDate.getMinutes() - parsedDate.getTimezoneOffset()
      );
      return parsedDate.toISOString().split("T")[0]; // Ora mantiene il giorno corretto!
    }

    return ""; // Se la conversione fallisce, restituisce stringa vuota
  }

  editButton.addEventListener("click", function (event) {
    event.preventDefault();

    if (!isEditing) {
      // Modalità modifica
      isEditing = true;

      const emailInput = document.createElement("input");
      emailInput.type = "text";
      emailInput.value = emailSpan.textContent.trim();
      emailInput.id = "emailInput";

      const phoneInput = document.createElement("input");
      phoneInput.type = "text";
      phoneInput.value = phoneSpan.textContent.trim();
      phoneInput.id = "phoneInput";

      const associateStaffInput = document.createElement("input");
      associateStaffInput.type = "text";
      associateStaffInput.value = associateStaffSpan.textContent.trim();
      associateStaffInput.id = "associateStaffInput";

      const lastVisitInput = document.createElement("input");
      lastVisitInput.type = "date";
      lastVisitInput.value = formatDateForInput(
        lastVisitSpan.textContent.trim()
      );
      lastVisitInput.id = "lastVisitInput";
      console.log(lastVisitSpan.textContent.trim());
      console.log(upcomingVisitSpan.textContent.trim());

      const upcomingVisitInput = document.createElement("input");
      upcomingVisitInput.type = "date";
      upcomingVisitInput.value = formatDateForInput(
        upcomingVisitSpan.textContent.trim()
      );
      upcomingVisitInput.id = "upcomingVisitInput";

      const bloodGroupInput = document.createElement("input");
      bloodGroupInput.type = "text";
      bloodGroupInput.value = bloodGroupSpan.textContent.trim();
      bloodGroupInput.id = "bloodGroupInput";

      emailSpan.textContent = "";
      emailSpan.appendChild(emailInput);

      phoneSpan.textContent = "";
      phoneSpan.appendChild(phoneInput);

      associateStaffSpan.textContent = "";
      associateStaffSpan.appendChild(associateStaffInput);

      lastVisitSpan.textContent = "";
      lastVisitSpan.appendChild(lastVisitInput);

      upcomingVisitSpan.textContent = "";
      upcomingVisitSpan.appendChild(upcomingVisitInput);

      bloodGroupSpan.textContent = "";
      bloodGroupSpan.appendChild(bloodGroupInput);

      editButton.innerHTML = `
        Save 
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
      editButton.title = "Save";
    } else {
      const emailInput = document.getElementById("emailInput");
      const phoneInput = document.getElementById("phoneInput");
      const associateStaffInput = document.getElementById(
        "associateStaffInput"
      );
      const lastVisitInput = document.getElementById("lastVisitInput");
      const upcomingVisitInput = document.getElementById("upcomingVisitInput");
      const bloodGroupInput = document.getElementById("bloodGroupInput");

      const updatedEmail = emailInput.value;
      const updatedPhone = phoneInput.value;
      const updatedAssociateStaff = associateStaffInput.value;
      const updatedLastVisit = lastVisitInput.value
        ? lastVisitInput.value
        : null;
      const updatedUpcomingVisit = upcomingVisitInput.value
        ? upcomingVisitInput.value
        : null;
      const updatedBloodGroup = bloodGroupInput.value;

      const formattedPhone = formatItalianPhoneNumber(updatedPhone);

      fetch(updatePersonaUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          email: updatedEmail,
          phone: formattedPhone,
          associate_staff: updatedAssociateStaff,
          lastVisit: updatedLastVisit,
          upcomingVisit: updatedUpcomingVisit,
          blood_group: updatedBloodGroup,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(
              `HTTP Error ${response.status}: ${response.statusText}`
            );
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            console.log("Dati aggiornati con successo.");
            emailSpan.textContent = updatedEmail;
            phoneSpan.textContent = formattedPhone;
            associateStaffSpan.textContent = updatedAssociateStaff;
            lastVisitSpan.textContent = updatedLastVisit;
            upcomingVisitSpan.textContent = updatedUpcomingVisit;
            bloodGroupSpan.textContent = updatedBloodGroup;

            editButton.innerHTML = `Edit
                  <svg class="svg" viewBox="0 0 512 512">
                    <path d="M410.3 231l11.3-11.3-33.9-33.9-62.1-62.1L291.7 89.8l-11.3 11.3-22.6 22.6L58.6 322.9c-10.4 10.4-18 23.3-22.2 37.4L1 480.7c-2.5 8.4-.2 17.5 6.1 23.7s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L387.7 253.7 410.3 231zM160 399.4l-9.1 22.7c-4 3.1-8.5 5.4-13.3 6.9L59.4 452l23-78.1c1.4-4.9 3.8-9.4 6.9-13.3l22.7-9.1v32c0 8.8 7.2 16 16 16h32zM362.7 18.7L348.3 33.2 325.7 55.8 314.3 67.1l33.9 33.9 62.1 62.1 33.9 33.9 11.3-11.3 22.6-22.6 14.5-14.5c25-25 25-65.5 0-90.5L453.3 18.7c-25-25-65.5-25-90.5 0zm-47.4 168l-144 144c-6.2 6.2-16.4 6.2-22.6 0s-6.2-16.4 0-22.6l144-144c6.2-6.2 16.4-6.2 22.6 0s6.2 16.4 0 22.6z"></path>
                  </svg>`;
            editButton.title = "Modifica";

            isEditing = false;

            // Mostra il messaggio di successo
            showAlert(successAlert, "Modifiche effettuate con successo!");
          } else {
            console.error("Errore dal server:", data.error);

            // Mostra il messaggio di errore
            showAlert(errorAlert, `Errore dal server: ${data.error}`);
          }
        })
        .catch((error) => {
          console.error("Errore nella richiesta:", error);

          // Mostra il messaggio di errore
          showAlert(errorAlert, `Errore nella richiesta: ${error.message}`);
        });
    }
  });

  function formatItalianPhoneNumber(phoneNumber) {
    const digits = phoneNumber.replace(/\D/g, ""); // Rimuovi caratteri non numerici

    if (digits.length < 10) {
      return phoneNumber; // Restituisce il numero originale se non è valido
    }

    return digits.startsWith("39") && digits.length > 10
      ? `+${digits.slice(0, 2)} ${digits.slice(2, 5)} ${digits.slice(
          5,
          8
        )} ${digits.slice(8)}`
      : `+39 ${digits.slice(0, 3)} ${digits.slice(3, 6)} ${digits.slice(6)}`;
  }
});

/*  -----------------------------------------------------------------------------------------------
  Funzione di loader
--------------------------------------------------------------------------------------------------- */
// Funzione che imposta "opacity: 0" e "z-index: -1" dopo 3 secondi
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    document.getElementById("loading-wrapper").style.opacity = "0";
    document.getElementById("loading-wrapper").style.zIndex = "-1";
  }, 500);
});

// Access to :root style css
const rootStyles = getComputedStyle(document.documentElement);

// Access to color in the :root
const bgColorDark = rootStyles.getPropertyValue("--contrast-color").trim();

function updateKidneyClock() {
  const kidneyClock = document.getElementById("kidneyClock");
  const kidneyPercentage = document.getElementById("kidneyPercentage");

  const percentage = 57;
  const angle = (percentage / 100) * 360;

  kidneyClock.style.background = `conic-gradient(${bgColorDark} ${angle}deg, #e0e0e0 ${angle}deg)`;

  kidneyPercentage.textContent = `${percentage}%`;
  kidneyPercentage.style.color = bgColorDark;
}
function updateLipidClock() {
  const lipidClock = document.getElementById("lipidClock");
  const lipidPercentage = document.getElementById("lipidPercentage");

  const percentage = 33;
  const angle = (percentage / 100) * 360;

  lipidClock.style.background = `conic-gradient(${bgColorDark} ${angle}deg, #e0e0e0 ${angle}deg)`;

  lipidPercentage.textContent = `${percentage}%`;
  lipidPercentage.style.color = bgColorDark;
}
function updateLiverClock() {
  const liverClock = document.getElementById("liverClock");
  const liverPercentage = document.getElementById("liverPercentage");

  const percentage = 73;
  const angle = (percentage / 100) * 360;

  liverClock.style.background = `conic-gradient(${bgColorDark} ${angle}deg, #e0e0e0 ${angle}deg)`;

  liverPercentage.textContent = `${percentage}%`;
  liverPercentage.style.color = bgColorDark;
}
function updateGlucoseClock() {
  const glucoseClock = document.getElementById("glucoseClock");
  const glucosePercentage = document.getElementById("glucosePercentage");

  const percentage = 15;
  const angle = (percentage / 100) * 360;

  glucoseClock.style.background = `conic-gradient(${bgColorDark} ${angle}deg, #e0e0e0 ${angle}deg)`;

  glucosePercentage.textContent = `${percentage}%`;
  glucosePercentage.style.color = bgColorDark;
}

updateKidneyClock();
updateLipidClock();
updateLiverClock();
updateGlucoseClock();

function generateChart(ctx, data, label) {
  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
      datasets: [
        {
          label: label,
          data: data,
          backgroundColor: "#3b255d2c",
          borderColor: "#3a255d",
          tension: 0.3,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: { display: false },
        y: { display: false },
      },
    },
  });
}

// Generate charts for each card
document.addEventListener("DOMContentLoaded", () => {
  generateChart(
    document.getElementById("chart1").getContext("2d"),
    [140, 190, 230, 210, 180],
    "BP Levels"
  );
  generateChart(
    document.getElementById("chart2").getContext("2d"),
    [90, 100, 110, 120, 130],
    "Sugar Levels"
  );
  generateChart(
    document.getElementById("chart3").getContext("2d"),
    [80, 85, 90, 95, 100],
    "Heart Rate"
  );
  generateChart(
    document.getElementById("chart4").getContext("2d"),
    [180, 220, 240, 200, 210],
    "Cholesterol"
  );
});





/* FILTRI TABELLA PRESCRIZIONE */
document.addEventListener("DOMContentLoaded", function () {
  const filterSelect = document.getElementById("filter");
  const tableContent = document.querySelector(".table-content.prescriptions");

  filterSelect.addEventListener("change", function () {
      let selectedFilter = filterSelect.value;
      let rows = Array.from(tableContent.getElementsByClassName("riga-container"));

      if (selectedFilter === "Tutti") {
          rows.forEach(row => row.style.display = "flex");
          return;
      }

      let columnIndex = parseInt(selectedFilter, 10);
      let isAscending = columnIndex === 0;

      rows.sort((a, b) => {
          let textA = a.getElementsByTagName("p")[columnIndex].innerText.trim().toLowerCase();
          let textB = b.getElementsByTagName("p")[columnIndex].innerText.trim().toLowerCase();

          return isAscending ? textA.localeCompare(textB) : textB.localeCompare(textA);
      });

      rows.forEach(row => tableContent.appendChild(row));
  });
});
