import showAlert from "../../components/showAlert.js";

/*  -----------------------------------------------------------------------------------------------
   FUNZIONE PER LA GESTIONE DELLA MODAL DEI COMMENTI
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const btnOpen = document.getElementById("btn_note_commenti");
  const modal = document.getElementById("notes-modal");
  const btnClose = modal.querySelector(".modal-close");
  const titleInput = document.getElementById("note-title");
  const contentInput = document.getElementById("note-content");
  const saveBtn = document.getElementById("save-note-btn");
  const listContainer = document.getElementById("notes-list");

  let notes = [];
  let editId = null;

  function openModal() {
    modal.classList.remove("hidden");
    gsap.fromTo(
      "#notes-modal .modal-content",
      { scale: 0.8, opacity: 0 },
      { scale: 1, opacity: 1, duration: 0.3 }
    );
  }

  function closeModal() {
    gsap.to("#notes-modal .modal-content", {
      scale: 0.8,
      opacity: 0,
      duration: 0.3,
      onComplete: () => {
        modal.classList.add("hidden");
        resetForm();
      },
    });
  }

  btnOpen.addEventListener("click", openModal);
  btnClose.addEventListener("click", closeModal);

  function resetForm() {
    titleInput.value = "";
    contentInput.value = "";
    saveBtn.textContent = "Aggiungi Nota";
    editId = null;
    document
      .querySelectorAll(".floating-label")
      .forEach((lbl) => lbl.classList.remove("active-label"));
  }

  function renderNotes() {
    listContainer.innerHTML = "";
    notes.forEach((note) => {
      const div = document.createElement("div");
      div.classList.add("note-item");
      div.innerHTML = `
          <h3>${note.title}</h3>
          <p>${note.content}</p>
          <button class="view-btn" data-id="${note.id}" title="Visualizza">
            👁️
          </button>
          <button class="edit-btn" data-id="${note.id}">Modifica</button>
          <button class="delete-btn" data-id="${note.id}">Elimina</button>
        `;
      listContainer.appendChild(div);
      gsap.to(div, { opacity: 1, y: 0, duration: 0.2, ease: "power1.out" });
    });
  }

  // Floating labels
  [titleInput, contentInput].forEach((input) => {
    const label = input.nextElementSibling;
    input.addEventListener("focus", () => label.classList.add("active-label"));
    input.addEventListener("blur", () => {
      if (!input.value) label.classList.remove("active-label");
    });
  });

  saveBtn.addEventListener("click", () => {
    const title = titleInput.value.trim();
    const content = contentInput.value.trim();
    if (!title || !content) return alert("Inserisci sia titolo che contenuto.");
    if (editId !== null)
      notes = notes.map((n) =>
        n.id === editId ? { id: n.id, title, content } : n
      );
    else notes.push({ id: Date.now(), title, content });
    renderNotes();
    resetForm();
  });

  listContainer.addEventListener("click", (e) => {
    const id = +e.target.dataset.id;
    if (e.target.classList.contains("view-btn")) {
      const note = notes.find((n) => n.id === id);
      alert(note.content);
    }
    if (e.target.classList.contains("delete-btn")) {
      notes = notes.filter((n) => n.id !== id);
      renderNotes();
    }
    if (e.target.classList.contains("edit-btn")) {
      const note = notes.find((n) => n.id === id);
      titleInput.value = note.title;
      contentInput.value = note.content;
      titleInput.nextElementSibling.classList.add("active-label");
      contentInput.nextElementSibling.classList.add("active-label");
      saveBtn.textContent = "Aggiorna Nota";
      editId = id;
      titleInput.focus();
    }
  });
});
