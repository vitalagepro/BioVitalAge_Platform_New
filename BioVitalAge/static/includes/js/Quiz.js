/*  -----------------------------------------------------------------------------------------------
    Function to select man or woman in strong test
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".tableRow").forEach((row) => {
    let inputs = row.querySelectorAll("input[type='text']");

    if (inputs.length === 2) {
      let maleInput = inputs[0];
      let femaleInput = inputs[1];

      maleInput.addEventListener("input", function () {
        if (maleInput.value.trim() !== "") {
          femaleInput.disabled = true;
          femaleInput.removeAttribute("required");
          femaleInput.setAttribute("placeholder", "N/A");
        } else {
            femaleInput.disabled = false;
            femaleInput.setAttribute("required", "required");
            femaleInput.setAttribute("placeholder", "Inserisci il valore");
        }
      });

      femaleInput.addEventListener("input", function () {
        if (femaleInput.value.trim() !== "") {
          maleInput.disabled = true;
          maleInput.removeAttribute("required");
          maleInput.setAttribute("placeholder", "N/A");
        } else {
          maleInput.disabled = false;
          maleInput.setAttribute("required", "required");
          maleInputsetAttribute("placeholder", "Inserisci il valore");
        }
      });
    }
  });
});

/*  -----------------------------------------------------------------------------------------------
    Quiz
--------------------------------------------------------------------------------------------------- */
const questionsContainer = document.getElementById("quiz-container");
const questions = questionsContainer.querySelectorAll(".question");
const nextBtn = document.getElementById("next-btn");
const prevBtn = document.getElementById("prev-btn");
const pagination = document.getElementById("pagination");

let currentQuestionIndex = 0;

// Funzione per aggiornare la domanda attiva
function updateQuestion(index) {
  questions[currentQuestionIndex].classList.remove("active");
  currentQuestionIndex = index;
  questions[currentQuestionIndex].classList.add("active");
  updatePagination();
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

// Funzione per aggiornare la paginazione
function updatePagination() {
  const paginationButtons = pagination.querySelectorAll(".pagination-btn");
  paginationButtons.forEach((btn, index) => {
    if (index === currentQuestionIndex) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });
}

// Funzione per generare i pulsanti della paginazione
function createPagination() {
  // Rimuovi i pulsanti esistenti
  pagination.innerHTML = "";

  // Genera nuovi pulsanti
  questions.forEach((_, index) => {
    const button = document.createElement("button");
    button.classList.add("pagination-btn");
    button.textContent = index + 1;
    button.addEventListener("click", () => updateQuestion(index));
    pagination.appendChild(button);
  });
}

// Gestori per i pulsanti successivo e precedente
function nextAnswer() {
  if (currentQuestionIndex < questions.length - 1) {
    updateQuestion(currentQuestionIndex + 1);
  }
}

function prevAnswer() {
  if (currentQuestionIndex > 0) {
    updateQuestion(currentQuestionIndex - 1);
  }
}

nextBtn.addEventListener("click", nextAnswer);
prevBtn.addEventListener("click", prevAnswer);

// Inizializzazione
createPagination();
updatePagination();

const submitBtn = document.getElementById("submit-btn");

function checkLastQuestion() {
  if (currentQuestionIndex === questions.length - 1) {
    const radios = questions[currentQuestionIndex].querySelectorAll(".answer");
    const oneSelected = Array.from(radios).some((radio) => radio.checked);
    submitBtn.disabled = !oneSelected;
  }
}

function handleCheckboxSelection() {
  const checkboxes =
    questions[currentQuestionIndex].querySelectorAll(".answer");
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      checkboxes.forEach((box) => {
        if (box !== checkbox) box.checked = false;
      });
      checkLastQuestion();
    });
  });
}

function updateQuestion(index) {
  questions[currentQuestionIndex].classList.remove("active");
  currentQuestionIndex = index;
  questions[currentQuestionIndex].classList.add("active");
  updatePagination();
  checkLastQuestion();
  if (currentQuestionIndex === questions.length - 1) {
    handleCheckboxSelection();
  }
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

// Aggiorna la funzione nextAnswer per includere il controllo
function nextAnswer() {
  if (currentQuestionIndex < questions.length - 1) {
    updateQuestion(currentQuestionIndex + 1);
  }
}

// Inizializzazione
createPagination();
updatePagination();
handleCheckboxSelection();
