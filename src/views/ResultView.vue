<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const route = useRoute()
const router = useRouter()
const store = useQuestionnaireStore()

const resultId = computed(() => String(route.params.id ?? ''))
const result = computed(() => store.resultsById[resultId.value] ?? store.lastEvaluation?.result ?? null)
const resultTag = computed(() => {
  const id = resultId.value || store.lastEvaluation?.result_id || ''
  return id ? `RESULT ${id}` : 'RESULT'
})

onMounted(async () => {
  await store.load()
  if (!store.resultsById[resultId.value] && store.lastEvaluation?.result_id !== resultId.value) {
    const r = await store.fetchResult(resultId.value)
    if (!r) await router.replace({ name: 'start' })
  }
})

async function restart() {
  store.reset()
  await router.push({ name: 'start' })
}
</script>

<template>
  <section v-if="result" class="card">
    <div class="card-body page-center">
      <div class="kicker">{{ resultTag }}</div>
      <header class="header">
        <h2 class="title">{{ result.title }}</h2>
        <p class="subtitle">{{ result.description }}</p>
      </header>

      <ul v-if="result.bullets?.length" class="bullets">
        <li v-for="b in result.bullets" :key="b">{{ b }}</li>
      </ul>
    </div>

    <div class="card-footer">
      <span />
      <button class="footer-btn" type="button" @click="restart">Restart</button>
    </div>
  </section>

  <section v-else class="card">
    <div class="card-body">
      <div class="muted">加载中…</div>
    </div>
  </section>
</template>

<style scoped>
.kicker {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.4px;
  color: rgba(12, 15, 18, 0.72);
  background: rgba(211, 167, 0, 0.14);
  border: 1px solid rgba(211, 167, 0, 0.35);
  margin-bottom: 16px;
}
</style>
