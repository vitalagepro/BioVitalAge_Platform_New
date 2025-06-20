/* FUNZIONE PER LA RICERCA PAZIENTE  */
document.addEventListener("DOMContentLoaded", () => {
  const rows = Array.from(document.querySelectorAll(".riga-container"));
  const rowsPerPage = 5;
  let currentPage = 1;

  function showPage(page, set = rows) {
    currentPage = page;
    // Nascondi tutte le righe
    rows.forEach(r => r.style.display = "none");
    // Calcola slice
    const start = (page - 1) * rowsPerPage;
    const end = page * rowsPerPage;
    const pageRows = set.slice(start, end);
    // Mostra e anima le righe
    pageRows.forEach(r => r.style.display = "flex");
    gsap.fromTo(pageRows,
      { opacity: 0,  y: -10 },
      { opacity: 1, y:  0, duration: 0.3, stagger: 0.05 }
    );
    renderPagination(set);
  }

  function renderPagination(set) {
    const totalPages = Math.ceil(set.length / rowsPerPage);
    const maxButtons = 6;
    let container = document.querySelector(".pagination-controls");

    if (!container) {
      container = document.createElement("div");
      container.className = "pagination-controls";
      document.querySelector(".bg-white").appendChild(container);
    }

    container.innerHTML = "";

    // ← Freccia indietro
    const prev = document.createElement("button");
    prev.className = "pagination-arrow prev";
    prev.textContent = "<";
    prev.disabled = currentPage === 1;
    prev.addEventListener("click", () => {
      if (currentPage > 1) showPage(currentPage - 1, set);
    });
    container.appendChild(prev);

    // Numeri di pagina (fino a maxButtons)
    const pagesToShow = Math.min(totalPages, maxButtons);
    for (let i = 1; i <= pagesToShow; i++) {
      const btn = document.createElement("button");
      btn.className = "button-style-pagination";
      btn.textContent = i;
      if (i === currentPage) btn.classList.add("active");
      btn.addEventListener("click", () => showPage(i, set));
      container.appendChild(btn);
    }

    // “…” se ci sono più pagine di maxButtons
    if (totalPages > maxButtons) {
      const ell = document.createElement("span");
      ell.className = "pagination-ellipsis";
      ell.textContent = "...";
      container.appendChild(ell);
    }

    // → Freccia avanti
    const next = document.createElement("button");
    next.className = "pagination-arrow next";
    next.textContent = ">";
    next.disabled = currentPage === totalPages;
    next.addEventListener("click", () => {
      if (currentPage < totalPages) showPage(currentPage + 1, set);
    });
    container.appendChild(next);
  }

  function filterRows() {
    const term = document.getElementById("Email").value.toLowerCase().trim();
    const type = document.getElementById("filter").value;
    const filtered = rows.filter(row => {
      const cells = row.querySelectorAll("p");
      switch (type) {
        case "name":
          return cells[0].textContent.toLowerCase().includes(term);
        case "surname":
          return cells[1].textContent.toLowerCase().includes(term);
        case "fisc_code":
          return cells[3].textContent.toLowerCase().includes(term);
        case "personal_association":
          return cells[6].textContent.toLowerCase().includes(term);
        default:
          return true;
      }
    });

    if (filtered.length) {
      document.querySelector(".table-container").style.display = "block";
      showPage(1, filtered);
    } else {
      document.querySelector(".table-container").style.display = "none";
    }
  }

  // Bind sul form e sull’input
  const form = document.querySelector(".barra-ricerca form");
  form.addEventListener("submit", e => {
    e.preventDefault();
    filterRows();
  });

  const input = document.getElementById("Email");
  input.addEventListener("input", () => {
    if (!input.value.trim()) {
      showPage(1);
    } else {
      filterRows();
    }
  });

  // Avvia mostrando la pagina 1 in ordine cronologico
  showPage(1);
});
