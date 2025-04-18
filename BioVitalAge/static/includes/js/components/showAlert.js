export default function showAlert(type, message, extraMessage = "") {
  // Rimuove eventuale alert esistente
  let existingAlert = document.getElementById("global-alert");
  if (existingAlert) existingAlert.remove();

  // Crea il contenitore principale
  const alertDiv = document.createElement("div");
  alertDiv.id = "global-alert";
  alertDiv.style.position = "fixed";
  alertDiv.style.top = "20px";
  alertDiv.style.left = "50%";
  alertDiv.style.transform = "translateX(-50%)";
  alertDiv.style.zIndex = "1050";
  alertDiv.style.maxWidth = "420px";
  alertDiv.style.backgroundColor = "#fff";
  alertDiv.style.borderRadius = "12px";
  alertDiv.style.padding = "15px 20px";
  alertDiv.style.boxShadow = "0 4px 14px rgba(0, 0, 0, 0.15)";
  alertDiv.style.display = "flex";
  alertDiv.style.flexDirection = "column";
  alertDiv.style.gap = "5px";
  alertDiv.style.opacity = "0";

  // Colori e icone
  const icon = type === "success" ? "✅" : "❌";
  const titleColor = type === "success" ? "#22c55e" : "#ef4444";

  // HTML interno
  alertDiv.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 20px;">${icon}</span>
        <span style="color: ${titleColor}; font-weight: 600; font-size: 18px;">
          ${type === "success" ? "Success!" : "Errore"}
        </span>
      </div>
      <button style="background: none; border: none; font-size: 16px; cursor: pointer;" onclick="this.closest('#global-alert').remove()">✖</button>
    </div>
    <div style="color: #333;">${message}</div>
    ${extraMessage ? `<div style="color: #dc2626; font-weight: 500;">${extraMessage}</div>` : ""}
  `;

  document.body.appendChild(alertDiv);

  // Animazione entrata
  gsap.to(alertDiv, { opacity: 1, duration: 0.3, ease: "power2.out" });

  // Auto close dopo 5s
  setTimeout(() => {
    gsap.to(alertDiv, {
      opacity: 0,
      duration: 0.3,
      ease: "power2.in",
      onComplete: () => alertDiv.remove()
    });
  }, 5000);
}