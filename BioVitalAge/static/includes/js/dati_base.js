
  const editButton = document.getElementById("btn_blood_group");
  const saveButton = document.getElementById("btn_save_changes");
  const form = document.querySelector("form");
  let isEditing = false;

  editButton.addEventListener("click", function (e) {
    e.preventDefault();
    isEditing = !isEditing;

    const inputs = form.querySelectorAll("input:disabled");

    inputs.forEach((input) => {
      if (isEditing) {
        input.disabled = false;
        input.classList.add("editing");
      } else {
        input.disabled = true;
        input.classList.remove("editing");
      }
    });

    // Mostra/Nasconde bottone Salva
    saveButton.style.display = isEditing ? "inline-flex" : "none";

    // Cambia testo/modifica/cancella
    editButton.querySelector("span").innerText = isEditing ? "Cancella" : "Modifica Dati";
  });

  saveButton.addEventListener("click", function (e) {
    e.preventDefault();
    form.submit(); // Submit normale
  });

