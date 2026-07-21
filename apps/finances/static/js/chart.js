let revenueChart = null;

function initializeRevenueChart() {
  const canvas = document.getElementById("monthlyRevenueChart");
  const labelsElement = document.getElementById("revenue-labels");
  const totalsElement = document.getElementById("revenue-totals");

  // Guard
  if (!canvas || !labelsElement || !totalsElement) {
    console.log("No chart canvas found.");
    return;
  }

  const labels = JSON.parse(labelsElement.textContent);
  const totals = JSON.parse(totalsElement.textContent);

  // Destroy existing chart before creating a new one
  if (revenueChart) {
    revenueChart.destroy();
  }

  revenueChart = new Chart(canvas, {
    type: "bar",

    data: {
      labels: labels,

      datasets: [
        {
          label: "Revenue",
          data: totals,
          backgroundColor: "#007AC2",
          borderSkipped: false,
          maxBarThickness: 40,
          categoryPercentage: 0.7,
          barPercentage: 0.9,
        },
      ],
    },

    options: {
      responsive: true,

      maintainAspectRatio: false,

      animation: {
        duration: 700,
      },

      plugins: {
        legend: {
          display: false,
        },

        tooltip: {
          displayColors: false,

          callbacks: {
            label(context) {
              return (
                "₱ " +
                context.parsed.y.toLocaleString("en-PH", {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })
              );
            },
          },
        },
      },

      scales: {
        x: {
          grid: {
            display: false,
          },

          ticks: {
            color: "#666",
          },
        },

        y: {
          beginAtZero: true,

          grid: {
            color: "#ececec",
          },

          ticks: {
            callback(value) {
              return "₱ " + Number(value).toLocaleString("en-PH");
            },
          },
        },
      },
    },
  });
}

// Initial page load
document.addEventListener("DOMContentLoaded", initializeRevenueChart);

// Recreate chart after HTMX swaps content
document.body.addEventListener("htmx:afterSettle", function (event) {
    if (event.target.id === "finance-content") {
        initializeRevenueChart();
    }
});