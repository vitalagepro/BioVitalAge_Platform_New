/*  -----------------------------------------------------------------------------------------------
  Indicator New function
--------------------------------------------------------------------------------------------------- */
const ContainerIndicatori = document.querySelectorAll(".indicator-container");

ContainerIndicatori.forEach((element) => {
  try {
    console.log("Elaborazione elemento:", element);

    const indicatorContainer = element.querySelector(".indicator-content-container");
    const indicator = element.querySelector(".indicatore");
    const valoreEsame = parseFloat(indicator?.getAttribute("data-value") || 0);

    const containerRangePositive = indicatorContainer.querySelector(".positiveTesto");
    const rangePositiveIndicator = containerRangePositive?.querySelectorAll("p") || [];
    let minPositive = rangePositiveIndicator[0]?.textContent.trim();
    let maxPositive = rangePositiveIndicator[1]?.textContent.trim();

    // Gestione del valore ">0"
    if (minPositive === ">0") {
      minPositive = 0.1; // Sostituisci con un valore numerico appropriato
    }

    // Converti in numeri per i calcoli
    minPositive = parseFloat(minPositive);
    maxPositive = parseFloat(maxPositive);

    const rangeNegativeIndicator = parseFloat(
      element.querySelector(".negativeTesto")?.textContent.split(" ")[0] || 0
    );
    const extremeRightRangeIndicator = parseFloat(
      element.querySelector(".extremeNegativeRange")?.textContent.split(" ")[1] || 0
    );

    if (isNaN(valoreEsame) || isNaN(minPositive) || isNaN(maxPositive)) {
      console.warn("Dati mancanti o non validi:", {
        valoreEsame,
        minPositive,
        maxPositive,
        rangeNegativeIndicator,
        extremeRightRangeIndicator,
      });
      return;
    }

    console.log("Valori iniziali:", {
      valoreEsame,
      minPositive,
      maxPositive,
      rangeNegativeIndicator,
      extremeRightRangeIndicator,
    });

    if (
      valoreEsame >= minPositive &&
      valoreEsame <= maxPositive
    ) {
      console.log("Caso 1: Dentro l'intervallo positivo");
      const percentuale = ((valoreEsame - minPositive) / (maxPositive - minPositive)) * 30 + 26;
      indicator.style.left = `${Math.round(percentuale)}%`;
    } else if (valoreEsame < minPositive) {
      console.log("Caso 2: Fuori range, sotto il minimo positivo");
      const percentuale = ((valoreEsame - rangeNegativeIndicator) / (minPositive - rangeNegativeIndicator)) * 30 - 4;
      indicator.style.left = `${Math.max(Math.round(percentuale), 0)}%`;
    } else if (valoreEsame > maxPositive) {
      console.log("Caso 3: Fuori range, sopra il massimo positivo");
      const percentuale = ((valoreEsame - maxPositive) / (extremeRightRangeIndicator - maxPositive)) * 30 + 66;
      indicator.style.left = `${Math.min(Math.round(percentuale), 100)}%`;
    } else {
      console.warn("Caso non gestito per valoreEsame:", valoreEsame);
    }

    console.log("Posizione indicatore:", indicator.style.left);
  } catch (error) {
    console.error("Errore durante l'elaborazione:", error, element);
  }
});


/*  -----------------------------------------------------------------------------------------------
  Function for section toggles
--------------------------------------------------------------------------------------------------- */

// Add event listener to toggle buttons
function setupSectionToggle() {
  document.querySelectorAll(".button-style.btn-selected").forEach((button) => {
    button.addEventListener("click", toggleSection);
  });

  // Add event listener to the section itself
  document.querySelectorAll(".header-section-exam").forEach((section) => {
    section.addEventListener("click", function (e) {
      // Prevent toggle if the button inside the section is clicked
      if (e.target.closest("button")) {
        return;
      }
      toggleSection.call(section.querySelector(".button-style.btn-selected"));
    });
  });
}

function toggleSection() {
  const container = this.closest(".section");
  const buttonIcon = this.querySelector("svg");

  container.classList.toggle("hidden-exam");

  if (container.classList.contains("hidden-exam")) {
    this.setAttribute("title", "Apri Sezione");
    buttonIcon.style.transform = "rotate(0deg)"; // Reset rotation
  } else {
    this.setAttribute("title", "Chiudi Sezione");
    buttonIcon.style.transform = "rotate(180deg)"; // Rotate arrow
  }
}

// Initialize the toggle functionality
document.addEventListener("DOMContentLoaded", setupSectionToggle);
/*  -----------------------------------------------------------------------------------------------
Function for gender selection
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const genderSelect = document.getElementById("gender");

  if (!genderSelect) {
    console.error("Elemento con ID 'gender' non trovato.");
    return;
  }

  // Funzione per aggiornare la visibilità dei form-group
  function updateFormGroups(selectedGender) {
    const formGroups = document.querySelectorAll(".form-group");

    formGroups.forEach((group) => {
      const label = group.querySelector("label");
      const numberInput = group.querySelector('input[type="number"]');
      const rangeInput = group.querySelector('input[type="range"]');

      if (label && numberInput && rangeInput) {
        const isMan = label.textContent.includes("Man");
        const isWoman = label.textContent.includes("Woman");

        if (
          (selectedGender === "M" && isWoman) ||
          (selectedGender === "F" && isMan)
        ) {
          numberInput.disabled = true;
          rangeInput.disabled = true;
          group.classList.add("hidden-form-group");
        } else {
          numberInput.disabled = false;
          rangeInput.disabled = false;
          group.classList.remove("hidden-form-group");
        }
      }
    });
  }

  // Inizializza il comportamento basato sul valore predefinito del select
  const initialGender = genderSelect.value;
  if (initialGender) {
    updateFormGroups(initialGender);
  }

  // Aggiungi l'evento per reagire ai cambiamenti del select
  genderSelect.addEventListener("change", function () {
    updateFormGroups(this.value);
  });
});

/*  -----------------------------------------------------------------------------------------------
  Slider Range
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  // Seleziona tutti gli input di tipo "number" e "range"
  const numericInputs = document.querySelectorAll('input[type="number"]');
  const rangeInputs = document.querySelectorAll('input[type="range"]');

  numericInputs.forEach((input) => {
    const rangeInput = document.getElementById(input.id + "_range");

    if (rangeInput) {
      // Sincronizzazione tra input numerico e range
      input.addEventListener("input", function () {
        if (!isNaN(input.value) && input.value !== "") {
          rangeInput.value = input.value;
          updateRangeStyle(rangeInput);
        } else if (input.value === "") {
          rangeInput.value = 0;
          updateRangeStyle(rangeInput);
        }
      });

      rangeInput.addEventListener("input", function () {
        input.value = rangeInput.value;
        updateRangeStyle(rangeInput);
      });
    }
  });

  rangeInputs.forEach(updateRangeStyle);

  function updateRangeStyle(slider) {
    const value =
      ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
    slider.style.setProperty("--value", `${value}%`);
  }
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

// AUTO PREFILL PROVINCIA FIELD
// Listener per l'autoprefill della provincia e del codice catastale
document
  .getElementById("place_of_birth")
  .addEventListener("input", function () {
    const inputCity = this.value;
    const dataList = document.getElementById("cities");
    const options = dataList.getElementsByTagName("option");
    let found = false;

    for (let option of options) {
      if (option.value.toLowerCase() === inputCity.toLowerCase()) {
        document.getElementById("province").value =
          option.getAttribute("data-province");
        const codiceCastale = option.getAttribute("data-codice-catastale");
        found = true;
        // Correzione: Chiamare direttamente la funzione generazione del codice fiscale
        generateFiscalCode(codiceCastale);
        break;
      }
    }

    if (!found) {
      document.getElementById("province").value = "";
      document.getElementById("codice_fiscale").value = "";
    }
  });
