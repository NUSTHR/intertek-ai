<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'
import { useLocaleStore } from '@/stores/locale'
import NavBar from '@/components/NavBar.vue'
import LoadingCard from '@/components/LoadingCard.vue'
import logoUrl from '@/assets/images/logo/b9d2336ed590ab1e2a8d517d7f555f72.png'
import portraitUrl from '@/assets/images/self-portrait/03ada209733101dff56722826aeaa67f.png'

const router = useRouter()
const store = useQuestionnaireStore()
const locale = useLocaleStore()
const helpCenterUrl = 'https://www.intertekinform.com/en-au/contact-us/'
const ui = computed(() =>
  locale.isZh
    ? {
        home: '首页',
        helpCenter: '帮助中心',
        mapperVersion: '合规映射器 v2.4',
        assessmentComplete: '评估完成',
        assessmentSummary: '基于欧盟AI法案条例细节与用户输入信息，系统已完成对产品的风险分类。',
        loading: '加载中…',
        regulatoryStatus: '监管类别',
        regulatoryClassification: (value: string) => `风险分类：${value}`,
        exclusionConfirmed: '已确认不适用',
        roleLabel: '角色',
        typeLabel: '产品类型',
        riskJustification: '风险等级说明',
        legalJustification: '法律依据',
        obligation: '义务',
        complianceSuggestion: '合规要点',
        optionalVerification: '可选',
        validateTitle: '验证您的',
        validateHighlight: '自我评估判定',
        validateDesc: '将初步自评升级为专家验证，强化合规策略。',
        bookMeeting: '预约会议',
        callLabel: '电话：020-82139147',
        specialistTitle: '欧盟AI监管专家',
        specialistDesc: 'AI 合规工程师，熟知欧盟人工智能法案细节，具备丰富的AI领域经验。',
        evaluateAnother: '再评估一个系统？',
        evaluateDesc: '清空当前会话数据并重新开始问卷。',
        restart: '重新开始',
        disclaimer:
          '本工具依据欧盟法规 (EU) 2024/1689（人工智能法案），基于用户提供的信息自动生成评估结果。该结果仅供参考，不构成任何法律意见或专业建议。Intertek 不对评估结果的准确性或完整性提供保证，亦不承担相关法律责任。最终分类结果请务必经由专家复核。使用本工具不构成双方任何形式的合同关系。',
        privacy: '隐私政策',
        terms: '服务条款',
        cookie: 'Cookie 政策',
      }
    : {
        home: 'Home',
        helpCenter: 'Help',
        mapperVersion: 'Compliance Mapper v2.4',
        assessmentComplete: 'Assessment Complete',
        assessmentSummary:
          'Based on the EU AI Act framework and your technical inputs, your system has been categorized for regulatory handling.',
        loading: 'Loading…',
        regulatoryStatus: 'Regulatory Level',
        regulatoryClassification: (value: string) => `Risk Level Classification: ${value}`,
        exclusionConfirmed: 'Exclusion Confirmed',
        roleLabel: 'Role',
        typeLabel: 'Product Type',
        riskJustification: 'Risk Level Justification',
        legalJustification: 'Legal Justification',
        obligation: 'Obligation',
        complianceSuggestion: 'Compliance Key Points',
        optionalVerification: 'Optional Verification',
        validateTitle: 'Validate Your',
        validateHighlight: 'Self-assessment',
        validateDesc:
          'Fortify your compliance strategy by transitioning from a preliminary self-assessment to a definitive, expert-verified validation.',
        bookMeeting: 'Book a Meeting',
        callLabel: 'call: 020-82139147',
        specialistTitle: 'EU AI Regulatory Specialist',
        specialistDesc: 'AI Compliance Engineer with extensive experience in AI field.',
        evaluateAnother: 'Evaluate Another System?',
        evaluateDesc: 'Clear all current session data and restart the regulatory mapping questionnaire.',
        restart: 'Restart',
        disclaimer:"The EU AI Act Compliance Mapper provides automated, general guidance based on user inputs and Regulation (EU) 2024/1689. This tool is for informational purposes only and does not constitute legal advice. Intertek expressly disclaims all liability and warranties regarding the accuracy or completeness of the results. The final classification remains the sole responsibility of the user and must be verified by a qualified expert. Use of this tool does not establish a contractual relationship.",
        privacy: 'Privacy Policy',
        terms: 'Terms of Service',
        cookie: 'Cookie Policy',
      },
)

const conclusion = computed(() => store.conclusion ?? {})
const roleValue = computed(() =>
  locale.isZh
    ? conclusion.value.Role_CN ?? store.parameters.Role_CN ?? conclusion.value.Role ?? store.parameters.Role ?? ''
    : conclusion.value.Role ?? store.parameters.Role ?? conclusion.value.Role_CN ?? store.parameters.Role_CN ?? '',
)
const typeValue = computed(() =>
  locale.isZh
    ? conclusion.value.Type_CN ?? store.parameters.Type_CN ?? conclusion.value.Type ?? store.parameters.Type ?? ''
    : conclusion.value.Type ?? store.parameters.Type ?? conclusion.value.Type_CN ?? store.parameters.Type_CN ?? '',
)
const riskValue = computed(() =>
  locale.isZh
    ? conclusion.value.Risk_level_CN ??
      store.parameters.Risk_level_CN ??
      conclusion.value.Risk_level ??
      store.parameters.Risk_level ??
      ''
    : conclusion.value.Risk_level ??
      store.parameters.Risk_level ??
      conclusion.value.Risk_level_CN ??
      store.parameters.Risk_level_CN ??
      '',
)
const summaryRows = computed(() => [
  { label: ui.value.roleLabel, value: roleValue.value },
  { label: ui.value.typeLabel, value: typeValue.value },
  { label: 'Risk_level', value: riskValue.value },
])
const riskLevelText = computed(() => String(riskValue.value ?? '').trim())
const statusTitle = computed(() => {
  const raw = riskLevelText.value
  if (!raw) return locale.isZh ? '不受监管' : 'Out of Regulation'
  return raw
})
const statusSubtitle = computed(() => {
  if (riskLevelText.value) return ui.value.regulatoryClassification(riskLevelText.value)
  return ui.value.exclusionConfirmed
})
onMounted(async () => {
  if (!store.sessionId) {
    await router.replace({ name: 'start' })
    return
  }
  await store.fetchResult()
})
watch(
  () => locale.lang,
  async () => {
    if (store.sessionId) {
      await store.fetchResult()
    }
  },
)

async function restart() {
  store.reset()
  const module = await store.init()
  if (!module) return
  await router.push({ name: 'module', params: { id: module.id } })
}

async function goHome() {
  await router.push({ name: 'start' })
}
</script>

<template>
  <div class="min-h-screen flex flex-col font-sans antialiased text-black bg-white">
    <NavBar
      :home-label="ui.home"
      :help-label="ui.helpCenter"
      :action-label="ui.restart"
      :action-disabled="store.loading"
      :help-href="helpCenterUrl"
      @home="goHome"
      @action="restart"
    />
    <main class="max-w-7xl mx-auto px-8 pt-20 pb-32 flex-grow w-full">
      <section class="mb-20">
      <!-- <section class="mb-24"> -->
        <div class="flex flex-col items-start gap-6 mb-12">
          <div class="flex items-center gap-3">
            <span class="h-px w-8 bg-[#FAD400]"></span>
            <span class="text-xs font-black tracking-[0.3em] uppercase text-gray-500">{{ ui.assessmentComplete }}</span>
          </div>
          <!-- <h1 class="text-xl font-light max-w-2xl leading-relaxed text-gray-600"> -->
          <h1 class="text-xl font-light max-w-2xl leading-relaxed text-gray-500">
            {{ ui.assessmentSummary }}
          </h1>
          <div v-if="store.error" class="text-sm text-red-600">{{ store.error }}</div>
          <div v-else-if="summaryRows.length === 0" class="flex items-center">
            <LoadingCard
              :loading="true"
              :loading-text="ui.loading"
              :failed-text="ui.loading"
            />
          </div>
        </div>
        <div class="relative py-4">
          <span class="block text-xs font-black tracking-[0.5em] mb-6 text-[#FAD400] uppercase">{{ ui.regulatoryStatus }}</span>
          <h2
            v-if="!locale.isZh"
            class="text-[clamp(2.2rem,5.5vw,4.5rem)] leading-[1] font-extrabold tracking-tighter uppercase mb-8 break-words"
          >
            {{ statusTitle.split(' ').slice(0, 2).join(' ') }}
            <br class="hidden md:block" />
            {{ statusTitle.split(' ').slice(2).join(' ') }}<span class="text-[#FAD400]">.</span>
          </h2>
          <h2 v-else class="text-[clamp(2.2rem,5.5vw,4.5rem)] leading-[1] font-extrabold tracking-tighter mb-8 break-words">
            {{ statusTitle }}<span class="text-[#FAD400]">。</span>
          </h2>
          <div class="flex items-center gap-4">
            <div class="h-2 bg-black w-32"></div>
            <span class="text-xs font-bold tracking-widest uppercase opacity-40">{{ statusSubtitle }}</span>
          </div>
        </div>
      </section>
      <section class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-32 border-t border-gray-100 pt-16">
        <div class="bg-[#F8FAFC] p-10 rounded-3xl border border-gray-100 hover:border-[#FAD400] transition-colors flex flex-col justify-center">
          <h3 class="font-black text-xl uppercase tracking-tighter mb-4">
            {{ roleValue }}<br />
            <span class="text-[#FAD400] text-sm tracking-widest font-bold">{{ ui.roleLabel }}</span>
          </h3>
          <p class="text-sm font-medium leading-relaxed text-gray-500 max-w-md">
            {{ conclusion.Role_Description ?? store.parameters.Role_Description ?? '' }}
          </p>
        </div>
        <div class="bg-[#F8FAFC] p-10 rounded-3xl border border-gray-100 hover:border-[#FAD400] transition-colors flex flex-col justify-center">
          <h3 class="font-black text-xl uppercase tracking-tighter mb-4">
            {{ typeValue }}<br />
            <span class="text-[#FAD400] text-sm tracking-widest font-bold">{{ ui.typeLabel }}</span>
          </h3>
          <p class="text-sm font-medium leading-relaxed text-gray-500 max-w-md">
            {{ conclusion.Product_Type_Description ?? store.parameters.Product_Type_Description ?? '' }}
          </p>
        </div>
        <div class="bg-white p-10 rounded-3xl border-2 border-black flex flex-col min-h-[400px]">
          <div class="mb-auto">
            <span class="material-symbols-outlined text-4xl mb-6 text-black">code_blocks</span>
            <h3 class="font-black text-3xl uppercase tracking-tighter mb-6">
              {{ conclusion.Risk_Level_Justification ?? store.parameters.Risk_Level_Justification ?? ui.riskJustification }}<br />
              <span class="text-[#FAD400] text-xs tracking-[0.3em] font-black">{{ ui.legalJustification }}</span>
            </h3>
          </div>
          <p class="text-base font-medium leading-relaxed text-gray-600">
            {{ conclusion.Risk_Level_Reason ?? store.parameters.Risk_Level_Reason ?? '' }}
          </p>
        </div>
        <div class="bg-black p-10 rounded-3xl flex flex-col min-h-[400px] text-white">
          <div class="mb-auto">
            <span class="material-symbols-outlined text-4xl mb-6 text-[#FAD400]">verified_user</span>
            <h3 class="font-black text-3xl uppercase tracking-tighter mb-6">
              {{ ui.obligation }}<br />
              <span class="text-[#FAD400] text-xs tracking-[0.3em] font-black">{{ ui.complianceSuggestion }}</span>
            </h3>
          </div>
          <p class="text-base font-medium leading-relaxed text-gray-300">
            {{ conclusion.View ?? store.parameters.View ?? '' }}
          </p>
        </div>
      </section>
      <section
        class="bg-white border border-gray-100 rounded-[2.5rem] p-8 md:p-12 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.08)] flex flex-col lg:flex-row items-center gap-16 relative overflow-hidden"
      >
        <div class="flex-1 space-y-10 z-10">
          <div class="space-y-4">
            <span class="inline-block px-4 py-1 bg-gray-100 text-gray-600 text-[10px] font-black tracking-widest uppercase rounded-full">
              {{ ui.optionalVerification }}
            </span>
            <h3 class="text-4xl md:text-5xl font-black tracking-tight leading-tight">
              {{ ui.validateTitle }} <br /><span class="relative inline-block before:content-[''] before:absolute before:-bottom-1 before:left-0 before:w-full before:h-2 before:bg-[#FAD400] before:-z-10">{{ ui.validateHighlight }}</span>
            </h3>
            <p class="text-gray-500 text-lg max-w-md">
              {{ ui.validateDesc }}
            </p>
          </div>
          <div class="flex flex-wrap gap-4">
            <a
              class="px-10 py-5 bg-black text-white text-sm font-black uppercase tracking-widest rounded-xl hover:bg-[#FAD400] hover:text-black transition-all flex items-center gap-3"
              href="mailto:tom.hr.tang@intertek.com?subject=AI%20Compliance%20Meeting%20Reservation"
            >
              {{ ui.bookMeeting }}
              <span class="material-symbols-outlined text-lg">calendar_today</span>
            </a>
            <div class="flex items-center justify-center w-fit px-10 py-5 border border-gray-200 text-black text-sm font-black uppercase tracking-widest rounded-xl hover:border-black transition-colors cursor-default">
              {{ ui.callLabel }}
            </div>
          </div>
        </div>
        <div class="flex-1 flex justify-center lg:justify-end">
          <div class="relative w-full max-w-md bg-white rounded-3xl p-6 border border-gray-100 shadow-xl shadow-gray-100/50">
            <div class="flex flex-col md:flex-row gap-8 items-center">
              <img
                alt="Tom Tang, AI Regulatory Specialist"
                class="w-32 h-32 md:w-48 md:h-64 object-cover rounded-2xl shadow-sm grayscale hover:grayscale-0 transition-all duration-500"
                :src="portraitUrl"
              />
              <div class="space-y-3 text-center md:text-left">
                <h4 class="text-2xl font-black leading-tight tracking-tight">Tom Tang</h4>
                <p class="text-[#FAD400] font-black text-[10px] tracking-[0.2em] uppercase">{{ ui.specialistTitle }}</p>
                <p class="text-gray-500 font-medium text-sm leading-relaxed">
                  {{ ui.specialistDesc }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="mt-40 flex flex-col items-center gap-10 text-center">
        <div class="h-12 w-px bg-gray-200"></div>
        <div class="space-y-3">
          <h2 class="text-2xl font-black uppercase tracking-tight">{{ ui.evaluateAnother }}</h2>
          <p class="text-gray-400 font-medium max-w-sm">{{ ui.evaluateDesc }}</p>
        </div>
        <button
          type="button"
          class="group flex items-center gap-4 px-10 py-5 bg-[#FAD400] text-black rounded-full font-black text-sm uppercase tracking-widest hover:bg-black hover:text-white transition-all duration-300"
          @click="restart"
        >
          <span class="material-symbols-outlined group-hover:rotate-180 transition-transform duration-700">refresh</span>
          {{ ui.restart }}
        </button>
        <div class="w-full max-w-6xl">
          <div class="bg-[#F9FAFB] p-8 rounded-lg border border-[#E5E7EB] w-full">
            <p class="text-sm text-[#4B5563] leading-relaxed text-center">{{ ui.disclaimer }}</p>
          </div>
        </div>
      </section>
    </main>
    <footer class="max-w-7xl mx-auto px-8 py-16 border-t border-gray-100 flex flex-col md:flex-row justify-between items-center gap-8 w-full">
      <div class="flex items-center gap-6">
        <a href="https://www.intertek.com/">
          <img alt="Intertek AI² Logo" class="w-8 h-8 rounded-md" :src="logoUrl" />
        </a>
        <span class="text-xl font-black uppercase italic tracking-tighter">Intertek AI²</span>
        <span class="w-px h-4 bg-gray-200"></span>
        <span class="text-gray-400 text-[10px] font-bold tracking-widest">© 2024 COMPLIANCE MAPPER</span>
      </div>
      <div class="flex gap-10 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">
        <a class="hover:text-black transition-colors" href="https://www.intertek.com/privacy/">{{ ui.privacy }}</a>
        <a class="hover:text-black transition-colors" href="https://www.intertek.com/terms/">{{ ui.terms }}</a>
        <a class="hover:text-black transition-colors" href="https://www.intertek.com/cookie-policy/">{{ ui.cookie }}</a>
        <a class="hover:text-black transition-colors" :href="helpCenterUrl">{{ ui.helpCenter }}</a>
      </div>
    </footer>
  </div>
</template>
late>
