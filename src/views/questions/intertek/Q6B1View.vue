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
        infoTip: '在得出义务结论前确认是否存在豁免。',
        viewFullAct: '查看法规全文。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        infoTip: 'Confirm whether an exemption applies before concluding the obligation.',
        viewFullAct: 'View Full Act.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: true,
          title: '是',
          description: '系统仅作为辅助工具（如拼写检查、轻微裁剪），不对主要内容进行实质性生成或改写。',
          icon: 'edit_note',
        },
        {
          value: false,
          title: '否',
          description: '系统具备生成能力或进行超出简单辅助编辑的实质性改动。',
          icon: 'auto_awesome',
        },
      ]
    : [
        {
          value: true,
          title: 'YES',
          description:
            'The system serves as an assistive tool (e.g., spellcheck, minor cropping) and does not fundamentally alter or generate the primary content.',
          icon: 'edit_note',
        },
        {
          value: false,
          title: 'NO',
          description:
            'The system performs generative functions or substantial alterations that go beyond simple assistive editing of existing content.',
          icon: 'auto_awesome',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const inputName = computed(() => props.question?.id?.replace(/[^a-zA-Z0-9]/g, '_') ?? 'q6')
const labelId = computed(() => `${inputName.value}_label`)
const questionTag = computed(() => computeQuestionTag(props.question?.id ?? '', locale.isZh))
const legalCopy = computed(() => props.question?.ref ?? '')
const tipMap = computed<Record<string, string>>(() =>
  locale.isZh
    ? {
        'q6.p.2.assistive': '确认系统仅执行标准编辑或轻微修改。',
        'q6.p.2.le_auth': '确认系统是否获得执法用途的法律授权。',
      }
    : {
        'q6.p.2.assistive': 'Confirm whether the system only performs standard editing or minor alteration.',
        'q6.p.2.le_auth': 'Confirm whether the system is legally authorized for law enforcement purposes.',
      },
)
const tipCopy = computed(() => tipMap.value[props.question?.id ?? ''] ?? '')
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
          <div class="border-b border-slate-100 dark:border-slate-800 pb-4">
            <h4 class="font-black text-slate-900 dark:text-white mb-3 text-xs uppercase tracking-tight">{{ ui.reference }}</h4>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              {{ legalCopy }}
            </p>
          </div>
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
          {{ tipCopy }}
        </p>
      </div>
    </template>
  </IntertekLayout>
</template>
