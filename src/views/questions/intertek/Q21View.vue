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
        articleTitleSystem: '法规第3(1)条：AI 系统',
        articleDescSystem:
          '“AI 系统”是指具有不同程度自治、部署后可适应的机器系统，并基于明确或隐含目标，从输入推断输出（如预测、内容、建议或决策），影响物理或虚拟环境。',
        articleTitleGpai: '法规第3(63)条：GPAI',
        articleDescGpai:
          '“通用目的 AI 模型”是指通常在规模化自监督训练下具备显著通用性，能胜任多种任务，可集成到多类下游系统或应用的 AI 模型。',
        viewFullAct: '查看法规全文。',
        tip: '对于集成了自定义AI模型的AI系统，根据法规序言第97条，系统本身及底层模型均负有相应义务。因此，必须针对这两个主体分别使用 EU AI ACT COMPLIANCE MAPPER 进行评估。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitleSystem: 'Article 3(1) - AI System',
        articleDescSystem:
          "'AI system' means a machine-based system that is designed to operate with varying levels of autonomy and that may exhibit adaptiveness after deployment, and that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments.",
        articleTitleGpai: 'Article 3(63) - GPAI',
        articleDescGpai:
          "'General-purpose AI model' means an AI model, including when trained with a large amount of data using self-supervision at scale, that displays significant generality and is capable to competently perform a wide range of distinct tasks regardless of the way the model is placed on the market and that can be integrated into a variety of downstream systems or applications.",
        viewFullAct: 'View Full Act.',
        tip: 'For AI systems integrating a custom AI model, obligations exist for both the system and the underlying model (per Recital 97). Consequently, the EU AI Act Compliance Mapper must be applied separately to each entity.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '通用目的 AI 模型（GPAI）',
          description: '具备显著通用性，可胜任多种不同任务的 AI 模型。',
          icon: 'hub',
        },
        {
          value: 2,
          title: 'AI 系统',
          description: '具有不同自治水平、部署后可适应的机器系统。',
          icon: 'psychology',
        },
        {
          value: 3,
          title: '非 AI 产品',
          description: '基于规则或预定义逻辑的传统软件，不符合本法对 AI 系统的定义。',
          icon: 'settings_input_component',
        },
        {
          value: 4,
          title: '不确定',
          description: '不确定产品属于哪个类别，需要进一步澄清。',
          icon: 'help_outline',
        },
      ]
    : [
        {
          value: 1,
          title: 'General Purpose AI Model (GPAI)',
          description:
            'An AI model that displays significant generality and is capable of competently performing a wide range of distinct tasks.',
          icon: 'hub',
        },
        {
          value: 2,
          title: 'AI System',
          description:
            'A machine-based system designed to operate with varying levels of autonomy and that may exhibit adaptiveness after deployment.',
          icon: 'psychology',
        },
        {
          value: 3,
          title: 'Non-AI Product',
          description:
            'Traditional software based on rules or predefined logic that does not meet the definition of an AI system under the Act.',
          icon: 'settings_input_component',
        },
        {
          value: 4,
          title: 'Uncertain',
          description: 'I am not sure which category my product falls into and need further clarification.',
          icon: 'help_outline',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const inputName = 'product_nature'
const labelId = 'q21-label'
const questionTag = computed(() => computeQuestionTag(props.question?.id ?? '', locale.isZh))
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
                {{ ui.articleTitleSystem }}
              </h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.articleDescSystem }}
              </p>
            </div>
            <div class="pb-2">
              <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">
                {{ ui.articleTitleGpai }}
              </h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.articleDescGpai }}
              </p>
            </div>
          </template>
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
