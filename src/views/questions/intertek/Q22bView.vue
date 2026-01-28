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
        articleTitle: '法规第3(3)与3(5)条',
        articleDesc: 'GPAI 模型提供方指开发或委托开发并将模型投放市场的主体。',
        infoTip: '未在欧盟设立的提供方必须指定授权代表以承担合规监督。',
        viewFullAct: '查看法规全文。',
        tip: '提供方以其名义或商标投放 GPAI 模型；授权代表代表非欧盟提供方。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitle: 'Article 3(3) & 3(5)',
        articleDesc: 'GPAI Model Providers are defined as persons who develop or have developed a model and place it on the market.',
        infoTip: 'Providers not established in the Union must appoint an authorized representative to ensure compliance oversight.',
        viewFullAct: 'View Full Act.',
        tip: 'Providers place a GPAI model on the market under their name or trademark; authorized representatives act on behalf of non-EU providers.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '提供方',
          description: '我的实体开发或委托开发通用目的 AI 模型，并以自身名义或商标投放市场。',
          icon: 'precision_manufacturing',
        },
        {
          value: 5,
          title: '授权代表',
          description: '我的实体在欧盟设立，获非欧盟 GPAI 提供方书面授权代其履行义务。',
          icon: 'assignment_ind',
        },
        {
          value: 0,
          title: '以上都不是',
          description: '我的实体为进口商、分销商或部署方，但不满足本 GPAI 模型的提供方或授权代表角色。',
          icon: 'block',
        },
      ]
    : [
        {
          value: 1,
          title: 'Provider',
          description:
            'My entity develops or has developed a general-purpose AI model and places it on the market under its own name or trademark.',
          icon: 'precision_manufacturing',
        },
        {
          value: 5,
          title: 'Authorized Representative',
          description:
            'My entity is established in the EU and has received a written mandate from a non-EU GPAI provider to act on their behalf.',
          icon: 'assignment_ind',
        },
        {
          value: 0,
          title: 'None of the above',
          description:
            'My entity is an importer, distributor, or deployer, but does not fulfill the specific roles of Provider or Representative for this GPAI model.',
          icon: 'block',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
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
    <div role="radiogroup" aria-labelledby="q22b-label" class="flex flex-col gap-4">
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
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-lg font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ opt.title }}</h3>
            <div class="flex items-center gap-3">
              <div class="relative group/info">
                <span class="material-symbols-outlined text-base text-slate-400 group-hover/info:text-intertek-yellow transition-colors">
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
