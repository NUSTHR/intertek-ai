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
    <header class="header">
      <h1 class="title">欧盟《人工智能法》合规认证快速自查问卷</h1>
      <p class="subtitle">点击答案逐题判断，最终给出结果。</p>
    </header>

    <div v-if="store.loading" class="muted">加载中…</div>
    <div v-else-if="store.error" class="error">
      <div>加载失败：{{ friendlyError }}</div>
      <button class="btn btn-ghost" type="button" @click="retry">重试</button>
    </div>
    <button v-else class="btn btn-primary" type="button" @click="start">开始</button>
  </section>
</template>

<style scoped></style>
