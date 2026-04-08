<template>
  <section class="kpi-grid">
    <article class="card kpi">
      <h3>Total gasto</h3>
      <strong>R$ {{ money(kpis.total) }}</strong>
    </article>
    <article class="card kpi">
      <h3>Transacoes</h3>
      <strong>{{ kpis.count }}</strong>
    </article>
    <article class="card kpi">
      <h3>Ticket medio</h3>
      <strong>R$ {{ money(kpis.avg) }}</strong>
    </article>
    <article class="card kpi">
      <h3>Maior gasto</h3>
      <strong>R$ {{ money(kpis.max) }}</strong>
    </article>
  </section>
</template>

<script setup>
defineProps({
  kpis: {
    type: Object,
    required: true,
    default: () => ({
      total: 0,
      count: 0,
      avg: 0,
      max: 0,
    }),
  },
});

function money(value) {
  return Number(value || 0).toLocaleString("pt-BR", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}
</script>

<style scoped>
.card {
  border: 1px solid #d1d5db;
  border-radius: 10px;
  background: #ffffff;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  height: 55px;
}

.kpi {
  padding: 6px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.kpi h3 {
  margin: 0;
  font-size: 0.7rem;
  color: #4b5563;
}

.kpi strong {
  margin-top: 2px;
  display: inline-block;
  color: #111827;
  font-size: 0.85rem;
}
</style>
