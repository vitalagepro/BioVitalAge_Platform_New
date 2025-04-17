// components/deleteAction.js

import showAlert from "./showAlert.js";

export function deleteAction({
  url,
  elementToRemove,
  confirmAlert = null,
  successMessage,
  errorMessage,
}) {
  fetch(url, {
    method: "POST", // ✅ compatibile con Django + CSRF
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrf-token]").content,
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
        if (elementToRemove) {
          gsap.to(elementToRemove, {
            opacity: 0,
            duration: 0.3,
            ease: "power2.in",
            onComplete: () => elementToRemove.remove(),
          });
        }

        if (confirmAlert) {
          gsap.to(confirmAlert, {
            opacity: 0,
            duration: 0.3,
            ease: "power2.in",
            onComplete: () => confirmAlert.remove(),
          });
        }

        showAlert("success", successMessage);
      } else {
        console.error("❌ Errore nella cancellazione:", data.error);
        showAlert("danger", errorMessage);
      }
    })
    .catch((error) => {
      console.error("❌ Errore nella richiesta:", error);
      showAlert("danger", "Errore nella richiesta al server.");
    });
}

export function confirmDeleteAction({
  url,
  elementToRemove,
  successMessage,
  errorMessage,
  confirmMessage,
}) {
  let existingAlert = document.getElementById("delete-alert");
  if (existingAlert) existingAlert.remove();

  let confirmAlert = document.createElement("div");
  confirmAlert.id = "delete-alert";
  confirmAlert.classList.add("alert", "alert-danger", "fade", "show");
  confirmAlert.style.position = "fixed";
  confirmAlert.style.top = "20px";
  confirmAlert.style.left = "50%";
  confirmAlert.style.transform = "translateX(-50%)";
  confirmAlert.style.zIndex = "1050";
  confirmAlert.style.width = "auto";
  confirmAlert.style.maxWidth = "425px";
  confirmAlert.style.display = "flex";
  confirmAlert.style.justifyContent = "space-between";
  confirmAlert.style.alignItems = "center";
  confirmAlert.style.padding = "10px 15px";
  confirmAlert.style.borderRadius = "6px";
  confirmAlert.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";
  confirmAlert.style.opacity = "0";

  confirmAlert.innerHTML = `
    <span>${confirmMessage}</span>
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-danger" id="confirmDelete">Elimina</button>
      <button type="button" class="btn btn-sm btn-secondary" id="cancelDelete">Annulla</button>
    </div>
  `;

  document.body.appendChild(confirmAlert);
  gsap.to(confirmAlert, { opacity: 1, duration: 0.3, ease: "power2.out" });

  document.getElementById("confirmDelete").addEventListener("click", () => {
    deleteAction({
      url,
      elementToRemove,
      confirmAlert,
      successMessage,
      errorMessage,
    });
  });

  document.getElementById("cancelDelete").addEventListener("click", () => {
    gsap.to(confirmAlert, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => confirmAlert.remove(),
    });
  });

  setTimeout(() => {
    gsap.to(confirmAlert, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => confirmAlert.remove(),
    });
  }, 10000);
}
