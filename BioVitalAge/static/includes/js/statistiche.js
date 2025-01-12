// Grafici
const weeklyCtx = document.getElementById("weeklyPatientsChart");
new Chart(weeklyCtx, {
  type: "line",
  data: {
    labels: ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"],
    datasets: [
      {
        label: "Pazienti Visitati",
        data: [5, 10, 8, 12, 15, 20, 5],
        borderColor: "#fff",
        backgroundColor: "rgba(255,255,255,0.3)",
        fill: true,
        tension: 0.3,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      x: {
        ticks: { color: "#fff" },
        grid: { color: "rgba(255,255,255,0.2)" },
      },
      y: {
        ticks: { color: "#fff" },
        grid: { color: "rgba(255,255,255,0.2)" },
      },
    },
    plugins: {
      legend: { display: false },
    },
  },
});

const patientsCtx = document.getElementById("patientsChart");
new Chart(patientsCtx, {
  type: "bar",
  data: {
    labels: [
      "Gen",
      "Feb",
      "Mar",
      "Apr",
      "Mag",
      "Giu",
      "Lug",
      "Ago",
      "Set",
      "Ott",
      "Nov",
      "Dic",
    ],
    datasets: [
      {
        label: "Pazienti Inseriti",
        data: [30, 45, 60, 50, 41, 66, 30, 50, 70, 90, 100, 120],
        backgroundColor: "#6a2dcc",
        categoryPercentage: 2.8, // Maggior spazio tra le categorie
        barPercentage: 0.1, // Barre più sottili
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: {
        ticks: {
          autoSkip: false, // Mostra tutte le etichette
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  },
});

const monthlyCtx = document.getElementById("monthlyPatientsChart");
const monthlyData = {
  labels: [
    "Gen",
    "Feb",
    "Mar",
    "Apr",
    "Mag",
    "Giu",
    "Lug",
    "Ago",
    "Set",
    "Ott",
    "Nov",
    "Dic",
  ],
  datasets: [
    {
      label: "Pazienti Mensili",
      data: [40, 60, 55, 70, 80, 90, 100, 85, 75, 95, 110, 120],
      backgroundColor: "#c3b0ec",
      borderColor: "#6a2dcc",
      borderWidth: 2,
      fill: true,
    },
  ],
};

let monthlyPatientsChart = new Chart(monthlyCtx, {
  type: "line",
  data: monthlyData,
  options: {
    responsive: true,
    interaction: {
      mode: "index",
      intersect: false,
    },
    plugins: {
      legend: { display: false },
    },
    scales: {
      y: { beginAtZero: true },
    },
    onHover: (event, chartElement) => {
      const tooltip = document.getElementById("monthlyTooltip");
      if (chartElement.length > 0) {
        const index = chartElement[0].index;
        const monthLabel = monthlyData.labels[index];
        const patientCount = monthlyData.datasets[0].data[index];
        const calcCount = Math.floor(patientCount * 0.6);

        tooltip.innerHTML = `
                      <strong>${monthLabel}</strong><br>
                      Pazienti: ${patientCount}<br>
                      Con calcolo età bio: ${calcCount}
                  `;
        const canvasPos = monthlyCtx.getBoundingClientRect();
        tooltip.style.opacity = 1;
        tooltip.style.left = event.clientX - canvasPos.left + "px";
        tooltip.style.top = event.clientY - canvasPos.top + "px";
      } else {
        const tooltip = document.getElementById("monthlyTooltip");
        tooltip.style.opacity = 0;
      }
    },
  },
});