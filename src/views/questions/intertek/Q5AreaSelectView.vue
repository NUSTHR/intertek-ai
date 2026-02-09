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
        annexTitle: '法案附件 III 第 1-8 点',
        annexDesc:
          '列出因对基本权利、健康或安全产生潜在影响而被视为高风险的具体领域。落入这些类别的系统需要严格遵守第 9-15 条。',
        infoTip: '判断系统是否属于法案附件 III 是路径 2 高风险评估的关键步骤。',
        viewFullAct: '查看法规全文。',
        tip: '若系统用于此处列出的任一法案附件 III 行业，可能被认定为高风险并需满足第 9–15 条要求。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        annexTitle: 'ANNEX III POINTS 1-8',
        annexDesc:
          'Lists the specific areas where AI systems are considered high-risk due to their potential impact on fundamental rights, health, or safety. Systems falling under these categories require strict compliance with AI Act Article 9-15.',
        infoTip:
          'Determining if a system falls under AI Act Annex III is a critical step in the Pathway 2 assessment for high-risk classification.',
        viewFullAct: 'View Full Act.',
        tip: 'If your system is used in any AI Act Annex III sector listed here, it may be classified as high-risk and must meet AI Act Articles 9–15 requirements.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '生物特征',
          description: '远程生物识别与分类。',
          icon: 'fingerprint',
        },
        {
          value: 2,
          title: '关键基础设施',
          description: '道路交通、水、燃气、供热与电力的管理与运行。',
          icon: 'factory',
        },
        {
          value: 3,
          title: '教育',
          description: '教育准入、职业培训与学生评估。',
          icon: 'school',
        },
        {
          value: 4,
          title: '就业',
          description: '招聘、选拔、晋升、解雇与员工监控。',
          icon: 'work',
        },
        {
          value: 5,
          title: '基本服务',
          description: '获取关键私人服务、公共服务与福利。',
          icon: 'account_balance_wallet',
        },
        {
          value: 6,
          title: '执法',
          description: '执法机构使用的犯罪风险评估、画像与测谎。',
          icon: 'shield_person',
        },
        {
          value: 7,
          title: '移民',
          description: '移民、庇护与边境管控管理与安全。',
          icon: 'public',
        },
        {
          value: 8,
          title: '司法',
          description: '司法管理与民主过程，包括选举。',
          icon: 'gavel',
        },
        {
          value: 0,
          title: '以上都不是',
          description: '我的 AI 系统不涉及这些敏感的法案附件 III 领域。',
          icon: 'block',
          span: 'md:col-span-2',
        },
      ]
    : [
        {
          value: 1,
          title: 'Biometrics',
          description: 'Remote biometric identification and categorization.',
          icon: 'fingerprint',
        },
        {
          value: 2,
          title: 'Critical Infrastructure',
          description: 'Management and operation of road traffic, water, gas, heating and electricity.',
          icon: 'factory',
        },
        {
          value: 3,
          title: 'Education',
          description: 'Access to education, vocational training and assessment of students.',
          icon: 'school',
        },
        {
          value: 4,
          title: 'Employment',
          description: 'Recruitment, selection, promotion, termination and monitoring of workers.',
          icon: 'work',
        },
        {
          value: 5,
          title: 'Essential Services',
          description: 'Access to essential private services, public services and benefits.',
          icon: 'account_balance_wallet',
        },
        {
          value: 6,
          title: 'Law Enforcement',
          description: 'Crime risk assessment, profiling, and polygraphs used by authorities.',
          icon: 'shield_person',
        },
        {
          value: 7,
          title: 'Migration',
          description: 'Migration, asylum and border control management and security.',
          icon: 'public',
        },
        {
          value: 8,
          title: 'Justice',
          description: 'Administration of justice and democratic processes, including elections.',
          icon: 'gavel',
        },
        {
          value: 0,
          title: 'None of the above',
          description: 'My AI system does not operate in any of these sensitive AI Act Annex III areas.',
          icon: 'block',
          span: 'md:col-span-2',
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
    <div class="max-h-[600px] overflow-y-auto pr-4 custom-scrollbar">
      <div role="radiogroup" aria-labelledby="q5-label" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label
          v-for="opt in options"
          :key="String(opt.value)"
          class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
          :class="[opt.span, { selected: modelValue === opt.value }]"
        >
          <input
            class="peer sr-only"
            name="area_select"
            type="radio"
            :value="opt.value"
            :checked="modelValue === opt.value"
            @change="emit('update:modelValue', opt.value as AnswerValue)"
          />
          <div class="flex-shrink-0 mr-4">
            <div class="size-12 bg-white dark:bg-slate-800 flex items-center justify-center text-slate-400 group-hover:bg-intertek-yellow group-hover:text-black transition-colors shadow-sm">
              <span class="material-symbols-outlined text-2xl">{{ opt.icon }}</span>
            </div>
          </div>
          <div class="flex-1">
            <div class="flex justify-between items-center mb-1">
              <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ opt.title }}</h3>
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
            </div>
            <p class="text-slate-500 dark:text-slate-400 text-[11px] leading-relaxed font-medium">{{ opt.description }}</p>
          </div>
          <div class="absolute inset-0 border-2 border-intertek-yellow opacity-0 peer-checked:opacity-100 pointer-events-none transition-opacity"></div>
        </label>
      </div>
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
