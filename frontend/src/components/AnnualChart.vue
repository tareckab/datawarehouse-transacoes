<template>
  <article class="card chart-card">
    <h3>Gastos Anuais</h3>
    <div class="chart-wrap chart-wrap-top">
      <canvas ref="chartRef" class="chart"></canvas>
    </div>
    <p v-if="!hasData" class="no-data">Sem dados anuais para os filtros atuais.</p>
  </article>
</template>

<script setup>
import { Chart, CategoryScale, LinearScale, BarElement, Tooltip, Legend, BarController } from "chart.js";
import { computed, onMounted, ref, watch, nextTick } from "vue";

Chart.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  BarController,
);

const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
});

const chartRef = ref(null);
let chartInstance = null;

const hasData = computed(() => (props.data || []).length > 0);

function baseOptions(maxXticks = 6) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    layout: {
      padding: { top: 6, right: 6, bottom: 6, left: 6 },
    },
    plugins: {
      legend: {
        display: false,
        labels: {
          color: "#111827",
          boxWidth: 12,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#374151",
          maxRotation: 35,
          minRotation: 20,
          autoSkip: true,
          maxTicksLimit: maxXticks,
        },
        grid: { color: "#eef2f7" },
      },
      y: {
        beginAtZero: true,
        ticks: { color: "#374151" },
        grid: { color: "#eef2f7" },
      },
    },
  };
}

function renderChart() {
  if (!chartRef.value) {
    console.warn("AnnualChart: chartRef not ready");
    return;
  }

  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }

  if (!hasData.value) {
    console.log("AnnualChart: No data to render");
    return;
  }

  const ctx = chartRef.value.getContext("2d");
  if (!ctx) {
    console.error("AnnualChart: Failed to get canvas context");
    return;
  }

  console.log("AnnualChart: Rendering chart with data:", props.data);

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: props.data.map((item) => item.ano),
      datasets: [
        {
          label: "Anual",
          data: props.data.map((item) => item.valor),
          backgroundColor: "#64748b",
          borderRadius: 6,
        },
      ],
    },
    options: baseOptions(6),
  });
}

watch(() => props.data, async () => {
  await nextTick();
  renderChart();
}, { deep: true });

onMounted(async () => {
  await nextTick();
  renderChart();
});
</script>

<style scoped>
.card {
  border: 1px solid #d1d5db;
  border-radius: 10px;
  background: #ffffff;
}

.chart-card {
  padding: 6px;
  display: flex;
  flex-direction: column;
  min-height: 300px;
  height: auto;
  overflow: visible;
}

.chart-card h3 {
  margin: 0 0 2px;
  color: #111827;
  font-size: 0.8rem;
}

.chart {
  width: 100%;
  height: 100%;
  display: block;
  max-width: 100%;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

.chart-wrap {
  position: relative;
  width: 100%;
  min-height: 250px;
  flex: 1;
  overflow: visible;
}

.chart-wrap-top {
  height: auto;
}

.no-data {
  margin: 0;
  color: #6b7280;
  font-size: 0.85rem;
  position: absolute;
  right: 12px;
  top: 8px;
  background: #ffffff;
  padding: 0 4px;
}
</style>
