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
        articleTitleRisk: '法规第6(1)(a)条',
        articleDescRisk:
          '当 AI 系统作为法规附件 I 所列协调立法覆盖产品的安全组件，或其本身即为产品时，为高风险。',
        articleTitleSafety: '法规第3(14)条',
        articleDescSafety:
          '“安全组件”是指履行安全功能的产品或系统部件，其失效或故障将危及人员健康安全或财产安全。',
        infoTip: '明确产品角色是判断是否适用第6(1)条分类的关键。',
        viewFullAct: '查看法规全文。',
        tip: '安全组件指其失效会危及健康或安全，且落入法规附件 I 协调立法范围。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        articleTitleRisk: 'Art 6(1)(a)',
        articleDescRisk:
          'An AI system is high-risk if it is intended to be used as a safety component of a product, or is itself a product, covered by Union harmonisation legislation listed in Annex I.',
        articleTitleSafety: 'Art 3(14)',
        articleDescSafety:
          "Defines 'safety component' as a component of a product or a system which fulfils a safety function for that product or system or the failure or malfunction of which endangers the health and safety of persons or property.",
        infoTip:
          'Identifying the product role is critical for determining if the AI system falls under Article 6(1) classification.',
        viewFullAct: 'View Full Act.',
        tip: 'Safety components are those whose failure endangers health or safety and fall under Annex I harmonisation legislation.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: 1,
          title: '独立产品',
          description: 'AI 系统本身即为法规附件 I 所列协调立法覆盖的产品。',
          icon: 'inventory_2',
        },
        {
          value: 2,
          title: '安全组件',
          description:
            'AI 系统拟作为产品安全组件使用，或本身即为安全组件，其失效或故障将危及人员或财产安全。',
          icon: 'shield_with_heart',
        },
        {
          value: 3,
          title: '非安全组件',
          description: 'AI 系统是产品组件但不承担安全功能，或仅用于功能/效用目的。',
          icon: 'settings_input_component',
        },
        {
          value: 0,
          title: '以上都不是',
          description: 'AI 系统与法规附件 I 所列协调立法覆盖的产品无关。',
          icon: 'block',
        },
      ]
    : [
        {
          value: 1,
          title: 'Standalone Product',
          description:
            'The AI system is itself a product covered by the Union harmonisation legislation listed in Annex I.',
          icon: 'inventory_2',
        },
        {
          value: 2,
          title: 'Safety Component',
          description:
            'The AI system is intended to be used as a safety component of a product, or is itself a safety component. A failure or malfunction endangers the health and safety of persons or property.',
          icon: 'shield_with_heart',
        },
        {
          value: 3,
          title: 'Non-Safety Component',
          description:
            'The AI system is a component of a product but does not perform a safety function, or is integrated for purely functional/utility purposes.',
          icon: 'settings_input_component',
        },
        {
          value: 0,
          title: 'None of the above',
          description:
            'The AI system is not related to products covered by the specific Union harmonisation legislation listed in Annex I.',
          icon: 'block',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const inputName = 'ai_role'
const labelId = 'q5-label'
const questionTag = computed(() => {
  const id = props.question?.id ?? ''
  if (!id) return ''
  return locale.isZh ? `问题 ${id.replace(/^q/i, '').toUpperCase()}` : `Question ${id.replace(/^q/i, '').toUpperCase()}`
})
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
            <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">{{ ui.reference }}</h4>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              {{ question.ref }}
            </p>
          </div>
          <template v-else>
            <div class="border-b border-slate-100 dark:border-slate-800 pb-4">
              <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">
                {{ ui.articleTitleRisk }}
              </h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.articleDescRisk }}
              </p>
            </div>
            <div class="border-b border-slate-100 dark:border-slate-800 pb-4">
              <h4 class="font-black text-slate-900 dark:text-white mb-2 text-xs uppercase tracking-tight">
                {{ ui.articleTitleSafety }}
              </h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {{ ui.articleDescSafety }}
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
