<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { AnswerValue } from '@/types/questionnaire'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const route = useRoute()
const router = useRouter()
const store = useQuestionnaireStore()

const questionId = computed(() => String(route.params.id ?? ''))
const question = computed(() => store.questionsById[questionId.value] ?? null)
const prompt = computed(() => question.value?.title ?? '')

const multiValues = ref<string[]>([])
const singleValue = ref<string>('')
const whyOpen = ref(false)

function extractStepNumber(id: string): number | null {
  const m = /^q(\d+)\b/i.exec(id.trim())
  if (!m) return null
  const n = Number(m[1])
  return Number.isFinite(n) ? n : null
}

const stepText = computed(() => {
  const q = question.value
  if (!q) return ''
  const current = extractStepNumber(q.id) ?? extractStepNumber(questionId.value)
  if (!current) return ''

  const allIds = Object.keys(store.questionsById)
  const nums = allIds.map(extractStepNumber).filter((n): n is number => typeof n === 'number')
  if (!nums.length) return ''
  const total = Math.max(...nums)
  if (!Number.isFinite(total) || total <= 0) return ''

  return `Step ${current} of ${total}`
})

onMounted(async () => {
  await store.load()
  if (!store.questionsById[questionId.value]) {
    const q = await store.fetchQuestion(questionId.value)
    if (!q) await router.replace({ name: 'start' })
  }
})

watch(
  () => [questionId.value, question.value] as const,
  () => {
    const q = question.value
    whyOpen.value = false
    if (!q) return
    const saved = store.answers[q.id]
    if (q.kind === 'multi') {
      multiValues.value = Array.isArray(saved) ? [...saved] : []
      return
    }
    singleValue.value = typeof saved === 'string' ? saved : ''
  },
  { immediate: true },
)

async function choose(value: AnswerValue) {
  const q = question.value
  if (!q) return

  store.setAnswer(q.id, value)
  const server = await store.answer(q.id, value)
  const next = server?.next ?? store.getNext(q.id, value)
  if (!next) return

  if (next.type === 'question') {
    await router.push({ name: 'question', params: { id: next.id } })
    return
  }

  const resultId =
    (server?.result?.id as string | undefined) ?? store.lastEvaluation?.result_id ?? (next.id as string | undefined) ?? ''
  await router.push({ name: 'result', params: { id: resultId } })
}

function toggleWhy() {
  whyOpen.value = !whyOpen.value
}

function onMultiToggle(value: string, checked: boolean) {
  const q = question.value
  if (!q || q.kind !== 'multi') return
  const opt = q.options.find((o) => o.value === value)
  if (!opt) return

  if (checked) {
    if (opt.exclusive) {
      multiValues.value = [value]
      return
    }
    const exclusiveValues = new Set(q.options.filter((o) => o.exclusive).map((o) => o.value))
    multiValues.value = [...new Set([...multiValues.value.filter((v) => !exclusiveValues.has(v)), value])]
    return
  }

  multiValues.value = multiValues.value.filter((v) => v !== value)
}

function getOptionIcon(label: string, value: string): string {
  const s = `${label} ${value}`.toLowerCase()
  if (/\byes\b|\btrue\b|\bok\b/.test(s)) return 'check_circle'
  if (/\bno\b|\bfalse\b/.test(s)) return 'cancel'
  if (/\buncertain\b|\bunknown\b|\bnot sure\b|\bmaybe\b/.test(s)) return 'help_center'
  return 'check_circle'
}

async function goBack() {
  if (window.history.length > 1) {
    router.back()
    return
  }
  await router.push({ name: 'start' })
}

async function goNext() {
  const q = question.value
  if (!q) return
  if (q.kind === 'single') {
    if (!singleValue.value) return
    await choose(singleValue.value)
    return
  }
  if (multiValues.value.length === 0) return
  await choose([...multiValues.value])
}
</script>

<template>
  <div v-if="question" class="q-page">
    <section class="card q-card">
      <div class="q-body">
        <div class="q-head">
          <div v-if="stepText" class="q-step">{{ stepText }}</div>
          <h2 class="q-title">{{ prompt }}</h2>

          <div v-if="question.description" class="q-callout">
            <span class="material-symbols-outlined q-callout-icon" aria-hidden="true">info</span>
            <p class="q-callout-text">{{ question.description }}</p>
          </div>
        </div>

        <div class="q-actions" :data-kind="question.kind">
          <template v-if="question.kind === 'single'">
            <button
              v-for="opt in question.options"
              :key="opt.value"
              class="bento-card"
              type="button"
              :data-selected="singleValue === opt.value"
              @click="singleValue = opt.value"
            >
              <div class="bento-icon">
                <span class="material-symbols-outlined" aria-hidden="true">{{ getOptionIcon(opt.label, opt.value) }}</span>
              </div>
              <span class="bento-label">{{ opt.label }}</span>
            </button>
          </template>

          <template v-else>
            <button
              v-for="opt in question.options"
              :key="opt.value"
              class="bento-card"
              type="button"
              :data-selected="multiValues.includes(opt.value)"
              @click="onMultiToggle(opt.value, !multiValues.includes(opt.value))"
            >
              <div class="bento-icon">
                <span class="material-symbols-outlined" aria-hidden="true">check_circle</span>
              </div>
              <span class="bento-label">{{ opt.label }}</span>
            </button>
          </template>
        </div>

        <div v-if="whyOpen && question.bullets?.length" class="q-why-panel">
          <ul class="q-why-list">
            <li v-for="b in question.bullets" :key="b">{{ b }}</li>
          </ul>
        </div>
      </div>

      <div class="q-footer">
        <button class="q-back" type="button" @click="goBack">
          <span class="material-symbols-outlined" aria-hidden="true">arrow_back</span>
          Previous
        </button>

        <button v-if="question.bullets?.length" class="q-why" type="button" :data-open="whyOpen" @click="toggleWhy">
          <span class="q-why-text">Why are we asking this?</span>
          <span class="material-symbols-outlined q-why-icon" aria-hidden="true">expand_more</span>
        </button>
        <span v-else />

        <button
          class="q-next"
          type="button"
          :disabled="(question.kind === 'single' && !singleValue) || (question.kind === 'multi' && multiValues.length === 0)"
          @click="goNext"
        >
          Continue
          <span class="material-symbols-outlined" aria-hidden="true">arrow_forward</span>
        </button>
      </div>
    </section>

    <footer class="q-global-footer" aria-label="Context">
      <div class="q-global-footer-inner">
        <span class="q-foot-item"><span class="material-symbols-outlined" aria-hidden="true">lock</span>Secure Session</span>
        <span class="q-foot-item"
          ><span class="material-symbols-outlined" aria-hidden="true">description</span>Annex II Reference</span
        >
        <span class="q-foot-item"
          ><span class="material-symbols-outlined" aria-hidden="true">verified</span>EU AI Act v.1.0</span
        >
      </div>
    </footer>
  </div>

  <section v-else class="card">
    <div class="card-body">
      <div class="muted">加载中…</div>
    </div>
  </section>
</template>

<style scoped>
.q-page {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 18px;
  align-items: center;
}

.q-card {
  width: min(980px, 100%);
  border-radius: 12px;
  border: 1px solid rgba(12, 15, 18, 0.08);
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.08);
}

.q-body {
  padding: 32px 32px 22px;
}

.q-head {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 18px;
}

.q-step {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 12px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 850;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--primary);
  background: rgba(211, 167, 0, 0.08);
  border: 1px solid rgba(211, 167, 0, 0.14);
}

.q-title {
  margin: 0;
  font-size: 28px;
  line-height: 1.2;
  letter-spacing: -0.01em;
  font-weight: 900;
  color: rgba(12, 15, 18, 0.96);
}

.q-callout {
  width: min(600px, 100%);
  position: relative;
  background: rgba(12, 15, 18, 0.03);
  border-radius: 12px;
  padding: 18px 18px 18px 24px;
  border-left: 4px solid rgba(211, 167, 0, 0.4);
}

.q-callout-icon {
  position: absolute;
  left: -14px;
  top: 16px;
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: #ffffff;
  color: var(--primary);
  font-size: 18px;
  border: 1px solid rgba(12, 15, 18, 0.06);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.06);
}

.q-callout-text {
  margin: 0;
  color: rgba(12, 15, 18, 0.62);
  font-size: 13px;
  line-height: 1.7;
  text-align: left;
}

.q-actions {
  margin-top: 34px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}

.bento-card {
  appearance: none;
  border: 2px solid rgba(12, 15, 18, 0.06);
  background: #ffffff;
  border-radius: 12px;
  padding: 18px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  transition: background 140ms ease, border-color 140ms ease, transform 140ms ease, box-shadow 140ms ease;
  text-align: center;
}

.bento-card:focus-visible {
  outline: none;
  box-shadow: var(--ring);
}

.bento-card:hover {
  border-color: rgba(211, 167, 0, 0.5);
  background: rgba(211, 167, 0, 0.02);
  transform: translateY(-1px);
}

.bento-card:active {
  transform: translateY(0px);
}

.bento-icon {
  width: 48px;
  height: 48px;
  border-radius: 999px;
  background: rgba(12, 15, 18, 0.04);
  display: grid;
  place-items: center;
  transition: background 140ms ease;
}

.bento-icon .material-symbols-outlined {
  font-size: 22px;
  color: rgba(12, 15, 18, 0.28);
  transition: color 140ms ease;
}

.bento-label {
  font-size: 16px;
  font-weight: 850;
  letter-spacing: 0.1px;
  color: rgba(12, 15, 18, 0.92);
  line-height: 1.35;
}

.bento-card[data-selected='true'] {
  border-color: rgba(211, 167, 0, 0.65);
  background: rgba(211, 167, 0, 0.04);
  box-shadow: 0 16px 36px rgba(211, 167, 0, 0.12);
}

.bento-card[data-selected='true'] .bento-icon {
  background: rgba(211, 167, 0, 0.12);
}

.bento-card[data-selected='true'] .bento-icon .material-symbols-outlined {
  color: var(--primary);
}

.q-why-panel {
  margin-top: 16px;
  border-top: 1px solid rgba(12, 15, 18, 0.08);
  padding-top: 16px;
}

.q-why-list {
  margin: 0;
  padding: 0 0 0 18px;
  color: rgba(12, 15, 18, 0.78);
  font-size: 13px;
  line-height: 1.7;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.q-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 18px 18px;
  border-top: 1px solid rgba(12, 15, 18, 0.08);
}

.q-back {
  appearance: none;
  border: 0;
  background: transparent;
  padding: 10px 12px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 850;
  color: rgba(12, 15, 18, 0.6);
  transition: color 140ms ease;
}

.q-back:hover {
  color: rgba(12, 15, 18, 0.92);
}

.q-back:focus-visible {
  outline: none;
  box-shadow: var(--ring);
  border-radius: 10px;
}

.q-why {
  appearance: none;
  border: 0;
  background: transparent;
  padding: 10px 10px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 10px;
  color: rgba(12, 15, 18, 0.55);
  font-weight: 850;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  font-size: 10px;
  transition: color 140ms ease;
}

.q-why:hover {
  color: var(--primary);
}

.q-why:focus-visible {
  outline: none;
  box-shadow: var(--ring);
}

.q-why-icon {
  font-size: 18px;
  transition: transform 160ms ease;
}

.q-why[data-open='true'] .q-why-icon {
  transform: rotate(180deg);
}

.q-next {
  appearance: none;
  border: 0;
  cursor: pointer;
  padding: 12px 18px;
  border-radius: 10px;
  background: var(--primary);
  color: #ffffff;
  font-weight: 900;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 14px 26px rgba(211, 167, 0, 0.22);
  transition: background 140ms ease, transform 140ms ease, box-shadow 140ms ease, opacity 140ms ease;
}

.q-next:hover {
  background: var(--primary-hi);
  transform: translateY(-1px);
}

.q-next:active {
  transform: translateY(0px);
}

.q-next:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.q-next:focus-visible {
  outline: none;
  box-shadow: var(--ring);
}

.q-global-footer {
  width: 100%;
  display: flex;
  justify-content: center;
  opacity: 0.4;
  padding: 18px 0 0;
}

.q-global-footer-inner {
  display: flex;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
  justify-content: center;
  font-size: 11px;
  font-weight: 850;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(12, 15, 18, 0.55);
}

.q-foot-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.q-foot-item .material-symbols-outlined {
  font-size: 14px;
}

@media (min-width: 768px) {
  .q-body {
    padding: 44px 48px 28px;
  }

  .q-title {
    font-size: 32px;
  }

  .q-actions {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }

  .q-global-footer-inner {
    gap: 32px;
  }
}

@media (max-width: 520px) {
  .q-footer {
    padding: 12px 12px 14px;
  }

  .q-back {
    padding: 10px 8px;
  }

  .q-next {
    padding: 12px 14px;
  }
}
</style>
