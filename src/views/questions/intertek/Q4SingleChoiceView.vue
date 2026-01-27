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
        infoTip: '在作答前确认范围、目的与豁免。',
        viewFullAct: '查看法规全文。',
      }
    : {
        legalContext: 'Legal Context',
        reference: 'REFERENCE',
        infoTip: 'Confirm scope, purpose, and exemptions before selecting an answer.',
        viewFullAct: 'View Full Act.',
      },
)
const fallbackOptions = computed(() =>
  locale.isZh
    ? [
        {
          value: true,
          title: '是',
          description: '若该陈述适用于你的系统，请选择此项。',
          icon: 'check_circle',
        },
        {
          value: false,
          title: '否',
          description: '若该陈述不适用于你的系统，请选择此项。',
          icon: 'cancel',
        },
      ]
    : [
        {
          value: true,
          title: 'YES',
          description: 'Select this if the statement applies to your system.',
          icon: 'check_circle',
        },
        {
          value: false,
          title: 'NO',
          description: 'Select this if the statement does not apply to your system.',
          icon: 'cancel',
        },
      ],
)
const options = computed(() => buildOptions(props.question, fallbackOptions.value))
const inputName = computed(() => props.question?.id?.replace(/[^a-zA-Z0-9]/g, '_') ?? 'q4')
const labelId = computed(() => `${inputName.value}_label`)
const questionTag = computed(() => {
  const id = props.question?.id ?? ''
  if (!id) return ''
  return locale.isZh ? `问题 ${id.replace(/^q/i, '').toUpperCase()}` : `Question ${id.replace(/^q/i, '').toUpperCase()}`
})
const tipTextMap = computed<Record<string, string>>(() =>
  locale.isZh
    ? {
        'q4.3_b': '确认负面处理是否发生在原始数据收集语境之外。',
        'q4.3_c': '评估结果是否与所分析行为不相称。',
        'q4.4_a': '聚焦于对个人犯罪风险的预测或评估场景。',
        'q4.4_b': '确认评估是否仅基于画像而非客观事实。',
        'q4.5_a': '识别是否创建或扩展人脸识别数据库。',
        'q4.5_b': '核实是否对互联网或监控视频进行无差别抓取。',
        'q4.6_a': '限定在工作场所和教育机构的情绪推断。',
        'q4.6_b': '确认是否适用医疗或安全例外。',
        'q4.7_a': '判断是否使用生物特征数据对个人进行分类。',
        'q4.7_b': '确认是否通过生物特征分类推断敏感特征。',
        'q4.7_c': '确认是否适用执法标注豁免。',
        'q4.8_a': '确认系统是否在公共场所进行实时远程生物识别。',
        'q4.8_b': '确认目的为执法而非私人用途。',
        'q4.8_c': '核验是否对列示的三类公共安全目标具有严格必要性。',
      }
    : {
        'q4.3_b': 'Confirm whether negative treatment occurs outside the original data-collection context.',
        'q4.3_c': 'Assess whether outcomes are disproportionate to the behaviour analyzed.',
        'q4.4_a': 'Focus on individual criminal risk prediction or assessment use cases.',
        'q4.4_b': 'Check if the assessment relies solely on profiling rather than objective facts.',
        'q4.5_a': 'Identify whether a facial recognition database is created or expanded.',
        'q4.5_b': 'Verify whether data is scraped indiscriminately from internet or CCTV sources.',
        'q4.6_a': 'Limit the scope to workplace and education emotion inference use.',
        'q4.6_b': 'Confirm whether the medical or safety exception applies.',
        'q4.7_a': 'Determine if biometric data is used to categorise individuals.',
        'q4.7_b': 'Confirm inference of sensitive traits via biometric categorisation.',
        'q4.7_c': 'Check whether the law enforcement labelling exemption applies.',
        'q4.8_a': 'Confirm the system performs real-time remote biometric identification in public spaces.',
        'q4.8_b': 'Confirm the purpose is law enforcement rather than private use.',
        'q4.8_c': 'Verify strict necessity for the three listed public-safety objectives.',
      },
)
const legalTextMap = computed<Record<string, string>>(() =>
  locale.isZh
    ? {
        'q4.3_b':
          '第5(1)(c)(i)条：在与数据最初生成或收集语境无关的社会情境中，对特定自然人或群体给予不利或不当待遇；',
        'q4.3_c':
          '第5(1)(c)(ii)条：对特定自然人或群体给予不利或不当待遇，且该待遇对其社会行为或严重性而言不具正当性或不成比例；',
        'q4.4_a':
          '第5(1)(d)条：为此特定目的将用于评估或预测自然人犯罪风险的 AI 系统投放市场、投入使用或使用……',
        'q4.4_b':
          '第5(1)(d)条：仅基于对自然人的画像或其人格特质评估；该禁令不适用于用于支持人类评估某人是否涉案的 AI 系统，前提是该评估已基于与犯罪活动直接相关的客观可核事实；',
        'q4.5_a':
          '第5(1)(e)条：为此特定目的将创建或扩展人脸识别数据库的 AI 系统投放市场、投入使用或使用……',
        'q4.5_b': '第5(1)(e)条：通过对互联网或监控视频中的人脸图像进行无差别抓取；',
        'q4.6_a':
          '第5(1)(f)条：为此特定目的将用于在工作场所和教育机构推断自然人情绪的 AI 系统投放市场、投入使用或使用……',
        'q4.6_b': '第5(1)(f)条：除非该 AI 系统用于医疗或安全目的并拟投放市场或投入使用；',
        'q4.7_a':
          '第5(1)(g)条：为此特定目的将基于生物特征数据对自然人进行个体分类的生物特征分类系统投放市场、投入使用或使用……',
        'q4.7_b':
          '第5(1)(g)条：以此推断其种族、政治观点、工会成员身份、宗教或哲学信仰、性生活或性取向；',
        'q4.7_c':
          '第5(1)(g)条：该禁令不涵盖对依法获得的生物特征数据集（如图像）进行标注或过滤，或在执法领域对生物特征数据进行分类；',
        'q4.8_a': '第5(1)(h)条：为执法目的在公共可进入空间使用“实时”远程生物识别系统……',
        'q4.8_b': '第5(1)(h)条：用于执法目的，且仅在为下列目标之一具有严格必要性时……',
        'q4.8_c':
          '第5(1)(h)(i)-(iii)条：(i) 定向搜寻绑架、贩运或性剥削受害者及失踪人员；(ii) 防止对自然人生命或人身安全的特定、重大且迫在眉睫的威胁，或真实存在或可预见的恐怖袭击威胁；(iii) 定位或识别涉嫌实施附件 II 所列犯罪的人员……',
      }
    : {
        'q4.3_b':
          'Art 5(1)(c)(i): detrimental or unfavourable treatment of certain natural persons or groups of persons in social contexts that are unrelated to the contexts in which the data was originally generated or collected;',
        'q4.3_c':
          'Art 5(1)(c)(ii): detrimental or unfavourable treatment of certain natural persons or groups of persons that is unjustified or disproportionate to their social behaviour or its gravity;',
        'q4.4_a':
          'Art 5(1)(d): the placing on the market, the putting into service for this specific purpose, or the use of an AI system for making risk assessments of natural persons in order to assess or predict the risk of a natural person committing a criminal offence...',
        'q4.4_b':
          'Art 5(1)(d): based solely on the profiling of a natural person or on assessing their personality traits and characteristics; this prohibition shall not apply to AI systems used to support the human assessment of the involvement of a person in a criminal activity, which is already based on objective and verifiable facts directly linked to a criminal activity;',
        'q4.5_a':
          'Art 5(1)(e): the placing on the market, the putting into service for this specific purpose, or the use of AI systems that create or expand facial recognition databases...',
        'q4.5_b': 'Art 5(1)(e): through the untargeted scraping of facial images from the internet or CCTV footage;',
        'q4.6_a':
          'Art 5(1)(f): the placing on the market, the putting into service for this specific purpose, or the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions...',
        'q4.6_b':
          'Art 5(1)(f): except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons;',
        'q4.7_a':
          'Art 5(1)(g): the placing on the market, the putting into service for this specific purpose, or the use of biometric categorisation systems that categorise individually natural persons based on their biometric data...',
        'q4.7_b':
          'Art 5(1)(g): to deduce or infer their race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation;',
        'q4.7_c':
          'Art 5(1)(g): this prohibition does not cover any labelling or filtering of lawfully acquired biometric datasets, such as images, based on biometric data or categorizing of biometric data in the area of law enforcement;',
        'q4.8_a':
          'Art 5(1)(h): the use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement...',
        'q4.8_b':
          'Art 5(1)(h): for the purposes of law enforcement, unless and in so far as such use is strictly necessary for one of the following objectives...',
        'q4.8_c':
          'Art 5(1)(h)(i)-(iii): (i) the targeted search for specific victims of abduction, trafficking in human beings or sexual exploitation of human beings, as well as the search for missing persons; (ii) the prevention of a specific, substantial and imminent threat to the life or physical safety of natural persons or a genuine and present or genuine and foreseeable threat of a terrorist attack; (iii) the localisation or identification of a person suspected of having committed a criminal offence referred to in Annex II...',
      },
)
const legalCopy = computed(() => props.question?.ref ?? legalTextMap.value[props.question?.id ?? ''] ?? '')
const tipCopy = computed(() => tipTextMap.value[props.question?.id ?? ''] ?? props.question?.description ?? '')
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
