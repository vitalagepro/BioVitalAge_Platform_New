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

      emailSpan.textContent = "";
      emailSpan.appendChild(emailInput);

      phoneSpan.textContent = "";
      phoneSpan.appendChild(phoneInput);

      editButton.innerHTML =
        '<img src="/static/includes/icone/modifica.png" alt="save" title="Save">';
      editButton.title = "Save";
    } else {
      const emailInput = document.getElementById("emailInput");
      const phoneInput = document.getElementById("phoneInput");
      const updatedEmail = emailInput.value;
      const updatedPhone = phoneInput.value;

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

            editButton.innerHTML =
              '<img src="/static/includes/icone/modifica.png" alt="modifica" title="Modifica">';
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
      ? `+${digits.slice(0, 2)} ${digits.slice(2, 5)} ${digits.slice(5, 8)} ${digits.slice(8)}`
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

const ctx1 = document.getElementById("chartDash2_1").getContext("2d");
new Chart(ctx1, {
  type: "bar",
  data: {
    labels: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "Claims",
        data: [5, 10, 15, 7, 8, 5, 12, 10, 6, 8, 9, 15],
        backgroundColor: "rgba(58, 37, 93, 0.8)",
        borderColor: "rgba(58, 37, 93, 1)",
        borderWidth: 1,
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
      x: {
        grid: { display: false },
        ticks: { color: "#666" },
      },
      y: {
        grid: { color: "#ddd" },
        ticks: { color: "#666" },
      },
    },
  },
});

const ctx2 = document.getElementById("chartDash_2").getContext("2d");
new Chart(ctx2, {
  type: "line",
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [
      {
        label: "Expenses",
        data: [200, 400, 600, 500, 700, 300],
        borderColor: "rgba(58, 37, 93, 0.5)",
        backgroundColor: "rgba(58, 37, 93, 1)",
        fill: true,
        tension: 0.3,
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
      x: {
        grid: { display: false },
        ticks: { color: "#666" },
      },
      y: {
        grid: { color: "#ddd" },
        ticks: { color: "#666" },
      },
    },
  },
});

/*  -----------------------------------------------------------------------------------------------
  User Modal log out
--------------------------------------------------------------------------------------------------- */
const userImg = document.getElementById("userImg");
const userModal = document.getElementById("userModal");
const userModalBtn = document.getElementById("nav-bar-user-modal-btn");

function showModal() {
  userModal.classList.add("show");
}

userImg.addEventListener("mouseover", showModal);

userModal.addEventListener("mouseout", () => {
  userModal.classList.remove("show");
});

userModalBtn.addEventListener("mouseover", showModal);
