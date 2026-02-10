<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerValue, Module, ModuleQuestion } from '@/types/questionnaire'
import IntertekLayout from './IntertekLayout.vue'
import IntertekSingleChoiceCards from './IntertekSingleChoiceCards.vue'
import { buildOptions } from './optionUtils'
import { computeQuestionTag } from './useQuestionCommon'
import { useLocaleStore } from '@/stores/locale'

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

const locale = useLocaleStore()
const ui = computed(() =>
  locale.isZh
    ? {
        legalContext: '法律依据',
        reference: '参考',
        articleTitle: '人工智能法案第 2(6) 与 2(8) 条',
        articleDesc: '法规不适用于仅用于科学研究与开发目的而开发并投入使用的 AI 系统。',
        infoTip: '仅当系统用于科学研究或上市前测试且未投放市场时，研发排除条款才适用。',
        viewFullAct: '查看法规全文。',
        tip: '若用于即将上市的产品评估，建议选择第三项。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitle: 'AI Act Article 2(6) & 2(8)',
        articleDesc:
          'The regulation does not apply to AI systems developed and put into service for the sole purpose of scientific research and development.',
        infoTip:
          'R&D exclusions apply only when the system is solely for scientific research or pre-market testing and not placed on the market.',
        viewFullAct: 'View Full Act.',
        tip: 'If you fill out this questionnaire for products soon to hit the market, we recommend selecting the third option.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '科学研发',
          description: '仅用于科学发现与研发，不用于商业投放。',
          icon: 'science',
        },
        {
          value: 2,
          title: '上市前研发',
          description: '用于上市前研究与测试的 AI 系统。',
          icon: 'biotech',
        },
        {
          value: 0,
          title: '以上都不是',
          description: '系统用于商业用途或在研发环境之外部署。',
          icon: 'public',
        },
      ]
    : [
        {
          value: 1,
          title: 'Scientific R&D',
          description:
            'Select this if your AI is strictly for scientific discovery and development, not intended for commercial placement.',
          icon: 'science',
        },
        {
          value: 2,
          title: 'Pre-market R&D',
          description: 'Select this for AI systems developed for research and testing before being placed on the market or put into service.',
          icon: 'biotech',
        },
        {
          value: 0,
          title: 'None of the above',
          description: 'My system is intended for commercial use or deployment outside of R&D environments.',
          icon: 'public',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const inputName = 'scope_type'
const labelId = 'q11-label'
const questionTag = computed(() => computeQuestionTag(props.question?.id ?? '', locale.isZh))
</script>

<template>
  <IntertekLayout
    module-label="Module 1 / 5"
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
          <h3 class="font-black text-white text-[11px] uppercase tracking-[0.2em]">{{ ui.legalContext }}</h3>
        </div>
        <div class="p-6 flex flex-col gap-6">
          <div v-if="question.ref" class="border-b border-slate-100 dark:border-slate-800 pb-4">
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">{{ ui.reference }}</h4>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              {{ question.ref }}
            </p>
          </div>
          <template v-else>
            <div class="border-b border-slate-100 dark:border-slate-800 pb-4">
              <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">{{ ui.articleTitle }}</h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.articleDesc }}
              </p>
            </div>
          </template>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                {{ ui.infoTip }}
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
            {{ ui.viewFullAct }}
            <span class="material-symbols-outlined text-sm">open_in_new</span>
          </a>
        </div>
      </div>
    </template>
    <template #tip>
      <div class="flex items-start gap-4 p-5 bg-intertek-yellow/5 border border-intertek-yellow/20">
        <span class="material-symbols-outlined text-intertek-yellow text-2xl">lightbulb</span>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium italic">
          {{ ui.tip }}
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
