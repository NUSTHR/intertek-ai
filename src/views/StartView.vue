<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const router = useRouter()
const store = useQuestionnaireStore()

const friendlyError = computed(() => {
  const raw = store.error ?? ''
  const lower = raw.toLowerCase()
  if (lower.includes('failed to fetch') || lower.includes('load_failed')) {
    return '后端未启动或不可达（127.0.0.1:8000）'
  }
  if (lower.includes('tree_http_') || lower.includes('results_http_')) {
    return '后端接口返回异常'
  }
  return raw
})

onMounted(async () => {
  await store.load()
})

async function start() {
  store.reset()
  await store.load()
  await router.push({ name: 'question', params: { id: store.startId } })
}

async function retry() {
  await store.load()
}
</script>

<template>
  <section class="card">
    <div class="card-body page-center">
      <div class="kicker">EU AI Act</div>
      <header class="header">
        <h2 class="title hero-title">EU AI Act Risk Classifier</h2>
        <p class="subtitle">Determine your risk level under the EU AI Act.</p>
      </header>

      <div v-if="store.loading" class="muted">加载中…</div>
      <div v-else-if="store.error" class="error">
        <div>加载失败：{{ friendlyError }}</div>
        <button class="btn" type="button" @click="retry">重试</button>
      </div>
    </div>

    <div class="card-footer">
      <button class="footer-btn" type="button" :disabled="!!store.error || store.loading" @click="start">Start</button>
    </div>
  </section>
</template>

<style scoped>
.card-footer {
  justify-content: center;
}

.kicker {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  margin-bottom: 14px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: rgba(12, 15, 18, 0.72);
  background: rgba(211, 167, 0, 0.14);
  border: 1px solid rgba(211, 167, 0, 0.35);
}

.hero-title {
  font-size: 26px;
  line-height: 1.22;
}
</style>
