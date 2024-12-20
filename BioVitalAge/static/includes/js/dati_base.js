/*  -----------------------------------------------------------------------------------------------
    ! Table
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".edit-save-btn").forEach((button) => {
    button.addEventListener("click", () => {
      // Trova la tabella associata al pulsante
      const table =
        button.parentElement.previousElementSibling.querySelector("table");
      const isEditing = button.textContent === "Save";

      // Attiva/disattiva la modalità di modifica per le celle
      table.querySelectorAll("td").forEach((cell) => {
        cell.contentEditable = !isEditing;
      });

      // Cambia il testo del pulsante
      button.textContent = isEditing ? "Edit" : "Save";

      // Log dei dati aggiornati (per debug)
      if (isEditing) {
        const updatedData = Array.from(table.querySelectorAll("tbody tr")).map(
          (row) =>
            Array.from(row.querySelectorAll("td")).map(
              (cell) => cell.textContent
            )
        );
        console.log("Dati aggiornati:", updatedData);
      }
    });
  });
});

/*  -----------------------------------------------------------------------------------------------
      ! Blood Data
  --------------------------------------------------------------------------------------------------- */

const btn = document.getElementById("btn_blood_group");
const bloodGroupInput = document.getElementById("blood_group");
const rhInput = document.getElementById("rh");
const bloodDataSection = document.querySelector(".blood_data");

let isEditing = false;

btn.addEventListener("click", function () {
  if (!isEditing) {
    // Abilita la modifica
    bloodGroupInput.removeAttribute("readonly");
    rhInput.removeAttribute("readonly");

    // Aggiunge la classe 'editing' per modificare il CSS
    bloodDataSection.classList.add("editing");

    // Cambia il testo del bottone
    btn.textContent = "Save";
    isEditing = true;
  } else {
    // Disabilita la modifica e salva i valori
    bloodGroupInput.setAttribute("readonly", true);
    rhInput.setAttribute("readonly", true);

    // Rimuove la classe 'editing'
    bloodDataSection.classList.remove("editing");

    // Recupera i valori modificati
    const newBloodGroup = bloodGroupInput.value;
    const newRh = rhInput.value;

    // Esegui azioni di salvataggio (ad esempio localStorage o chiamate AJAX)
    // localStorage.setItem('blood_group', newBloodGroup);
    // localStorage.setItem('rh', newRh);

    console.log("Salvataggio completato:", {
      bloodGroup: newBloodGroup,
      rh: newRh,
    });

    // Ripristina il testo del bottone
    btn.textContent = "Update";
    isEditing = false;
  }
});

/*  ----------------
            User Modal
        -------------------- */
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
