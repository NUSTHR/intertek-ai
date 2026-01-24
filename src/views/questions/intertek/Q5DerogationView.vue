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
    title: 'Narrow Task',
    description: 'The system performs a narrow procedural task (e.g., transforming data into a specific format).',
    icon: 'target',
  },
  {
    value: 2,
    title: 'Human Activity Improvement',
    description: 'The system is intended to improve the result of a previously completed human activity.',
    icon: 'trending_up',
  },
  {
    value: 3,
    title: 'Pattern Detection',
    description: 'The system is used to detect decision-making patterns or deviations from prior patterns.',
    icon: 'hub',
  },
  {
    value: 4,
    title: 'Preparatory Task',
    description: 'The system performs a purely preparatory task for an assessment (without determining the outcome).',
    icon: 'assignment',
  },
  {
    value: 0,
    title: 'None of the above',
    description: 'Select this if none of the specific operational exemptions apply to your system.',
    icon: 'block',
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
    module-label="Module 5 / 5"
    :module-title="props.module.title"
    :module-description="props.module.description"
    question-tag="Question 5.Derogation"
    :question-text="question.text"
    :question-description="question.description"
    :error="error"
    :message="message"
    :disable-next="!canSubmit || loading"
    @restart="emit('restart')"
    @next="emit('next')"
  >
    <div role="group" aria-labelledby="q5-label" class="flex flex-col gap-4">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: isSelected(opt.value) }"
      >
        <input
          class="peer sr-only"
          name="derogation_type"
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
            <div class="size-6 border-2 border-slate-200 dark:border-slate-700 peer-checked:border-intertek-yellow peer-checked:bg-intertek-yellow flex items-center justify-center opacity-0 peer-checked:opacity-100 transition-all">
              <span class="material-symbols-outlined text-black font-black text-lg">check</span>
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
          <div class="border-b border-slate-100 dark:border-slate-800 pb-4">
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">ARTICLE 6(3) CONDITIONS</h4>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              According to Article 6(3), a high-risk AI system mentioned in Annex III shall not be considered high-risk
              if it does not pose a significant risk of harm to the health, safety or fundamental rights, including by
              not materially influencing the outcome of decision making. This applies if it fulfills conditions (a) to
              (d).
            </p>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                These derogations do not apply if the AI system performs profiling of natural persons.
              </p>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-100 dark:border-slate-800">
          <a class="inline-flex items-center gap-2 text-[10px] font-black text-intertek-dark dark:text-intertek-yellow uppercase tracking-widest hover:underline" href="#">
            Reference Archive
            <span class="material-symbols-outlined text-sm">open_in_new</span>
          </a>
        </div>
      </div>
    </template>
    <template #tip>
      <div class="flex items-start gap-4 p-5 bg-intertek-yellow/5 border border-intertek-yellow/20">
        <span class="material-symbols-outlined text-intertek-yellow text-2xl">lightbulb</span>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium italic">
          Unsure about the operational scope? Consult the
          <a class="text-intertek-dark dark:text-intertek-yellow font-black underline" href="#">Article 6(3) Guidance</a>
          for detailed examples.
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
