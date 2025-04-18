import showAlert from "../../js/components/showAlert.js";
import { confirmDeleteAction } from "../../js/components/deleteAction.js";

/*  -----------------------------------------------------------------------------------------------
  Actions on appointments
--------------------------------------------------------------------------------------------------- */

// 🔹 Aggiungo l'evento al caricamento del DOM
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".action-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const row = this.closest("tr"); // Trova la riga
      const appointmentId = row.getAttribute("data-id"); // Ottiene l'ID dall'attributo data-id
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
              row.style.backgroundColor = "#d4edda"; // Verde per indicare confermato
              showAlert("success", "Appuntamento confermato!", "", "var(--positive-color)");
            } else {
              showAlert("danger", "Errore: " + data.error, "", "#EF4444");
            }
          });
      } else if (action === "delete") {
        confirmDeleteAction({
          url: `/delete-appointment/${appointmentId}/`,
          elementToRemove: row,
          successMessage: "Appuntamento eliminato con successo!",
          errorMessage: "Errore nella cancellazione dell'appuntamento",
          confirmMessage: "Sei sicuro di voler eliminare questo appuntamento?",
          borderColor: "#EF4444",
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
    ANIMAZIONE NUMERI
--------------------------------------------------------------------------------------------------- */
// 🔹 Anima i numeri che calolano il totale
document.addEventListener('DOMContentLoaded', function(){
  // Funzione per animare il conteggio di un elemento
  const animateNumber = (selector, duration = 2) => {
    const element = document.querySelector(selector);
    if (!element) return;
    const target = parseInt(element.textContent, 10);
    // Inizializza un oggetto con count = 0
    const obj = { count: 0 };
    gsap.to(obj, {
      duration: duration,
      count: target,
      ease: "power1.out",
      roundProps: "count",  // Arrotonda il numero durante l'animazione
      onUpdate: () => {
        element.textContent = obj.count;
      }
    });
  };
  
  // Anima i numeri
  animateNumber("#total-pazienti");
  animateNumber("#total-biological-age");
});

/*  -----------------------------------------------------------------------------------------------
    ANIMAZIONE NUMERI DELLE CARD DEI REPORT
--------------------------------------------------------------------------------------------------- */
// Registra ScrollTrigger in GSAP
gsap.registerPlugin(ScrollTrigger);

// Seleziona tutti gli elementi che hanno la classe "animate-num"
document.querySelectorAll('.animate-num').forEach(function(elem) {
  var target = parseFloat(elem.getAttribute('data-target')) || 0;
  var obj = { value: 0 };

  gsap.to(obj, {
    value: target,
    duration: 2,
    ease: "power1.out",
    scrollTrigger: {
      trigger: elem,
      start: "top 80%",
      once: true
    },
    onUpdate: function() {
      elem.textContent = Math.round(obj.value);
    }
  });
});


/*  -----------------------------------------------------------------------------------------------
    RIMUOVI APPUNTAMENTI PASSATI
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const today = new Date();
  today.setHours(0, 0, 0, 0); // resetta ora per confrontare solo la data

  const rows = document.querySelectorAll("table tbody tr");

  rows.forEach((row) => {
    const dateCell = row.querySelector("td:nth-child(3)"); // 3ª colonna = Data

    if (dateCell) {
      const dateParts = dateCell.textContent.trim().split("/");
      const rowDate = new Date(
        parseInt(dateParts[2]),
        parseInt(dateParts[1]) - 1,
        parseInt(dateParts[0])
      );

      rowDate.setHours(0, 0, 0, 0);

      if (rowDate < today) {
        row.style.display = "none";
      }
    }
  });
});

