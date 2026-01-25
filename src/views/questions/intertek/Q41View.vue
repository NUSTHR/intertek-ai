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

const fallbackOptions: Option[] = [
  {
    value: 1,
    title: 'Subliminal or manipulative techniques',
    description:
      "Use of subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques.",
    icon: 'warning',
  },
  {
    value: 2,
    title: 'Exploitation of vulnerabilities',
    description:
      'Exploiting vulnerabilities related to age, disability, or a specific social or economic situation.',
    icon: 'report',
  },
  {
    value: 3,
    title: 'Social scoring',
    description:
      'Evaluation or classification of persons over time based on social behaviour or personal characteristics.',
    icon: 'fact_check',
  },
  {
    value: 4,
    title: 'Individual Risk Assessments',
    description:
      'Making individual risk assessments for criminal offenses based solely on profiling or personality traits (excluding assessments to support human evaluation).',
    icon: 'balance',
  },
  {
    value: 5,
    title: 'Facial scraping',
    description:
      'Creating or expanding facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage.',
    icon: 'face',
  },
  {
    value: 6,
    title: 'Emotion recognition',
    description:
      'Using AI to infer emotions of persons in the workplace or educational institutions, except for medical or safety reasons.',
    icon: 'mood',
  },
  {
    value: 7,
    title: 'Biometric categorization',
    description:
      'Categorizing individuals based on biometric data to infer race, political opinions, trade union membership, religious beliefs, or sexual orientation.',
    icon: 'groups',
  },
  {
    value: 8,
    title: 'Real-time Remote Biometric ID',
    description:
      "Use of 'real-time' remote biometric identification systems in publicly accessible spaces for law enforcement, with specific narrow exceptions.",
    icon: 'sensors',
  },
  {
    value: 0,
    title: 'None of the above',
    description: 'My AI system does not engage in any of the prohibited practices listed above.',
    icon: 'close',
    exclusive: true,
  },
]
const options = computed(() => buildOptions(props.question, fallbackOptions))

const selectedValues = () => (Array.isArray(props.modelValue) ? (props.modelValue as AnswerScalar[]) : [])

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
    module-label="Module 4 / 5"
    :module-title="props.module.title"
    :module-description="props.module.description"
    question-tag="Question 4.1"
    :question-text="question.text"
    :question-description="question.description"
    :error="error"
    :message="message"
    :disable-next="!canSubmit || loading"
    @restart="emit('restart')"
    @next="emit('next')"
  >
    <div class="flex items-center gap-3 mb-6 text-[11px] font-black uppercase tracking-[0.2em] text-slate-500">
      Select all that apply
    </div>
    <div role="group" aria-labelledby="q41-label" class="flex flex-col gap-4 max-h-[620px] overflow-y-auto pr-2">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: isSelected(opt.value) }"
      >
        <input
          class="peer sr-only"
          name="practice_category"
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
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ opt.title }}</h3>
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
          <p class="text-slate-600 dark:text-slate-400 text-xs leading-relaxed max-w-2xl font-medium">
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
        <div class="p-6 flex flex-col gap-6 max-h-[500px] overflow-y-auto custom-scrollbar">
          <div v-if="question.ref" class="border-b border-slate-100 dark:border-slate-800 pb-4">
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">REFERENCE</h4>
            <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              {{ question.ref }}
            </p>
          </div>
          <template v-else>
            <div class="border-b border-slate-100 dark:border-slate-800 pb-4">
              <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">
                Article 5: Prohibited AI Practices
              </h4>
              <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium mb-3">
                1. The following AI practices shall be prohibited:
              </p>
              <ul class="text-[10px] text-slate-600 dark:text-slate-400 leading-relaxed list-disc pl-4 flex flex-col gap-2">
                <li>
                  The placing on the market, the putting into service or the use of an AI system that deploys subliminal
                  techniques beyond a person's consciousness in order to materially distort a person's behavior.
                </li>
                <li>
                  The use of an AI system that exploits any of the vulnerabilities of a specific group of persons due to
                  their age, disability or a specific social or economic situation.
                </li>
                <li>
                  The use of AI systems by public authorities for the evaluation or classification of natural persons
                  based on their social behavior or personality characteristics (social scoring).
                </li>
                <li>
                  The use of 'real-time' remote biometric identification systems in publicly accessible spaces for law
                  enforcement, unless strictly necessary for specific objectives.
                </li>
              </ul>
            </div>
          </template>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                Any AI system falling under these categories is considered to pose an 'Unacceptable Risk' and is banned
                in the EU.
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
          Compliance with Article 5 is mandatory. Systems identified as prohibited cannot be placed on the EU market.
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
