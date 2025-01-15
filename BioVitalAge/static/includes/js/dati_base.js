document.addEventListener('DOMContentLoaded', function () {
  // Seleziona tutti i bottoni con la classe "tools-table"
  document.querySelectorAll('.tools-table').forEach(button => {
    // Inizializza un contatore di click su ogni pulsante
    button.dataset.clickCount = 0;

    button.addEventListener('click', function (event) {
      // Previeni azioni di default nel caso di type="submit"
      event.preventDefault();

      const menuId = this.closest('.tools-menu-button')?.id;
      // Se non trovi il menuId (pulsante fuori .tools-menu-button), interrompi
      if (!menuId) return;

      // Controlla il titolo del pulsante
      const title = this.title || "";

      // Logica in base al "title"
      if (title.includes("Aggiungi")) {
        addRow(menuId);
      }
      else if (title.includes("Modifica")) {
        let clickCount = parseInt(this.dataset.clickCount) || 0;
        clickCount++;
        this.dataset.clickCount = clickCount;

        // Primo click -> abilita campi
        if (clickCount === 1) {
          openMenuTools(menuId);
        } 
        // Secondo click -> conferma e invia il form
        else if (clickCount === 2) {
          submitMenuTools(menuId);
          // Azzera il contatore
          this.dataset.clickCount = 0;
        }
      }
      else if (title.includes("Chiudi")) {
        closeMenuTools(menuId);
      }
      else if (title.includes("Cestino")) {
        if (confirm("Sei sicuro di voler eliminare questa riga?")) {
          this.closest('.riga-container')?.remove();
        }
      }
    });
  });
});

// Funzione: abilita i campi input (primo click)
function openMenuTools(menuId) {
  const form = document.querySelector(`#${menuId}`)?.closest('form');
  if (!form) return;

  // Abilita gli input
  const inputs = form.querySelectorAll('input');
  inputs.forEach(input => {
    input.removeAttribute('disabled');
  });

  // Mostra il menu con animazione
  const menu = document.getElementById(menuId);
  if (menu) {
    menu.style.display = 'flex'; 
    setTimeout(() => {
      menu.style.opacity = '1';
      menu.style.transform = 'translateX(0)';
    }, 10);
  }
}

// Funzione: chiede conferma e invia il form (secondo click)
function submitMenuTools(menuId) {
  const form = document.querySelector(`#${menuId}`)?.closest('form');
  if (!form) return;

  if (confirm("Vuoi salvare le modifiche?")) {
    form.submit();
  }
}

// Funzione: chiude il menu e disabilita i campi
function closeMenuTools(menuId) {
  const form = document.querySelector(`#${menuId}`)?.closest('form');
  if (form) {
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => input.setAttribute('disabled', true));
  }

  const menu = document.getElementById(menuId);
  if (menu) {
    menu.style.opacity = '0';
    menu.style.transform = 'translateX(20px)';
    setTimeout(() => {
      menu.style.display = 'none';
    }, 300);
  }

  alert("Modifiche annullate!");
}

// Aggiunge una nuova riga
function addRow(menuId) {
  const form = document.querySelector(`#${menuId}`)?.closest('form');
  if (!form) return;

  const newRow = document.createElement('div');
  newRow.classList.add('riga-container');
  newRow.innerHTML = `
    <p><input type="text" name="new_height"></p>
    <p><input type="text" name="new_weight"></p>
    <p><input type="text" name="new_bmi"></p>
    <p><input type="date" name="new_bmi_detection_date"></p>
  `;
  form.querySelector('.table-content')?.appendChild(newRow);
}


/*  -----------------------------------------------------------------------------------------------
    ! Table
--------------------------------------------------------------------------------------------------- */
// Funzione che imposta "opacity: 0" e "z-index: -1" dopo 3 secondi
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    document.getElementById("loading-wrapper").style.opacity = "0";
    document.getElementById("loading-wrapper").style.zIndex = "-1";
  }, 500);
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".edit-save-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const table =
        button.parentElement.previousElementSibling.querySelector("table");
      const isEditing = button.textContent === "Save";

      // Memorizza lo stato iniziale della tabella per il rollback
      if (!isEditing) {
        table.dataset.originalState = table.innerHTML;
      }

      // Attiva/disattiva la modifica dei campi
      table.querySelectorAll("td").forEach((cell) => {
        cell.contentEditable = !isEditing;
      });

      // Cambia il testo del pulsante
      button.textContent = isEditing ? "Edit" : "Save";

      // Aggiunge pulsanti "Add Row" e "Cancel" in modalità modifica
      if (!isEditing) {
        const addRowButton = document.createElement("button");
        addRowButton.textContent = "Add Row";
        addRowButton.className = "edit-save-btn add-row-btn";
        button.parentElement.appendChild(addRowButton);

        const cancelButton = document.createElement("button");
        cancelButton.textContent = "Cancel";
        cancelButton.className = "edit-save-btn cancel-btn";
        button.parentElement.appendChild(cancelButton);

        // Mostra i pulsanti con transizione
        setTimeout(() => {
          addRowButton.classList.add("show");
          cancelButton.classList.add("show");
        }, 10);

        // Evento per aggiungere una riga
        addRowButton.addEventListener("click", () => {
          const newRow = document.createElement("tr");
          const columns = table.querySelectorAll("thead th").length;

          for (let i = 0; i < columns; i++) {
            const newCell = document.createElement("td");
            newCell.contentEditable = true;
            newCell.textContent = ""; // Cella vuota
            newRow.appendChild(newCell);
          }

          table.querySelector("tbody").appendChild(newRow);
        });

        // Evento per annullare le modifiche
        cancelButton.addEventListener("click", () => {
          table.innerHTML = table.dataset.originalState; // Ripristina lo stato iniziale
          button.textContent = "Edit";
          addRowButton.classList.remove("show");
          cancelButton.classList.remove("show");

          setTimeout(() => {
            addRowButton.remove();
            cancelButton.remove();
          }, 300);
        });

        // Rimuove i pulsanti "Add Row" e "Cancel" quando si salva
        button.addEventListener("click", () => {
          addRowButton.classList.remove("show");
          cancelButton.classList.remove("show");

          setTimeout(() => {
            addRowButton.remove();
            cancelButton.remove();
          }, 300);
        });
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
