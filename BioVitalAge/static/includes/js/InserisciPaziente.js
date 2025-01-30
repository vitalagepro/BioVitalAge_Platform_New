/*  -----------------------------------------------------------------------------------------------
        Modal User
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
/*  -----------------------------------------------------------------------------------------------
        Script per la logica dei pulsanti "Yes/No"
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  // Selezioniamo tutti i blocchi che contengono i pulsanti "Yes/No"
  const chooseButtonsContainers = document.querySelectorAll(".choose-buttons");

  chooseButtonsContainers.forEach((buttonsContainer) => {
    const yesButton = buttonsContainer.querySelector('[data-choice="yes"]');
    const noButton = buttonsContainer.querySelector('[data-choice="no"]');

    // Troviamo il contenitore delle tabelle per la sezione Sport (o altre)
    const containerCard = buttonsContainer.closest(".container-card");

    if (!containerCard) return;

    // Troviamo le due tabelle "sporting" e "sedentary"
    const sportingLifestyle = containerCard.querySelector(
      '[data-lifestyle="sporting-lifestyle"]'
    );
    const sedentaryLifestyle = containerCard.querySelector(
      '[data-lifestyle="sedentary-lifestyle"]'
    );

    function toggleInputsInHiddenTables() {
      document.querySelectorAll(".responsive-table.hidden").forEach(table => {
        table.querySelectorAll("input").forEach(input => {
          input.setAttribute("disabled", "true");
        });
      });
    
      document.querySelectorAll(".responsive-table:not(.hidden)").forEach(table => {
        table.querySelectorAll("input").forEach(input => {
          input.removeAttribute("disabled");
        });
      });
    }
    

    // Se esistono entrambe, vuol dire che è la sezione "Sport"
    if (sportingLifestyle && sedentaryLifestyle) {
      // Di default rimangono entrambe nascoste, perché nel tuo HTML
      // hai messo class="hidden" su entrambe

      // Se clicco "Yes" → mostro sporting, nascondo sedentary
      yesButton.addEventListener("click", (event) => {
        event.preventDefault();
        sportingLifestyle.classList.remove("hidden");
        sedentaryLifestyle.classList.add("hidden");
        toggleInputsInHiddenTables();
      });

      // Se clicco "No" → mostro sedentary, nascondo sporting
      noButton.addEventListener("click", (event) => {
        event.preventDefault();
        sportingLifestyle.classList.add("hidden");
        sedentaryLifestyle.classList.remove("hidden");
        toggleInputsInHiddenTables();
      });
    } else {
      // Se non è la sezione "Sport", manteniamo la logica generica
      // (mostro/nascondo una sola tabella successiva)
      const hiddenTable = buttonsContainer.nextElementSibling;

      yesButton.addEventListener("click", (event) => {
        event.preventDefault();
        hiddenTable?.classList.remove("hidden");
        toggleInputsInHiddenTables();
      });
      noButton.addEventListener("click", (event) => {
        event.preventDefault();
        hiddenTable?.classList.add("hidden");
        toggleInputsInHiddenTables();
      });
    }
  });
});

/*  -----------------------------------------------------------------------------------------------
  BMI CALCULATOR
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const heightInput = document.querySelector("input[name='height']");
  const weightInput = document.querySelector("input[name='weight']");
  const bmiInput = document.querySelector("input[name='bmi']");

  function calculateBMI() {
    const heightValue = parseFloat(heightInput.value);
    const weightValue = parseFloat(weightInput.value);

    if (!isNaN(heightValue) && !isNaN(weightValue) && heightValue > 0) {
      const heightInMeters = heightValue / 100; // Convert cm to meters
      const bmi = weightValue / (heightInMeters * heightInMeters);
      bmiInput.value = bmi.toFixed(2); // Set BMI with 2 decimal places
    } else {
      bmiInput.value = ""; // Clear BMI if values are invalid
    }
  }

  heightInput.addEventListener("input", calculateBMI);
  weightInput.addEventListener("input", calculateBMI);
});
