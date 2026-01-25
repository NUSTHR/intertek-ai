<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerScalar, AnswerValue, Module, ModuleQuestion } from '@/types/questionnaire'
import IntertekLayout from './IntertekLayout.vue'
import { buildOptions } from './optionUtils'

type Option = {
  value: AnswerScalar
  title: string
  description: string
  icon: string
  cite?: string
  exclusive?: boolean
}

const props = defineProps<{
  module: Module
  question: ModuleQuestion
  modelValue: AnswerValue | undefined
  error: string | null
  message: string | null
  loading: boolean
  canSubmit: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: AnswerValue): void
  (e: 'next'): void
  (e: 'restart'): void
}>()

const fallbackOptions: Option[] = []
const iconMap: Record<string, Record<string, string>> = {
  'q5.spec_a': {
    '13': 'flight_takeoff',
    '20': 'flight',
    '18': 'directions_car',
    '19': 'car_repair',
    '15': 'agriculture',
    '14': 'two_wheeler',
    '16': 'directions_boat',
    '3': 'sailing',
    '17': 'train',
    '0': 'block',
  },
  'q5.spec_c': {
    '1': 'precision_manufacturing',
    '4': 'elevator',
    '5': 'warning',
    '7': 'compress',
    '10': 'local_fire_department',
    '0': 'block',
  },
  'q5.spec_b': {
    '11': 'medical_services',
    '12': 'biotech',
    '0': 'block',
  },
  'q5.spec_d': {
    '2': 'toys',
    '9': 'health_and_safety',
    '6': 'radio',
    '8': 'cable',
    '0': 'block',
  },
  'q5.spec_bi': {
    '1': 'camera',
    '2': 'fingerprint',
    '3': 'sentiment_satisfied',
    '0': 'block',
  },
  'q5.spec_ci': {
    '1': 'traffic',
    '2': 'router',
    '0': 'block',
  },
  'q5.spec_ed': {
    '1': 'school',
    '2': 'grading',
    '3': 'menu_book',
    '4': 'fact_check',
    '0': 'block',
  },
  'q5.spec_em': {
    '1': 'person_search',
    '2': 'work_off',
    '3': 'monitoring',
    '0': 'block',
  },
  'q5.spec_es': {
    '1': 'account_balance',
    '2': 'credit_score',
    '3': 'health_and_safety',
    '4': 'emergency',
    '0': 'block',
  },
  'q5.spec_le': {
    '1': 'person_alert',
    '2': 'psychology',
    '3': 'memory',
    '4': 'shield',
    '5': 'gavel',
    '0': 'block',
  },
  'q5.spec_mi': {
    '1': 'passport',
    '2': 'security',
    '3': 'assignment',
    '4': 'location_on',
    '0': 'block',
  },
  'q5.spec_jd': {
    '1': 'balance',
    '2': 'how_to_vote',
    '0': 'block',
  },
}
const options = computed(() => {
  const built = buildOptions(props.question, fallbackOptions)
  const map = iconMap[props.question?.id ?? '']
  if (!map) return built
  return built.map((opt) => ({
    ...opt,
    icon: map[String(opt.value)] ?? opt.icon,
  }))
})
const selectedValues = () => (Array.isArray(props.modelValue) ? (props.modelValue as AnswerScalar[]) : [])
const inputName = computed(() => props.question?.id?.replace(/[^a-zA-Z0-9]/g, '_') ?? 'q5_spec')
const labelId = computed(() => `${inputName.value}_label`)
const questionTag = computed(() => {
  const id = props.question?.id ?? ''
  if (!id) return ''
  return `Question ${id.replace(/^q/i, '').toUpperCase()}`
})
const infoText = computed(() => {
  if (props.question?.id === 'q5.spec_b') {
    return 'Medical devices requiring third-party assessment under MDR or IVDR are automatically classified as High-Risk AI Systems.'
  }
  return 'Choose all applicable options. Use “None of the above” only if no listed category applies.'
})
const tipText = computed(() => {
  if (props.question?.id === 'q5.spec_b') {
    return 'Medical devices covered by MDR or IVDR that require third-party assessment are classified as high-risk under Annex I.'
  }
  return 'Select all categories that apply to your system’s intended use.'
})

function toggleValue(value: AnswerScalar) {
  const current = selectedValues()
  const isSelected = current.includes(value)
  const exclusiveValues = options.value.filter((opt) => opt.exclusive).map((opt) => opt.value)
  if (isSelected) {
    emit(
      'update:modelValue',
      current.filter((v) => v !== value) as AnswerValue,
    )
    return
  }
  if (exclusiveValues.includes(value)) {
    emit('update:modelValue', [value])
    return
  }
  const withoutExclusive = current.filter((v) => !exclusiveValues.includes(v))
  emit('update:modelValue', Array.from(new Set([...withoutExclusive, value])) as AnswerValue)
}

function isSelected(value: AnswerScalar) {
  return selectedValues().includes(value)
}
</script>

<template>
  <IntertekLayout
    module-label="Module 5 / 5"
    :module-title="props.module.title"
    :module-description="props.module.description"
    :question-tag="questionTag"
    :question-text="question.text"
    :question-description="question.description"
    :error="error"
    :message="message"
    :disable-next="!canSubmit || loading"
    @restart="emit('restart')"
    @next="emit('next')"
  >
    <div role="group" :aria-labelledby="labelId" class="flex flex-col gap-4">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: isSelected(opt.value) }"
      >
        <input
          class="peer sr-only"
          :name="inputName"
          type="checkbox"
          :value="opt.value"
          :checked="isSelected(opt.value)"
          @change="toggleValue(opt.value)"
        />
        <div class="flex-shrink-0 mr-6">
          <div class="size-14 bg-white dark:bg-slate-800 flex items-center justify-center text-slate-400 group-hover:bg-intertek-yellow group-hover:text-black transition-colors shadow-sm">
            <span class="material-symbols-outlined text-3xl">{{ opt.icon }}</span>
          </div>
        </div>
        <div class="flex-1">
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-lg font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ opt.title }}</h3>
            <div class="flex items-center gap-3">
              <div class="relative group/info">
                <span
                  class="material-symbols-outlined text-base text-slate-400 group-hover/info:text-intertek-yellow transition-colors"
                >
                  info
                </span>
                <div
                  v-if="opt.cite"
                  class="absolute right-0 top-6 z-10 w-72 rounded bg-slate-900 text-white text-[10px] leading-relaxed px-3 py-2 shadow-lg opacity-0 invisible group-hover/info:visible group-hover/info:opacity-100 transition-opacity"
                >
                  {{ opt.cite }}
                </div>
              </div>
              <div class="size-6 border-2 border-slate-200 dark:border-slate-700 peer-checked:border-intertek-yellow peer-checked:bg-intertek-yellow flex items-center justify-center opacity-0 peer-checked:opacity-100 transition-all">
                <span class="material-symbols-outlined text-black font-black text-lg">check</span>
              </div>
            </div>
          </div>
          <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed max-w-xl font-medium">
            {{ opt.description }}
          </p>
        </div>
        <div class="absolute inset-0 border-2 border-intertek-yellow opacity-0 peer-checked:opacity-100 pointer-events-none transition-opacity"></div>
      </label>
    </div>
    <template #sidebar>
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="bg-intertek-dark px-5 py-4 flex items-center gap-3">
          <span class="material-symbols-outlined text-intertek-yellow text-xl">gavel</span>
          <h3 class="font-black text-white text-[11px] uppercase tracking-[0.2em]">Legal Context</h3>
        </div>
        <div class="p-6 flex flex-col gap-6">
          <div v-if="question.ref" class="border-b border-slate-100 dark:border-slate-800 pb-4">
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">REFERENCE</h4>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              {{ question.ref }}
            </p>
          </div>
          <template v-else>
            <div class="border-b border-slate-100 dark:border-slate-800 pb-4">
              <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">ANNEX I / ANNEX III</h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                Select all relevant Annex I or Annex III categories that match the system’s sector or use case.
              </p>
            </div>
          </template>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                {{ infoText }}
              </p>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-100 dark:border-slate-800">
          <a
            class="inline-flex items-center gap-2 text-[10px] font-black text-intertek-dark dark:text-intertek-yellow uppercase tracking-widest hover:underline"
            href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng"
            target="_blank"
            rel="noreferrer"
          >
            View Full Act.
            <span class="material-symbols-outlined text-sm">open_in_new</span>
          </a>
        </div>
      </div>
    </template>
    <template #tip>
      <div class="flex items-start gap-4 p-5 bg-intertek-yellow/5 border border-intertek-yellow/20">
        <span class="material-symbols-outlined text-intertek-yellow text-2xl">lightbulb</span>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium italic">
          {{ tipText }}
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
