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
    FUNZIONE MODIFICA DATI
--------------------------------------------------------------------------------------------------- */
function formatDateForInput(dateString) {
  if (!dateString) return ""; // Se è vuoto, restituisci stringa vuota

  // Controlla se è già in formato YYYY-MM-DD
  if (dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
    return dateString;
  }

  // Prova a convertire una data in formato testuale ("June 25, 2024", "Jan. 31, 2025")
  const parsedDate = new Date(dateString);
  if (!isNaN(parsedDate.getTime())) {
    // Aggiunge l'offset del fuso orario locale per evitare lo shift di un giorno
    parsedDate.setMinutes(
      parsedDate.getMinutes() - parsedDate.getTimezoneOffset()
    );
    return parsedDate.toISOString().split("T")[0]; // Ora mantiene il giorno corretto!
  }

  return ""; // Se la conversione fallisce, restituisce stringa vuota
}

document.addEventListener("DOMContentLoaded", function () {
  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");

  const editButton = document.querySelector('a[title="Modifica"]');
  if (!editButton) {
    console.error('Il pulsante "Modifica" non è stato trovato.');
    return;
  }

  const peso = document.getElementById("peso");
  const bmi = document.getElementById("bmi");
  const bmi_detection_date = document.getElementById("bmi_detection_date");
  const girth_value = document.getElementById("girth_value");
  const girth_date = document.getElementById("girth_date");
  const girth_notes = document.getElementById("girth_notes");
  const sport_frequency = document.getElementById("sport_frequency");
  const livello_sedentarieta = document.getElementById("livello_sedentarieta");
  const grasso = document.getElementById("grasso");
  const acqua = document.getElementById("acqua");
  const massaOssea = document.getElementById("massa_ossea");
  const massaMuscolare = document.getElementById("massa_muscolare");
  const bmr = document.getElementById("bmr");
  const etaMetabolica = document.getElementById("eta_metabolica");
  const grassoViscerale = document.getElementById("grasso_viscerale");
  const whr = document.getElementById("whr");
  const whtr = document.getElementById("whtr");

  let isEditing = false; // Stato per determinare se siamo in modalità modifica

  // Funzione per mostrare una notifica
  function showAlert(alertElement, message) {
    const messageElement = alertElement.querySelector("span");
    messageElement.textContent = message;
    alertElement.style.display = "block";
    alertElement.classList.add("show");

    // Nascondi la notifica dopo 3 secondi
    setTimeout(() => {
      alertElement.classList.remove("show");
      setTimeout(() => (alertElement.style.display = "none"), 500);
    }, 3000);
  }

  editButton.addEventListener("click", function (event) {
    event.preventDefault();

    if (!isEditing) {
      // Modalità modifica
      isEditing = true;

      // Crea i campi di input
      const pesoInput = document.createElement("input");
      pesoInput.type = "text";
      pesoInput.value = peso.textContent.trim();
      pesoInput.id = "pesoInput";

      const bmiInput = document.createElement("input");
      bmiInput.type = "text";
      bmiInput.value = bmi.textContent.trim();
      bmiInput.id = "bmiInput";

      const bmiDetectionDateInput = document.createElement("input");
      bmiDetectionDateInput.type = "date";
      bmiDetectionDateInput.value = formatDateForInput(
        bmi_detection_date.textContent.trim()
      );
      bmiDetectionDateInput.value = bmi_detection_date.textContent.trim();
      bmiDetectionDateInput.id = "bmiDetectionDateInput";

      const girthValueInput = document.createElement("input");
      girthValueInput.type = "text";
      girthValueInput.value = girth_value.textContent.trim();
      girthValueInput.id = "girthValueInput";

      const girthDateInput = document.createElement("input");
      girthDateInput.type = "date";
      girthDateInput.value = formatDateForInput(girth_date.textContent.trim());
      girthDateInput.value = girth_date.textContent.trim();
      girthDateInput.id = "girthDateInput";

      const girthNotesInput = document.createElement("input");
      girthNotesInput.type = "text";
      girthNotesInput.value = girth_notes.textContent.trim();
      girthNotesInput.id = "girthNotesInput";

      const sportFrequencyInput = document.createElement("input");
      if (document.getElementById("sport_frequency")) {
        sportFrequencyInput.type = "text";
        sportFrequencyInput.placeholder = "Inserisci valore";
        sportFrequencyInput.value = sport_frequency.textContent.trim();
        sportFrequencyInput.id = "sportFrequencyInput";
      }

      const livelloSedentarietaInput = document.createElement("input");
      if (document.getElementById("livello_sedentarieta")) {
        livelloSedentarietaInput.type = "text";
        livelloSedentarietaInput.placeholder = "Inserisci valore";
        livelloSedentarietaInput.value = livello_sedentarieta.textContent.trim();
        livelloSedentarietaInput.id = "livelloSedentarietaInput";
      }

      const grassoInput = document.createElement("input");
      grassoInput.type = "text";
      grassoInput.value = grasso.textContent.trim();
      grassoInput.id = "grassoInput";

      const acquaInput = document.createElement("input");
      acquaInput.type = "text";
      acquaInput.value = acqua.textContent.trim();
      acquaInput.id = "acquaInput";

      const massaOsseaInput = document.createElement("input");
      massaOsseaInput.type = "text";
      massaOsseaInput.value = massaOssea.textContent.trim();
      massaOsseaInput.id = "massaOsseaInput";

      const massaMuscolareInput = document.createElement("input");
      massaMuscolareInput.type = "text";
      massaMuscolareInput.value = massaMuscolare.textContent.trim()
      massaMuscolareInput.id = "massaMuscolareInput";

      const bmrInput = document.createElement("input");
      bmrInput.type = "text";
      bmrInput.value = bmr.textContent.trim()
      bmrInput.id = "bmrInput";

      const etaMetabolicaInput = document.createElement("input");
      etaMetabolicaInput.type = "text";
      etaMetabolicaInput.value = etaMetabolica.textContent.trim();
      etaMetabolicaInput.id = "etaMetabolicaInput";

      const grassoVisceraleInput = document.createElement("input");
      grassoVisceraleInput.type = "text";
      grassoVisceraleInput.value = grassoViscerale.textContent.trim();
      grassoVisceraleInput.id = "grassoVisceraleInput";

      const whrInput = document.createElement("input");
      whrInput.type = "text";
      whrInput.value = whr.textContent.trim();
      whrInput.id = "whrInput";

      const whtrInput = document.createElement("input");
      whtrInput.type = "text";
      whtrInput.value = whtr.textContent.trim();
      whtrInput.id = "whtrInput";
      
      peso.textContent = "";
      peso.appendChild(pesoInput);

      bmi.textContent = "";
      bmi.appendChild(bmiInput);

      bmi_detection_date.textContent = "";
      bmi_detection_date.appendChild(bmiDetectionDateInput);

      girth_value.textContent = "";
      girth_value.appendChild(girthValueInput);

      girth_date.textContent = "";
      girth_date.appendChild(girthDateInput);

      girth_notes.textContent = "";
      girth_notes.appendChild(girthNotesInput);

      sport_frequency.textContent = "";
      sport_frequency.appendChild(sportFrequencyInput);

      if (document.getElementById("livello_sedentarieta")) {
          livello_sedentarieta.textContent = "";
          livello_sedentarieta.appendChild(livelloSedentarietaInput);
      }

      grasso.textContent = "";
      grasso.appendChild(grassoInput);

      acqua.textContent = "";
      acqua.appendChild(acquaInput);

      massaOssea.textContent = "";
      massaOssea.appendChild(massaOsseaInput);

      massaMuscolare.textContent = "";
      massaMuscolare.appendChild(massaMuscolareInput);

      bmr.textContent = "";
      bmr.appendChild(bmrInput);

      etaMetabolica.textContent = "";
      etaMetabolica.appendChild(etaMetabolicaInput);

      grassoViscerale.textContent = "";
      grassoViscerale.appendChild(grassoVisceraleInput);

      whr.textContent = "";
      whr.appendChild(whrInput);

      whtr.textContent = "";
      whtr.appendChild(whtrInput);

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
      editButton.title = "Save";
    } else {
      const pesoInput = document.getElementById("pesoInput");
      const bmiInput = document.getElementById("bmiInput");
      const bmiDetectionDateInput = document.getElementById(
        "bmiDetectionDateInput"
      );
      const girthValueInput = document.getElementById("girthValueInput");
      const girthDateInput = document.getElementById("girthDateInput");
      const girthNotesInput = document.getElementById("girthNotesInput");
      const sportFrequencyInput = document.getElementById(
        "sportFrequencyInput"
      );
      const livelloSedentarietaInput = document.getElementById(
        "livelloSedentarietaInput"
      );
      const grassoInput = document.getElementById("grassoInput");
      const acquaInput = document.getElementById("acquaInput");
      const massaOsseaInput = document.getElementById("massaOsseaInput");
      const massaMuscolareInput = document.getElementById(
        "massaMuscolareInput"
      );
      const bmrInput = document.getElementById("bmrInput");
      const etaMetabolicaInput = document.getElementById("etaMetabolicaInput");
      const grassoVisceraleInput = document.getElementById(
        "grassoVisceraleInput"
      );
      const whrInput = document.getElementById("whrInput");
      const whtrInput = document.getElementById("whtrInput");

      const updatedPeso = pesoInput.value;
      const updatedBmi = bmiInput.value;
      const updatedBmiDetectionDate = bmiDetectionDateInput.value;
      const updatedGirthValue = girthValueInput.value;
      const updatedGirthDate = girthDateInput.value;
      const updatedGirthNotes = girthNotesInput.value;
      const updatedSportFrequency = sportFrequencyInput.value;
      const updatedLivelloSedentarieta = livello_sedentarieta ? livelloSedentarietaInput.value : "";
      const updatedGrasso = grassoInput.value;
      const updatedAcqua = acquaInput.value;
      const updatedMassaOssea = massaOsseaInput.value;
      const updatedMassaMuscolare = massaMuscolareInput.value;
      const updatedbmr = bmrInput.value;
      const updatedEtaMetabolica = etaMetabolicaInput.value;
      const updatedGrassoViscerale = grassoVisceraleInput.value;
      const updatedWHR = whrInput.value;
      const updatedWHTR = whtrInput.value;

      if (sport_frequency) {
        fetch(update_persona_contact, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({
            peso: updatedPeso,
            bmi: updatedBmi,
            bmi_detection_date: updatedBmiDetectionDate,
            girth_value: updatedGirthValue,
            girth_date: updatedGirthDate,
            girth_notes: updatedGirthNotes,
            sport_frequency: updatedSportFrequency,
            grasso: updatedGrasso,
            acqua: updatedAcqua,
            massa_muscolare: updatedMassaMuscolare,
            massa_ossea: updatedMassaOssea,
            bmr: updatedbmr,
            eta_metabolica: updatedEtaMetabolica,
            grasso_viscerale: updatedGrassoViscerale,
            whr: updatedWHR,
            whtr: updatedWHTR,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(
                `HTTP Error ${response.status}: ${response.statusText}`
              );
            }
            return response.json();
          })
          .then((data) => {
            if (data.success) {
              console.log("Dati aggiornati con successo.");

              peso.textContent = updatedPeso;
              bmi.textContent = updatedBmi;
              bmi_detection_date.textContent = updatedBmiDetectionDate;
              girth_value.textContent = updatedGirthValue;
              girth_date.textContent = updatedGirthDate;
              girth_notes.textContent = updatedGirthNotes;
              sport_frequency.textContent = updatedSportFrequency;
              livello_sedentarieta.textContent = updatedLivelloSedentarieta;
              grasso.textContent = updatedGrasso;
              acqua.textContent = updatedAcqua;
              massaMuscolare.textContent = updatedMassaMuscolare;
              massaOssea.textContent = updatedMassaOssea;
              bmr.textContent = updatedbmr;
              etaMetabolica.textContent = updatedEtaMetabolica;
              grassoViscerale.textContent = updatedGrassoViscerale;
              whr.textContent = updatedWHR;
              whtr.textContent = updatedWHTR;

              editButton.innerHTML = `Edita
                    <svg class="svg" viewBox="0 0 512 512">
                      <path d="M410.3 231l11.3-11.3-33.9-33.9-62.1-62.1L291.7 89.8l-11.3 11.3-22.6 22.6L58.6 322.9c-10.4 10.4-18 23.3-22.2 37.4L1 480.7c-2.5 8.4-.2 17.5 6.1 23.7s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L387.7 253.7 410.3 231zM160 399.4l-9.1 22.7c-4 3.1-8.5 5.4-13.3 6.9L59.4 452l23-78.1c1.4-4.9 3.8-9.4 6.9-13.3l22.7-9.1v32c0 8.8 7.2 16 16 16h32zM362.7 18.7L348.3 33.2 325.7 55.8 314.3 67.1l33.9 33.9 62.1 62.1 33.9 33.9 11.3-11.3 22.6-22.6 14.5-14.5c25-25 25-65.5 0-90.5L453.3 18.7c-25-25-65.5-25-90.5 0zm-47.4 168l-144 144c-6.2 6.2-16.4 6.2-22.6 0s-6.2-16.4 0-22.6l144-144c6.2-6.2 16.4-6.2 22.6 0s6.2 16.4 0 22.6z"></path>
                    </svg>`;
              editButton.title = "Modifica";

              isEditing = false;

              // Mostra il messaggio di successo
              showAlert(successAlert, "Modifiche effettuate con successo!");
            } else {
              console.error("Errore dal server:", data.error);

              // Mostra il messaggio di errore
              showAlert(errorAlert, `Errore dal server: ${data.error}`);
            }
          })
          .catch((error) => {
            console.error("Errore nella richiesta:", error);

            // Mostra il messaggio di errore
            showAlert(errorAlert, `Errore nella richiesta: ${error.message}`);
          });
      }else if (livello_sedentarieta) {
                fetch(update_persona_contact, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({
            peso: updatedPeso,
            bmi: updatedBmi,
            bmi_detection_date: updatedBmiDetectionDate,
            girth_value: updatedGirthValue,
            girth_date: updatedGirthDate,
            girth_notes: updatedGirthNotes,
            livello_sedentarieta: updatedLivelloSedentarieta,
            grasso: updatedGrasso,
            acqua: updatedAcqua,
            massa_muscolare: updatedMassaMuscolare,
            massa_ossea: updatedMassaOssea,
            bmr: updatedbmr,
            eta_metabolica: updatedEtaMetabolica,
            grasso_viscerale: updatedGrassoViscerale,
            whr: updatedWHR,
            whtr: updatedWHTR,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(
                `HTTP Error ${response.status}: ${response.statusText}`
              );
            }
            return response.json();
          })
          .then((data) => {
            if (data.success) {
              console.log("Dati aggiornati con successo.");

              peso.textContent = updatedPeso;
              bmi.textContent = updatedBmi;
              bmi_detection_date.textContent = updatedBmiDetectionDate;
              girth_value.textContent = updatedGirthValue;
              girth_date.textContent = updatedGirthDate;
              girth_notes.textContent = updatedGirthNotes;
              sport_frequency.textContent = updatedSportFrequency;
              livello_sedentarieta.textContent = updatedLivelloSedentarieta;
              grasso.textContent = updatedGrasso;
              acqua.textContent = updatedAcqua;
              massaMuscolare.textContent = updatedMassaMuscolare;
              massaOssea.textContent = updatedMassaOssea;
              bmr.textContent = updatedbmr;
              etaMetabolica.textContent = updatedEtaMetabolica;
              grassoViscerale.textContent = updatedGrassoViscerale;
              whr.textContent = updatedWHR;
              whtr.textContent = updatedWHTR;

              editButton.innerHTML = `Edita
                    <svg class="svg" viewBox="0 0 512 512">
                      <path d="M410.3 231l11.3-11.3-33.9-33.9-62.1-62.1L291.7 89.8l-11.3 11.3-22.6 22.6L58.6 322.9c-10.4 10.4-18 23.3-22.2 37.4L1 480.7c-2.5 8.4-.2 17.5 6.1 23.7s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L387.7 253.7 410.3 231zM160 399.4l-9.1 22.7c-4 3.1-8.5 5.4-13.3 6.9L59.4 452l23-78.1c1.4-4.9 3.8-9.4 6.9-13.3l22.7-9.1v32c0 8.8 7.2 16 16 16h32zM362.7 18.7L348.3 33.2 325.7 55.8 314.3 67.1l33.9 33.9 62.1 62.1 33.9 33.9 11.3-11.3 22.6-22.6 14.5-14.5c25-25 25-65.5 0-90.5L453.3 18.7c-25-25-65.5-25-90.5 0zm-47.4 168l-144 144c-6.2 6.2-16.4 6.2-22.6 0s-6.2-16.4 0-22.6l144-144c6.2-6.2 16.4-6.2 22.6 0s6.2 16.4 0 22.6z"></path>
                    </svg>`;
              editButton.title = "Modifica";

              isEditing = false;

              // Mostra il messaggio di successo
              showAlert(successAlert, "Modifiche effettuate con successo!");
            } else {
              console.error("Errore dal server:", data.error);

              // Mostra il messaggio di errore
              showAlert(errorAlert, `Errore dal server: ${data.error}`);
            }
          })
          .catch((error) => {
            console.error("Errore nella richiesta:", error);

            // Mostra il messaggio di errore
            showAlert(errorAlert, `Errore nella richiesta: ${error.message}`);
          });
      }
    }
  });
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

    const name = document.getElementById("name").textContent;
    const surname = document.getElementById("surname").textContent;
    const dob = document.getElementById("dob").textContent;
    const cf = document.getElementById("codice_fiscale").textContent;
    const place_birth = document.getElementById("place_birth").textContent;
    const chronological_age =
      document.getElementById("chronological_age").textContent;

    const peso = document.getElementById("peso").textContent;
    const altezza = document.getElementById("altezza").textContent;

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
