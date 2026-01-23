<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerValue, ModuleQuestion } from '@/types/questionnaire'
import IntertekLayout from './IntertekLayout.vue'

const props = defineProps<{
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
    value: 1,
    title: 'Computation Threshold',
    description: 'The cumulative amount of computation used for its training is greater than 10^25 FLOPs.',
    icon: 'memory',
  },
  {
    value: 2,
    title: 'Commission Decision',
    description: 'The Commission has adopted a decision designating the model as having systemic risk.',
    icon: 'gavel',
  },
  {
    value: 0,
    title: 'None of the above',
    description: 'The model does not meet the 10^25 FLOPs threshold and has not been designated by the Commission.',
    icon: 'close',
  },
]
const options = computed(() => {
  const backendOptions = props.question.options ?? []
  if (!backendOptions.length) return fallbackOptions
  return backendOptions.map((opt, index) => {
    const base = fallbackOptions[index]
    const label = opt.label ?? base?.title ?? String(opt.value)
    return {
      value: opt.value,
      title: label,
      description: opt.description ?? base?.description ?? '',
      icon: base?.icon ?? 'help',
    }
  })
})
</script>

<template>
  <IntertekLayout
    module-label="Module 7 / 9"
    module-title="GPAI Systemic Risk Check"
    step-label="Step 1"
    step-total="of 1"
    progress-width="100%"
    question-tag="Question Q7.1"
    :question-text="question.text"
    :error="error"
    :message="message"
    :disable-next="!canSubmit || loading"
    @restart="emit('restart')"
    @prev="emit('restart')"
    @next="emit('next')"
  >
    <div role="radiogroup" aria-labelledby="q7-1-label" class="flex flex-col gap-4">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: modelValue === opt.value }"
      >
        <input
          class="peer sr-only"
          name="systemic_risk_criteria"
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
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">ARTICLE 51</h4>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              Article 51 establishes criteria for classifying general-purpose AI (GPAI) models as having systemic risk.
              A model is considered to have systemic risk if it has high-impact capabilities, evaluated through
              technical tools/methodologies, or based on the cumulative computation used for training.
            </p>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                The 10^25 FLOPs threshold is a rebuttable presumption that the model possesses high-impact capabilities.
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
          Models with systemic risk are subject to additional transparency and risk management obligations. Consult
          <a class="text-intertek-dark dark:text-intertek-yellow font-black underline" href="#">Article 51-55 Guidance</a>
          for details.
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
