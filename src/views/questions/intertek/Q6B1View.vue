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
    value: true,
    title: 'YES',
    description:
      'The system serves as an assistive tool (e.g., spellcheck, minor cropping) and does not fundamentally alter or generate the primary content.',
    icon: 'edit_note',
  },
  {
    value: false,
    title: 'NO',
    description:
      'The system performs generative functions or substantial alterations that go beyond simple assistive editing of existing content.',
    icon: 'auto_awesome',
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
    module-label="Module 6 / 6"
    module-title="Transparency Obligation Check"
    step-label="Step 3"
    step-total="of 15"
    progress-width="20%"
    question-tag="Question q6.b.1"
    :question-text="question.text"
    :error="error"
    :message="message"
    :disable-next="!canSubmit || loading"
    @restart="emit('restart')"
    @prev="emit('restart')"
    @next="emit('next')"
  >
    <div role="radiogroup" aria-labelledby="q6b1-label" class="flex flex-col gap-4">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: modelValue === opt.value }"
      >
        <input
          class="peer sr-only"
          name="function_check"
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
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">ARTICLE 50(2)</h4>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              Providers of an AI system that generates or manipulates image, audio or video content that appreciably
              resembles existing persons, objects, places or other entities or events and would falsely appear to a
              person to be authentic or truthful ('deep fake'), shall disclose that the content has been artificially
              generated or manipulated.
            </p>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                Transparency obligations do not apply where the AI system performs an assistive function for standard
                editing or does not change the input data provided by the user or the semantics thereof.
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
          Unsure if your system is purely assistive? Check the
          <a class="text-intertek-dark dark:text-intertek-yellow font-black underline" href="#">Transparency Guidelines</a>
          for technical definitions of "standard editing".
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
