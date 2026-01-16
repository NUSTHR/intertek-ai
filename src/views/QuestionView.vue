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
const infoOpen = ref(false)

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
    infoOpen.value = false
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

function toggleInfo() {
  infoOpen.value = !infoOpen.value
}

function getChecked(e: Event): boolean {
  const t = e.target as HTMLInputElement | null
  return t?.checked ?? false
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
  <section v-if="question" class="card">
    <div class="card-body">
      <div class="meta">
        <span />
        <button class="link" type="button" @click="router.push({ name: 'start' })">Restart</button>
      </div>

      <div class="question-row">
        <h2 class="question-title">{{ prompt }}</h2>
        <button v-if="question.description" class="info" type="button" title="Info" @click="toggleInfo">i</button>
      </div>

      <ul v-if="question.bullets?.length" class="bullets bullets-plain">
        <li v-for="b in question.bullets" :key="b">{{ b }}</li>
      </ul>

      <div v-if="infoOpen && question.description" class="info-panel">
        <p class="subtitle">{{ question.description }}</p>
      </div>

      <div v-if="question.kind === 'single'" class="options">
        <div v-for="opt in question.options" :key="opt.value" class="optionContainer">
          <label class="optionRow">
            <span class="p-radiobutton p-component controlElementColor">
              <input v-model="singleValue" class="p-radiobutton-input" type="radio" name="single" :value="opt.value" />
              <span class="p-radiobutton-box">
                <span class="p-radiobutton-icon" />
              </span>
            </span>
            <span class="ml-2 optionText">{{ opt.label }}</span>
          </label>
        </div>
      </div>

      <div v-else class="options">
        <div v-for="opt in question.options" :key="opt.value" class="optionContainer">
          <label class="optionRow">
            <span class="p-checkbox p-component controlElementColor">
              <input
                class="p-checkbox-input"
                type="checkbox"
                :checked="multiValues.includes(opt.value)"
                @change="onMultiToggle(opt.value, getChecked($event))"
              />
              <span class="p-checkbox-box">
                <span class="p-checkbox-icon" />
              </span>
            </span>
            <span class="ml-2 optionText">{{ opt.label }}</span>
          </label>
        </div>
      </div>
    </div>

    <div class="card-footer">
      <button class="footer-btn" type="button" @click="goBack">Back</button>
      <button
        class="footer-btn"
        type="button"
        :disabled="(question.kind === 'single' && !singleValue) || (question.kind === 'multi' && multiValues.length === 0)"
        @click="goNext"
      >
        Next
      </button>
    </div>
  </section>

  <section v-else class="card">
    <div class="card-body">
      <div class="muted">加载中…</div>
    </div>
  </section>
</template>

<style scoped>
.meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.link {
  appearance: none;
  border: 0;
  background: transparent;
  padding: 6px 8px;
  cursor: pointer;
  color: #bf952c;
  font-weight: 750;
  letter-spacing: 0.2px;
}

.question-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin: 8px 0 0;
}

.question-title {
  margin: 0;
  font-size: 24px;
  line-height: 1.25;
  letter-spacing: 0.1px;
}

.info {
  width: 26px;
  height: 26px;
  border-radius: 999px;
  border: 1px solid rgba(211, 167, 0, 0.45);
  background: rgba(211, 167, 0, 0.12);
  color: rgba(12, 15, 18, 0.92);
  cursor: pointer;
  font-weight: 900;
  display: grid;
  place-items: center;
  flex: 0 0 auto;
}

.info-panel {
  margin-top: 12px;
  padding: 14px 16px;
  border: 1px solid rgba(211, 167, 0, 0.28);
  background: rgba(211, 167, 0, 0.09);
}

.bullets-plain {
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
  color: rgba(12, 15, 18, 0.84);
}

.bullets-plain li {
  position: relative;
  padding-left: 18px;
  line-height: 1.55;
}

.bullets-plain li::before {
  content: '•';
  position: absolute;
  left: 0;
  top: 0;
  color: rgba(194, 150, 0, 0.95);
}

.options {
  display: grid;
  gap: 10px;
  margin-top: 18px;
}

.optionContainer {
  display: flex;
}

.optionRow {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 10px 0;
  width: 100%;
  cursor: pointer;
}

.ml-2 {
  margin-left: 8px;
}

.optionText {
  line-height: 1.55;
  font-size: 15px;
  color: rgba(12, 15, 18, 0.9);
}

.controlElementColor {
  color: var(--primary);
}

.p-radiobutton,
.p-checkbox {
  position: relative;
  display: inline-flex;
  width: 20px;
  height: 20px;
  flex: 0 0 20px;
}

.p-radiobutton-input,
.p-checkbox-input {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  opacity: 0;
  cursor: pointer;
}

.p-radiobutton-box,
.p-checkbox-box {
  width: 20px;
  height: 20px;
  box-sizing: border-box;
  display: grid;
  place-items: center;
  border: 2px solid rgba(12, 15, 18, 0.32);
  background: #ffffff;
  transition: border-color 120ms ease, box-shadow 120ms ease, background 120ms ease;
}

.p-radiobutton-box {
  border-radius: 999px;
}

.p-checkbox-box {
  border-radius: 3px;
}

.p-radiobutton-icon {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--primary);
  transform: scale(0);
  transition: transform 120ms ease;
}

.p-checkbox-icon {
  width: 10px;
  height: 6px;
  border-right: 2px solid #ffffff;
  border-bottom: 2px solid #ffffff;
  transform: rotate(45deg) scale(0);
  transition: transform 120ms ease;
  margin-top: -2px;
}

.p-radiobutton-input:checked + .p-radiobutton-box {
  border-color: var(--primary);
}

.p-radiobutton-input:checked + .p-radiobutton-box .p-radiobutton-icon {
  transform: scale(1);
}

.p-checkbox-input:checked + .p-checkbox-box {
  border-color: var(--primary);
  background: var(--primary);
}

.p-checkbox-input:checked + .p-checkbox-box .p-checkbox-icon {
  transform: rotate(45deg) scale(1);
}

.p-radiobutton-input:focus-visible + .p-radiobutton-box,
.p-checkbox-input:focus-visible + .p-checkbox-box {
  outline: none;
  box-shadow: var(--ring);
}

.optionRow:hover .p-radiobutton-box,
.optionRow:hover .p-checkbox-box {
  border-color: rgba(12, 15, 18, 0.5);
}
</style>
