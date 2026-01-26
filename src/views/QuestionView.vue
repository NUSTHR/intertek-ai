<script setup lang="ts">
import { computed, onMounted, provide, reactive, ref, watch, type Component } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { AnswerScalar, AnswerValue, ModuleQuestion, Module } from '@/types/questionnaire'
import { useQuestionnaireStore } from '@/stores/questionnaire'
import DefaultQuestionView from '@/views/questions/DefaultQuestionView.vue'
import Q11View from '@/views/questions/intertek/Q11View.vue'
import Q12View from '@/views/questions/intertek/Q12View.vue'
import Q21View from '@/views/questions/intertek/Q21View.vue'
import Q21aView from '@/views/questions/intertek/Q21aView.vue'
import Q21bView from '@/views/questions/intertek/Q21bView.vue'
import Q22aView from '@/views/questions/intertek/Q22aView.vue'
import Q22bView from '@/views/questions/intertek/Q22bView.vue'
import Q3a1View from '@/views/questions/intertek/Q3a1View.vue'
import Q3a2View from '@/views/questions/intertek/Q3a2View.vue'
import Q41View from '@/views/questions/intertek/Q41View.vue'
import Q41aView from '@/views/questions/intertek/Q41aView.vue'
import Q41bView from '@/views/questions/intertek/Q41bView.vue'
import Q42aView from '@/views/questions/intertek/Q42aView.vue'
import Q43aView from '@/views/questions/intertek/Q43aView.vue'
import Q4SingleChoiceView from '@/views/questions/intertek/Q4SingleChoiceView.vue'
import Q5RoleView from '@/views/questions/intertek/Q5RoleView.vue'
import Q5SectorView from '@/views/questions/intertek/Q5SectorView.vue'
import Q5SpecMultiView from '@/views/questions/intertek/Q5SpecMultiView.vue'
import Q5AreaSelectView from '@/views/questions/intertek/Q5AreaSelectView.vue'
import Q5ProfilingView from '@/views/questions/intertek/Q5ProfilingView.vue'
import Q5DerogationView from '@/views/questions/intertek/Q5DerogationView.vue'
import Q53rdPartyView from '@/views/questions/intertek/Q53rdPartyView.vue'
import Q6GatewayView from '@/views/questions/intertek/Q6GatewayView.vue'
import Q6A1View from '@/views/questions/intertek/Q6A1View.vue'
import Q6B1View from '@/views/questions/intertek/Q6B1View.vue'
import Q6C1View from '@/views/questions/intertek/Q6C1View.vue'
import Q6D1View from '@/views/questions/intertek/Q6D1View.vue'
import Q6D2View from '@/views/questions/intertek/Q6D2View.vue'
import Q6D3View from '@/views/questions/intertek/Q6D3View.vue'
import Q6D4View from '@/views/questions/intertek/Q6D4View.vue'
import Q6D6View from '@/views/questions/intertek/Q6D6View.vue'
import Q71View from '@/views/questions/intertek/Q71View.vue'
import Q81View from '@/views/questions/intertek/Q81View.vue'

const route = useRoute()
const router = useRouter()
const store = useQuestionnaireStore()
const PREV_HANDLER_KEY = 'questionnaire_prev_handler'
const PROGRESS_OVERRIDE_KEY = 'progressOverride'

const GLOBAL_QUESTION_SEQUENCE = [
  'q1.1',
  'q1.2',
  'q2.1',
  'q2.1a',
  'q2.1b',
  'q2.2a',
  'q2.2b',
  'q3a.1',
  'q3a.2',
  'q4.1',
  'q4.1_a',
  'q4.1_b',
  'q4.1_c',
  'q4.1_d',
  'q4.2_a',
  'q4.2_b',
  'q4.2_c',
  'q4.3_a',
  'q4.3_b',
  'q4.3_c',
  'q4.4_a',
  'q4.4_b',
  'q4.5_a',
  'q4.5_b',
  'q4.6_a',
  'q4.6_b',
  'q4.7_a',
  'q4.7_b',
  'q4.7_c',
  'q4.8_a',
  'q4.8_b',
  'q4.8_c',
  'q5.role',
  'q5.sector',
  'q5.spec_a',
  'q5.spec_b',
  'q5.spec_c',
  'q5.spec_d',
  'q5.3rd_party',
  'q5.area_select',
  'q5.spec_bi',
  'q5.spec_ci',
  'q5.spec_ed',
  'q5.spec_em',
  'q5.spec_es',
  'q5.spec_le',
  'q5.spec_mi',
  'q5.spec_jd',
  'q5.profiling',
  'q5.derogation',
  'q6.gateway',
  'q6.a.1',
  'q6.a.2',
  'q6.a.3',
  'q6.b.1',
  'q6.b.2',
  'q6.c.1',
  'q6.d.1',
  'q6.d.2',
  'q6.d.3',
  'q6.d.4',
  'q6.d.5',
  'q6.d.6',
  'q7.1',
  'q8.1',
]

const moduleId = computed(() => String(route.params.id ?? ''))
const moduleData = computed(() => (store.currentModule?.id === moduleId.value ? store.currentModule : null))
const localAnswers = reactive<Record<string, AnswerValue | undefined>>({})
const questionHistory = ref<{ moduleId: string; question: ModuleQuestion }[]>([])
const historyIndex = ref(0)
const pendingQuestionId = ref<string | null>(null)
const currentQuestion = computed(() => {
  if (questionHistory.value.length > 0) {
    return (
      questionHistory.value[historyIndex.value]?.question ??
      questionHistory.value[questionHistory.value.length - 1]?.question ??
      null
    )
  }
  return moduleData.value?.questions?.[0] ?? null
})
const intertekMap: Record<string, Component> = {
  'q1.1': Q11View,
  'q1.2': Q12View,
  'q2.1': Q21View,
  'q2.1a': Q21aView,
  'q2.1b': Q21bView,
  'q2.2a': Q22aView,
  'q2.2b': Q22bView,
  'q3a.1': Q3a1View,
  'q3a.2': Q3a2View,
  'q4.1': Q41View,
  'q4.1_a': Q41aView,
  'q4.1_b': Q41bView,
  'q4.1_c': Q4SingleChoiceView,
  'q4.1_d': Q4SingleChoiceView,
  'q4.2_a': Q42aView,
  'q4.2_b': Q4SingleChoiceView,
  'q4.2_c': Q4SingleChoiceView,
  'q4.3_a': Q43aView,
  'q4.3_b': Q4SingleChoiceView,
  'q4.3_c': Q4SingleChoiceView,
  'q4.4_a': Q4SingleChoiceView,
  'q4.4_b': Q4SingleChoiceView,
  'q4.5_a': Q4SingleChoiceView,
  'q4.5_b': Q4SingleChoiceView,
  'q4.6_a': Q4SingleChoiceView,
  'q4.6_b': Q4SingleChoiceView,
  'q4.7_a': Q4SingleChoiceView,
  'q4.7_b': Q4SingleChoiceView,
  'q4.7_c': Q4SingleChoiceView,
  'q4.8_a': Q4SingleChoiceView,
  'q4.8_b': Q4SingleChoiceView,
  'q4.8_c': Q4SingleChoiceView,
  'q5.role': Q5RoleView,
  'q5.sector': Q5SectorView,
  'q5.spec_a': Q5SpecMultiView,
  'q5.spec_b': Q5SpecMultiView,
  'q5.spec_c': Q5SpecMultiView,
  'q5.spec_d': Q5SpecMultiView,
  'q5.3rd_party': Q53rdPartyView,
  'q5.area_select': Q5AreaSelectView,
  'q5.spec_bi': Q5SpecMultiView,
  'q5.spec_ci': Q5SpecMultiView,
  'q5.spec_ed': Q5SpecMultiView,
  'q5.spec_em': Q5SpecMultiView,
  'q5.spec_es': Q5SpecMultiView,
  'q5.spec_le': Q5SpecMultiView,
  'q5.spec_mi': Q5SpecMultiView,
  'q5.spec_jd': Q5SpecMultiView,
  'q5.profiling': Q5ProfilingView,
  'q5.derogation': Q5DerogationView,
  'q6.gateway': Q6GatewayView,
  'q6.a.1': Q6A1View,
  'q6.a.2': Q6A1View,
  'q6.a.3': Q6A1View,
  'q6.b.1': Q6B1View,
  'q6.b.2': Q6B1View,
  'q6.c.1': Q6C1View,
  'q6.d.1': Q6D1View,
  'q6.d.2': Q6D2View,
  'q6.d.3': Q6D3View,
  'q6.d.4': Q6D4View,
  'q6.d.5': Q6D2View,
  'q6.d.6': Q6D6View,
  'q7.1': Q71View,
  'q8.1': Q81View,
}
const intertekComponent = computed(() => {
  const id = currentQuestion.value?.id
  if (!id) return null
  return intertekMap[id] ?? null
})

function isAnswerValid(question: ModuleQuestion, value: AnswerValue | undefined) {
  if (question.type === 'multi_choice' || question.type === 'multiple_choice') {
    return Array.isArray(value) && value.length > 0
  }
  if (question.type === 'boolean') {
    return typeof value === 'boolean'
  }
  return value !== undefined && value !== ''
}

const canSubmit = computed(() => {
  const question = currentQuestion.value
  if (!question) return false
  return isAnswerValid(question, localAnswers[question.id])
})

const progressOverride = computed(() => {
  const question = currentQuestion.value
  if (!question) return null
  const index = GLOBAL_QUESTION_SEQUENCE.indexOf(question.id)
  const total = GLOBAL_QUESTION_SEQUENCE.length
  const step = index >= 0 ? index + 1 : Math.min(historyIndex.value + 1, total)
  const width = `${((step / total) * 100).toFixed(2)}%`
  return {
    stepLabel: `Step ${step}`,
    stepTotal: `of ${total}`,
    progressWidth: width,
  }
})

provide(PROGRESS_OVERRIDE_KEY, progressOverride)

function hydrateAnswers(question: ModuleQuestion) {
  const saved = store.answers[question.id]
  if (question.type === 'multi_choice' || question.type === 'multiple_choice') {
    localAnswers[question.id] = Array.isArray(saved) ? [...saved] : localAnswers[question.id] ?? []
    return
  }
  if (question.type === 'boolean') {
    if (typeof localAnswers[question.id] !== 'boolean') {
      localAnswers[question.id] = typeof saved === 'boolean' ? saved : undefined
    }
    return
  }
  if (localAnswers[question.id] === undefined) {
    localAnswers[question.id] = saved ?? ''
  }
}

function pushQuestion(module: Module, question: ModuleQuestion) {
  if (questionHistory.value.length === 0) {
    questionHistory.value = [{ moduleId: module.id, question }]
    historyIndex.value = 0
    return
  }
  const currentEntry = questionHistory.value[historyIndex.value]
  if (currentEntry && currentEntry.moduleId === module.id && currentEntry.question.id === question.id) {
    return
  }
  const last = questionHistory.value[questionHistory.value.length - 1]
  if (!last) {
    questionHistory.value = [{ moduleId: module.id, question }]
    historyIndex.value = 0
    return
  }
  if (last.question.id === question.id && last.moduleId === module.id) {
    historyIndex.value = questionHistory.value.length - 1
    return
  }
  if (historyIndex.value < questionHistory.value.length - 1) {
    questionHistory.value = questionHistory.value.slice(0, historyIndex.value + 1)
  }
  questionHistory.value = [...questionHistory.value, { moduleId: module.id, question }]
  historyIndex.value = questionHistory.value.length - 1
}

function resetHistory() {
  questionHistory.value = []
  historyIndex.value = 0
}

function resetLocalAnswers() {
  for (const key of Object.keys(localAnswers)) {
    delete localAnswers[key]
  }
}

async function ensureModuleLoaded(targetId: string) {
  if (!store.sessionId) {
    await router.replace({ name: 'start' })
    return
  }
  if (targetId === '9') {
    await router.replace({ name: 'result' })
    return
  }
  if (store.currentModule?.id !== targetId) {
    const module = await store.loadModule(targetId)
    if (!module) {
      await router.replace({ name: 'start' })
      return
    }
  }
  if (store.currentModule?.questions?.[0]) {
    const targetId = pendingQuestionId.value
    pendingQuestionId.value = null
    const targetQuestion =
      (targetId ? store.currentModule.questions.find((q) => q.id === targetId) : null) ??
      store.currentModule.questions[0]
    if (targetQuestion) {
      pushQuestion(store.currentModule, targetQuestion)
      hydrateAnswers(targetQuestion)
    }
  }
}

onMounted(async () => {
  const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined
  const isReload =
    nav?.type === 'reload' || (performance as Performance & { navigation?: { type?: number } }).navigation?.type === 1
  if (isReload) {
    await restart()
    return
  }
  await ensureModuleLoaded(moduleId.value)
})

watch(
  () => moduleId.value,
  async (nextId) => {
    await ensureModuleLoaded(nextId)
  },
)

watch(
  () => store.sessionId,
  (next, prev) => {
    if (!next || next !== prev) {
      resetHistory()
      resetLocalAnswers()
    }
  },
)

watch(
  () => moduleData.value?.questions?.[0],
  (question) => {
    if (question && moduleData.value) {
      pushQuestion(moduleData.value, question)
      hydrateAnswers(question)
    }
  },
)

function toggleMulti(q: ModuleQuestion, value: AnswerScalar, checked: boolean) {
  const current = Array.isArray(localAnswers[q.id]) ? [...(localAnswers[q.id] as AnswerScalar[])] : []
  const options = q.options ?? []
  const exclusiveValues = new Set<AnswerScalar>(options.filter((o) => o.exclusive).map((o) => o.value))
  if (checked) {
    if (exclusiveValues.has(value)) {
      localAnswers[q.id] = [value]
      return
    }
    const withoutExclusive = current.filter((v) => !exclusiveValues.has(v))
    localAnswers[q.id] = Array.from(new Set([...withoutExclusive, value]))
    return
  }
  localAnswers[q.id] = current.filter((v) => v !== value)
}

function updateAnswer(id: string, value: AnswerValue) {
  localAnswers[id] = value
}

function handleToggleMulti(payload: { id: string; value: AnswerValue }) {
  const module = moduleData.value
  if (!module) return
  const question = module.questions.find((q) => q.id === payload.id)
  if (!question) return
  const current = Array.isArray(localAnswers[question.id]) ? (localAnswers[question.id] as AnswerScalar[]) : []
  const checked = !current.includes(payload.value as AnswerScalar)
  toggleMulti(question, payload.value as AnswerScalar, checked)
}

async function submitModule() {
  const module = moduleData.value
  if (!module) return
  if (historyIndex.value < questionHistory.value.length - 1) {
    questionHistory.value = questionHistory.value.slice(0, historyIndex.value + 1)
  }
  const scopedHistory = questionHistory.value.slice(0, historyIndex.value + 1)
  const payload: Record<string, AnswerValue> = {}
  for (const entry of scopedHistory) {
    const val = localAnswers[entry.question.id]
    if (val === undefined || val === '' || (Array.isArray(val) && val.length === 0)) continue
    payload[entry.question.id] = val as AnswerValue
  }
  const res = await store.submit(module.id, payload)
  if (!res) return
  if (res.next.type === 'module' && res.next.module_id) {
    if (res.next.module_id === module.id) {
      if (res.module?.questions?.[0]) {
        pushQuestion(res.module, res.module.questions[0])
        hydrateAnswers(res.module.questions[0])
        return
      }
      const refreshed = await store.loadModule(module.id)
      if (refreshed?.questions?.[0]) {
        pushQuestion(refreshed, refreshed.questions[0])
        hydrateAnswers(refreshed.questions[0])
      }
      return
    }
    await router.push({ name: 'module', params: { id: res.next.module_id } })
    return
  }
  await router.push({ name: 'result' })
}

function goPrev() {
  const nextIndex = historyIndex.value - 1
  if (nextIndex >= 0) {
    const entry = questionHistory.value[nextIndex]
    if (!entry) return
    historyIndex.value = nextIndex
    if (moduleId.value !== entry.moduleId) {
      pendingQuestionId.value = entry.question.id
      void router.push({ name: 'module', params: { id: entry.moduleId } })
      return
    }
    hydrateAnswers(entry.question)
    return
  }
}

async function goNext() {
  const module = moduleData.value
  if (!module) return
  await submitModule()
}

provide(PREV_HANDLER_KEY, goPrev)

async function restart() {
  store.reset()
  resetHistory()
  resetLocalAnswers()
  const module = await store.init()
  if (!module) return
  await router.push({ name: 'module', params: { id: module.id } })
}
</script>

<template>
  <component
    v-if="moduleData && currentQuestion && intertekComponent"
    :is="intertekComponent"
    :module="moduleData"
    :question="currentQuestion"
    :model-value="localAnswers[currentQuestion.id]"
    :error="store.error"
    :message="store.lastMessage"
    :loading="store.loading"
    :can-submit="canSubmit"
    @update:modelValue="updateAnswer(currentQuestion.id, $event)"
    @next="goNext"
    @prev="goPrev"
    @restart="restart"
  />

  <DefaultQuestionView
    v-else-if="moduleData && currentQuestion"
    :module="{ id: moduleData.id, title: moduleData.title, description: moduleData.description, questions: [currentQuestion] }"
    :answers="localAnswers"
    :error="store.error"
    :message="store.lastMessage"
    :can-submit="canSubmit"
    :loading="store.loading"
    @update-answer="updateAnswer($event.id, $event.value)"
    @toggle-multi="handleToggleMulti"
    @submit="submitModule"
    @prev="goPrev"
    @restart="restart"
  />

  <section v-else class="card">
    <div v-if="store.error" class="error">Loading Failed {{ store.error }}</div>
    <div v-else class="muted">Loading…</div>
    <div class="actions">
      <button type="button" @click="restart">返回</button>
    </div>
  </section>
</template>
