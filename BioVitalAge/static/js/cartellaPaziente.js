/*  -----------------------------------------------------------------------------------------------
  Funzione di paginazione con controllo di tabelle con la stessa classe
  --------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const tables = document.querySelectorAll(".table-content");

  tables.forEach((table) => {
    const rows = table.querySelectorAll(".riga-container");
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

      if (existingControls) existingControls.remove();

      if (rows.length > rowsPerPage) {
        const controls = document.createElement("div");
        controls.classList.add("pagination-controls");

        const range = 10;
        let startPage = Math.max(1, currentPage - Math.floor(range / 2));
        let endPage = Math.min(totalPages, startPage + range - 1);

        if (endPage - startPage < range - 1) {
          startPage = Math.max(1, endPage - range + 1);
        }

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

        tables.appendChild(controls);
      }
    }

    showPage(currentPage);
    updatePaginationControls();
  });
});

/*  -----------------------------------------------------------------------------------------------
  Funzione di formattazione del telefono
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  function formatItalianPhoneNumber(phoneNumber) {
    const digits = phoneNumber.replace(/\D/g, ""); // Rimuove caratteri non numerici

    if (digits.length < 10) {
      return phoneNumber; // Restituisce il numero originale se non è valido
    }

    // Se il numero inizia con 39 (senza il "+"), assume che abbia già il prefisso internazionale
    if (digits.startsWith("39") && digits.length > 10) {
      return `+${digits.slice(0, 2)} ${digits.slice(2, 5)} ${digits.slice(
        5,
        8
      )} ${digits.slice(8)}`;
    }

    // Se il numero è lungo 10 cifre (formato italiano senza prefisso), aggiunge +39
    return `+39 ${digits.slice(0, 3)} ${digits.slice(3, 6)} ${digits.slice(6)}`;
  }

  let phoneElement = document.getElementById("phone");
  if (phoneElement) {
    let formattedPhone = formatItalianPhoneNumber(
      phoneElement.innerText.trim()
    );
    phoneElement.innerText = formattedPhone;
  }
});











/* FILTRI TABELLA PRESCRIZIONE */
// document.addEventListener("DOMContentLoaded", function () {
//   const filterSelect = document.getElementById("filter");
//   const tableContent = document.querySelector(".table-content.prescriptions");

//   filterSelect.addEventListener("change", function () {
//     let selectedFilter = filterSelect.value;
//     let rows = Array.from(
//       tableContent.getElementsByClassName("riga-container")
//     );

//     if (selectedFilter === "Tutti") {
//       rows.forEach((row) => (row.style.display = "flex"));
//       return;
//     }

//     let columnIndex = parseInt(selectedFilter, 10);
//     let isAscending = columnIndex === 0;

//     rows.sort((a, b) => {
//       let textA = a
//         .getElementsByTagName("p")
//         [columnIndex].innerText.trim()
//         .toLowerCase();
//       let textB = b
//         .getElementsByTagName("p")
//         [columnIndex].innerText.trim()
//         .toLowerCase();

//       return isAscending
//         ? textA.localeCompare(textB)
//         : textB.localeCompare(textA);
//     });

//     rows.forEach((row) => tableContent.appendChild(row));
//   });
// });


/*  -----------------------------------------------------------------------------------------------
    Mostra di più
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  // Seleziona il tasto "Mostra di più"
  const toggleButton = document.querySelector(".button-view-all");
  if (!toggleButton) return;
  
  // Seleziona l'intero contenitore dei bottoni
  const buttonGrid = document.querySelector(".button-grid");
  // Crea un array con tutti i figli del buttonGrid tranne il toggle button
  const otherButtons = Array.from(buttonGrid.children).filter(el =>
    !el.classList.contains("button-view-all")
  );
  
  // Inizialmente nasconde gli altri bottoni (mantiene visibile solo il toggle)
  otherButtons.forEach((btn) => {
    gsap.set(btn, { opacity: 0, display: "none" });
  });

  // Seleziona i contenitori che già gestisci per i campi della card
  const infoContainer = document.querySelector(".container_box");
  const contactContainer = document.querySelector(".Contact-Container");
  const subCardsContainer = document.querySelector(".subCard-container");
  
  // Seleziona i campi della card (compresi email e telefono)
  const hiddenFields = infoContainer.querySelectorAll(".field, .email, .telefono");

  // Nasconde i campi all'inizio
  hiddenFields.forEach((field) => {
    gsap.set(field, { opacity: 0, display: "none" });
  });

  // Nasconde anche le sub-card e il container dei contatti
  gsap.set(subCardsContainer, { opacity: 0, display: "none" });
  gsap.set(contactContainer, { opacity: 0, display: "none" });
  
  // Aggiunge una classe per gestire il layout se necessario
  infoContainer.classList.add("hidden-row-grid");

  // Aggiunge il listener al toggle button (Mostra di più / Mostra di meno)
  toggleButton.addEventListener("click", function () {
    // Determina se i campi sono attualmente nascosti
    const isHidden = hiddenFields[0].style.display === "none";

    // Toggle per i campi della card
    hiddenFields.forEach((field) => {
      if (isHidden) {
        gsap.to(field, { opacity: 1, display: "flex", duration: 0.5 });
      } else {
        gsap.to(field, { opacity: 0, display: "none", duration: 0.5 });
      }
    });

    // Toggle per le sub-card e i contatti
    if (isHidden) {
      gsap.to(subCardsContainer, { opacity: 1, display: "flex", duration: 0.5 });
      gsap.to(contactContainer, { opacity: 1, display: "flex", duration: 0.5 });
      infoContainer.classList.remove("hidden-row-grid");
      // Mostra gli altri bottoni quando la card è visibile
      otherButtons.forEach((btn) => {
        gsap.to(btn, { opacity: 1, display: "flex", duration: 0.5 });
      });
    } else {
      gsap.to(subCardsContainer, { opacity: 0, display: "none", duration: 0.5 });
      gsap.to(contactContainer, { opacity: 0, display: "none", duration: 0.5 });
      infoContainer.classList.add("hidden-row-grid");
      // Nasconde gli altri bottoni quando la card viene chiusa
      otherButtons.forEach((btn) => {
        gsap.to(btn, { opacity: 0, display: "none", duration: 0.5 });
      });
    }

    // Aggiorna il testo e le icone del bottone toggle
    toggleButton.innerHTML = `
      <span class="button__icon-wrapper">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" width="18" class="button__icon-svg">
          <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" width="18" class="button__icon-svg button__icon-svg--copy">
          <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
      </span>
      ${isHidden ? "Mostra di meno" : "Mostra di più"}
    `;
  });
});



/* FUNZIONE PER ABILITARE GLI INPUT PER LA MODIFICA */
document.addEventListener("DOMContentLoaded", function() {
  var modifyBtn = document.querySelector(".Btn-modify");
  var form = document.getElementById("personaForm");
  var inputs = form.querySelectorAll(".input-disabled");
  
  var isEditing = false;
  
  modifyBtn.addEventListener("click", function(e) {
      e.preventDefault();
      if (!isEditing) {
          // Abilita gli input e aggiunge la classe "editing"
          inputs.forEach(function(input) {
              input.removeAttribute("disabled");
              input.classList.add("editing"); // Aggiunge la classe
          });
          
          var btnText = modifyBtn.querySelector(".btn-text");
          if (btnText) {
              btnText.textContent = "Salva";
          } else {
              modifyBtn.textContent = "Salva";
          }
          isEditing = true;
      } else {
          // Se si clicca in modalità "Salva", invia il form
          form.submit();
      }
  });
});










/* FUNZIONE SCARICA PDF PRESCRIZIONE */
/* document.addEventListener("DOMContentLoaded", function () {
  const pdfButtons = document.querySelectorAll(".generatePDFButton");
  const modal = document.getElementById("pdfDisclaimerModal");
  const closeBtn = document.getElementById("closeDisclaimerBtn");

  pdfButtons.forEach((button) => {
    button.addEventListener("click", async (event) => {
      event.preventDefault();
      
      const pdfUrl = button.getAttribute("data-pdf-url");
      const name = button.getAttribute("data-name") || "N/A";
      const surname = button.getAttribute("data-surname") || "N/A";
      const dob = button.getAttribute("data-dob") || "N/A";
      const cf = button.getAttribute("data-cf") || "N/A";

      if (!pdfUrl) {
        console.error("Errore: URL PDF non trovato!");
        return;
      }

      // Mostra il disclaimer modal
      modal.classList.remove("hidden");

      // Dopo che il disclaimer viene accettato, genera il PDF
      closeBtn.addEventListener("click", async () => {
        modal.classList.add("hidden");
        await generatePDF(pdfUrl, name, surname, dob, cf);
      }, { once: true }); // `{ once: true }` evita multiple generazioni
    });
  });
});
 */
