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
const legalTextMap: Record<string, string> = {
  'q4.3_b':
    'Art 5(1)(c)(i): detrimental or unfavourable treatment of certain natural persons or groups of persons in social contexts that are unrelated to the contexts in which the data was originally generated or collected;',
  'q4.3_c':
    'Art 5(1)(c)(ii): detrimental or unfavourable treatment of certain natural persons or groups of persons that is unjustified or disproportionate to their social behaviour or its gravity;',
  'q4.4_a':
    'Art 5(1)(d): the placing on the market, the putting into service for this specific purpose, or the use of an AI system for making risk assessments of natural persons in order to assess or predict the risk of a natural person committing a criminal offence...',
  'q4.4_b':
    'Art 5(1)(d): based solely on the profiling of a natural person or on assessing their personality traits and characteristics; this prohibition shall not apply to AI systems used to support the human assessment of the involvement of a person in a criminal activity, which is already based on objective and verifiable facts directly linked to a criminal activity;',
  'q4.5_a':
    'Art 5(1)(e): the placing on the market, the putting into service for this specific purpose, or the use of AI systems that create or expand facial recognition databases...',
  'q4.5_b': 'Art 5(1)(e): through the untargeted scraping of facial images from the internet or CCTV footage;',
  'q4.6_a':
    'Art 5(1)(f): the placing on the market, the putting into service for this specific purpose, or the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions...',
  'q4.6_b':
    'Art 5(1)(f): except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons;',
  'q4.7_a':
    'Art 5(1)(g): the placing on the market, the putting into service for this specific purpose, or the use of biometric categorisation systems that categorise individually natural persons based on their biometric data...',
  'q4.7_b':
    'Art 5(1)(g): to deduce or infer their race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation;',
  'q4.7_c':
    'Art 5(1)(g): this prohibition does not cover any labelling or filtering of lawfully acquired biometric datasets, such as images, based on biometric data or categorizing of biometric data in the area of law enforcement;',
  'q4.8_a':
    'Art 5(1)(h): the use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement...',
  'q4.8_b':
    'Art 5(1)(h): for the purposes of law enforcement, unless and in so far as such use is strictly necessary for one of the following objectives...',
  'q4.8_c':
    'Art 5(1)(h)(i)-(iii): (i) the targeted search for specific victims of abduction, trafficking in human beings or sexual exploitation of human beings, as well as the search for missing persons; (ii) the prevention of a specific, substantial and imminent threat to the life or physical safety of natural persons or a genuine and present or genuine and foreseeable threat of a terrorist attack; (iii) the localisation or identification of a person suspected of having committed a criminal offence referred to in Annex II...',
}
const legalCopy = computed(() => props.question?.ref ?? legalTextMap[props.question?.id ?? ''] ?? '')
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
    <IntertekSingleChoiceCards
      :options="options"
      :model-value="modelValue"
      :input-name="inputName"
      :label-id="labelId"
      @update:modelValue="emit('update:modelValue', $event)"
    />
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
          {{ tipCopy }}
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
