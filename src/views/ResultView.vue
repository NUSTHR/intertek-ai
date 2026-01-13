<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const route = useRoute()
const router = useRouter()
const store = useQuestionnaireStore()

const resultId = computed(() => String(route.params.id ?? ''))
const result = computed(() => store.resultsById[resultId.value] ?? store.lastEvaluation?.result ?? null)

onMounted(async () => {
  await store.load()
  if (!store.resultsById[resultId.value] && store.lastEvaluation?.result_id !== resultId.value) {
    await router.replace({ name: 'start' })
  }
})

async function restart() {
  store.reset()
  await router.push({ name: 'start' })
}
</script>

<template>
  <section v-if="result" class="card">
    <header class="header">
      <h2 class="title">{{ result.title }}</h2>
      <p class="subtitle">{{ result.description }}</p>
    </header>

    <ul v-if="result.bullets?.length" class="bullets">
      <li v-for="b in result.bullets" :key="b">{{ b }}</li>
    </ul>

    <button class="primary" type="button" @click="restart">重新开始</button>
  </section>

  <section v-else class="card">
    <div class="muted">加载中…</div>
  </section>
</template>

<style scoped>
.card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 20px;
}

.header {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 14px;
}

.title {
  margin: 0;
  font-size: 18px;
  line-height: 1.35;
}

.subtitle {
  margin: 0;
  color: rgba(230, 237, 243, 0.82);
  font-size: 14px;
  line-height: 1.6;
}

.bullets {
  margin: 0 0 18px;
  padding: 0 0 0 18px;
  color: rgba(230, 237, 243, 0.9);
  font-size: 14px;
  line-height: 1.6;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.primary {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: #2563eb;
  color: #fff;
  font-size: 14px;
  padding: 10px 14px;
  border-radius: 12px;
  cursor: pointer;
}

.primary:hover {
  background: #1d4ed8;
}

.muted {
  color: rgba(230, 237, 243, 0.72);
}
</style>

