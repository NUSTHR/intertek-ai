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
        legalContext: '法律依据',
        reference: '参考',
        articleTitle: '第 50 条参考',
        articleDesc: '第 50 条规定了特定 AI 系统的透明度义务，以确保相关人员知悉与 AI 的交互或技术使用。',
        infoTip: '无论系统是否为高风险分类，都需要遵守这些透明度规则。',
        viewFullAct: '查看法规全文。',
        tip: '如果系统生成或操纵的内容可能误导用户真实性，应视为深度伪造内容并履行第 50 条义务。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitle: 'ARTICLE 50 REFERENCE',
        articleDesc:
          'Article 50 outlines specific transparency obligations for certain AI systems to ensure that individuals are aware they are interacting with an AI or being subjected to certain AI techniques.',
        infoTip: 'These transparency rules apply regardless of whether the AI system is classified as high-risk.',
        viewFullAct: 'View Full Act.',
        tip: 'If your system generates or manipulates content that could mislead users about authenticity, treat it as deep-fake content for Article 50 transparency duties.',
      },
)
const fallbackOptions = computed<Option[]>(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '直接交互',
          description: 'AI 系统用于与自然人直接交互（如聊天机器人、虚拟助手）。',
          icon: 'forum',
        },
        {
          value: 2,
          title: '生成/操纵合成内容',
          description: 'AI 系统生成或操纵图像、音频或视频内容（如生成式模型）。',
          icon: 'auto_fix_high',
        },
        {
          value: 3,
          title: '生物特征/情绪分析',
          description: 'AI 系统包含情绪识别或生物特征分类系统。',
          icon: 'psychology_alt',
        },
        {
          value: 4,
          title: '内容发布（深度伪造）',
          description: 'AI 系统生成或操纵文本并用于面向公众的公共利益发布。',
          icon: 'movie_edit',
        },
        {
          value: 0,
          title: '以上都不是',
          description: 'AI 系统不属于第 50 条定义的任何透明度敏感类别。',
          icon: 'block',
          exclusive: true,
        },
      ]
    : [
        {
          value: 1,
          title: 'Direct Interaction',
          description:
            'The AI system is intended to interact directly with natural persons (e.g., chatbots, virtual assistants).',
          icon: 'forum',
        },
        {
          value: 2,
          title: 'Synthetic Content Generation',
          description: 'The AI system generates or manipulates image, audio, or video content (e.g., generative AI models).',
          icon: 'auto_fix_high',
        },
        {
          value: 3,
          title: 'Biometric/Emotion Analysis',
          description: 'The AI system includes an emotion recognition or a biometric categorization system.',
          icon: 'psychology_alt',
        },
        {
          value: 4,
          title: 'Content Publication (Deep Fakes)',
          description:
            'The AI system generates or manipulates text which is published with the intent to inform the public on matters of public interest.',
          icon: 'movie_edit',
        },
        {
          value: 0,
          title: 'None of the above',
          description: 'The AI system does not fall into any of the transparency-sensitive categories defined in Article 50.',
          icon: 'block',
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
    module-label="Module 6 / 9"
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
    <div role="group" aria-labelledby="q6-label" class="flex flex-col gap-4">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: isSelected(opt.value) }"
      >
        <input
          class="peer sr-only"
          name="transparency_type"
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
            <h3 class="text-lg font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ opt.title }}</h3>
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
