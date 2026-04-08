<template>
  <aside class="sidebar card">
    <h2>Filtros</h2>
    <p class="small">Selecione os filtros para atualizar o dashboard.</p>

    <div class="filter-block">
      <div class="filter-header">
        <span>Meses</span>
        <button class="mini-btn" @click="toggleAllMonths">
          {{ allMonthsSelected ? 'Limpar' : 'Todos' }}
        </button>
      </div>
      <div class="checklist">
        <label v-for="month in months" :key="month" class="todo-item">
          <input v-model="selectedMonths" type="checkbox" :value="month" />
          <span>{{ month }}</span>
        </label>
      </div>
    </div>

    <div class="filter-block">
      <div class="filter-header">
        <span>Categorias</span>
        <button class="mini-btn" @click="toggleAllCategories">
          {{ allCategoriesSelected ? 'Limpar' : 'Todos' }}
        </button>
      </div>
      <div class="checklist categories">
        <label v-for="category in categories" :key="category" class="todo-item">
          <input v-model="selectedCategories" type="checkbox" :value="category" />
          <span>{{ category }}</span>
        </label>
      </div>
    </div>

    <button class="apply-btn" @click="applyFilters">Aplicar filtros</button>

    <div class="updated-at">Atualizado em: {{ formattedUpdatedAt }}</div>
  </aside>
</template>

<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  months: {
    type: Array,
    default: () => [],
  },
  categories: {
    type: Array,
    default: () => [],
  },
  updatedAt: {
    type: [String, null],
    default: null,
  },
});

const emit = defineEmits(['apply-filters']);

const selectedMonths = ref([...props.months]);
const selectedCategories = ref([...props.categories]);

// Watch para manter sincronizado quando os props mudam
watch(() => props.months, (newMonths) => {
  if (newMonths.length > 0 && selectedMonths.value.length === 0) {
    selectedMonths.value = [...newMonths];
  }
}, { deep: true });

watch(() => props.categories, (newCategories) => {
  if (newCategories.length > 0 && selectedCategories.value.length === 0) {
    selectedCategories.value = [...newCategories];
  }
}, { deep: true });

const allMonthsSelected = computed(
  () => props.months.length > 0 && selectedMonths.value.length === props.months.length,
);

const allCategoriesSelected = computed(
  () => props.categories.length > 0 && selectedCategories.value.length === props.categories.length,
);

const formattedUpdatedAt = computed(() => {
  if (!props.updatedAt) return "-";
  const date = new Date(props.updatedAt);
  return date.toLocaleString("pt-BR");
});

function toggleAllMonths() {
  selectedMonths.value = allMonthsSelected.value ? [] : [...props.months];
}

function toggleAllCategories() {
  selectedCategories.value = allCategoriesSelected.value ? [] : [...props.categories];
}

function applyFilters() {
  emit('apply-filters', {
    months: selectedMonths.value,
    categories: selectedCategories.value,
  });
}
</script>

<style scoped>
.sidebar {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
}

.sidebar h2 {
  margin: 0;
  font-size: 1rem;
  color: #111827;
}

.small {
  margin: 0;
  font-size: 0.82rem;
  color: #4b5563;
}

.filter-block {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  color: #111827;
  font-size: 0.88rem;
  font-weight: 600;
}

.mini-btn {
  border: 1px solid #93c5fd;
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 6px;
  font-size: 0.75rem;
  padding: 4px 8px;
  cursor: pointer;
}

.checklist {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 120px;
  overflow: auto;
}

.checklist.categories {
  max-height: 190px;
}

.todo-item {
  display: flex;
  gap: 6px;
  align-items: center;
  color: #1f2937;
  font-size: 0.8rem;
}

.apply-btn {
  border: 1px solid #1d4ed8;
  background: #2563eb;
  color: #ffffff;
  border-radius: 8px;
  padding: 8px;
  font-weight: 600;
  cursor: pointer;
}

.updated-at {
  margin-top: auto;
  font-size: 0.8rem;
  color: #374151;
  padding-top: 8px;
  border-top: 1px solid #e5e7eb;
}

.card {
  border: 1px solid #d1d5db;
  border-radius: 10px;
  background: #ffffff;
}
</style>
