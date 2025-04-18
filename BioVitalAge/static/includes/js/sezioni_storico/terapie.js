import showAlert from "../components/showAlert.js";
import { confirmDeleteAction } from "../components/deleteAction.js";

document.addEventListener("DOMContentLoaded", function () {
  const terapiaStudioForm = document.getElementById("studio-terapia-form");
  const tabellaTerapie = document.getElementById("tabella-terapie-studio");
  const modalElement = document.getElementById("studioModal");
  const modal = new bootstrap.Modal(modalElement);
  let terapiaInModificaId = null;

  terapiaStudioForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(terapiaStudioForm);

    const url = terapiaInModificaId
      ? `/modifica-terapia-studio/${terapiaInModificaId}/`
      : `/CartellaPaziente/${pazienteId}/Terapie`;

    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrf-token]").content,
      },
      body: new URLSearchParams({
        form_type: "studio",
        tipologia: formData.get("tipologia"),
        descrizione: formData.get("descrizione"),
        data_inizio: formData.get("data_inizio"),
        data_fine: formData.get("data_fine"),
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success && data.terapia) {
          const rigaHtml = `
              <tr data-id="${data.terapia.id}">
                <td>${data.terapia.descrizione}</td>
                <td>${data.terapia.data_inizio}</td>
                <td>${data.terapia.data_fine || "—"}</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary btn-modifica" data-id="${
                    data.terapia.id
                  }">✎</button>
                  <button class="btn btn-sm btn-outline-danger btn-elimina" data-id="${
                    data.terapia.id
                  }">✖</button>
                </td>
              </tr>`;

          if (terapiaInModificaId) {
            const oldRow = tabellaTerapie.querySelector(
              `tr[data-id="${terapiaInModificaId}"]`
            );
            if (oldRow) oldRow.remove();
          }

          // Rimuove la riga "Nessuna terapia in studio registrata" se presente
          const noTerapieRow =
            tabellaTerapie.querySelector("tr td.text-muted")?.parentElement;
          if (noTerapieRow) noTerapieRow.remove();

          tabellaTerapie.insertAdjacentHTML("afterbegin", rigaHtml);

          terapiaStudioForm.reset();
          modal.hide();
          terapiaInModificaId = null;
          terapiaStudioForm.querySelector('button[type="submit"]').textContent =
            "Salva";
        } else {
          showAlert({
            type: "danger",
            message:
              "Errore nel salvataggio della terapia, controlla di aver compilato tutti i campi necessari.",
            borderColor: "#ef4444",
          });
        }
      })
      .catch(() => {
        alert("Errore durante la richiesta al server.");
      });
  });

  // Event delegation: modifica + elimina
  tabellaTerapie.addEventListener("click", (e) => {
    const row = e.target.closest("tr");
    const id = e.target.dataset.id;

    // MODIFICA
    if (e.target.classList.contains("btn-modifica")) {
      terapiaInModificaId = id;
      const descrizione = row.children[0].innerText;
      const dataInizio = row.children[1].innerText
        .split("/")
        .reverse()
        .join("-");
      const dataFine =
        row.children[2].innerText !== "—"
          ? row.children[2].innerText.split("/").reverse().join("-")
          : "";

      terapiaStudioForm.querySelector('[name="tipologia"]').value =
        "IV Therapy";
      terapiaStudioForm.querySelector('[name="descrizione"]').value =
        descrizione;
      terapiaStudioForm.querySelector('[name="data_inizio"]').value =
        dataInizio;
      terapiaStudioForm.querySelector('[name="data_fine"]').value = dataFine;
      terapiaStudioForm.querySelector('button[type="submit"]').textContent =
        "Salva Modifiche";

      modal.show();
    }

    // ELIMINA
    const btnElimina = row.querySelector(".btn-elimina");

    btnElimina.addEventListener("click", () => {
      confirmDeleteAction({
        url: `/elimina-terapia-studio/${id}/`,
        elementToRemove: row,
        successMessage: "Terapia eliminata con successo!",
        errorMessage: "Errore durante l'eliminazione della terapia.",
        confirmMessage: "Sei sicuro di voler eliminare questa terapia?",
        borderColor: "#EF4444",
      });
    });
  });
});

/*  -----------------------------------------------------------------------------------------------
    FUNZIONI PER GENERARE IL DOCX
--------------------------------------------------------------------------------------------------- */
// Funzione per caricare l'immagine e creare un paragrafo con l'immagine
async function loadImageToParagraph(url, width, height) {
  const response = await fetch(url);
  const blob = await response.blob();
  const imageData = await blob.arrayBuffer();

  return new window.docx.Paragraph({
      children: [
          new window.docx.ImageRun({
              data: imageData,
              transformation: {
                  width: width,
                  height: height,
              },
          }),
      ],
      alignment: window.docx.AlignmentType.CENTER
  });
}

// Funzione per generare il docx
async function generateDocx() {
  const { Document, Packer, Paragraph, TextRun, AlignmentType, Media } = window.docx;

  const persona = {
      name: pazienteName,
      surname: pazienteSurname,
      pob: pazientePob,
      dob: pazienteDob
  };

  const today = new Date();
  const formattedDate = today.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric' });

  const doc = new Document({
      creator: "Sant'Andrea Longevity",
      description: "Prescrizione Esami",
      title: "Prescrizione Esami Utente",
      sections: [{
          properties: {},
          children: [

              // LOGO PICCOLO ALTO
              await loadImageToParagraph("/static/includes/pdfTemplates/logo2.png", 200, 80),

              new Paragraph({ text: "", spacing: { after: 400 } }),

              // DATI PAZIENTE DESTRA
              new Paragraph({
                  text: `Sig.ra/Sig. ${persona.name} ${persona.surname}`,
                  alignment: AlignmentType.RIGHT,
                  spacing: { 
                      after: 200,
                      before: 400
                   }
              }),

              new Paragraph({
                  text: "Si prescrivono i seguenti esami:",
                  bold: true,
                  spacing: { after: 4000 }
              }),


              new Paragraph({
                  text: `Bari, ${formattedDate}`,
                  spacing: { after: 400 }
              }),

              new Paragraph({
                  text: "Dott. Luigi Aprile:",
                  alignment: AlignmentType.RIGHT,
              }),

              new Paragraph({ text: "", spacing: { after: 4000 } }),

              await loadImageToParagraph("/static/includes/pdfTemplates/logo.png", 250, 100),
          ]
      }]
  });

  const blob = await Packer.toBlob(doc);
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${persona.name}_${persona.surname}.docx`;
  link.click();
}

// Attiva la funzione generateDocx al caricamento della pagina
document.addEventListener('DOMContentLoaded', function () {
  const downloadButton = document.getElementById('downloadPrescrizioneVuota');

  if (downloadButton) {
      downloadButton.addEventListener('click', generateDocx);
  }
});