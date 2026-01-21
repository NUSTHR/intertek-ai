<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const router = useRouter()
const store = useQuestionnaireStore()

const friendlyError = computed(() => {
  const raw = store.error ?? ''
  const lower = raw.toLowerCase()
  if (lower.includes('failed to fetch') || lower.includes('init_failed')) {
    return '后端未启动或不可达（127.0.0.1:8000）'
  }
  if (lower.includes('init_http_') || lower.includes('module_http_') || lower.includes('submit_http_')) {
    return '后端接口返回异常'
  }
  return raw
})

async function start() {
  store.reset()
  const module = await store.init()
  if (!module) return
  await router.push({ name: 'module', params: { id: module.id } })
}

async function retry() {
  await store.init()
}
</script>

<template>
  <section class="card">
    <h2>开始</h2>
    <p class="muted">回答问题并获得结果。</p>

    <p v-if="store.loading" class="muted">加载中…</p>
    <div v-else-if="store.error" class="error">
      <div>加载失败：{{ friendlyError }}</div>
      <div class="actions">
        <button type="button" @click="retry">重试</button>
      </div>
    </div>

    <div class="actions">
      <button type="button" :disabled="!!store.error || store.loading" @click="start">开始</button>
    </div>
  </section>
</template>
