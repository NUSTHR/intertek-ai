<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerValue, Module, ModuleQuestion } from '@/types/questionnaire'
import IntertekLayout from './IntertekLayout.vue'
import IntertekSingleChoiceCards from './IntertekSingleChoiceCards.vue'
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
const options = computed(() => buildOptions(props.question, fallbackOptions))
const inputName = 'role_type'
const labelId = 'q22a-label'
const containerClass = 'max-h-[600px] overflow-y-auto pr-2'
const titleRowClass = 'mb-1'
</script>

<template>
  <IntertekLayout
    module-label="Module 2 / 5"
    :module-title="props.module.title"
    :module-description="props.module.description"
    question-tag="Question 2.2a"
    :question-text="question.text"
    :question-description="question.description"
    :error="error"
    :message="message"
    :disable-next="!canSubmit || loading"
    @restart="emit('restart')"
    @next="emit('next')"
  >
    <IntertekSingleChoiceCards
      :options="options"
      :model-value="modelValue"
      :input-name="inputName"
      :label-id="labelId"
      :container-class="containerClass"
      :title-row-class="titleRowClass"
      @update:modelValue="emit('update:modelValue', $event)"
    />
    <template #sidebar>
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="bg-intertek-dark px-5 py-4 flex items-center gap-3">
          <span class="material-symbols-outlined text-intertek-yellow text-xl">gavel</span>
          <h3 class="font-black text-white text-[11px] uppercase tracking-[0.2em]">Legal Context</h3>
        </div>
        <div class="p-6 flex flex-col gap-6">
          <div v-if="question.ref" class="pb-4 border-b border-slate-100 dark:border-slate-800">
            <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">REFERENCE</h4>
            <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              {{ question.ref }}
            </p>
          </div>
          <template v-else>
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
          </template>
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
        <span class="material-symbols-outlined text-intertek-yellow text-2xl">help</span>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium italic">
          Multiple roles can apply to a single entity. Choose the primary role for this specific mapping session.
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
