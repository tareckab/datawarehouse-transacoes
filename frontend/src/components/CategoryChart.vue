<template>
  <article class="card chart-card full-width">
    <h3>Gastos por Categoria</h3>
    <div class="chart-wrap chart-wrap-bottom">
      <canvas ref="chartRef" class="chart"></canvas>
    </div>
    <p v-if="!hasData" class="no-data">Sem dados por categoria para os filtros atuais.</p>
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

function shortLabel(value, maxLen) {
  if (!value) return "";
  return value.length > maxLen ? `${value.slice(0, maxLen - 1)}…` : value;
}

function baseOptions(maxXticks = 10) {
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
    console.warn("CategoryChart: chartRef not ready");
    return;
  }

  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }

  if (!hasData.value) {
    console.log("CategoryChart: No data to render");
    return;
  }

  const topCats = [...props.data].slice(0, 10);
  const ctx = chartRef.value.getContext("2d");
  if (!ctx) {
    console.error("CategoryChart: Failed to get canvas context");
    return;
  }

  console.log("CategoryChart: Rendering chart with data:", topCats);

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: topCats.map((item) => shortLabel(item.categoria, 18)),
      datasets: [
        {
          label: "Categorias",
          data: topCats.map((item) => item.valor),
          backgroundColor: "#94a3b8",
          borderRadius: 6,
        },
      ],
    },
    options: baseOptions(10),
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
  min-height: 360px;
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
  min-height: 300px;
  flex: 1;
  overflow: visible;
}

.chart-wrap-bottom {
  height: auto;
}

.full-width {
  grid-column: 1 / 3;
  min-height: 0;
}

.full-width .chart {
  min-height: 0;
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
