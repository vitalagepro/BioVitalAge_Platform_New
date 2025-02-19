/*  -----------------------------------------------------------------------------------------------
  Animazioni
--------------------------------------------------------------------------------------------------- */
gsap.from(".card-appointments", { opacity: 0, y: -50, duration: 1 });

/*  -----------------------------------------------------------------------------------------------
  Prenota un appuntamento
--------------------------------------------------------------------------------------------------- */
$(document).ready(function () {
  $("#appointmentForm").submit(function (event) {
    event.preventDefault();
    const appointmentData = {
      cognome_paziente: $("#cognome").val(),
      nome_paziente: $("#nome_paziente").val(),
      eta: $("#eta").val(),
      tipologia_visita: $("#tipologia_visita").val(),
      diagnosi: $("#diagnosi").val(),
      orario: $("#orario").val(),
      numero_stanza: $("#numero_stanza").val(),
    };

    $.ajax({
      type: "POST",
      url: "/api/appointments/",
      contentType: "application/json",
      data: JSON.stringify(appointmentData),
      success: function () {
        $("#successModal").modal("show");
        $("#appointmentForm")[0].reset();
      },
      error: function () {
        $("#errorModal").modal("show");
      },
    });
  });
});

// Funzione per riempire i campi con i dati del paziente selezionato
$(document).ready(function () {
  $("#patients-select").change(function () {
    let selectedOption = $(this).find(":selected");

    $("#cognome").val(selectedOption.data("cognome"));
    $("#nome_paziente").val(selectedOption.data("nome"));
    $("#eta").val(selectedOption.data("eta"));

    setTimeout(() => {
      $(this).val("default");
    }, 100);
  });
});

/*  -----------------------------------------------------------------------------------------------
    Actions on appointments
  --------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".action-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const row = this.closest("tr");
      const appointmentId = row.getAttribute("data-id");
      const action = this.classList.contains("approve") ? "approve" : "delete";

      if (action === "approve") {
        fetch(`/api/appointments/${appointmentId}/approve/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              row.style.backgroundColor = "#d4edda";
              $("#successModal .modal-body").text("Appuntamento confermato!");
              $("#successModal").modal("show");
            } else {
              $("#errorModal .modal-body").text("Errore: " + data.error);
              $("#errorModal").modal("show");
            }
          });
      } else if (action === "delete") {
        if (!confirm("Sei sicuro di voler eliminare questo appuntamento?"))
          return;

        fetch(`/api/appointments/${appointmentId}/delete/`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              row.remove();
              $("#successModal .modal-body").text("Appuntamento eliminato!");
              $("#successModal").modal("show");
            } else {
              $("#errorModal .modal-body").text("Errore: " + data.error);
              $("#errorModal").modal("show");
            }
          });
      }
    });
  });

  function getCSRFToken() {
    let csrfToken = null;
    document.cookie.split(";").forEach((cookie) => {
      let [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") csrfToken = value;
    });
    return csrfToken;
  }
});

/*  -----------------------------------------------------------------------------------------------
  Pagination
--------------------------------------------------------------------------------------------------- */
$(document).ready(function () {
  const rowsPerPage = 6; // Numero di righe per pagina
  let rows = $(".cardAppuntamenti tbody tr"); // Seleziona le righe della tabella
  let totalRows = rows.length;
  let totalPages = Math.ceil(totalRows / rowsPerPage);
  let currentPage = 1;

  function showPage(page) {
    let start = (page - 1) * rowsPerPage;
    let end = start + rowsPerPage;

    rows.hide().slice(start, end).fadeIn();

    updatePagination(page);
  }

  function updatePagination(current) {
    let pagination = $("#pagination");
    pagination.empty();

    if (totalPages <= 1) return; // Nasconde la paginazione se c'è solo una pagina

    let pagesToShow = 10; // Numero massimo di pagine visibili prima dei puntini

    let startPage = Math.max(1, current - 2); // Mostra sempre 2 pagine prima della corrente
    let endPage = Math.min(totalPages, startPage + pagesToShow - 1); // Mostra massimo 10 pagine

    if (endPage - startPage < pagesToShow - 1) {
      startPage = Math.max(1, endPage - pagesToShow + 1);
    }

    // Aggiungi il pulsante "Precedente"
    if (current > 1) {
      pagination.append(
        `<button class="page-btn" data-page="${current - 1}">&laquo;</button>`
      );
    }

    // Mostra sempre la prima pagina
    if (startPage > 1) {
      pagination.append(`<button class="page-btn" data-page="1">1</button>`);
      if (startPage > 2) {
        pagination.append(`<span class="dots">...</span>`);
      }
    }

    // Mostra i numeri di pagina dinamici
    for (let i = startPage; i <= endPage; i++) {
      if (i === current) {
        pagination.append(
          `<button class="page-btn active" data-page="${i}">${i}</button>`
        );
      } else {
        pagination.append(
          `<button class="page-btn" data-page="${i}">${i}</button>`
        );
      }
    }

    // Aggiungi puntini e ultima pagina
    if (endPage < totalPages - 1) {
      pagination.append(`<span class="dots">...</span>`);
    }
    if (endPage < totalPages) {
      pagination.append(
        `<button class="page-btn" data-page="${totalPages}">${totalPages}</button>`
      );
    }

    // Aggiungi il pulsante "Successivo"
    if (current < totalPages) {
      pagination.append(
        `<button class="page-btn" data-page="${current + 1}">&raquo;</button>`
      );
    }

    $(".page-btn").click(function () {
      let newPage = parseInt($(this).attr("data-page"));
      showPage(newPage);
    });
  }

  showPage(1);
});
