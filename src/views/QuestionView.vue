<script setup lang="ts">
import { computed, onMounted, provide, reactive, ref, watch, type Component, type ComputedRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { AnswerScalar, AnswerValue, ModuleQuestion } from '@/types/questionnaire'
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
import Q5RoleView from '@/views/questions/intertek/Q5RoleView.vue'
import Q5SectorView from '@/views/questions/intertek/Q5SectorView.vue'
import Q5SpecBView from '@/views/questions/intertek/Q5SpecBView.vue'
import Q5AreaSelectView from '@/views/questions/intertek/Q5AreaSelectView.vue'
import Q5ProfilingView from '@/views/questions/intertek/Q5ProfilingView.vue'
import Q5DerogationView from '@/views/questions/intertek/Q5DerogationView.vue'
import Q6GatewayView from '@/views/questions/intertek/Q6GatewayView.vue'
import Q6A1View from '@/views/questions/intertek/Q6A1View.vue'
import Q6B1View from '@/views/questions/intertek/Q6B1View.vue'
import Q6C1View from '@/views/questions/intertek/Q6C1View.vue'
import Q6D1View from '@/views/questions/intertek/Q6D1View.vue'
import Q6D3View from '@/views/questions/intertek/Q6D3View.vue'
import Q6D4View from '@/views/questions/intertek/Q6D4View.vue'
import Q6D6View from '@/views/questions/intertek/Q6D6View.vue'
import Q71View from '@/views/questions/intertek/Q71View.vue'
import Q81View from '@/views/questions/intertek/Q81View.vue'

const route = useRoute()
const router = useRouter()
const store = useQuestionnaireStore()
const QUESTION_INDEX_PREFIX = 'questionnaire_question_index'
const PREV_HANDLER_KEY = 'questionnaire_prev_handler'

const moduleId = computed(() => String(route.params.id ?? ''))
const moduleData = computed(() => (store.currentModule?.id === moduleId.value ? store.currentModule : null))
const localAnswers = reactive<Record<string, AnswerValue | undefined>>({})
const currentIndex = ref(0)
const currentQuestion = computed(() => moduleData.value?.questions?.[currentIndex.value] ?? null)
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
  'q4.2_a': Q42aView,
  'q4.3_a': Q43aView,
  'q5.role': Q5RoleView,
  'q5.sector': Q5SectorView,
  'q5.spec_b': Q5SpecBView,
  'q5.area_select': Q5AreaSelectView,
  'q5.profiling': Q5ProfilingView,
  'q5.derogation': Q5DerogationView,
  'q6.gateway': Q6GatewayView,
  'q6.a.1': Q6A1View,
  'q6.b.1': Q6B1View,
  'q6.c.1': Q6C1View,
  'q6.d.1': Q6D1View,
  'q6.d.3': Q6D3View,
  'q6.d.4': Q6D4View,
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
  if (question.type === 'multi_choice') {
    return Array.isArray(value) && value.length > 0
  }
  if (question.type === 'boolean') {
    return typeof value === 'boolean'
  }
  return value !== undefined && value !== ''
}

const canSubmit = computed(() => {
  const module = moduleData.value
  const question = currentQuestion.value
  if (!module || !question) return false
  if (currentIndex.value < module.questions.length - 1) {
    return isAnswerValid(question, localAnswers[question.id])
  }
  return module.questions.every((q) => isAnswerValid(q, localAnswers[q.id]))
})

const progressOverride = computed(() => {
  const module = moduleData.value
  const question = currentQuestion.value
  if (!module || !question) return null
  const total = module.questions.length || 1
  const step = Math.min(currentIndex.value + 1, total)
  const width = `${Math.round((step / total) * 100)}%`
  return {
    moduleLabel: `Module ${module.id}`,
    stepLabel: `Step ${step}`,
    stepTotal: `of ${total}`,
    progressWidth: width,
    questionTag: `Question ${question.id}`,
  }
})

provide('progressOverride', progressOverride as ComputedRef<Record<string, string> | null>)

function hydrateAnswers(module: { questions: ModuleQuestion[] }) {
  for (const key of Object.keys(localAnswers)) {
    delete localAnswers[key]
  }
  for (const q of module.questions) {
    const saved = store.answers[q.id]
    if (q.type === 'multi_choice') {
      localAnswers[q.id] = Array.isArray(saved) ? [...saved] : []
      continue
    }
    if (q.type === 'boolean') {
      localAnswers[q.id] = typeof saved === 'boolean' ? saved : undefined
      continue
    }
    localAnswers[q.id] = saved ?? ''
  }
}

function restoreQuestionIndex(module: { id: string; questions: ModuleQuestion[] }) {
  if (!store.sessionId) {
    currentIndex.value = 0
    return
  }
  const key = `${QUESTION_INDEX_PREFIX}_${store.sessionId}_${module.id}`
  const stored = Number(sessionStorage.getItem(key))
  if (Number.isFinite(stored) && stored >= 0 && stored < module.questions.length) {
    currentIndex.value = stored
    return
  }
  currentIndex.value = 0
}

function persistQuestionIndex() {
  const module = moduleData.value
  if (!store.sessionId || !module) return
  const key = `${QUESTION_INDEX_PREFIX}_${store.sessionId}_${module.id}`
  sessionStorage.setItem(key, String(currentIndex.value))
}

function consumePrevFlag() {
  const key = 'questionnaire_prev'
  const value = sessionStorage.getItem(key)
  if (value) {
    sessionStorage.removeItem(key)
    return true
  }
  return false
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
  if (store.currentModule) hydrateAnswers(store.currentModule)
  if (store.currentModule) restoreQuestionIndex(store.currentModule)
}

onMounted(async () => {
  await ensureModuleLoaded(moduleId.value)
})

watch(
  () => moduleId.value,
  async (nextId) => {
    await ensureModuleLoaded(nextId)
  },
)

watch(
  () => moduleData.value,
  (module) => {
    if (module) {
      hydrateAnswers(module)
      restoreQuestionIndex(module)
    }
  },
)

watch(
  () => currentIndex.value,
  () => {
    persistQuestionIndex()
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
  const payload: Record<string, AnswerValue> = {}
  for (const q of module.questions) {
    const val = localAnswers[q.id]
    if (val === undefined || val === '' || (Array.isArray(val) && val.length === 0)) continue
    payload[q.id] = val as AnswerValue
  }
  const res = await store.submit(module.id, payload)
  if (!res) return
  if (res.next.type === 'module' && res.next.module_id) {
    await router.push({ name: 'module', params: { id: res.next.module_id } })
    return
  }
  await router.push({ name: 'result' })
}

function goPrev() {
  consumePrevFlag()
  if (currentIndex.value > 0) {
    currentIndex.value -= 1
  }
}

async function goNext() {
  const module = moduleData.value
  if (!module) return
  if (currentIndex.value < module.questions.length - 1) {
    currentIndex.value += 1
    return
  }
  await submitModule()
}

provide(PREV_HANDLER_KEY, goPrev)

async function restart() {
  if (consumePrevFlag()) {
    goPrev()
    return
  }
  store.reset()
  const module = await store.init()
  if (!module) return
  await router.push({ name: 'module', params: { id: module.id } })
}
</script>

<template>
  <component
    v-if="moduleData && currentQuestion && intertekComponent"
    :is="intertekComponent"
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
    v-else-if="moduleData"
    :module="moduleData"
    :answers="localAnswers"
    :error="store.error"
    :message="store.lastMessage"
    :can-submit="canSubmit"
    :loading="store.loading"
    @update-answer="updateAnswer($event.id, $event.value)"
    @toggle-multi="handleToggleMulti"
    @submit="submitModule"
    @restart="restart"
  />

  <section v-else class="card">
    <div v-if="store.error" class="error">加载失败：{{ store.error }}</div>
    <div v-else class="muted">加载中…</div>
    <div class="actions">
      <button type="button" @click="restart">返回</button>
    </div>
  </section>
</template>
