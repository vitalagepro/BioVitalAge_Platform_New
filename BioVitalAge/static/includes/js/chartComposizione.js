// ✅ Definizione colori
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
      console.error("Errore: #userData non trovato");
      return;
    }

    const gender = personaDataDiv.getAttribute("data-gender");
    const acquaAttuale = parseFloat(data.personaComposizione.acqua) || 0;
    const massaMuscolare = parseFloat(data.personaComposizione.massa_muscolare) || 0;
    const massaOssea = parseFloat(data.personaComposizione.massa_ossea) || 0;
    const grasso = parseFloat(data.personaComposizione.grasso) || 0;
    const grassoViscerale = parseFloat(data.personaComposizione.grasso_viscerale) || 0;
    let bmiAttuale = parseFloat(data.personaComposizione.bmi) || 0;
    let punteggioAttuale = parseFloat(data.personaComposizione.punteggio_fisico) || 1;

    // ✅ Se il BMI supera 50, attiva sempre "Obesità III"
    if (bmiAttuale > 50) {
      bmiAttuale = 50;
    }

    // ✅ Forza il punteggio fisico a stare tra 1 e 9
    punteggioAttuale = Math.max(1, Math.min(9, punteggioAttuale));

    console.log("Dati persona:", { gender, acquaAttuale, massaMuscolare, massaOssea, grasso, grassoViscerale, bmiAttuale, punteggioAttuale });

    const acquaNormale = gender === "M" ? 60 : 55;

    // ✅ Recupera lo storico del punteggio fisico
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

    // ✅ Definizione dei range BMI con colori
    const bmiRanges = [
      { label: "Sottopeso", min: 0, max: 18.5, color: colors.positiveColor },
      { label: "Normopeso", min: 18.6, max: 24.9, color: colors.contrastColor },
      { label: "Sovrappeso", min: 25, max: 29.9, color: colors.contrastColor2 },
      { label: "Obesità I", min: 30, max: 34.9, color: colors.dark2 },
      { label: "Obesità II", min: 35, max: 39.9, color: colors.neutralGray },
      { label: "Obesità III", min: 40, max: 50, color: colors.dark1 }
    ];

    // ✅ Genera i dati per il grafico BMI
    const bmiLabels = bmiRanges.map(range => range.label);
    const bmiData = bmiRanges.map(range => range.max);

    // ✅ Determina il colore delle barre: solo quella corrispondente al BMI attuale sarà colorata
    const bmiBackgroundColors = bmiRanges.map(range =>
      bmiAttuale >= range.min && bmiAttuale <= range.max ? range.color : colors.light1
    );

    // ✅ Creazione dei grafici
    const chartsData = [
      {
        elementId: "composizioneChart",
        type: "doughnut",
        labels: ["Massa Ossea", "Massa Muscolare", "Grasso Corporeo", "Grasso Viscerale"],
        data: [massaOssea, massaMuscolare, grasso, grassoViscerale],
        backgroundColor: [colors.contrastColor, colors.positiveColor, colors.contrastColor2, colors.dark2],
      },
      {
        elementId: "acquaChart",
        type: "pie",
        labels: ["Valore nella norma", "Valore attuale"],
        data: [acquaNormale, acquaAttuale],
        backgroundColor: [colors.positiveColor, colors.contrastColor2],
      },
      {
        elementId: "bmiChart",
        type: "bar",
        labels: bmiLabels,
        data: bmiData,
        backgroundColor: bmiBackgroundColors,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, suggestedMax: 50, ticks: { stepSize: 10 } },
          },
          plugins: {
            legend: { display: false },
          },
        },
      },
    ];

    // ✅ Creazione dei grafici
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
          datasets: [{ label: chart.elementId, data: chart.data, backgroundColor: chart.backgroundColor }],
        },
        options: chart.options || {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "bottom", labels: { font: { size: 14, weight: "bold" }, color: colors.dark1 } },
          },
        },
      });
    });

    // ✅ Creazione del grafico dell’andamento del punteggio fisico
    const ctxPunteggio = document.getElementById("GraficoPunteggio")?.getContext("2d");
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
            y: { suggestedMin: 1, suggestedMax: 9, ticks: { stepSize: 1 } },
          },
        },
      });
    }

  } catch (error) {
    console.error("Errore nel caricamento dei dati:", error);
  }
});
