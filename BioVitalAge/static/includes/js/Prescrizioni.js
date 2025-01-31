import { renderingRisultati } from "./fetchDatiArchivio.js";

let arrayFoglio1 = [];

async function populateDropdown() {
  const data = await renderingRisultati();
  arrayFoglio1 = data[0].Foglio1;

  const menuTendinaModale = document.getElementById(
    "menu_tendina_prescrizioni"
  );
  menuTendinaModale.innerHTML = "";

  const placeholderOption = document.createElement("option");
  placeholderOption.value = "";
  placeholderOption.textContent = "Seleziona esame";
  placeholderOption.selected = true;
  menuTendinaModale.appendChild(placeholderOption);

  arrayFoglio1.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.DESCRIZIONE_ESAME;
    option.textContent = item.DESCRIZIONE_ESAME;
    menuTendinaModale.appendChild(option);
  });
}

async function populateResults(filteredData = null) {
  if (!filteredData) {
    const data = await renderingRisultati();
    arrayFoglio1 = data[0].Foglio1;
    filteredData = arrayFoglio1;
  }

  const resultContainer = document.querySelector(".Modale-Result-content");
  const queueContainer = document.querySelector(".conteiner-CodaPrescrizioni");

  resultContainer.innerHTML = "";

  filteredData.forEach((item) => {
    const row = document.createElement("div");
    row.classList.add("rowModale");

    let rowContent = `
            <div class="colModale">${
              item.CODICE_UNIVOCO_ESAME_PIATTAFORMA || ""
            }</div>
            <div class="colModale nomeEsame">${
              item.DESCRIZIONE_ESAME || ""
            }</div>
            <div class="colModale">${
              item.COD_ASL ? `${item.COD_ASL} <span> (cod. asl) </span>` : ""
            }</div>
            <div class="colModale">${
              item.COD_REG ? `${item.COD_REG}<span> (cod. reg)</span>` : ""
            }</div>
            <div class="colModale metodica">${item.METODICA || ""}</div>
            <div class="colModale">
                <button class="add-btn" data-id="${item.id}" data-nome="${
      item.DESCRIZIONE_ESAME
    }" data-codice="${item.CODICE_UNIVOCO_ESAME_PIATTAFORMA || ""}" data-asl="${
      item.COD_ASL || ""
    }" data-reg="${item.COD_REG || ""}" data-metodica="${
      item.METODICA || ""
    }">➕</button>
            </div>
        `;

    row.innerHTML = rowContent;
    resultContainer.appendChild(row);
  });

  document.querySelectorAll(".add-btn").forEach((button) => {
    button.addEventListener("click", (event) => {
      const esameId = event.target.getAttribute("data-id");
      const esameNome = event.target.getAttribute("data-nome");
      const esameCodice = event.target.getAttribute("data-codice");
      const esameAsl = event.target.getAttribute("data-asl");
      const esameReg = event.target.getAttribute("data-reg");
      const esameMetodica = event.target.getAttribute("data-metodica");

      const codaItem = document.createElement("div");
      codaItem.classList.add("rowModale", "coda-item");
      codaItem.setAttribute("data-id", esameId);
      codaItem.innerHTML = `
                <div class="colModale" name="codiceEsame">${esameCodice}</div>
                <input type="hidden" id="codiceEsameInput" name="codiceEsame" value="${esameCodice}">
                <div class="colModale nomeEsame">${esameNome}</div>
                <div class="colModale">${
                  esameAsl ? `${esameAsl} (cod. asl)` : ""
                }</div>
                <div class="colModale">${
                  esameReg ? `${esameReg} (cod. reg)` : ""
                }</div>
                <div class="colModale metodica">${esameMetodica}</div>
                <div class="colModale">
                    <button class="remove-btn">❌</button>
                </div>
            `;

      queueContainer.appendChild(codaItem);

      codaItem.querySelector(".remove-btn").addEventListener("click", () => {
        codaItem.remove();
      });
    });
  });
}

function filterResults() {
  console.log("Filtraggio in corso...");

  const searchText = document
    .querySelector(".barra-ricercaModale input")
    .value.toLowerCase();
  const selectedFilter = document.querySelector(".ModaleHeader select").value;

  let filteredData = arrayFoglio1.filter((item) => {
    if (!searchText) return true;

    return (
      item.DESCRIZIONE_ESAME?.toLowerCase().includes(searchText) ||
      item.METODICA?.toLowerCase().includes(searchText) ||
      item.COD_ASL?.toString().toLowerCase().includes(searchText) ||
      item.COD_REG?.toString().toLowerCase().includes(searchText)
    );
  });

  switch (selectedFilter) {
    case "1":
      filteredData.sort((a, b) =>
        a.DESCRIZIONE_ESAME.localeCompare(b.DESCRIZIONE_ESAME)
      );
      break;

    case "2":
      filteredData.sort((a, b) =>
        b.DESCRIZIONE_ESAME.localeCompare(a.DESCRIZIONE_ESAME)
      );
      break;

    case "3":
      filteredData.sort(
        (a, b) =>
          (a.METODICA || "").localeCompare(b.METODICA || "") ||
          a.DESCRIZIONE_ESAME.localeCompare(b.DESCRIZIONE_ESAME)
      );
      break;

    case "4":
      filteredData.sort(
        (a, b) =>
          (a.COD_ASL?.toString() || "").localeCompare(
            b.COD_ASL?.toString() || ""
          ) || a.DESCRIZIONE_ESAME.localeCompare(b.DESCRIZIONE_ESAME)
      );
      break;

    case "5":
      filteredData.sort(
        (a, b) =>
          (a.COD_REG?.toString() || "").localeCompare(
            b.COD_REG?.toString() || ""
          ) || a.DESCRIZIONE_ESAME.localeCompare(b.DESCRIZIONE_ESAME)
      );
      break;

    case "6":
      filteredData.sort(
        (a, b) =>
          (a.COD_REG?.toString() || "").localeCompare(
            b.COD_REG?.toString() || ""
          ) || a.DESCRIZIONE_ESAME.localeCompare(b.DESCRIZIONE_ESAME)
      );
      break;

    default:
      break;
  }

  populateResults(filteredData);
}

function selectSingleResult() {
  const selectedValue = document.getElementById(
    "menu_tendina_prescrizioni"
  ).value;

  if (selectedValue) {
    const selectedItem = arrayFoglio1.find(
      (item) => item.DESCRIZIONE_ESAME === selectedValue
    );
    populateResults(selectedItem ? [selectedItem] : []);
  } else {
    populateResults();
  }
}

document
  .querySelector(".barra-ricercaModale input")
  .addEventListener("input", filterResults);
document
  .querySelector(".ModaleHeader select")
  .addEventListener("change", filterResults);
document
  .getElementById("menu_tendina_prescrizioni")
  .addEventListener("change", selectSingleResult);

// Avvio delle funzioni iniziali
populateDropdown();
populateResults();

/*  -----------------------------------------------------------------------------------------------
  Funzione di paginazione con controllo di tabelle con la stessa classe
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const tables = document.querySelectorAll(".table-content");

  tables.forEach((table) => {
    const rows = table.querySelectorAll(".rowTable");
    const rowsPerPage = 5;
    let currentPage = 1;
    const totalPages = Math.ceil(rows.length / rowsPerPage);

    function showPage(page, filteredRows = rows) {
      rows.forEach((row) =>
        gsap.to(row, {
          opacity: 0,
          height: 0,
          duration: 0.3,
          onComplete: () => (row.style.display = "none"),
        })
      );

      filteredRows.forEach((row, index) => {
        if (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage) {
          gsap.to(row, {
            opacity: 1,
            height: "5rem",
            duration: 0.3,
            display: "flex",
            onStart: () => (row.style.display = "flex"),
          });
        }
      });
    }

    function updatePaginationControls() {
      let existingControls = table.querySelector(".pagination-controls");

      // Rimuovere i controlli esistenti
      if (existingControls) existingControls.remove();

      // Condizione per mostrare la paginazione solo se necessario
      if (rows.length > rowsPerPage) {
        const controls = document.createElement("div");
        controls.classList.add("pagination-controls");

        const range = 10; // Numero massimo di bottoni visibili
        let startPage = Math.max(1, currentPage - Math.floor(range / 2));
        let endPage = Math.min(totalPages, startPage + range - 1);

        // Aggiusta la visualizzazione se siamo vicini all'inizio o alla fine
        if (endPage - startPage < range - 1) {
          startPage = Math.max(1, endPage - range + 1);
        }

        // Bottone per andare alla prima pagina
        if (startPage > 1) {
          const firstPageBtn = document.createElement("button");
          firstPageBtn.classList.add("button-style-pagination");
          firstPageBtn.textContent = "1";
          firstPageBtn.addEventListener("click", () => {
            currentPage = 1;
            showPage(currentPage);
            updatePaginationControls();
          });
          controls.appendChild(firstPageBtn);

          // Aggiungi i dots
          const dots = document.createElement("span");
          dots.textContent = "...";
          controls.appendChild(dots);
        }

        // Bottoni numerati
        for (let i = startPage; i <= endPage; i++) {
          const btn = document.createElement("button");
          btn.classList.add("button-style-pagination");
          btn.textContent = i;
          if (i === currentPage) {
            btn.classList.add("active");
          }
          btn.addEventListener("click", () => {
            currentPage = i;
            showPage(currentPage);
            updatePaginationControls();
          });
          controls.appendChild(btn);
        }

        // Bottone per andare all'ultima pagina
        if (endPage < totalPages) {
          const dots = document.createElement("span");
          dots.textContent = "...";
          controls.appendChild(dots);

          const lastPageBtn = document.createElement("button");
          lastPageBtn.classList.add("button-style-pagination");
          lastPageBtn.textContent = totalPages;
          lastPageBtn.addEventListener("click", () => {
            currentPage = totalPages;
            showPage(currentPage);
            updatePaginationControls();
          });
          controls.appendChild(lastPageBtn);
        }

        table.appendChild(controls);
      }
    }

    // Mostra la prima pagina e controlla se la paginazione è necessaria
    showPage(currentPage);
    updatePaginationControls();
  });
});
