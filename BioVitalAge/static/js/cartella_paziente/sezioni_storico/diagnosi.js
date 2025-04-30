/*  -----------------------------------------------------------------------------------------------
    Range Gravità
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const range = document.getElementById("gravitaRange");
  const indicator = document.getElementById("indicator");
  const label = document.getElementById("gravitaLabel");

  const map = {
    1: { label: "Lieve", x: 40, y: 10, color: "#4CAF50" },
    2: { label: "Moderata", x: 140, y: 10, color: "#FFC107" },
    3: { label: "Grave", x: 240, y: 10, color: "#F44336" },
  };

  function updateIndicator(value, animate = true) {
    const { x: targetX, y: targetY, label: gravitaLabel, color } = map[value];

    if (animate) {
      gsap.to(indicator, {
        x: targetX,
        y: targetY,
        fill: color,
        duration: 0.4,
        ease: "back.out(1.7)",
      });
    } else {
      gsap.set(indicator, { x: targetX, y: targetY, fill: color });
    }

    label.textContent = gravitaLabel;
  }

  range.addEventListener("input", () => {
    updateIndicator(range.value);
  });

  // Inizializza
  updateIndicator(range.value, false);
});

/*  -----------------------------------------------------------------------------------------------
    Modale
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.getElementById("openDiagnosisBtn");
  const modal = document.getElementById("diagnosisModal");
  const modalInner = modal.querySelector(".modal-content-appointments");
  const closeIcon = document.getElementById("closeDiagnosisModal");
  const closeFooter = document.getElementById("closeDiagnosisBtn");

  // Timeline GSAP (inizialmente in pausa)
  const tl = gsap.timeline({ paused: true });

  // Stati iniziali (per sicurezza)
  gsap.set(modal, { autoAlpha: 0, backdropFilter: "blur(0px)" });
  gsap.set(modalInner, { scale: 0.8, opacity: 0 });

  // Definisci l’animazione
  tl.to(modal, {
    autoAlpha: 1, // visibility: visible + opacity
    backdropFilter: "blur(6px)",
    duration: 0.3,
  }).to(
    modalInner,
    {
      scale: 1,
      opacity: 1,
      duration: 0.4,
      ease: "back.out(1.5)",
    },
    "-=0.25"
  ); // parte leggermente in sovrapposizione

  // Apri modale
  openBtn.addEventListener("click", () => {
    tl.play(0);
    document.body.style.overflow = "hidden";
  });

  // Funzione di chiusura
  function closeModal() {
    tl.reverse();
    document.body.style.overflow = "auto";
  }

  closeIcon.addEventListener("click", closeModal);
  closeFooter.addEventListener("click", closeModal);
  window.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });
});
