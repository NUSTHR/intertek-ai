<script setup lang="ts">
import { computed, onMounted, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { AnswerScalar, AnswerValue, ModuleQuestion } from '@/types/questionnaire'
import { useQuestionnaireStore } from '@/stores/questionnaire'

const route = useRoute()
const router = useRouter()
const store = useQuestionnaireStore()

const moduleId = computed(() => String(route.params.id ?? ''))
const moduleData = computed(() => (store.currentModule?.id === moduleId.value ? store.currentModule : null))
const localAnswers = reactive<Record<string, AnswerValue | undefined>>({})

const canSubmit = computed(() => {
  const module = moduleData.value
  if (!module) return false
  for (const q of module.questions) {
    const val = localAnswers[q.id]
    if (q.type === 'multi_choice') {
      if (!Array.isArray(val) || val.length === 0) return false
      continue
    }
    if (q.type === 'boolean') {
      if (typeof val !== 'boolean') return false
      continue
    }
    if (val === undefined || val === '') return false
  }
  return true
})

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

async function ensureModuleLoaded(targetId: string) {
  if (!store.sessionId) {
    await router.replace({ name: 'start' })
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
    if (module) hydrateAnswers(module)
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

async function submitModule() {
  const module = moduleData.value
  if (!module) return
  const payload: Record<string, AnswerValue> = {}
  for (const q of module.questions) {
    const val = localAnswers[q.id]
    if (val === undefined) continue
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

async function restart() {
  store.reset()
  await router.push({ name: 'start' })
}
</script>

<template>
  <section v-if="moduleData" class="card">
    <h2>{{ moduleData.title }}</h2>
    <p v-if="moduleData.description" class="muted">{{ moduleData.description }}</p>

    <div v-if="store.error" class="error" style="margin: 10px 0">{{ store.error }}</div>
    <div v-if="store.lastMessage" class="muted" style="margin: 10px 0">{{ store.lastMessage }}</div>

    <div v-for="q in moduleData.questions" :key="q.id" class="card" style="margin-top: 12px">
      <div class="muted">{{ q.id }}</div>
      <h3 style="margin: 6px 0">{{ q.text }}</h3>
      <p v-if="q.description" class="muted">{{ q.description }}</p>
      <p v-if="q.ref" class="muted">{{ q.ref }}</p>

      <div v-if="q.type === 'boolean'">
        <label class="field">
          <input v-model="localAnswers[q.id]" type="radio" :value="true" />
          是
        </label>
        <label class="field">
          <input v-model="localAnswers[q.id]" type="radio" :value="false" />
          否
        </label>
      </div>

      <div v-else-if="q.type === 'single_choice'">
        <label v-for="opt in q.options ?? []" :key="String(opt.value)" class="field">
          <input v-model="localAnswers[q.id]" type="radio" :value="opt.value" />
          {{ opt.label }}
        </label>
      </div>

      <div v-else>
        <label v-for="opt in q.options ?? []" :key="String(opt.value)" class="field">
          <input
            type="checkbox"
            :checked="Array.isArray(localAnswers[q.id]) && (localAnswers[q.id] as AnswerValue[]).includes(opt.value)"
            @change="toggleMulti(q, opt.value, ($event.target as HTMLInputElement).checked)"
          />
          {{ opt.label }}
        </label>
      </div>
    </div>

    <div class="actions">
      <button type="button" @click="restart">重新开始</button>
      <button type="button" :disabled="!canSubmit" @click="submitModule">提交并继续</button>
    </div>
  </section>

  <section v-else class="card">
    <div v-if="store.error" class="error">加载失败：{{ store.error }}</div>
    <div v-else class="muted">加载中…</div>
    <div v-if="store.error" class="actions">
      <button type="button" @click="restart">重新开始</button>
    </div>
  </section>
</template>
