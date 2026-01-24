<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerValue, Module, ModuleQuestion } from '@/types/questionnaire'
import IntertekLayout from './IntertekLayout.vue'
import { buildOptions } from './optionUtils'

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

const fallbackOptions = [
  {
    value: true,
    title: 'YES',
    description: 'Select this if the statement applies to your system.',
    icon: 'check_circle',
  },
  {
    value: false,
    title: 'NO',
    description: 'Select this if the statement does not apply to your system.',
    icon: 'cancel',
  },
]
const options = computed(() => buildOptions(props.question, fallbackOptions))
const inputName = computed(() => props.question?.id?.replace(/[^a-zA-Z0-9]/g, '_') ?? 'q4')
const labelId = computed(() => `${inputName.value}_label`)
const questionTag = computed(() => {
  const id = props.question?.id ?? ''
  if (!id) return ''
  return `Question ${id.replace(/^q/i, '').toUpperCase()}`
})
const tipTextMap: Record<string, string> = {
  'q4.3_b': 'Confirm whether negative treatment occurs outside the original data-collection context.',
  'q4.3_c': 'Assess whether outcomes are disproportionate to the behaviour analyzed.',
  'q4.4_a': 'Focus on individual criminal risk prediction or assessment use cases.',
  'q4.4_b': 'Check if the assessment relies solely on profiling rather than objective facts.',
  'q4.5_a': 'Identify whether a facial recognition database is created or expanded.',
  'q4.5_b': 'Verify whether data is scraped indiscriminately from internet or CCTV sources.',
  'q4.6_a': 'Limit the scope to workplace and education emotion inference use.',
  'q4.6_b': 'Confirm whether the medical or safety exception applies.',
  'q4.7_a': 'Determine if biometric data is used to categorise individuals.',
  'q4.7_b': 'Confirm inference of sensitive traits via biometric categorisation.',
  'q4.7_c': 'Check whether the law enforcement labelling exemption applies.',
  'q4.8_a': 'Confirm the system performs real-time remote biometric identification in public spaces.',
  'q4.8_b': 'Confirm the purpose is law enforcement rather than private use.',
  'q4.8_c': 'Verify strict necessity for the three listed public-safety objectives.',
}
const legalCopy = computed(() => props.question?.ref ?? '')
const tipCopy = computed(() => tipTextMap[props.question?.id ?? ''] ?? props.question?.description ?? '')
</script>

<template>
  <IntertekLayout
    module-label="Module 4 / 5"
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
    <div role="radiogroup" :aria-labelledby="labelId" class="flex flex-col gap-4">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: modelValue === opt.value }"
      >
        <input
          class="peer sr-only"
          :name="inputName"
          type="radio"
          :value="opt.value"
          :checked="modelValue === opt.value"
          @change="emit('update:modelValue', opt.value as AnswerValue)"
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
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">REFERENCE</h4>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
          {{ legalCopy }}
        </p>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                Confirm scope, purpose, and exemptions before selecting an answer.
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
          {{ tipCopy }}
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
