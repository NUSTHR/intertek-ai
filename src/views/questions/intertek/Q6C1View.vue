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
        articleTitle: '法规第50(3)条',
        articleDesc:
          '对接触生物特征分类或情绪识别系统的个人的告知义务，不适用于在执法目的下且该用途由欧盟或成员国法律允许的 AI 系统。',
        infoTip: '豁免仅在执法活动具有明确法律授权时适用。',
        viewFullAct: '查看法规全文。',
        tip: '执法用途包括公共安全与预防生命威胁，但仅在有明确法律授权时适用。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitle: 'ARTICLE 50(3)',
        articleDesc:
          'The transparency obligation to inform individuals exposed to a biometric categorization or emotion recognition system does not apply to AI systems used for law enforcement purposes where such use is permitted by Union or national law.',
        infoTip: 'Exemptions only apply if legal authorization is explicitly provided for law enforcement activities.',
        viewFullAct: 'View Full Act.',
        tip: 'Law enforcement purposes include public security and the prevention of threats to life, but only when explicit legal authorization is in place.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: true,
          title: '是',
          description: '用途受到欧盟或成员国法律授权，用于执法目的，包括侦测、预防或调查犯罪。',
          icon: 'verified_user',
        },
        {
          value: false,
          title: '否',
          description: '用途在其他场景（如工作场所、教育）中进行，生物特征分类或情绪识别可能受到限制。',
          icon: 'domain_disabled',
        },
      ]
    : [
        {
          value: true,
          title: 'YES',
          description:
            'The use is authorized by Union or national law for the purpose of law enforcement, including detecting, preventing or investigating criminal offences.',
          icon: 'verified_user',
        },
        {
          value: false,
          title: 'NO',
          description:
            'The use is intended for other settings (e.g., workplace, education) where biometric categorization or emotion recognition may be restricted.',
          icon: 'domain_disabled',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const questionTag = computed(() => computeQuestionTag(props.question?.id ?? '', locale.isZh))
</script>

<template>
  <IntertekLayout
    module-label="Module 6 / 6"
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
    <div role="radiogroup" aria-labelledby="q6c1-label" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <label
        v-for="opt in options"
        :key="String(opt.value)"
        class="option-card cursor-pointer relative flex flex-col p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
        :class="{ selected: modelValue === opt.value }"
      >
        <input
          class="peer sr-only"
          name="legal_auth"
          type="radio"
          :value="opt.value"
          :checked="modelValue === opt.value"
          @change="emit('update:modelValue', opt.value as AnswerValue)"
        />
        <div class="flex items-start mb-6">
          <div class="size-14 bg-white dark:bg-slate-800 flex items-center justify-center text-slate-400 group-hover:bg-intertek-yellow group-hover:text-black transition-colors shadow-sm">
            <span class="material-symbols-outlined text-3xl">{{ opt.icon }}</span>
          </div>
          <div class="ml-auto flex items-center gap-3">
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
        <div class="flex-1">
          <h3 class="text-lg font-black text-slate-900 dark:text-white uppercase tracking-tight mb-2">{{ opt.title }}</h3>
          <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed font-medium">
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
