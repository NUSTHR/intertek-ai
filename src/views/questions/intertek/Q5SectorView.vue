<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerValue, Module, ModuleQuestion } from '@/types/questionnaire'
import IntertekLayout from './IntertekLayout.vue'
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
        annexTitle: 'AI法案附件 I',
        annexDesc:
          '指第 6(1) 条所列的联盟协调立法产品清单。高风险分类取决于 AI 系统是否作为产品安全组件使用，或本身即为法规AI法案附件 I 所列产品。',
        infoTip: '法规AI法案附件 I 所覆盖的系统需要履行特定的高风险合格评定程序。',
        viewFullAct: '查看法规全文。',
        tip: '不确定产品所属行业？请查阅产品技术文件中的 CE 标志指令。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        annexTitle: 'AI Act Annex I',
        annexDesc:
          'Refers to the list of Union harmonisation legislation for products as specified in AI Act Article 6(1). The high-risk classification depends on whether the AI system is intended to be used as a safety component of a product, or is itself a product, covered by the legislation listed in AI Act Annex I.',
        infoTip:
          'Systems covered by AI Act Annex I harmonisation legislation are subject to specific high-risk conformity assessment procedures.',
        viewFullAct: 'View Full Act.',
        tip: "Unsure about your product's sector? Check your product's technical documentation for references to CE marking directives.",
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: 'A',
          title: '交通运输',
          icon: 'directions_bus',
        },
        {
          value: 'B',
          title: '健康医疗',
          icon: 'medical_services',
        },
        {
          value: 'C',
          title: '工业与特殊基础设施',
          icon: 'factory',
        },
        {
          value: 'D',
          title: '人身安全与一般消费品',
          icon: 'shield_with_heart',
        },
        {
          value: 'E',
          title: '以上都不是',
          icon: 'block',
        },
      ]
    : [
        {
          value: 'A',
          title: 'Transport',
          icon: 'directions_bus',
        },
        {
          value: 'B',
          title: 'Health',
          icon: 'medical_services',
        },
        {
          value: 'C',
          title: 'Industrial & Special Infrastructure',
          icon: 'factory',
        },
        {
          value: 'D',
          title: 'Personal Safety & General Consumer',
          icon: 'shield_with_heart',
        },
        {
          value: 'E',
          title: 'None of the above',
          icon: 'block',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const questionTag = computed(() => computeQuestionTag(props.question?.id ?? '', locale.isZh))
</script>

<template>
  <IntertekLayout
    module-label="Module 5 / 5"
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
    <div role="radiogroup" aria-labelledby="q5-label" class="flex flex-col gap-3">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-center p-5 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: modelValue === opt.value }"
      >
        <input
          class="peer sr-only"
          name="sector"
          type="radio"
          :value="opt.value"
          :checked="modelValue === opt.value"
          @change="emit('update:modelValue', opt.value as AnswerValue)"
        />
        <div class="flex-shrink-0 mr-6">
          <div class="size-12 bg-white dark:bg-slate-800 flex items-center justify-center text-slate-400 group-hover:bg-intertek-yellow group-hover:text-black transition-colors shadow-sm">
            <span class="material-symbols-outlined text-2xl">{{ opt.icon }}</span>
          </div>
        </div>
        <div class="flex-1">
          <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ opt.title }}</h3>
        </div>
        <div class="flex items-center gap-3">
          <div class="relative group/info">
            <span
              class="material-symbols-outlined text-base text-slate-400 group-hover/info:text-intertek-yellow transition-colors"
            >
              info
            </span>
            <div
              v-if="opt.cite"
              class="absolute right-0 top-6 z-10 w-72 rounded bg-slate-900 text-white text-[10px] leading-relaxed px-3 py-2 shadow-lg opacity-0 invisible group-hover/info:visible group-hover/info:opacity-100 transition-opacity"
            >
              {{ opt.cite }}
            </div>
          </div>
          <div class="size-6 border-2 border-slate-200 dark:border-slate-700 peer-checked:border-intertek-yellow peer-checked:bg-intertek-yellow flex items-center justify-center opacity-0 peer-checked:opacity-100 transition-all">
            <span class="material-symbols-outlined text-black font-black text-lg">check</span>
          </div>
        </div>
        <div class="absolute inset-0 border-2 border-intertek-yellow opacity-0 peer-checked:opacity-100 pointer-events-none transition-opacity"></div>
      </label>
    </div>
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
              <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">{{ ui.annexTitle }}</h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.annexDesc }}
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
