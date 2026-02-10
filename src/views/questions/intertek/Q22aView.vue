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
  (e: 'prev'): void
  (e: 'next'): void
  (e: 'restart'): void
}>()

const locale = useLocaleStore()
const ui = computed(() =>
  locale.isZh
    ? {
        legalContext: '法律依据',
        reference: '参考',
        articleTitleRoles: '人工智能法案第3(3)-(7)条：运营者角色',
        articleDescRoles:
          '“提供方”是指以自身名义或商标投放市场或投入使用而开发 AI 系统的人；“部署方”是指在其权限下使用 AI 系统从事专业活动的人。',
        articleTitleScope: '人工智能法案第2(1)(e)条：适用范围',
        articleDescScope: '本法规适用于在欧盟境内设立或位于欧盟的 AI 系统提供方与部署方。',
        infoTip: '不同角色的义务差异显著，正确选择对合规映射至关重要。',
        viewFullAct: '查看法规全文。',
        tip: '一个主体可能同时承担多个角色。本次映射请选择主要角色。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitleRoles: 'AI Act Article 3(3-7): Operator Roles',
        articleDescRoles:
          "'Provider' means a person who develops an AI system with a view to placing it on the market under its own name. 'Deployer' means any person using an AI system under its authority.",
        articleTitleScope: 'AI Act Article 2(1)(e): Scope',
        articleDescScope:
          'The regulation applies to providers and deployers of AI systems that have their place of establishment or are located in the Union.',
        infoTip:
          'Responsibilities differ significantly based on these roles. Selecting the correct role is critical for the compliance mapping accuracy.',
        viewFullAct: 'View Full Act.',
        tip: 'Multiple roles can apply to a single entity. Choose the primary role for this specific mapping session.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '提供方',
          description: '开发 AI 系统或委托开发，并以自身名义或商标投放市场或投入使用。',
          icon: 'factory',
        },
        {
          value: 2,
          title: '部署方',
          description: '在其权限下于专业活动中使用 AI 系统。',
          icon: 'computer',
        },
        {
          value: 3,
          title: '进口商',
          description: '位于欧盟，在市场上投放带有欧盟外主体商标的 AI 系统。',
          icon: 'sailing',
        },
        {
          value: 4,
          title: '分销商',
          description: '除提供方或进口商外，在供应链中将 AI 系统投放欧盟市场的人。',
          icon: 'local_shipping',
        },
        {
          value: 5,
          title: '授权代表',
          description: '在欧盟设立并获 AI 系统提供方书面授权履行义务的自然人或法人。',
          icon: 'assignment_ind',
        },
        {
          value: 6,
          title: '产品制造商',
          description: '将 AI 系统与其产品一并以自身名义或商标投放市场或投入使用。',
          icon: 'precision_manufacturing',
        },
        {
          value: 0,
          title: '以上都不是',
          description: '我的实体不属于上述任何监管角色类别。',
          icon: 'block',
        },
      ]
    : [
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
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const inputName = 'role_type'
const labelId = 'q22a-label'
const containerClass = 'max-h-[600px] overflow-y-auto pr-2'
const titleRowClass = 'mb-1'
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
      :container-class="containerClass"
      :title-row-class="titleRowClass"
      @update:modelValue="emit('update:modelValue', $event)"
    />
    <template #sidebar>
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="bg-intertek-dark px-5 py-4 flex items-center gap-3">
          <span class="material-symbols-outlined text-intertek-yellow text-xl">gavel</span>
          <h3 class="font-black text-white text-[11px] uppercase tracking-[0.2em]">{{ ui.legalContext }}</h3>
        </div>
        <div class="p-6 flex flex-col gap-6">
          <div v-if="question.ref" class="pb-4 border-b border-slate-100 dark:border-slate-800">
            <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">{{ ui.reference }}</h4>
            <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              {{ question.ref }}
            </p>
          </div>
          <template v-else>
            <div class="pb-4 border-b border-slate-100 dark:border-slate-800">
              <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">
                {{ ui.articleTitleRoles }}
              </h4>
              <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.articleDescRoles }}
              </p>
            </div>
            <div class="pb-4 border-b border-slate-100 dark:border-slate-800">
              <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">
                {{ ui.articleTitleScope }}
              </h4>
              <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.articleDescScope }}
              </p>
            </div>
          </template>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[10px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">{{ ui.infoTip }}</p>
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
        <span class="material-symbols-outlined text-intertek-yellow text-2xl">help</span>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium italic">
          {{ ui.tip }}
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
