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
  (e: 'prev'): void
  (e: 'next'): void
  (e: 'restart'): void
}>()

const fallbackOptions = [
  {
    value: 1,
    title: 'Provider',
    description:
      'Developing an AI system or having it developed with a view to placing it on the market or putting it into service under your name or trademark.',
    icon: 'factory',
  },
  {
    value: 2,
    title: 'Deployer',
    description: 'Using an AI system under your authority in the course of professional activity.',
    icon: 'computer',
  },
  {
    value: 3,
    title: 'Importer',
    description:
      'Located in the EU and placing on the market an AI system that bears the trademark of a person established outside the EU.',
    icon: 'sailing',
  },
  {
    value: 4,
    title: 'Distributor',
    description:
      'Any person in the supply chain, other than the provider or the importer, that makes an AI system available on the Union market.',
    icon: 'local_shipping',
  },
  {
    value: 5,
    title: 'Authorized Representative',
    description:
      'Any natural or legal person established in the Union who has received a written mandate from a provider of an AI system to fulfill obligations.',
    icon: 'assignment_ind',
  },
  {
    value: 6,
    title: 'Product Manufacturer',
    description:
      'Placing on the market or putting into service an AI system together with their product and under their own name or trademark.',
    icon: 'precision_manufacturing',
  },
  {
    value: 0,
    title: 'None of the above',
    description: 'My entity does not fall into any of these regulatory role categories.',
    icon: 'block',
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
    module-label="Module 2 / 5"
    module-title="Classification & Role Identification"
    step-label="Step 6"
    step-total="of 12"
    progress-width="50%"
    question-tag="Question 2.2a"
    :question-text="question.text"
    :error="error"
    :message="message"
    :disable-next="!canSubmit || loading"
    @restart="emit('restart')"
    @prev="emit('prev')"
    @next="emit('next')"
  >
    <div role="radiogroup" aria-labelledby="q22a-label" class="flex flex-col gap-4 max-h-[600px] overflow-y-auto pr-2">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: modelValue === opt.value }"
      >
        <input
          class="peer sr-only"
          name="role_type"
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
          <div class="flex justify-between items-center mb-1">
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
          <div class="pb-4 border-b border-slate-100 dark:border-slate-800">
            <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">Article 3(3-7): Operator Roles</h4>
            <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              'Provider' means a person who develops an AI system with a view to placing it on the market under its own name. 'Deployer' means any person using an AI system under its authority.
            </p>
          </div>
          <div class="pb-4 border-b border-slate-100 dark:border-slate-800">
            <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">Article 2(1)(e): Scope</h4>
            <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              The regulation applies to providers and deployers of AI systems that have their place of establishment or are located in the Union.
            </p>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[10px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                Responsibilities differ significantly based on these roles. Selecting the correct role is critical for the compliance mapping accuracy.
              </p>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-100 dark:border-slate-800">
          <a class="inline-flex items-center gap-2 text-[10px] font-black text-intertek-dark dark:text-intertek-yellow uppercase tracking-widest hover:underline" href="#">
            View Full Art. 3 Definitions
            <span class="material-symbols-outlined text-sm">open_in_new</span>
          </a>
        </div>
      </div>
    </template>
    <template #tip>
      <div class="flex items-start gap-4 p-5 bg-intertek-yellow/5 border border-intertek-yellow/20">
        <span class="material-symbols-outlined text-intertek-yellow text-2xl">help</span>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium italic">
          Multiple roles can apply to a single entity. Choose the primary role for this specific mapping session.
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
