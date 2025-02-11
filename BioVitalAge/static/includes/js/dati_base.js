/*  -----------------------------------------------------------------------------------------------
  function to transform the first letter of a string to uppercase
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  // Seleziona tutti gli elementi con la classe 'field'
  let fields = document.querySelectorAll(".info_container .field");

  fields.forEach((field) => {
    let label = field.querySelector("p:first-of-type"); // Prende il primo <p> (etichetta)
    let valueP = field.querySelector("p:nth-of-type(2)"); // Prende il secondo <p> (valore)

    if (label && valueP) {
      let labelText = label.innerText.trim();

      // Controlla se il campo è "Nome:" o "Cognome:"
      if (labelText === "Nome:" || labelText === "Cognome:") {
        let text = valueP.innerText.trim();
        if (text.length > 0) {
          // Converte la prima lettera in maiuscolo di ogni parola se la parola è tutta in minuscolo
          let formattedText = text
            .split(" ") // Divide il testo in parole
            .map((word) =>
              word === word.toLowerCase()
                ? word.charAt(0).toUpperCase() + word.slice(1)
                : word
            ) // Se è minuscola, la corregge
            .join(" "); // Ricompone la stringa

          valueP.innerText = formattedText;
        }
      }
    }
  });
});

/*  -----------------------------------------------------------------------------------------------
  ! Form di modifica dati base
--------------------------------------------------------------------------------------------------- */
/*  -----------------------------------------------------------------------------------------------
  ! Form di modifica dati base
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  let modificationsExist = false;
  const removedRows = new Map(); // Mappa per memorizzare le righe rimosse
  const addedRows = new Set(); // Set per memorizzare le righe aggiunte

  // Cambia titolo del pulsante "Apri Menu" in "Salva le modifiche" solo se ci sono modifiche
  document.querySelectorAll('button[title="Apri Menu"]').forEach((button) => {
    button.addEventListener("click", function (event) {
      const form = this.closest("form");

      if (this.title === "Apri Menu") {
        this.title = "Salva le modifiche";
        this.type = modificationsExist ? "submit" : "button";
      } else {
        this.title = "Apri Menu";
        this.type = "button";

        if (modificationsExist) {
          // Usa fetch per inviare il form senza ricaricare la pagina
          const formData = new FormData(form);

          fetch(form.action, {
            method: form.method || "POST",
            body: formData,
          })
            .then((response) => {
              if (response.ok) {
                showPopup("Modifiche salvate con successo!");
                modificationsExist = false; // Resetta lo stato delle modifiche

                // Disabilita tutti gli input dopo il salvataggio
                form.querySelectorAll(".riga-container input").forEach((input) => {
                  input.disabled = true;
                  input.style.backgroundColor = "inherit";
                  input.style.border = "none";
                  // Salva lo stato attuale degli input come valore originale
                  input.dataset.originalValue = input.value;
                });

                // Svuota righe rimosse e aggiunte dopo il salvataggio
                removedRows.clear();
                addedRows.clear();

                // Rimuove eventuali checkbox residue
                clearCheckboxes(form);
              } else {
                showPopup("Errore nel salvataggio delle modifiche.", true);
              }
            })
            .catch(() => {
              showPopup("Errore di connessione.", true);
            });

          // Previeni il comportamento predefinito del form
          event.preventDefault();
        } else {
          rollbackValues(form);
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
      const rows = this.closest("form").querySelectorAll(".riga-container");
      let hasModifications = false;

      rows.forEach((row) => {
        const inputs = row.querySelectorAll("input");
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
            hasModifications = true;
          });
        });
      });

      if (!hasModifications) {
        modificationsExist = true; // Anche se non ci sono modifiche, registra l'azione
      }
    });
  });

  // Rimuovi righe selezionate
  document.querySelectorAll('img[title="Cestino"]').forEach((button) => {
    button.addEventListener("click", function () {
      const tableContent = this.closest("form").querySelector(".table-content");
      let rowRemoved = false;

      // Aggiungi le checkbox se non esistono
      if (!tableContent.querySelector(".container-checkbox")) {
        tableContent.querySelectorAll(".riga-container").forEach((row) => {
          if (!row.querySelector(".container-checkbox")) {
            const checkboxContainer = document.createElement("div");
            checkboxContainer.innerHTML = `
              <label class="container-checkbox">
                <input type="checkbox">
                <div class="checkmark"></div>
              </label>
            `;
            row.insertAdjacentElement("afterbegin", checkboxContainer);
            row.dataset.originalState = row.innerHTML.replace(checkboxContainer.outerHTML, ""); // Salva lo stato originale della riga senza la checkbox
          }
        });
      } else {
        // Rimuovi le righe selezionate
        tableContent.querySelectorAll(".container-checkbox input:checked").forEach((checkbox) => {
          const row = checkbox.closest(".riga-container");
          const rowId = Date.now() + Math.random(); // Genera un ID univoco
          removedRows.set(rowId, row.dataset.originalState); // Salva lo stato originale nella mappa
          row.remove();
          rowRemoved = true;
        });

        // Rimuovi tutte le checkbox residue
        if (!rowRemoved) {
          tableContent.querySelectorAll(".container-checkbox").forEach((checkboxContainer) => {
            checkboxContainer.remove();
          });
        }
      }

      modificationsExist = true; // Segna l'azione come una modifica
    });
  });

  // Ripristina righe e valori originali
  function rollbackValues(form) {
    form.querySelectorAll(".riga-container input").forEach((input) => {
      if (input.dataset.originalValue !== undefined) {
        input.value = input.dataset.originalValue; // Ripristina il valore originale
        input.disabled = true; // Disabilita gli input
        input.style.backgroundColor = "inherit";
        input.style.border = "none";
      }
    });
  
    clearCheckboxes(form); // Rimuove eventuali checkbox residue
    removedRows.clear(); // Pulisci righe rimosse
    addedRows.clear(); // Pulisci righe aggiunte
  }  

  // Rimuove tutte le checkbox residue
  function clearCheckboxes(form) {
    form.querySelectorAll(".container-checkbox").forEach((checkbox) => {
      checkbox.parentElement.remove();
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

  // Mostra una modale con bottoni Si/No
  function showModal(message, onConfirm, onCancel) {
    const modalOverlay = document.createElement("div");
    modalOverlay.style.position = "fixed";
    modalOverlay.style.top = "0";
    modalOverlay.style.left = "0";
    modalOverlay.style.width = "100%";
    modalOverlay.style.height = "100%";
    modalOverlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    modalOverlay.style.zIndex = "1000";

    const modal = document.createElement("div");
    modal.style.position = "absolute";
    modal.style.top = "50%";
    modal.style.left = "50%";
    modal.style.transform = "translate(-50%, -50%)";
    modal.style.backgroundColor = "#f1c40f"; // Colore giallo segnaletico
    modal.style.color = "black";
    modal.style.padding = "20px";
    modal.style.borderRadius = "5px";
    modal.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
    modal.style.textAlign = "center";

    const modalText = document.createElement("p");
    modalText.textContent = message;
    modal.appendChild(modalText);

    const buttonContainer = document.createElement("div");
    buttonContainer.style.marginTop = "10px";

    const yesButton = document.createElement("button");
    yesButton.textContent = "Si";
    yesButton.style.marginRight = "10px";
    yesButton.style.padding = "5px 10px";
    yesButton.style.border = "none";
    yesButton.style.borderRadius = "3px";
    yesButton.style.backgroundColor = "#27ae60";
    yesButton.style.color = "white";
    yesButton.style.cursor = "pointer";
    yesButton.addEventListener("click", () => {
      modalOverlay.remove();
      document.body.style.overflow = ""; // Ripristina lo scroll
      if (onConfirm) onConfirm();
    });

    const noButton = document.createElement("button");
    noButton.textContent = "No";
    noButton.style.padding = "5px 10px";
    noButton.style.border = "none";
    noButton.style.borderRadius = "3px";
    noButton.style.backgroundColor = "#e74c3c";
    noButton.style.color = "white";
    noButton.style.cursor = "pointer";
    noButton.addEventListener("click", () => {
      modalOverlay.remove();
      document.body.style.overflow = ""; // Ripristina lo scroll
      if (onCancel) onCancel();
    });

    buttonContainer.appendChild(yesButton);
    buttonContainer.appendChild(noButton);
    modal.appendChild(buttonContainer);
    modalOverlay.appendChild(modal);
    document.body.appendChild(modalOverlay);
    document.body.style.overflow = "hidden"; // Disabilita lo scroll
  }

  // Chiudi con conferma
  document.querySelectorAll('img[title="Chiudi"]').forEach((button) => {
    button.addEventListener("click", function () {
      const form = this.closest("form");
      if (modificationsExist) {
        showModal(
          "Ci sono modifiche non salvate. Vuoi annullarle?",
          () => {
            rollbackValues(form);
            modificationsExist = false;
          },
          () => {
            // No action needed on cancel
          }
        );
      } else {
        rollbackValues(form);
      }
    });
  });

  // Salva stato iniziale degli input
  document.querySelectorAll(".riga-container input").forEach((input) => {
    input.dataset.originalValue = input.value;
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // Disabilita tutti gli input all'inizio
  document.querySelectorAll(".riga-container input").forEach((input) => {
    input.disabled = true; // Disabilita
    input.style.backgroundColor = "inherit"; // Rimuove lo stile di modifica
    input.style.border = "none";
  });

  // Ripristina gli input come disabilitati dopo il salvataggio
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault(); // Previeni il comportamento predefinito

      // Debug: Mostra i dati inviati
      const formData = new FormData(form);
      console.log("Dati inviati:", Object.fromEntries(formData.entries()));

      // Disabilita tutti gli input dopo l'invio
      form.querySelectorAll("input").forEach((input) => {
        input.disabled = true;
        input.style.backgroundColor = "inherit"; // Rimuove lo stile di modifica
        input.style.border = "none";
      });

      // Esegui la richiesta AJAX o il comportamento predefinito
      fetch(form.action, {
        method: form.method || "POST",
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            console.log(`Modifiche salvate correttamente per il form ${form.id}`);
          } else {
            console.error(`Errore durante il salvataggio per il form ${form.id}`);
          }
        })
        .catch((error) => {
          console.error("Errore di connessione:", error);
        });
    });
  });
});
/*  -----------------------------------------------------------------------------------------------
      ! Blood Data
  --------------------------------------------------------------------------------------------------- */

document.addEventListener("DOMContentLoaded", () => {
  let modificationsExist = false;

  const btn = document.getElementById("btn_blood_group");
  const pressureInput = document.getElementById("pressure")
  const heartRateInput = document.getElementById("heart_rate")
  const bloodGroupInput = document.getElementById("blood_group");
  const rhInput = document.getElementById("rh");
  const bloodDataSection = document.querySelector(".blood_data");

  let isEditing = false;

  // Abilita la modifica dei campi quando si preme il bottone
  btn.addEventListener("click", function () {
    if (!isEditing) {
      bloodGroupInput.removeAttribute("readonly");
      rhInput.removeAttribute("readonly");
      pressureInput.removeAttribute("readonly");
      heartRateInput.removeAttribute("readonly");

      bloodDataSection.classList.add("editing");

      btn.innerHTML = `
        <span class="button__icon-wrapper">
          <svg
            viewBox="0 0 14 15"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            class="button__icon-svg"
            width="14"
          >
            <path
              d="M2 2H12V13H2V2Z"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M4 2V6H10V2"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M4 9H10"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          <svg
            viewBox="0 0 14 15"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            class="button__icon-svg button__icon-svg--copy"
            width="14"
          >
            <path
              d="M2 2H12V13H2V2Z"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M4 2V6H10V2"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M4 9H10"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </span>
        Save
        `;
      isEditing = true;
    } else {
      // Disabilita i campi dopo la modifica
      bloodGroupInput.setAttribute("readonly", true);
      rhInput.setAttribute("readonly", true);
      pressureInput.setAttribute("readonly", true);
      heartRateInput.setAttribute("readonly", true);

      bloodDataSection.classList.remove("editing");

      const newBloodGroup = bloodGroupInput.value.trim();
      const newRh = rhInput.value.trim();
      const newPressureInput = pressureInput.value.trim();
      const newHeartRateInput = heartRateInput.value.trim();

      // Solo se ci sono modifiche
      if (
        newBloodGroup !== bloodGroupInput.dataset.originalValue ||
        newRh !== rhInput.dataset.originalValue ||
        newPressureInput !== pressureInput.dataset.originalValue ||
        newHeartRateInput !== heartRateInput.dataset.originalValue
      ) {
        modificationsExist = true;
      }

      if (modificationsExist) {
        const patientId =
          document.getElementById("blood_group").dataset.patientId; // Supponiamo che l'ID sia in un dataset

        // Invia i dati modificati al backend Django
        fetch(`/api/update_blood_data/${patientId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(), // Recupera il CSRF token
          },
          body: JSON.stringify({
            blood_group: newBloodGroup,
            rh_factor: newRh,
            pressure: newPressureInput,
            heart_rate: newHeartRateInput
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              showPopup("Modifiche salvate con successo!");
              modificationsExist = false; // Resetta lo stato
            } else {
              showPopup("Errore nel salvataggio.", true);
            }
          })
          .catch(() => {
            showPopup("Errore di connessione.", true);
          });

        // Memorizza il nuovo valore originale
        bloodGroupInput.dataset.originalValue = newBloodGroup;
        rhInput.dataset.originalValue = newRh;
      }

      btn.innerHTML = `
          <span class="button__icon-wrapper">
              <svg
                viewBox="0 0 14 15"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                class="button__icon-svg"
                width="14"
              >
                <path
                  d="M7 1V4M7 11V14M1 7H4M10 7H13M3.5 3.5L5 5M9 9L10.5 10.5M3.5 10.5L5 9M9 5L10.5 3.5"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>

              <svg
                viewBox="0 0 14 15"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                class="button__icon-svg button__icon-svg--copy"
                width="14"
              >
                <path
                  d="M7 1V4M7 11V14M1 7H4M10 7H13M3.5 3.5L5 5M9 9L10.5 10.5M3.5 10.5L5 9M9 5L10.5 3.5"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
          </span>
          Update
        `;
      isEditing = false;
    }
  });

  // Funzione per ottenere il token CSRF dai cookie
  function getCSRFToken() {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
    return cookieValue || "";
  }

  // Funzione per mostrare popup di notifica
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

  // Memorizza lo stato originale dei campi
  bloodGroupInput.dataset.originalValue = bloodGroupInput.value;
  rhInput.dataset.originalValue = rhInput.value;
});
