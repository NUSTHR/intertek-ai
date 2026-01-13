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

    <button class="btn btn-primary" type="button" @click="restart">重新开始</button>
  </section>

  <section v-else class="card">
    <div class="muted">加载中…</div>
  </section>
</template>

<style scoped></style>
