/*  -----------------------------------------------------------------------------------------------
  Function for section toggles
--------------------------------------------------------------------------------------------------- */
document.querySelectorAll(".button-style.btn-selected").forEach((button) => {
  button.addEventListener("click", function () {
    const container = this.closest(".section");
    container.classList.toggle("hidden-exam");
    if (container.classList.contains("hidden-exam")) {
      this.setAttribute("title", "Apri Sezione");
    } else {
      this.setAttribute("title", "Chiudi Sezione");
    }
  });
});
/*  -----------------------------------------------------------------------------------------------
Function for gender selection
--------------------------------------------------------------------------------------------------- */
document.getElementById("gender").addEventListener("change", function () {
  const selectedGender = this.value;

  // Seleziona TUTTI gli elementi di input all'interno dei form-group
  const formGroups = document.querySelectorAll(".form-group");

  formGroups.forEach((group) => {
    const label = group.querySelector("label");
    const numberInput = group.querySelector('input[type="number"]');
    const rangeInput = group.querySelector('input[type="range"]');

    if (label && numberInput && rangeInput) {
      const isMan = label.textContent.includes("Man");
      const isWoman = label.textContent.includes("Woman");

      // Logica di disabilitazione e rimozione
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
document.getElementById("place_of_birth").addEventListener("input", function () {
    const inputCity = this.value;
    const dataList = document.getElementById("cities");
    const options = dataList.getElementsByTagName("option");
    let found = false;

    for (let option of options) {
      if (option.value.toLowerCase() === inputCity.toLowerCase()) {
        document.getElementById("province").value = option.getAttribute("data-province");
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
