<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const router = useRouter()
const store = useQuestionnaireStore()

const entries = computed(() => Object.entries(store.parameters))

onMounted(async () => {
  if (!store.sessionId) {
    await router.replace({ name: 'start' })
    return
  }
  await store.fetchResult()
})

async function restart() {
  store.reset()
  await router.push({ name: 'start' })
}
</script>

<template>
  <section class="card">
    <h2>合规参数报告</h2>
    <p class="muted">以下为系统根据你的答案推断出的全部参数。</p>

    <div v-if="store.error" class="error" style="margin: 10px 0">{{ store.error }}</div>
    <div v-if="entries.length === 0" class="muted">加载中…</div>

    <table v-else style="width: 100%; border-collapse: collapse; margin-top: 12px">
      <thead>
        <tr>
          <th style="text-align: left; border-bottom: 1px solid #e5e7eb; padding: 6px 0">参数</th>
          <th style="text-align: left; border-bottom: 1px solid #e5e7eb; padding: 6px 0">值</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="[key, value] in entries" :key="key">
          <td style="padding: 6px 0; vertical-align: top">{{ key }}</td>
          <td style="padding: 6px 0; vertical-align: top">{{ Array.isArray(value) ? JSON.stringify(value) : String(value) }}</td>
        </tr>
      </tbody>
    </table>

    <div class="actions">
      <button type="button" @click="restart">重新开始</button>
    </div>
  </section>
</template>
