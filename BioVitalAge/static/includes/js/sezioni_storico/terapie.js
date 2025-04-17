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
                  }">Modifica</button>
                  <button class="btn btn-sm btn-outline-danger btn-elimina" data-id="${
                    data.terapia.id
                  }">Elimina</button>
                </td>
              </tr>`;

          if (terapiaInModificaId) {
            const oldRow = tabellaTerapie.querySelector(
              `tr[data-id="${terapiaInModificaId}"]`
            );
            if (oldRow) oldRow.remove(); // Rimuovi riga vecchia
          }

          tabellaTerapie.insertAdjacentHTML("afterbegin", rigaHtml);

          terapiaStudioForm.reset();
          modal.hide();
          terapiaInModificaId = null;
          terapiaStudioForm.querySelector('button[type="submit"]').textContent =
            "Salva";
        } else {
          showAlert("danger", "Errore durante il salvataggio.");
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
    confirmDeleteAction({
      url: `/elimina-terapia-studio/${id}/`,
      elementToRemove: row,
      successMessage: "Terapia eliminata con successo!",
      errorMessage: "Errore durante l'eliminazione della terapia.",
      confirmMessage: "Sei sicuro di voler eliminare questa terapia?",
    })
  });
});
