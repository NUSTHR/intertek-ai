<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const router = useRouter()
const store = useQuestionnaireStore()

const conclusion = computed(() => store.conclusion ?? {})
const summaryRows = computed(() => {
  const role = conclusion.value.Role ?? store.parameters.Role ?? ''
  const type = conclusion.value.Type ?? store.parameters.Type ?? ''
  const riskLevel = conclusion.value.Risk_level ?? store.parameters.Risk_level ?? ''
  return [
    { label: 'Role', value: role },
    { label: 'Type', value: type },
    { label: 'Risk_level', value: riskLevel },
  ]
})
const conclusionView = computed(() => {
  const view = (conclusion.value as Record<string, unknown>).View ?? store.parameters.View
  return typeof view === 'string' ? view : ''
})

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
    <h2>合规结论</h2>
    <p class="muted">以下为系统根据你的答案生成的最终结论。</p>

    <div v-if="store.error" class="error" style="margin: 10px 0">{{ store.error }}</div>
    <div v-if="!store.error && summaryRows.length === 0" class="muted">加载中…</div>

    <div v-if="summaryRows.length > 0" style="margin-top: 12px">
      <table style="width: 100%; border-collapse: collapse">
        <thead>
          <tr>
            <th style="text-align: left; border-bottom: 1px solid #e5e7eb; padding: 6px 0">字段</th>
            <th style="text-align: left; border-bottom: 1px solid #e5e7eb; padding: 6px 0">值</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in summaryRows" :key="row.label">
            <td style="padding: 6px 0; vertical-align: top">{{ row.label }}</td>
            <td style="padding: 6px 0; vertical-align: top">{{ String(row.value) }}</td>
          </tr>
        </tbody>
      </table>
      <pre v-if="conclusionView" style="margin-top: 12px; white-space: pre-wrap">{{ conclusionView }}</pre>
    </div>

    <div class="actions">
      <button type="button" @click="restart">重新开始</button>
    </div>
  </section>
</template>
