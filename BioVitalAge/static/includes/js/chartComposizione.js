// ✅ Definiamo colors PRIMA di usarlo
const colors = {
  dark1: "#0c042c",
  dark2: "#0c214b",
  light1: "#c3ccd4",
  neutralGray: "#b0b8c1",
  contrastColor: "#3a255d",
  contrastColor2: "#6a2dcc",
  positiveColor: "#2ac670",
};

document.addEventListener("DOMContentLoaded", async function () {
  function getBmiDistribution(bmi) {
    if (bmi < 18.5) {
      return [100, 0, 0, 0]; // Tutto in "Insufficientemente grasso"
    } else if (bmi >= 18.5 && bmi < 25) {
      return [0, 100, 0, 0]; // Tutto in "Sano"
    } else if (bmi >= 25 && bmi < 30) {
      return [0, 0, 100, 0]; // Tutto in "Eccessivamente grasso"
    } else {
      return [0, 0, 0, 100]; // Tutto in "Obeso"
    }
  }

  try {
    // ✅ Recupera i dati dal backend
    const response = await fetch(updatePersonaComposizioneUrl);
    const data = await response.json();
    console.log("Dati ricevuti:", data);

    if (!data.success) {
      console.error("Errore nel caricamento dei dati:", data.error);
      return;
    }

    // ✅ Recupera i dati dal backend e dal div nascosto
    const personaDataDiv = document.getElementById("userData");
    if (!personaDataDiv) {
      console.error("Errore: #personaData non trovato");
      return;
    }

    const gender = personaDataDiv.getAttribute("data-gender");
    const acquaAttuale =
      parseFloat(personaDataDiv.getAttribute("data-acqua")) || 0;
    const massaMuscolare =
      parseFloat(personaDataDiv.getAttribute("data-massa-muscolare")) || 0;
    const massaOssea =
      parseFloat(personaDataDiv.getAttribute("data-massa-ossea")) || 0;
    const grasso = parseFloat(personaDataDiv.getAttribute("data-grasso")) || 0;
    const bmi = parseFloat(data.personaComposizione.bmi) || 0;
    let punteggioAttuale =
      parseFloat(data.personaComposizione.punteggio_fisico) || 1;

    // ✅ Forza il punteggio fisico a stare tra 1 e 9
    punteggioAttuale = Math.max(1, Math.min(9, punteggioAttuale));

    console.log("Dati persona:", {
      gender,
      acquaAttuale,
      massaMuscolare,
      massaOssea,
      grasso,
      bmi,
      punteggioAttuale,
    });

    // ✅ Imposta il valore normale dell'acqua in base al genere
    const acquaNormale = gender === "M" ? 60 : 55;

    // ✅ Recupera lo storico dal backend
    let storicoPunteggi = data.personaComposizione.storico_punteggi || [];

    if (storicoPunteggi.length === 0) {
      storicoPunteggi.push({
        punteggio: punteggioAttuale,
        data: new Date().toISOString(),
      });
    }

    // ✅ Convertiamo le date in un formato leggibile
    const labelsStorico = storicoPunteggi.map((entry) =>
      new Date(entry.data).toLocaleDateString()
    );
    const datiStorico = storicoPunteggi.map((entry) => entry.punteggio);

    // ✅ Creazione di tutti i grafici
    const chartsData = [
      {
        elementId: "bmiChart",
        type: "doughnut",
        labels: [
          "Insufficientemente grasso",
          "Sano",
          "Eccessivamente grasso",
          "Obeso",
        ],
        data: getBmiDistribution(bmi),
        backgroundColor: [
          colors.contrastColor,
          colors.positiveColor,
          colors.contrastColor2,
          colors.dark2,
        ],
      },
      {
        elementId: "acquaChart",
        type: "pie",
        labels: ["Valore nella norma", "Valore attuale"],
        data: [acquaNormale, acquaAttuale],
        backgroundColor: [colors.positiveColor, colors.contrastColor2],
      },
      {
        elementId: "massaChart",
        type: "bar",
        labels: ["Massa Muscolare", "Massa Grassa", "Massa Ossea"],
        data: [massaMuscolare, grasso, massaOssea],
        backgroundColor: [
          colors.positiveColor,
          colors.contrastColor,
          colors.contrastColor2,
        ],
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              suggestedMax: 100,
            },
          },
        },
      },
    ];

    // ✅ Creazione dei grafici statici
    chartsData.forEach((chart) => {
      const ctx = document.getElementById(chart.elementId)?.getContext("2d");
      if (!ctx) {
        console.error(`Errore: Canvas #${chart.elementId} non trovato`);
        return;
      }

      new Chart(ctx, {
        type: chart.type,
        data: {
          labels: chart.labels,
          datasets: [
            {
              label: chart.elementId,
              data: chart.data,
              backgroundColor: chart.backgroundColor,
            },
          ],
        },
        options: chart.options || {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                font: { size: 14, weight: "bold" },
                color: colors.dark1,
              },
            },
          },
        },
      });
    });

    // ✅ Creazione del grafico dell’andamento del punteggio fisico
    const ctxPunteggio = document
      .getElementById("GraficoPunteggio")
      ?.getContext("2d");
    let punteggioChart;

    if (ctxPunteggio) {
      punteggioChart = new Chart(ctxPunteggio, {
        type: "line",
        data: {
          labels: labelsStorico,
          datasets: [
            {
              label: "Andamento Punteggio Fisico",
              data: datiStorico,
              borderColor: colors.contrastColor,
              borderWidth: 3,
              pointBackgroundColor: colors.positiveColor,
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              suggestedMin: 1,
              suggestedMax: 9,
              ticks: {
                stepSize: 1,
              },
            },
          },
        },
      });
    }

    // ✅ Rileva cambiamenti del punteggio fisico e aggiorna il grafico
    const punteggioSelect = document.getElementById("punteggio_fisico");
    if (punteggioSelect) {
      punteggioSelect.addEventListener("change", async function () {
        let nuovoPunteggio = parseInt(this.value);
        if (isNaN(nuovoPunteggio) || nuovoPunteggio < 1 || nuovoPunteggio > 9)
          return;

        // ✅ Invia il nuovo punteggio al backend
        const postResponse = await fetch(updatePersonaComposizioneUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ punteggio_fisico: nuovoPunteggio }),
        });

        const postData = await postResponse.json();
        if (!postData.success) {
          console.error("Errore nel salvataggio:", postData.error);
          return;
        }

        // ✅ Recupera di nuovo i dati aggiornati
        const updatedResponse = await fetch(updatePersonaComposizioneUrl);
        const updatedData = await updatedResponse.json();
        let updatedStorico =
          updatedData.personaComposizione.storico_punteggi || [];

        // ✅ Aggiorna i dati del grafico
        punteggioChart.data.labels = updatedStorico.map((entry) =>
          new Date(entry.data).toLocaleDateString()
        );
        punteggioChart.data.datasets[0].data = updatedStorico.map(
          (entry) => entry.punteggio
        );
        punteggioChart.update();

        console.log("Punteggio fisico aggiornato:", updatedStorico);
      });
    }
  } catch (error) {
    console.error("Errore nel caricamento dei dati:", error);
  }
});
