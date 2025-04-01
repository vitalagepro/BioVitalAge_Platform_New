/*  -----------------------------------------------------------------------------------------------
  Actions on appointments
--------------------------------------------------------------------------------------------------- */
function confirmDeleteAppointment(appointmentId) {
  // Controllo se c'è già un alert visibile
  let existingAlert = document.getElementById("delete-alert");
  if (existingAlert) existingAlert.remove();

  // 🔹 Creazione alert Bootstrap personalizzato
  let confirmAlert = document.createElement("div");
  confirmAlert.id = "delete-alert";
  confirmAlert.classList.add("alert", "alert-danger", "fade", "show");
  confirmAlert.style.position = "fixed";
  confirmAlert.style.top = "20px";
  confirmAlert.style.left = "50%";
  confirmAlert.style.transform = "translateX(-50%)";
  confirmAlert.style.zIndex = "1050";
  confirmAlert.style.width = "auto";
  confirmAlert.style.maxWidth = "420px";
  confirmAlert.style.display = "flex";
  confirmAlert.style.justifyContent = "space-between";
  confirmAlert.style.alignItems = "center";
  confirmAlert.style.padding = "10px 15px";
  confirmAlert.style.borderRadius = "6px";
  confirmAlert.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";
  confirmAlert.style.opacity = "0"; // 🔹 Opacità iniziale per GSAP

  confirmAlert.innerHTML = `
      <span>Sei sicuro di voler eliminare questo appuntamento?</span>
      <div class="d-flex gap-2">
          <button type="button" class="btn btn-sm btn-danger" id="confirmDelete">Elimina</button>
          <button type="button" class="btn btn-sm btn-secondary" id="cancelDelete">Annulla</button>
      </div>
  `;

  // 🔹 Aggiungo l'alert al DOM
  document.body.appendChild(confirmAlert);

  // 🔹 Effetto GSAP per far apparire l'alert con un fade-in
  gsap.to(confirmAlert, { opacity: 1, duration: 0.3, ease: "power2.out" });

  // 🔹 Eventi sui bottoni
  document.getElementById("confirmDelete").addEventListener("click", () => {
    deleteAppointment(appointmentId, confirmAlert);
  });

  document.getElementById("cancelDelete").addEventListener("click", () => {
    gsap.to(confirmAlert, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => confirmAlert.remove(),
    });
  });

  // 🔹 Rimuove automaticamente l'alert dopo 10 secondi con un fade-out GSAP
  setTimeout(() => {
    gsap.to(confirmAlert, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => confirmAlert.remove(),
    });
  }, 10000);
}

function deleteAppointment(appointmentId, confirmAlert) {
  fetch(`/delete-appointment/${appointmentId}/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Errore HTTP: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        // 🔹 Rimuove anche l'alert di conferma
        gsap.to(confirmAlert, {
          opacity: 0,
          duration: 0.3,
          ease: "power2.in",
          onComplete: () => confirmAlert.remove(),
        });

        // 🔹 Mostra l'alert di successo
        showAlert("success", "Appuntamento eliminato con successo!");
      } else {
        console.error("❌ Errore nella cancellazione:", data.error);
        showAlert("danger", "Errore nella cancellazione dell'appuntamento.");
      }
    })
    .catch((error) => {
      console.error("❌ Errore nella richiesta:", error);
      showAlert("danger", "Errore nella richiesta al server.");
    });
}

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
              showAlert("success", "Appuntamento confermato!");
            } else {
              showAlert("danger", "Errore: " + data.error);
            }
          });
      } else if (action === "delete") {
        confirmDeleteAppointment(appointmentId);
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