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

// Funzione per generare il codice fiscale
function generateFiscalCode(codiceCastale) {
  const name = document.getElementById("name").value.toUpperCase();
  const surname = document.getElementById("surname").value.toUpperCase();
  const dob = document.getElementById("dob").value;
  const gender = document.getElementById("gender").value;

  if (!name || !surname || !dob || !gender || !codiceCastale) {
    alert("Tutti i campi sono obbligatori.");
    return;
  }

  const surnameCode = getCodeFromName(surname, false);
  const nameCode = getCodeFromName(name, true);
  const year = dob.slice(2, 4);
  const month = getMonthCode(dob.slice(5, 7));
  const day = getDayCode(dob.slice(8, 10), gender);

  const partialCode =
    surnameCode + nameCode + year + month + day + codiceCastale;
  const controlChar = calculateControlChar(partialCode);

  const fiscalCode = partialCode + controlChar;

  document.getElementById("codice_fiscale").value = fiscalCode;
}

// Funzioni di supporto
function getCodeFromName(name, isFirstName) {
  const consonants = name.replace(/[^BCDFGHJKLMNPQRSTVWXYZ]/g, "");
  const vowels = name.replace(/[^AEIOU]/g, "");

  if (isFirstName && consonants.length >= 4) {
    return consonants[0] + consonants[2] + consonants[3];
  }
  return (consonants + vowels + "XXX").slice(0, 3);
}

function getMonthCode(month) {
  const codes = ["A", "B", "C", "D", "E", "H", "L", "M", "P", "R", "S", "T"];
  return codes[parseInt(month, 10) - 1];
}

function getDayCode(day, gender) {
  let dayInt = parseInt(day, 10);
  if (gender === "F") dayInt += 40;
  return dayInt.toString().padStart(2, "0");
}

function calculateControlChar(partialCode) {
  const oddValues = {
    0: 1,
    1: 0,
    2: 5,
    3: 7,
    4: 9,
    5: 13,
    6: 15,
    7: 17,
    8: 19,
    9: 21,
    A: 1,
    B: 0,
    C: 5,
    D: 7,
    E: 9,
    F: 13,
    G: 15,
    H: 17,
    I: 19,
    J: 21,
    K: 2,
    L: 4,
    M: 18,
    N: 20,
    O: 11,
    P: 3,
    Q: 6,
    R: 8,
    S: 12,
    T: 14,
    U: 16,
    V: 10,
    W: 22,
    X: 25,
    Y: 24,
    Z: 23,
  };

  const evenValues = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    A: 0,
    B: 1,
    C: 2,
    D: 3,
    E: 4,
    F: 5,
    G: 6,
    H: 7,
    I: 8,
    J: 9,
    K: 10,
    L: 11,
    M: 12,
    N: 13,
    O: 14,
    P: 15,
    Q: 16,
    R: 17,
    S: 18,
    T: 19,
    U: 20,
    V: 21,
    W: 22,
    X: 23,
    Y: 24,
    Z: 25,
  };

  const remainderToLetter = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
  ];

  let sum = 0;
  for (let i = 0; i < partialCode.length; i++) {
    const char = partialCode[i];
    sum += i % 2 === 0 ? oddValues[char] : evenValues[char];
  }
  const remainder = sum % 26;
  return remainderToLetter[remainder];
}

// Listener per calcolare automaticamente l'età dal DOB
document.getElementById("dob").addEventListener("input", function () {
  const dob = new Date(this.value);
  const today = new Date();

  // Calcolo dell'età
  let age = today.getFullYear() - dob.getFullYear();
  const monthDiff = today.getMonth() - dob.getMonth();
  const dayDiff = today.getDate() - dob.getDate();

  // Corregge l'età se il compleanno non è ancora passato quest'anno
  if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
    age--;
  }

  // Aggiorna il campo dell'età
  document.getElementById("chronological_age").value = age;
});
