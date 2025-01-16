/*  -----------------------------------------------------------------------------------------------
  ! Loader
--------------------------------------------------------------------------------------------------- */
// Funzione che imposta "opacity: 0" e "z-index: -1" dopo 3 secondi
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    document.getElementById("loading-wrapper").style.opacity = "0";
    document.getElementById("loading-wrapper").style.zIndex = "-1";
  }, 500);
});

/*  -----------------------------------------------------------------------------------------------
  ! Form di modifica dati base
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  let modificationsExist = false;
  const removedRows = new Map(); // Mappa per memorizzare le righe rimosse
  const addedRows = new Set(); // Set per memorizzare le righe aggiunte

  // Cambia titolo del pulsante "Apri Menu" in "Salva le modifiche" solo se ci sono modifiche
  document.querySelectorAll('button[title="Apri Menu"]').forEach((button) => {
    button.addEventListener("click", function () {
      const menuId = this.getAttribute("onclick").match(/'(.*?)'/)?.[1];

      if (this.title === "Apri Menu") {
        this.title = "Salva le modifiche";
        this.type = modificationsExist ? "submit" : "button";
      } else {
        this.title = "Apri Menu";
        this.type = "button";
        if (!modificationsExist && menuId) {
          closeMenuTools(menuId);
        } else {
          saveModifications(this.closest("form"));
          rollbackValues(this.closest("form")); // Ripristina lo stato degli input quando si chiude il menu con "Salva le modifiche"
        }
      }
    });
  });

  // Aggiungi nuova riga
  document.querySelectorAll('img[title="Aggiungi"]').forEach((button) => {
    button.addEventListener("click", function () {
      const tableContent = this.closest("form").querySelector(".table-content");
      const existingRow = tableContent.querySelector(".riga-container");
      const columnCount = existingRow ? existingRow.querySelectorAll("p").length : 3; // Default to 3 columns if no rows exist
      const newRow = document.createElement("div");
      newRow.classList.add("riga-container");
      newRow.innerHTML = `<p><input type="text" style="background-color: inherit; color: inherit;"></p>`.repeat(columnCount);
      newRow.dataset.newRow = "true";
      tableContent.appendChild(newRow);
      addedRows.add(newRow); // Memorizza la riga aggiunta
      modificationsExist = true;
    });
  });

  // Modifica righe esistenti
  document.querySelectorAll('img[title="Modifica"]').forEach((button) => {
    button.addEventListener("click", function () {
      const inputs = this.closest("form").querySelectorAll(".riga-container input");
      inputs.forEach((input) => {
        input.disabled = !input.disabled;
        input.style.backgroundColor = input.disabled ? "inherit" : "white";
        input.style.border = input.disabled ? "none" : "1px solid var(--contrast-color-shadow)";
        input.style.width = input.disabled ? "100%" : "max-content";
        input.style.height = input.disabled ? "100%" : "max-content";
        input.style.borderRadius = input.disabled ? "none" : "5px";

        // Aggiungi un listener per rilevare modifiche al valore
        input.addEventListener("input", () => {
          modificationsExist = true;
        });
      });
    });
  });

  // Rimuovi righe selezionate
  document.querySelectorAll('img[title="Cestino"]').forEach((button) => {
    button.addEventListener("click", function () {
      const tableContent = this.closest("form").querySelector(".table-content");

      if (!tableContent.querySelector(".container-checkbox")) {
        tableContent.querySelectorAll(".riga-container").forEach((row) => {
          const checkboxContainer = document.createElement("div");
          checkboxContainer.innerHTML = `
            <label class="container-checkbox">
              <input type="checkbox">
              <div class="checkmark"></div>
            </label>
          `;
          row.insertAdjacentElement("afterbegin", checkboxContainer);
          row.dataset.originalState = row.innerHTML.replace(checkboxContainer.outerHTML, ""); // Salva lo stato originale della riga senza la checkbox
        });
      } else {
        let rowRemoved = false;
        tableContent.querySelectorAll(".container-checkbox input:checked").forEach((checkbox) => {
          const row = checkbox.closest(".riga-container");
          const rowId = Date.now() + Math.random(); // Genera un ID univoco
          removedRows.set(rowId, row.dataset.originalState); // Salva lo stato originale nella mappa
          row.remove();
          rowRemoved = true;
        });

        tableContent.querySelectorAll(".container-checkbox").forEach((container) => {
          container.remove();
        });

        modificationsExist = rowRemoved;
      }
    });
  });

  // Ripristina righe e valori originali
  function rollbackValues(form) {
    removedRows.forEach((originalState, rowId) => {
      const restoredRow = document.createElement("div");
      restoredRow.classList.add("riga-container");
      restoredRow.innerHTML = originalState; // Ripristina lo stato originale della riga senza checkbox
      form.querySelector(".table-content").appendChild(restoredRow);
    });
    removedRows.clear(); // Svuota la mappa

    addedRows.forEach((row) => {
      row.remove(); // Rimuove le righe aggiunte
    });
    addedRows.clear(); // Svuota il set delle righe aggiunte

    form.querySelectorAll(".riga-container input").forEach((input) => {
      if (input.dataset.originalValue !== undefined) {
        input.value = input.dataset.originalValue;
        input.disabled = true;
        input.style.backgroundColor = "inherit";
        input.style.border = "none";
      }
    });

    // Rimuovi eventuali checkbox residue
    form.querySelectorAll(".container-checkbox").forEach((checkbox) => {
      checkbox.remove();
    });
  }

  // Salva modifiche
  function saveModifications(form) {
    if (modificationsExist) {
      form.querySelectorAll(".riga-container[data-new-row]").forEach((row) => {
        row.removeAttribute("data-new-row");
      });

      const formData = new FormData(form);
      fetch(form.action, {
        method: form.method,
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            showPopup("Modifiche salvate con successo!");
            removedRows.clear(); // Pulisce le righe memorizzate dopo il salvataggio
            addedRows.clear(); // Pulisce le righe aggiunte dopo il salvataggio

            // Rimuove eventuali checkbox residue dopo il salvataggio
            form.querySelectorAll(".container-checkbox").forEach((checkbox) => {
              checkbox.remove();
            });
          } else {
            showPopup("Errore nel salvataggio delle modifiche.", true);
          }
        })
        .catch(() => {
          showPopup("Errore di connessione.", true);
        });
    } else {
      showPopup("Nessuna modifica da salvare.");

      // Rimuove eventuali checkbox residue
      form.querySelectorAll(".container-checkbox").forEach((checkbox) => {
        checkbox.remove();
      });
    }
    // Rimuove eventuali checkbox residue
    form.querySelectorAll(".container-checkbox").forEach((checkbox) => {
      checkbox.remove();
    });
  }

  // Mostra un pop-up
  function showPopup(message, isError = false) {
    const popup = document.createElement("div");
    popup.textContent = message;
    popup.style.position = "fixed";
    popup.style.top = "80px";
    popup.style.right = "50%";
    popup.style.backgroundColor = isError ? "#e74c3c" : "#2ecc71";
    popup.style.color = "white";
    popup.style.padding = "10px 20px";
    popup.style.borderRadius = "5px";
    popup.style.zIndex = "1000";
    document.body.appendChild(popup);

    setTimeout(() => popup.remove(), 3000);
  }

  // Chiudi con conferma
  document.querySelectorAll('img[title="Chiudi"]').forEach((button) => {
    button.addEventListener("click", function () {
      const form = this.closest("form");
      if (modificationsExist && confirm("Ci sono modifiche non salvate. Vuoi annullarle?")) {
        rollbackValues(form);
        modificationsExist = false;
      }
      rollbackValues(form);
    });
  });

  // Salva stato iniziale degli input
  document.querySelectorAll(".riga-container input").forEach((input) => {
    input.dataset.originalValue = input.value;
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
