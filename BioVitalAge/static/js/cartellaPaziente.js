import showAlert from "./components/showAlert.js";

/*----------------------------------------------------
  Funzione per gestire dinamicamente la popolazione
  delle Modali degli Indici di Performance
-----------------------------------------------------*/

const cards = document.querySelectorAll('.cardIndici')
const modaleIndici = document.getElementById('modaleIndici')
const backdropIndici = document.getElementById('backdropIndici')
const dynamicTitle = document.getElementById('dynamicTitle')
const closeButton = document.getElementById('closeModale')
const dynamicImage = document.getElementById('dynamicImage')


function getScrollbarWidth() {
  return window.innerWidth - document.documentElement.clientWidth;
}

function lockBodyScroll() {
  const sbWidth = getScrollbarWidth();
  document.documentElement.style.setProperty('--scrollbar-width', `${sbWidth}px`);
  document.body.classList.add('body--no-scroll');
}

function unlockBodyScroll() {
  document.body.classList.remove('body--no-scroll');
  document.documentElement.style.removeProperty('--scrollbar-width');
}

cards.forEach(card => {
  card.addEventListener('click', () => {

    window.scrollTo({ top: 0, behavior: 'smooth' });

    const name     = card.getAttribute('card-name');  
    const imgPath  = card.getAttribute('img-card');   

    dynamicTitle.textContent = name;
    dynamicImage.src         = imgPath;

    modaleIndici.style.display   = 'block';
    backdropIndici.style.display = 'block';
    lockBodyScroll();
  });
});

closeButton.addEventListener('click', () => {
  modaleIndici.style.display   = 'none';
  backdropIndici.style.display = 'none';
  unlockBodyScroll();        
});


























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
// document.addEventListener("DOMContentLoaded", function () {
//   // Seleziona il tasto "Mostra di più"
//   const toggleButton = document.querySelector(".button-view-all");
//   if (!toggleButton) return;
  
//   // Seleziona l'intero contenitore dei bottoni
//   const buttonGrid = document.querySelector(".button-grid");
//   // Crea un array con tutti i figli del buttonGrid tranne il toggle button
//   const otherButtons = Array.from(buttonGrid.children).filter(el =>
//     !el.classList.contains("button-view-all")
//   );
  
//   // Inizialmente nasconde gli altri bottoni (mantiene visibile solo il toggle)
//   otherButtons.forEach((btn) => {
//     gsap.set(btn, { opacity: 0, display: "none" });
//   });

//   // Seleziona i contenitori che già gestisci per i campi della card
//   const infoContainer = document.querySelector(".container_box");
//   const contactContainer = document.querySelector(".Contact-Container");
//   const subCardsContainer = document.querySelector(".subCard-container");
  
//   // Seleziona i campi della card (compresi email e telefono)
//   const hiddenFields = infoContainer.querySelectorAll(".field, .email, .telefono");

//   // Nasconde i campi all'inizio
//   hiddenFields.forEach((field) => {
//     gsap.set(field, { opacity: 0, display: "none" });
//   });

//   // Nasconde anche le sub-card e il container dei contatti
//   gsap.set(subCardsContainer, { opacity: 0, display: "none" });
//   gsap.set(contactContainer, { opacity: 0, display: "none" });
  
//   // Aggiunge una classe per gestire il layout se necessario
//   infoContainer.classList.add("hidden-row-grid");

//   // Aggiunge il listener al toggle button (Mostra di più / Mostra di meno)
//   toggleButton.addEventListener("click", function () {
//     // Determina se i campi sono attualmente nascosti
//     const isHidden = hiddenFields[0].style.display === "none";

//     // Toggle per i campi della card
//     hiddenFields.forEach((field) => {
//       if (isHidden) {
//         gsap.to(field, { opacity: 1, display: "flex", duration: 0.5 });
//       } else {
//         gsap.to(field, { opacity: 0, display: "none", duration: 0.5 });
//       }
//     });

//     // Toggle per le sub-card e i contatti
//     if (isHidden) {
//       gsap.to(subCardsContainer, { opacity: 1, display: "flex", duration: 0.5 });
//       gsap.to(contactContainer, { opacity: 1, display: "flex", duration: 0.5 });
//       infoContainer.classList.remove("hidden-row-grid");
//       // Mostra gli altri bottoni quando la card è visibile
//       otherButtons.forEach((btn) => {
//         gsap.to(btn, { opacity: 1, display: "flex", duration: 0.5 });
//       });
//     } else {
//       gsap.to(subCardsContainer, { opacity: 0, display: "none", duration: 0.5 });
//       gsap.to(contactContainer, { opacity: 0, display: "none", duration: 0.5 });
//       infoContainer.classList.add("hidden-row-grid");
//       // Nasconde gli altri bottoni quando la card viene chiusa
//       otherButtons.forEach((btn) => {
//         gsap.to(btn, { opacity: 0, display: "none", duration: 0.5 });
//       });
//     }

//     // Aggiorna il testo e le icone del bottone toggle
//     toggleButton.innerHTML = `
//       <span class="button__icon-wrapper">
//         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" width="18" class="button__icon-svg">
//           <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
//         </svg>
//         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" width="18" class="button__icon-svg button__icon-svg--copy">
//           <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
//         </svg>
//       </span>
//       ${isHidden ? "Mostra di meno" : "Mostra di più"}
//     `;
//   });
// });



/* FUNZIONE PER ABILITARE GLI INPUT PER LA MODIFICA */
// document.addEventListener("DOMContentLoaded", () => {
//   const modifyBtn       = document.querySelector(".Btn-modify");
//   const displaySpan     = document.getElementById("associate-display");
//   const selectField     = document.getElementById("associate-select");
//   const otherInputs     = document.querySelectorAll(".input-disabled:not([name='associate_staff'])");
//   let   isEditing       = false;


//   modifyBtn.addEventListener("click", e => {
//     e.preventDefault();

//     // ➊ Se non sei segretaria/o, alert su click dello span

//     if (displaySpan && !window.isSecretary) {
//       console.log("Non sei segretaria/o, non puoi modificare questo campo.");
//       displaySpan.style.cursor = "pointer";
//       displaySpan.addEventListener("click", () => {
//         showAlert({
//           type: "warning",
//           message: "Non hai i permessi per modificare questo campo.",
//           extraMessage: "Solo la segreteria può modificare questo campo.",
//           borderColor: "#f97316",
//         });
//       });
//     }

//     if (!isEditing) {
//       // 1) se sono segretaria, nascondi lo span e mostra il select
//       if (window.isSecretary && selectField) {
//         displaySpan.style.display = "none";
//         selectField.style.display = "";   // rimuove display:none
//         selectField.classList.add("editing");
//       }

//       // 2) abilita TUTTI gli altri input
//       otherInputs.forEach(inp => {
//         inp.removeAttribute("disabled");
//         inp.classList.add("editing");
//       });

//       modifyBtn.innerHTML = `
//         <span class="btn-text">Salva</span>
//         <svg class="svg" style="width: 25px; height: 25px;" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
//           <!-- Cloud -->
//           <path d="M19.35 10.04A7.49 7.49 0 0 0 12 4C9.24 4 7 6.24 7 9a5 5 0 0 0 .11 1H5a4 4 0 0 0 0 8h14a3 3 0 0 0 .35-5.96z"/>
//           <!-- Freccia verso il basso -->
//           <path d="M13 12v5h-2v-5H8l4-4 4 4h-3z" style="fill: grey;"/>
//         </svg>
//       `;
//       isEditing = true;

//     } else {
//       // invia il form in modalità "Salva"
//       document.getElementById("personaForm").submit();
//     }
//   });
// });














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
