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
        class="btn btn-option"
        type="button"
        @click="choose(opt.value)"
      >
        {{ opt.label }}
      </button>
    </div>

    <button class="btn btn-ghost" type="button" @click="router.push({ name: 'start' })">重新开始</button>
  </section>

  <section v-else class="card">
    <div class="muted">加载中…</div>
  </section>
</template>

<style scoped></style>
