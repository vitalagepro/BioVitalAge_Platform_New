/*  -----------------------------------------------------------------------------------------------
        Listener per la paginazione
--------------------------------------------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function () {
  document.addEventListener('click', function (event) {
      const target = event.target;

      // Se hai cliccato su un <a> dentro la paginazione
      if (target.closest('.pagination_tabella a')) {
          event.preventDefault();

          const link = target.closest('a');
          const url = link.href;

          fetch(url)
              .then(response => response.text())
              .then(html => {
                  const parser = new DOMParser();
                  const doc = parser.parseFromString(html, 'text/html');
                  const newContent = doc.querySelector('.table-wrapper');
                  document.querySelector('.table-wrapper').innerHTML = newContent.innerHTML;
              });
      }
  });
});

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
  const form = document.getElementById("diagnosis-form");

  // Timeline GSAP (inizialmente in pausa)
  const tl = gsap.timeline({ paused: true });

  // Stati iniziali (per sicurezza)
  gsap.set(modal, { autoAlpha: 0, backdropFilter: "blur(0px)" });
  gsap.set(modalInner, { scale: 0.8, opacity: 0 });

  // Animazione modale
  tl.to(modal, {
    autoAlpha: 1,
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
  );

  // Apri modale
  openBtn.addEventListener("click", () => {
    tl.play(0);
    document.body.style.overflow = "hidden";
  });

  // Chiudi modale
  function closeModal() {
    tl.reverse();
    document.body.style.overflow = "auto";
    form.reset(); // resetta il form dopo la chiusura
  }

  closeIcon.addEventListener("click", closeModal);
  closeFooter.addEventListener("click", closeModal);
  window.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  // Intercetta il submit del form
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // blocca il comportamento di default

    const formData = new FormData(form);
    const data = {
      descrizione: formData.get("descrizione"),
      data_diagnosi: formData.get("data_diagnosi"),
      stato: formData.get("stato"),
      note: formData.get("note"),
      gravita: formData.get("gravita"),
    };

    try {
      const response = await fetch(window.location.pathname, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrf-token]").content,
          "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      if (result.success) {
        // Puoi aggiungere dinamicamente la nuova diagnosi alla tabella, se vuoi
        closeModal(); // chiudi modale
        // opzionale: mostra un alert o aggiorna parzialmente la UI
      } else {
        alert("Errore: " + (result.error || "Impossibile salvare la diagnosi."));
      }
    } catch (error) {
      console.error("Errore nel salvataggio:", error);
      alert("Errore nella richiesta.");
    }
  });
});

