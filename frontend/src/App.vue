<template>
  <div class="layout">
    <FilterSidebar 
      :months="months" 
      :categories="categories" 
      :updated-at="dashboard.updated_at"
      @apply-filters="handleApplyFilters"
    />

    <main class="content">
      <section v-if="errorMessage" class="card alert">
        {{ errorMessage }}
      </section>

      <KpiCards :kpis="dashboard.kpis" />

      <section class="charts-grid">
        <MonthlyChart :data="dashboard.monthly" />
        <AnnualChart :data="dashboard.yearly" />
        <CategoryChart :data="dashboard.categories" />
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import FilterSidebar from "./components/FilterSidebar.vue";
import KpiCards from "./components/KpiCards.vue";
import MonthlyChart from "./components/MonthlyChart.vue";
import AnnualChart from "./components/AnnualChart.vue";
import CategoryChart from "./components/CategoryChart.vue";
import { fetchDashboardData, fetchFilterOptions } from "./api/dashboardApi";

const months = ref([]);
const categories = ref([]);
const errorMessage = ref("");

const dashboard = ref({
  kpis: { total: 0, count: 0, avg: 0, max: 0 },
  monthly: [],
  yearly: [],
  categories: [],
  updated_at: null,
});

async function loadFilters() {
  const data = await fetchJson(() => fetchFilterOptions());
  if (!data) return;
  months.value = data.months || [];
  categories.value = data.categories || [];
}

async function loadDashboard(selectedMonths, selectedCategories) {
  const data = await fetchJson(() =>
    fetchDashboardData({
      months: selectedMonths,
      categories: selectedCategories,
    }),
  );
  if (!data) return;

  dashboard.value = {
    ...dashboard.value,
    ...data,
    kpis: data.kpis || { total: 0, count: 0, avg: 0, max: 0 },
    monthly: data.monthly || [],
    yearly: data.yearly || [],
    categories: data.categories || [],
  };
}

async function fetchJson(apiCall) {
  try {
    errorMessage.value = "";
    return await apiCall();
  } catch {
    errorMessage.value = "Nao foi possivel conectar na API Python. Inicie o backend em http://127.0.0.1:8000.";
    return null;
  }
}

function handleApplyFilters({ months: selectedMonths, categories: selectedCategories }) {
  loadDashboard(selectedMonths, selectedCategories);
}

onMounted(async () => {
  await loadFilters();
  await loadDashboard(months.value, categories.value);
});
</script>

<style scoped>
.layout {
  min-height: 100vh;
  height: auto;
  display: grid;
  grid-template-columns:0.2fr 1fr;
  gap: 12px;
  padding: 12px;
  background: #ffffff;
  overflow: auto;
}

.card {
  border: 1px solid #d1d5db;
  border-radius: 10px;
  background: #ffffff;
}

.content {
  display: grid;
  grid-template-rows: 0.1fr ;
  gap: 12px;
  height: 100%;
  min-height: 0;
  overflow: visible;
}

.alert {
  padding: 10px;
  color: #991b1b;
  border-color: #fecaca;
  background: #fef2f2;
  font-size: 0.86rem;
}

.charts-grid {
  display: grid;
 
  grid-template-columns: 0.5fr 0.5fr;
  grid-template-rows: 0.5fr 0.5fr;
  height: 100%;

  gap: 10px;
}

@media (max-width: 1200px) {
  .layout {
    grid-template-columns: 240px 1fr;
  }
}
</style>
