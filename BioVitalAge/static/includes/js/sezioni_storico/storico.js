import showAlert from "../components/showAlert.js";

/*  -----------------------------------------------------------------------------------------------
        Listener per la paginazione
--------------------------------------------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // ⏱️ Inizializza subito i bottoni all'avvio della pagina
    inizializeButtons();

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
                    const newContent = doc.querySelector('#storico-wrapper');
                    document.querySelector('#storico-wrapper').innerHTML = newContent.innerHTML;

                    // 🔁 Reinizializza i listener dopo il nuovo contenuto
                    inizializeButtons();
                });
        }
    });
});
        

/*  -----------------------------------------------------------------------------------------------
Listener per il pulsante "Modifica"
--------------------------------------------------------------------------------------------------- */
const appuntamentiUrl = document.body.dataset.appuntamentiUrl;

document.querySelectorAll(".edit").forEach(btn => {
    btn.addEventListener("click", () => {
        const appointmentId = btn.dataset.id;
        localStorage.setItem("editAppointmentId", appointmentId);
        window.location.href = appuntamentiUrl;  // cambia se hai un path diverso
    });
});


// /*  -----------------------------------------------------------------------------------------------
// Funzione per mostrare un alert
// --------------------------------------------------------------------------------------------------- */
// function showAlert(type, message) {
//     // Controllo se esiste già un alert visibile
//     let existingAlert = document.getElementById("global-alert");
//     if (existingAlert) existingAlert.remove();

//     // Creazione del div per l'alert Bootstrap
//     let alertDiv = document.createElement("div");
//     alertDiv.id = "global-alert";
//     alertDiv.classList.add("alert", `alert-${type}`, "fade", "show");
//     alertDiv.style.position = "fixed";
//     alertDiv.style.top = "20px";
//     alertDiv.style.left = "50%";
//     alertDiv.style.transform = "translateX(-50%)";
//     alertDiv.style.zIndex = "1050";
//     alertDiv.style.width = "auto";
//     alertDiv.style.maxWidth = "400px";
//     alertDiv.style.display = "flex";
//     alertDiv.style.justifyContent = "space-between";
//     alertDiv.style.alignItems = "center";
//     alertDiv.style.padding = "10px 15px";
//     alertDiv.style.borderRadius = "6px";
//     alertDiv.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";
//     alertDiv.style.opacity = "0"; // Inizialmente nascosto

//     // Contenuto dell'alert
//     alertDiv.innerHTML = `
//                 <span>${message}</span>
//                 <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
//             `;

//     // Aggiunge l'alert al DOM
//     document.body.appendChild(alertDiv);

//     // Effetto di comparsa con GSAP
//     gsap.to(alertDiv, { opacity: 1, duration: 0.3, ease: "power2.out" });

//     // Rimuove automaticamente l'alert dopo 5 secondi con un fade-out
//     setTimeout(() => {
//         gsap.to(alertDiv, {
//             opacity: 0,
//             duration: 0.3,
//             ease: "power2.in",
//             onComplete: () => alertDiv.remove(),
//         });
//     }, 5000);
// }

/*  -----------------------------------------------------------------------------------------------
|   JS PER ELIMINARE UN APPUNTAMENTO
--------------------------------------------------------------------------------------------------- */
function inizializeButtons() {
    /*  -----------------------------------------------------------------------------------------------
        Gestione tabella storico appuntamenti
    --------------------------------------------------------------------------------------------------- */
    // Funzione per eliminare un appuntamento
    document.querySelectorAll(".btn.delete").forEach(btn => {
        btn.addEventListener("click", function () {
            const appointmentId = this.dataset.id;
            const row = this.closest("tr");
            confirmDeleteAppointment(appointmentId, row);
        });
    });

    // Funzione per modificare un appuntamento
    document.querySelectorAll(".btn.edit").forEach(btn => {
        const appointmentDate = new Date(btn.dataset.date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        appointmentDate.setHours(0, 0, 0, 0);

        // Disabilita il bottone se data nel passato
        if (appointmentDate < today) {
            btn.disabled = true;
        }

        btn.addEventListener("click", function () {
            const appointmentId = this.dataset.id;
            localStorage.setItem("editAppointmentId", appointmentId);
            window.location.href = appuntamentiUrl;
        });
    });
}
// Funzione per eliminare un appuntamento
function deleteAppointment(appointmentId, appointmentBox, confirmAlert) {
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
                // 🔹 Effetto GSAP per la rimozione fluida del box appuntamento
                gsap.to(appointmentBox, {
                    opacity: 0,
                    duration: 0.3,
                    ease: "power2.in",
                    onComplete: () => appointmentBox.remove(),
                });

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

// Funzione per confermare l'eliminazione di un appuntamento tramite modale bootstrap con GSAP
function confirmDeleteAppointment(appointmentId, appointmentBox) {
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
        deleteAppointment(appointmentId, appointmentBox, confirmAlert);
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


/*  -----------------------------------------------------------------------------------------------
    Grafico Appuntamenti
--------------------------------------------------------------------------------------------------- */
const ctx = document.getElementById('graficoDiagnosi').getContext('2d');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'],
        datasets: [{
            label: 'Appuntamenti Mensili',
            data: appuntamenti_per_mese_var,
            backgroundColor: 'rgba(128, 90, 213, 0.3)',
            borderColor: 'rgba(128, 90, 213, 1)',
            pointBackgroundColor: 'rgba(128, 90, 213, 1)',
            fill: true,
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        interaction: {
            mode: 'nearest',
            intersect: false
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 30,
                ticks: {
                    stepSize: 5
                }
            }
        }
    }
});