<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerScalar, AnswerValue, Module, ModuleQuestion } from '@/types/questionnaire'
import IntertekLayout from './IntertekLayout.vue'
import { buildOptions } from './optionUtils'
import { useLocaleStore } from '@/stores/locale'

type Option = {
  value: AnswerScalar
  title: string
  description: string
  icon: string
  cite?: string
  exclusive?: boolean
}

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
        selectAll: '可多选',
        legalContext: '法律依据',
        reference: '参考',
        articleTitle: '法规第 5 条：禁止的 AI 实践',
        articleIntro: '1. 以下 AI 实践被禁止：',
        articleItems: [
          '将使用超出个人意识的潜意识技术的 AI 系统投放市场、投入使用或用于实质性扭曲个人行为。',
          '利用特定群体（因年龄、残疾或特定社会或经济处境）脆弱性的 AI 系统。',
          '公共当局基于社会行为或人格特征对自然人进行评估或分类的 AI 系统（社会评分）。',
          '用于执法的“实时”远程生物识别系统，除非为特定目标且严格必要。',
        ],
        tip: '落入上述类别的 AI 系统被视为“不可接受风险”，在欧盟被禁止。',
        viewFullAct: '查看法规全文。',
        complianceTip: '法规第 5 条要求必须遵守。被认定为禁止的系统不得在欧盟市场投放。',
      }
    : {
        selectAll: 'Select all that apply',
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitle: 'Article 5: Prohibited AI Practices',
        articleIntro: '1. The following AI practices shall be prohibited:',
        articleItems: [
          "The placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person's consciousness in order to materially distort a person's behavior.",
          'The use of an AI system that exploits any of the vulnerabilities of a specific group of persons due to their age, disability or a specific social or economic situation.',
          'The use of AI systems by public authorities for the evaluation or classification of natural persons based on their social behavior or personality characteristics (social scoring).',
          "The use of 'real-time' remote biometric identification systems in publicly accessible spaces for law enforcement, unless strictly necessary for specific objectives.",
        ],
        tip: "Any AI system falling under these categories is considered to pose an 'Unacceptable Risk' and is banned in the EU.",
        viewFullAct: 'View Full Act.',
        complianceTip: 'Compliance with Article 5 is mandatory. Systems identified as prohibited cannot be placed on the EU market.',
      },
)
const fallbackOptions = computed<Option[]>(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '潜意识或操控性技术',
          description: '使用超出个人意识的潜意识技术或刻意操控、欺骗性技术。',
          icon: 'warning',
        },
        {
          value: 2,
          title: '利用脆弱性',
          description: '利用因年龄、残疾或特定社会经济处境带来的脆弱性。',
          icon: 'report',
        },
        {
          value: 3,
          title: '社会评分',
          description: '基于社会行为或人格特征对个人进行长期评估或分类。',
          icon: 'fact_check',
        },
        {
          value: 4,
          title: '个人风险评估',
          description: '仅基于画像或人格特征进行犯罪风险评估（不含支持人工评估的情形）。',
          icon: 'balance',
        },
        {
          value: 5,
          title: '人脸抓取',
          description: '通过无差别抓取互联网或监控视频的人脸图像来创建或扩展数据库。',
          icon: 'face',
        },
        {
          value: 6,
          title: '情绪识别',
          description: '在工作场所或教育机构推断情绪（医疗或安全原因除外）。',
          icon: 'mood',
        },
        {
          value: 7,
          title: '生物特征分类',
          description: '基于生物特征推断种族、政治观点、工会成员身份、宗教信仰或性取向。',
          icon: 'groups',
        },
        {
          value: 8,
          title: '实时远程生物识别',
          description: '在公共场所用于执法的“实时”远程生物识别，仅限严格必要的例外。',
          icon: 'sensors',
        },
        {
          value: 0,
          title: '以上都不是',
          description: '我的 AI 系统不涉及上述任何被禁止的实践。',
          icon: 'close',
          exclusive: true,
        },
      ]
    : [
        {
          value: 1,
          title: 'Subliminal or manipulative techniques',
          description:
            "Use of subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques.",
          icon: 'warning',
        },
        {
          value: 2,
          title: 'Exploitation of vulnerabilities',
          description: 'Exploiting vulnerabilities related to age, disability, or a specific social or economic situation.',
          icon: 'report',
        },
        {
          value: 3,
          title: 'Social scoring',
          description:
            'Evaluation or classification of persons over time based on social behaviour or personal characteristics.',
          icon: 'fact_check',
        },
        {
          value: 4,
          title: 'Individual Risk Assessments',
          description:
            'Making individual risk assessments for criminal offenses based solely on profiling or personality traits (excluding assessments to support human evaluation).',
          icon: 'balance',
        },
        {
          value: 5,
          title: 'Facial scraping',
          description:
            'Creating or expanding facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage.',
          icon: 'face',
        },
        {
          value: 6,
          title: 'Emotion recognition',
          description:
            'Using AI to infer emotions of persons in the workplace or educational institutions, except for medical or safety reasons.',
          icon: 'mood',
        },
        {
          value: 7,
          title: 'Biometric categorization',
          description:
            'Categorizing individuals based on biometric data to infer race, political opinions, trade union membership, religious beliefs, or sexual orientation.',
          icon: 'groups',
        },
        {
          value: 8,
          title: 'Real-time Remote Biometric ID',
          description:
            "Use of 'real-time' remote biometric identification systems in publicly accessible spaces for law enforcement, with specific narrow exceptions.",
          icon: 'sensors',
        },
        {
          value: 0,
          title: 'None of the above',
          description: 'My AI system does not engage in any of the prohibited practices listed above.',
          icon: 'close',
          exclusive: true,
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const questionTag = computed(() => {
  const id = props.question?.id ?? ''
  if (!id) return ''
  return locale.isZh ? `问题 ${id.replace(/^q/i, '').toUpperCase()}` : `Question ${id.replace(/^q/i, '').toUpperCase()}`
})

const selectedValues = () => (Array.isArray(props.modelValue) ? (props.modelValue as AnswerScalar[]) : [])

function toggleValue(value: AnswerScalar) {
  const current = selectedValues()
  const isSelected = current.includes(value)
  const exclusiveValues = options.value.filter((opt) => opt.exclusive).map((opt) => opt.value)
  if (isSelected) {
    emit(
      'update:modelValue',
      current.filter((v) => v !== value) as AnswerValue,
    )
    return
  }
  if (exclusiveValues.includes(value)) {
    emit('update:modelValue', [value])
    return
  }
  const withoutExclusive = current.filter((v) => !exclusiveValues.includes(v))
  emit('update:modelValue', Array.from(new Set([...withoutExclusive, value])) as AnswerValue)
}

function isSelected(value: AnswerScalar) {
  return selectedValues().includes(value)
}
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
    <div class="flex items-center gap-3 mb-6 text-[11px] font-black uppercase tracking-[0.2em] text-slate-500">
      {{ ui.selectAll }}
    </div>
    <div role="group" aria-labelledby="q41-label" class="flex flex-col gap-4 max-h-[620px] overflow-y-auto pr-2">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: isSelected(opt.value) }"
      >
        <input
          class="peer sr-only"
          name="practice_category"
          type="checkbox"
          :value="opt.value"
          :checked="isSelected(opt.value)"
          @change="toggleValue(opt.value)"
        />
        <div class="flex-shrink-0 mr-6">
          <div class="size-14 bg-white dark:bg-slate-800 flex items-center justify-center text-slate-400 group-hover:bg-intertek-yellow group-hover:text-black transition-colors shadow-sm">
            <span class="material-symbols-outlined text-3xl">{{ opt.icon }}</span>
          </div>
        </div>
        <div class="flex-1">
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ opt.title }}</h3>
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
          </div>
          <p class="text-slate-600 dark:text-slate-400 text-xs leading-relaxed max-w-2xl font-medium">
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
        <div class="p-6 flex flex-col gap-6 max-h-[500px] overflow-y-auto custom-scrollbar">
          <div v-if="question.ref" class="border-b border-slate-100 dark:border-slate-800 pb-4">
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">{{ ui.reference }}</h4>
            <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              {{ question.ref }}
            </p>
          </div>
          <template v-else>
            <div class="border-b border-slate-100 dark:border-slate-800 pb-4">
              <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">
                {{ ui.articleTitle }}
              </h4>
              <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium mb-3">
                {{ ui.articleIntro }}
              </p>
              <ul class="text-[10px] text-slate-600 dark:text-slate-400 leading-relaxed list-disc pl-4 flex flex-col gap-2">
                <li v-for="item in ui.articleItems" :key="item">{{ item }}</li>
              </ul>
            </div>
          </template>
          <div class="bg-slate-50 dark:bg-slate-800 p-4 border-l-4 border-intertek-yellow">
            <div class="flex gap-3">
              <span class="material-symbols-outlined text-intertek-dark dark:text-intertek-yellow text-xl">info</span>
              <p class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-normal italic">
                {{ ui.tip }}
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
          {{ ui.complianceTip }}
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
