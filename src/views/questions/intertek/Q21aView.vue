<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerValue, Module, ModuleQuestion } from '@/types/questionnaire'
import IntertekLayout from './IntertekLayout.vue'
import IntertekSingleChoiceCards from './IntertekSingleChoiceCards.vue'
import { buildOptions } from './optionUtils'
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
        articleTitle: 'GPAI范围',
        articleDesc:
          '通用目的 AI 模型通常作为组件集成到下游系统中。',
        infoTip: '若产品为“模型”，在第五章下可能适用特定文档与透明度义务。',
        viewFullAct: '查看法规全文。',
        tip: '不确定是组件还是系统？请对照附件 I 中 “AI 系统” 与 “GPAI 模型”的定义。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitle: 'GPAI Scope',
        articleDesc:
          'General-purpose AI models (GPAI) are often integrated as components into downstream systems.',
        infoTip:
          "If your product is a 'model', specific obligations regarding documentation and transparency may apply under Chapter V.",
        viewFullAct: 'View Full Act.',
        tip: "Unsure if it's a component or system? Check Annex I definitions of 'AI system' vs 'GPAI model'.",
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '可集成的模型',
          description: 'AI 为组件或通用模型，计划集成到其他系统中。',
          icon: 'extension',
        },
        {
          value: 2,
          title: '完整系统',
          description: 'AI 为独立产品或可直接交付终端用户使用的完整系统。',
          icon: 'precision_manufacturing',
        },
        {
          value: 0,
          title: '以上都不是',
          description: '产品描述不符合上述类别，或为复杂混合形态。',
          icon: 'question_mark',
        },
      ]
    : [
        {
          value: 1,
          title: 'Model for integration',
          description: 'The AI is a component or general-purpose model intended to be integrated into another system.',
          icon: 'extension',
        },
        {
          value: 2,
          title: 'Complete system',
          description: 'The AI is a standalone product or a fully functional system ready for final use by an end-user.',
          icon: 'precision_manufacturing',
        },
        {
          value: 0,
          title: 'None of above',
          description: 'The product description does not fit the above categories or involves a complex hybrid approach.',
          icon: 'question_mark',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const inputName = 'nature_type'
const labelId = 'q21a-label'
const questionTag = computed(() => {
  const id = props.question?.id ?? ''
  if (!id) return ''
  return locale.isZh ? `问题 ${id.replace(/^q/i, '').toUpperCase()}` : `Question ${id.replace(/^q/i, '').toUpperCase()}`
})
</script>

<template>
  <IntertekLayout
    module-label="Module 2 / 5"
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
              <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">
                {{ ui.articleTitle }}
              </h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.articleDesc }}
              </p>
            </div>
          </template>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">{{ ui.infoTip }}</p>
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
