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
  borderColor
}) {
  let existingAlert = document.getElementById("delete-alert");
  if (existingAlert) existingAlert.remove();

  const confirmAlert = document.createElement("div");
  confirmAlert.id = "delete-alert";
  confirmAlert.style.position = "fixed";
  confirmAlert.style.top = "20px";
  confirmAlert.style.left = "50%";
  confirmAlert.style.transform = "translateX(-50%)";
  confirmAlert.style.zIndex = "1050";
  confirmAlert.style.maxWidth = "430px";
  confirmAlert.style.backgroundColor = "#fff";
  confirmAlert.style.borderRadius = "12px";
  confirmAlert.style.padding = "15px 20px";
  confirmAlert.style.boxShadow = "0 4px 14px rgba(0, 0, 0, 0.15)";
  confirmAlert.style.display = "flex";
  confirmAlert.style.flexDirection = "column";
  confirmAlert.style.gap = "10px";
  confirmAlert.style.opacity = "0";
  confirmAlert.style.borderBottom = "4px solid " + borderColor;

  confirmAlert.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 20px;">⚠️</span>
        <span style="color: #ef4444; font-weight: 600; font-size: 18px;">
          Conferma eliminazione
        </span>
      </div>
      <button style="background: none; border: none; font-size: 16px; cursor: pointer;" onclick="this.closest('#delete-alert').remove()">✖</button>
    </div>
    <div style="color: #333;">${confirmMessage}</div>
    <div style="display: flex; justify-content: flex-end; gap: 10px;">
      <button id="cancelDelete" style="background-color: #e5e7eb; color: #111827; padding: 6px 12px; border: none; border-radius: 6px; cursor: pointer;">Annulla</button>
      <button id="confirmDelete" style="background-color: #dc2626; color: white; padding: 6px 12px; border: none; border-radius: 6px; cursor: pointer;">Elimina</button>
    </div>
  `;

  document.body.appendChild(confirmAlert);

  // Entrata animata
  gsap.to(confirmAlert, { opacity: 1, duration: 0.3, ease: "power2.out" });

  // Listener per "Elimina"
  document.getElementById("confirmDelete").addEventListener("click", () => {
    deleteAction({
      url,
      elementToRemove,
      confirmAlert,
      successMessage,
      errorMessage,
    });
  });

  // Listener per "Annulla"
  document.getElementById("cancelDelete").addEventListener("click", () => {
    gsap.to(confirmAlert, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => confirmAlert.remove(),
    });
  });

  // Timeout auto-rimozione dopo 10s
  setTimeout(() => {
    if (document.body.contains(confirmAlert)) {
      gsap.to(confirmAlert, {
        opacity: 0,
        duration: 0.3,
        ease: "power2.in",
        onComplete: () => confirmAlert.remove(),
      });
    }
  }, 10000);
}
