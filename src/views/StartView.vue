<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const router = useRouter()
const store = useQuestionnaireStore()

onMounted(async () => {
  await store.load()
})

async function start() {
  store.reset()
  await store.load()
  await router.push({ name: 'question', params: { id: store.startId } })
}
</script>

<template>
  <section class="card">
    <header class="header">
      <h1 class="title">欧盟《人工智能法》合规认证快速自查问卷</h1>
      <p class="subtitle">点击答案逐题判断，最终给出结果。</p>
    </header>

    <div v-if="store.loading" class="muted">加载中…</div>
    <div v-else-if="store.error" class="error">加载失败：{{ store.error }}</div>
    <button v-else class="primary" type="button" @click="start">开始</button>
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
  gap: 8px;
  margin-bottom: 18px;
}

.title {
  margin: 0;
  font-size: 22px;
  line-height: 1.25;
}

.subtitle {
  margin: 0;
  color: rgba(230, 237, 243, 0.72);
  font-size: 14px;
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

.error {
  color: #fecaca;
}
</style>

