/*  -----------------------------------------------------------------------------------------------
    FUNZIONE VIGNETTA
--------------------------------------------------------------------------------------------------- */
document
  .getElementById("punteggio_fisico")
  .addEventListener("change", function () {
    var valore = this.value;
    var vignettaContainer = document.getElementById("vignetta-container");
    var vignettaContent = document.getElementById("vignetta-content");

    switch (valore) {
      case "1":
        vignettaContent.innerHTML = `Sovrappeso di ossatura piccola. Individui all’apparenza di tipologia fisica sana, che 
                                        tuttavia registrano un’elevata % di grasso corporeo associata ad un livello basso di massa muscolare.`;
        break;
      case "2":
        vignettaContent.innerHTML = `Sovrappeso di ossatura media. Individui che registrano un’elevata % di grasso corporeo associata ad un livello moderato di massa muscolare.`;
        break;
      case "3":
        vignettaContent.innerHTML = `Sovrappeso di ossatura grande. Individui che registrano una % di grasso corporeo e massa muscolare.`;
        break;
      case "4":
        vignettaContent.innerHTML = `Bassa massa muscolare e % media di grasso corporeo. Individui che registrano una percentuale di grasso corporeo media e grasso muscolare inferiore alla media`;
        break;
      case "5":
        vignettaContent.innerHTML = `Media massa muscolare e % media di grasso corporeo Individui che registrano livelli medi di grasso corporeo e massa muscolare`;
        break;
      case "6":
        vignettaContent.innerHTML = `Elevata massa muscolare e % media di grasso corporeo (atleta). Individuo che registra una % media di grasso corporeo e i livelli più elevati di massa muscolare rispetto alla media.`;
        break;
      case "7":
        vignettaContent.innerHTML = `Bassa massa muscolare e % bassa di grasso corporeo. Individuo che registra una bassa % di grasso corporeo e una massa muscolare inferiore alla media.`;
        break;
      case "8":
        vignettaContent.innerHTML = `Magro e muscoloso (atleta) Individuo che registra una percentuale di grasso corporeo inferiore alla media e adeguata massa muscolare.`;
        break;
      case "9":
        vignettaContent.innerHTML = `Molto muscoloso (atleta) Individuo che registra una percentuale di grasso corporeo inferiore alla media e massa muscolare superiore alla media.`;
        break;
      default:
        gsap.to("#vignetta-container", {
          opacity: 0,
          duration: 0.5,
          onComplete: function () {
            document.getElementById("vignetta-container").style.display =
              "none";
          },
        });
        return;
    }
    vignettaContainer.style.display = "inline-block";
    gsap.to(vignettaContainer, { opacity: 1, duration: 0.5 });
  });

function chiudiVignetta() {
  gsap.to("#vignetta-container", {
    opacity: 0,
    duration: 0.5,
    onComplete: function () {
      document.getElementById("vignetta-container").style.display = "none";
    },
  });
}

/*  -----------------------------------------------------------------------------------------------
    Funzione per la selezione del punteggio fisico
--------------------------------------------------------------------------------------------------- */

function showConfirmModal(callback) {
  const modal = document.getElementById("confirm-reset-modal");
  const confirmButton = document.getElementById("confirm-reset-btn");
  const cancelButton = document.getElementById("cancel-reset-btn");

  modal.classList.remove("hidden-modal-custom");

  confirmButton.onclick = function () {
    modal.classList.add("hidden-modal-custom");
    callback(true); // Confermato
  };

  cancelButton.onclick = function () {
    modal.classList.add("hidden-modal-custom");
    callback(false); // Annullato
  };

  // Chiudi la modale cliccando fuori
  modal.onclick = function (event) {
    if (event.target === modal) {
      modal.classList.add("hidden-modal-custom");
      callback(false); // Annullato
    }
  };
}

document.addEventListener("DOMContentLoaded", function () {
  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");

  const punteggioFisicoSelect = document.getElementById("punteggio_fisico");
  const resetButton = document.getElementById("reset-score");

  if (punteggioFisicoSelect) {
    // ✅ Evento per il salvataggio automatico del punteggio fisico
    punteggioFisicoSelect.addEventListener("change", function () {
      const selectedValue = punteggioFisicoSelect.value;

      if (selectedValue) {
        fetch(updatePersonaComposizioneUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({
            punteggio_fisico: selectedValue,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              console.log("Punteggio Fisico aggiornato con successo.");
            } else {
              console.error("Errore dal server:", data.error);
            }
          })
          .catch((error) => {
            console.error("Errore nella richiesta:", error);
          });
      }
    });
  }

  // ✅ Evento per il reset dello storico dei punteggi
  if (resetButton) {
    resetButton.addEventListener("click", function () {
      showConfirmModal(function (confirmed) {
        if (!confirmed) return; // Se annulla, esce dalla funzione

        fetch(updatePersonaComposizioneUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ reset_storico_punteggi: true }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              console.log("Storico punteggi resettato con successo.");

              // ✅ Resetta il select a "-- Seleziona il punteggio --"
              punteggioFisicoSelect.selectedIndex = 0;

              // ✅ Ricarica la pagina per riflettere il reset
              location.reload();
            } else {
              console.error("Errore dal server:", data.error);
            }
          })
          .catch((error) => {
            console.error("Errore nella richiesta:", error);
          });
      });
    });
  }
});

/*  -----------------------------------------------------------------------------------------------
    FUNZIONE MODIFICA DATI
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const editButton = document.querySelector('a[title="Modifica"]');
  if (!editButton) {
    console.error('Il pulsante "Modifica" non è stato trovato.');
    return;
  }

  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");

  const fields = {
    height: "altezza",
    weight: "peso",
    bmi: "bmi",
    bmi_detection_date: "bmi_detection_date",
    girth_value: "girth_value",
    girth_date: "girth_date",
    girth_notes: "girth_notes",
    sport_frequency: "sport_frequency",
    livello_sedentarieta: "livello_sedentarieta",
    grasso: "grasso",
    acqua: "acqua",
    massa_ossea: "massa_ossea",
    massa_muscolare: "massa_muscolare",
    bmr: "bmr",
    eta_metabolica: "eta_metabolica",
    grasso_viscerale: "grasso_viscerale",
    whr: "whr",
    whtr: "whtr",
  };

  let originalValues = {};
  let isEditing = false;

  editButton.addEventListener("click", function (event) {
    event.preventDefault();

    if (!isEditing) {
      // ---- ENTRA IN MODIFICA ----
      isEditing = true;

      Object.keys(fields).forEach((key) => {
        const fieldElement = document.getElementById(fields[key]);
        if (fieldElement) {
          const originalValue = fieldElement.dataset.value?.trim() || fieldElement.textContent.trim() || "";
          originalValues[key] = originalValue;

          const input = document.createElement("input");
          input.type = fieldElement.id.includes("date") ? "date" : "text";

          // Se è una data, la convertiamo, altrimenti lasciamo il valore originale
          input.value = fieldElement.id.includes("date")
            ? formatDateForInput(originalValue)
            : originalValue;

          input.id = `${key}Input`;
          input.dataset.originalValue = originalValue;

          fieldElement.textContent = "";
          fieldElement.appendChild(input);
        }
      });

      // Attiva il calcolo automatico del BMI (altezza x peso)
      setupBMICalculation();

      editButton.innerHTML = `
        Salva 
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              width="30"
              height="30"
              class="svg save-icon"
            >
              <path
                d="M22,15.04C22,17.23 20.24,19 18.07,19H5.93C3.76,19 2,17.23 2,15.04C2,13.07 3.43,11.44 5.31,11.14C5.28,11 5.27,10.86 5.27,10.71C5.27,9.33 6.38,8.2 7.76,8.2C8.37,8.2 8.94,8.43 9.37,8.8C10.14,7.05 11.13,5.44 13.91,5.44C17.28,5.44 18.87,8.06 18.87,10.83C18.87,10.94 18.87,11.06 18.86,11.17C20.65,11.54 22,13.13 22,15.04Z"
              ></path>
            </svg>
        `;
      editButton.title = "Salva";
    } else {
      // ---- SALVA MODIFICHE ----
      let updatedValues = {};
      let finalPayload = {};

      Object.keys(fields).forEach((key) => {
        const input = document.getElementById(`${key}Input`);
        if (input) {
          let newValue = input.value.trim();
          let oldValue = input.dataset.originalValue.trim();

          // Se è un campo data, lo converto in formato yyyy-mm-dd (o vuoto)
          if (input.type === "date") {
            newValue = formatDateForInput(newValue);
          } else {
            // Altri campi → se vuoto o 'inserisci valore', metto null
            // se è un numero valido, parseFloat,
            // altrimenti ripristino oldValue (non vogliamo un testo non numerico per i campi che devono essere numerici)
            if (newValue.toLowerCase() === "inserisci valore" || newValue === "") {
              newValue = null;
            } else if (!isNaN(newValue)) {
              newValue = parseFloat(newValue);
            } else {
              // Se non è un numero valido, manteniamo il vecchio valore (qualunque esso fosse)
              newValue = oldValue;
            }
          }

          // Se il valore è stato modificato davvero, lo includiamo in finalPayload
          if (String(newValue) !== String(oldValue)) {
            // Aggiorno la lista di campi modificati
            updatedValues[key] = newValue;
            finalPayload[key] = newValue;
          }
        }
      });

      // Se non ci sono effettive modifiche, non invio nulla
      if (Object.keys(updatedValues).length === 0) {
        console.log("Nessuna modifica rilevata. Nessuna richiesta inviata.");
        resetEditingState();
        return;
      }

      // Invia i dati al server
      fetch(updatePersonaComposizioneUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(finalPayload),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            console.log("Dati aggiornati con successo.");

            // Aggiorna la vista con i nuovi valori
            Object.keys(finalPayload).forEach((key) => {
              const fieldElement = document.getElementById(fields[key]);
              if (fieldElement) {
                fieldElement.textContent = finalPayload[key] !== null ? finalPayload[key] : "Inserisci valore";
              }
            });

            resetEditingState();
          } else {
            console.error("Errore dal server:", data.error);
          }
        })
        .catch((error) => {
          console.error("Errore nella richiesta:", error);
        });
    }
  });

  // Calcolo automatico del BMI mentre si scrive (altezza e peso)
  function setupBMICalculation() {
    const altezzaInput = document.getElementById("altezzaInput");
    const pesoInput = document.getElementById("pesoInput");
    const bmiInput = document.getElementById("bmiInput");

    if (altezzaInput && pesoInput && bmiInput) {
      // Se il BMI ha già un valore valido, non lo ricalcoliamo
      if (bmiInput.value.trim() !== "" && !isNaN(parseFloat(bmiInput.value))) {
        return;
      }

      const calculateBMI = () => {
        const altezza = parseFloat(altezzaInput.value) / 100; // da cm a metri
        const peso = parseFloat(pesoInput.value);

        if (!isNaN(altezza) && altezza > 0 && !isNaN(peso) && peso > 0) {
          const bmi = (peso / (altezza * altezza)).toFixed(2);
          bmiInput.value = bmi;
        }
      };

      altezzaInput.addEventListener("input", calculateBMI);
      pesoInput.addEventListener("input", calculateBMI);
    }
  }

  // Formatta data in YYYY-MM-DD (accettabile per <input type="date">)
  function formatDateForInput(dateString) {
    if (!dateString || dateString.trim() === "" || dateString.toLowerCase() === "inserisci valore") {
      return ""; // se vuoto o placeholder, restituisco stringa vuota
    }

    // Se è già YYYY-MM-DD, lo lascio così
    if (dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
      return dateString;
    }

    // Altrimenti provo a fare il parsing come data generica
    const parsedDate = new Date(dateString);
    if (!isNaN(parsedDate.getTime())) {
      // Aggiusto il fuso orario
      parsedDate.setMinutes(parsedDate.getMinutes() - parsedDate.getTimezoneOffset());
      return parsedDate.toISOString().split("T")[0];
    }

    // Se niente funziona, restituisco stringa vuota
    return "";
  }

  // Torna alla visualizzazione "normale" (senza input)
  function resetEditingState() {
    Object.keys(fields).forEach((key) => {
      const fieldElement = document.getElementById(fields[key]);
      const input = document.getElementById(`${key}Input`);
      if (fieldElement && input) {
        fieldElement.textContent = input.value.trim() || "Inserisci valore";
      }
    });

    editButton.innerHTML = `Edita
                  <svg class="svg" viewBox="0 0 512 512">
                    <path d="M410.3 231l11.3-11.3-33.9-33.9-62.1-62.1L291.7 89.8l-11.3 11.3-22.6 22.6L58.6 322.9c-10.4 10.4-18 23.3-22.2 37.4L1 480.7c-2.5 8.4-.2 17.5 6.1 23.7s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L387.7 253.7 410.3 231zM160 399.4l-9.1 22.7c-4 3.1-8.5 5.4-13.3 6.9L59.4 452l23-78.1c1.4-4.9 3.8-9.4 6.9-13.3l22.7-9.1v32c0 8.8 7.2 16 16 16h32zM362.7 18.7L348.3 33.2 325.7 55.8 314.3 67.1l33.9 33.9 62.1 62.1 33.9 33.9 11.3-11.3 22.6-22.6 14.5-14.5c25-25 25-65.5 0-90.5L453.3 18.7c-25-25-65.5-25-90.5 0zm-47.4 168l-144 144c-6.2 6.2-16.4 6.2-22.6 0s-6.2-16.4 0-22.6l144-144c6.2-6.2 16.4-6.2 22.6 0s6.2 16.4 0 22.6z"></path>
                  </svg>`;
    editButton.title = "Modifica";
    isEditing = false;
  }
});

/*  -----------------------------------------------------------------------------------------------
    FUNZIONE GENERAZIONE PDF
--------------------------------------------------------------------------------------------------- */
const generaBtn = document.getElementById("genereReport");

const { PDFDocument, rgb, StandardFonts } = PDFLib;

async function generatePDF() {
  try {
    const existingPdfBytes = await fetch(
      "/static/includes/pdfTemplates/composizione.pdf"
    ).then((res) => res.arrayBuffer());
    const pdfDoc = await PDFDocument.load(existingPdfBytes);

    const pages = pdfDoc.getPages();

    // Stampa Informazioni Personali
    const personalInformationPages = pages[0];

    const userData = document.getElementById("userData");
    const name = userData.getAttribute("data-name");
    const surname = userData.getAttribute("data-surname");
    const dob = userData.getAttribute("data-dob");
    const cf = userData.getAttribute("data-cf");
    const place_birth = userData.getAttribute("data-place_birth");
    const chronological_age = userData.getAttribute("data-chronological_age");

    const peso = document.getElementById("peso").textContent;
    const altezza = document.getElementById("altezza").textContent;
    const bmi = document.getElementById("bmi").textContent;
    const grasso = document.getElementById("grasso").textContent;
    const acqua = document.getElementById("acqua").textContent;
    const massaMuscolare =
      document.getElementById("massa_muscolare").textContent;
    const massaOssea = document.getElementById("massa_ossea").textContent;
    const bmr = document.getElementById("bmr").textContent;
    const etaMetabolica = document.getElementById("eta_metabolica").textContent;
    const grassoViscerale =
      document.getElementById("grasso_viscerale").textContent;
    const punteggioFisicoSelect = document.getElementById("punteggio_fisico");
    const punteggioFisico = punteggioFisicoSelect.value;
    const punteggioFisicoDescrizione = punteggioFisicoSelect.options[punteggioFisicoSelect.selectedIndex].textContent;
    
    

    personalInformationPages.drawText(`${name}`, {
      x: 380,
      y: 644,
      size: 12,
      color: rgb(0, 0, 0),
    });
    personalInformationPages.drawText(`${surname}`, {
      x: 455,
      y: 644,
      size: 12,
      color: rgb(0, 0, 0),
    });
    personalInformationPages.drawText(`${dob}`, {
      x: 340,
      y: 632,
      size: 12,
      color: rgb(0, 0, 0),
    });
    personalInformationPages.drawText(`${cf}`, {
      x: 295,
      y: 618,
      size: 12,
      color: rgb(0, 0, 0),
    });
    personalInformationPages.drawText(`${place_birth}`, {
      x: 280,
      y: 632,
      size: 12,
      color: rgb(0, 0, 0),
    });
    personalInformationPages.drawText(`${chronological_age}`, {
      x: 480,
      y: 632,
      size: 12,
      color: rgb(0, 0, 0),
    });
    personalInformationPages.drawText(`${altezza}`, {
      x: 314,
      y: 488,
      size: 12,
      color: rgb(0, 0, 0),
    });
    personalInformationPages.drawText(`${peso}`, {
      x: 314,
      y: 430,
      size: 12,
      color: rgb(0, 0, 0),
    });
    personalInformationPages.drawText(`${bmi}`, {
      x: 170,
      y: 130,
      size: 12,
      color: rgb(0, 0, 0),
    });

    // Stampa Grasso
    const grassoPages = pages[1];
    grassoPages.drawText(`${grasso}`, {
      x: 270,
      y: 512,
      size: 12,
      color: rgb(0, 0, 0),
    });

    // Stampa Acqua
    const acquaPages = pages[2];
    acquaPages.drawText(`${acqua}`, {
      x: 270,
      y: 700,
      size: 12,
      color: rgb(0, 0, 0),
    });
    acquaPages.drawText(`${massaMuscolare}`, {
      x: 330,
      y: 189,
      size: 12,
      color: rgb(0, 0, 0),
    });

    // Stampa punteggio fisico
    const punteggioFisicoPages = pages[3];
    punteggioFisicoPages.drawText(`${punteggioFisico}`, {
      x: 370,
      y: 598,
      size: 12,
      color: rgb(0, 0, 0),
    });
    punteggioFisicoPages.drawText(`${punteggioFisicoDescrizione}`, {
      x: 270,
      y: 598,
      size: 12,
      color: rgb(0, 0, 0),
    });

    // Stampa massa ossea
    const massaOsseaPages = pages[4];
    massaOsseaPages.drawText(`${massaOssea}`, {
      x: 212,
      y: 412,
      size: 12,
      color: rgb(0, 0, 0),
    });

    // Stampa ete metabolica
    const eteMetabolicaPages = pages[6];
    eteMetabolicaPages.drawText(`${bmr}`, {
      x: 315,
      y: 705,
      size: 12,
      color: rgb(0, 0, 0),
    });
    eteMetabolicaPages.drawText(`${etaMetabolica}`, {
      x: 315,
      y: 523,
      size: 12,
      color: rgb(0, 0, 0),
    });
    eteMetabolicaPages.drawText(`${grassoViscerale}`, {
      x: 300,
      y: 355,
      size: 12,
      color: rgb(0, 0, 0),
    });

    const modifiedPdfBytes = await pdfDoc.save();
    const blob = new Blob([modifiedPdfBytes], { type: "application/pdf" });
    const nameUpperCase = name.toUpperCase();
    const surnameUpperCase = surname.toUpperCase();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `COMPOSIZIONE-CORPOREA-${nameUpperCase}-${surnameUpperCase}.pdf`;
    link.click();
  } catch (error) {
    console.error("Errore durante la generazione del PDF:", error);
  }
}

generaBtn.addEventListener("click", generatePDF);
