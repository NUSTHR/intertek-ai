<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { AnswerValue } from '@/types/questionnaire'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const route = useRoute()
const router = useRouter()
const store = useQuestionnaireStore()

const questionId = computed(() => String(route.params.id ?? ''))
const question = computed(() => store.questionsById[questionId.value] ?? null)

onMounted(async () => {
  await store.load()
  if (!store.questionsById[questionId.value]) {
    await router.replace({ name: 'start' })
  }
})

async function choose(value: AnswerValue) {
  const q = question.value
  if (!q) return

  store.setAnswer(q.id, value)
  const next = store.getNext(q.id, value)
  if (!next) return

  if (next.type === 'question') {
    await router.push({ name: 'question', params: { id: next.id } })
    return
  }

  const evaluated = await store.evaluate().catch(() => null)
  const resultId = evaluated?.result_id ?? next.id
  await router.push({ name: 'result', params: { id: resultId } })
}
</script>

<template>
  <section v-if="question" class="card">
    <header class="header">
      <h2 class="title">{{ question.title }}</h2>
      <p v-if="question.description" class="subtitle">{{ question.description }}</p>
    </header>

    <ul v-if="question.bullets?.length" class="bullets">
      <li v-for="b in question.bullets" :key="b">{{ b }}</li>
    </ul>

    <div class="actions">
      <button
        v-for="opt in question.options"
        :key="opt.value"
        class="option"
        type="button"
        @click="choose(opt.value)"
      >
        {{ opt.label }}
      </button>
    </div>

    <button class="ghost" type="button" @click="router.push({ name: 'start' })">重新开始</button>
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
  margin-bottom: 16px;
}

.title {
  margin: 0;
  font-size: 18px;
  line-height: 1.35;
}

.subtitle {
  margin: 0;
  color: rgba(230, 237, 243, 0.72);
  font-size: 14px;
  line-height: 1.5;
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

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.option {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.08);
  color: #e6edf3;
  font-size: 14px;
  padding: 10px 14px;
  border-radius: 12px;
  cursor: pointer;
  min-width: 88px;
}

.option:hover {
  background: rgba(255, 255, 255, 0.12);
}

.ghost {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: transparent;
  color: rgba(230, 237, 243, 0.8);
  font-size: 13px;
  padding: 8px 12px;
  border-radius: 12px;
  cursor: pointer;
}

.ghost:hover {
  color: #e6edf3;
  background: rgba(255, 255, 255, 0.06);
}

.muted {
  color: rgba(230, 237, 243, 0.72);
}
</style>

