<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'
import { useLocaleStore } from '@/stores/locale'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const store = useQuestionnaireStore()
const locale = useLocaleStore()
const helpCenterUrl = 'https://www.intertekinform.com/en-au/contact-us/'
const ui = computed(() =>
  locale.isZh
    ? {
        navHome: '首页',
        navHelp: '帮助中心',
        navStart: '开始评估',
        heroTitle: 'EU AI Act',
        heroSubtitle: 'Compliance Mapper',
        heroDesc: '深度解码欧盟AI法案，精准界定监管义务',
        startAssessment: '开始评估',
        readMethodology: '阅读方法论',
        loading: '加载中…',
        loadingFailed: '加载失败',
        retry: '重试',
        trusted: 'Intertek 被 1000+ 全球企业信赖',
        methodologyTitle: 'Compliance Mapper 如何工作',
        methodologyDesc: '遵循三步流程，确保AI系统满足欧盟监管标准。',
        step1Title: '1. 适用范围判定',
        step1Desc: '根据投放市场与使用场景，判断AI系统是否适用欧盟AI法案。',
        step2Title: '2. 分类与角色',
        step2Desc: '识别提供者、部署者、进口商或分销商角色，明确法律责任。',
        step3Title: '3. 风险评估',
        step3Desc: '基于风险等级映射监管义务（不可接受/高/有限/最低）。',
        readyTitle: '准备确保合规？',
        readyDesc: '现在开始初步评估，获得清晰的AI治理路线。',
        startNow: '立即开始',
        disclaimer:
          '本工具依据欧盟法规 (EU) 2024/1689（人工智能法案），基于用户提供的信息自动生成评估结果。该结果仅供参考，不构成任何法律意见或专业建议。Intertek 不对评估结果的准确性或完整性提供保证，亦不承担相关法律责任。最终分类结果请务必经由专家复核。使用本工具不构成双方任何形式的合同关系。',
        privacy: '隐私政策',
        legal: '法律免责声明',
        terms: '服务条款',
        cookie: 'Cookie 政策',
        rights: '© 2024 COMPLIANCE MAPPER. 保留所有权利。',
        langEn: 'EN',
        langZh: '中文',
        errorBackend: '后端未启动或不可达（127.0.0.1:8000）',
        errorHttp: '后端接口返回异常',
      }
    : {
        navHome: 'Home',
        navHelp: 'Help',
        navStart: 'Start Assessment',
        heroTitle: 'EU AI Act',
        heroSubtitle: 'Compliance Mapper',
        heroDesc:
          'Determine your regulatory obligations with precision. The authoritative tool for technical and legal teams navigating the complexities of the European AI Act.',
        startAssessment: 'Start Assessment',
        readMethodology: 'Read Methodology',
        loading: 'Loading…',
        loadingFailed: 'Loading Failed',
        retry: 'Retry',
        trusted: 'Intertek is trusted by 1000+ global enterprises',
        methodologyTitle: 'How the Compliance Mapper Works',
        methodologyDesc: 'Follow our systematic three-step process to ensure your AI systems meet strict EU regulatory standards.',
        step1Title: '1. Scope Determination',
        step1Desc:
          'Identify if your AI system falls under the jurisdiction of the EU AI Act based on its market placement and usage.',
        step2Title: '2. Classification & Role',
        step2Desc:
          'Determine if you act as a Provider, Deployer, Importer or Distributor to clarify your specific legal liabilities.',
        step3Title: '3. Risk Assessment',
        step3Desc: "Map specific regulatory obligations based on your system's risk tier (Unacceptable, High, Limited, or Minimal).",
        readyTitle: 'Ready to ensure compliance?',
        readyDesc: 'Start your preliminary assessment today and get a clear roadmap for your AI governance strategy.',
        startNow: 'Start Assessment Now',
        disclaimer:"The EU AI Act Compliance Mapper provides automated, general guidance based on user inputs and Regulation (EU) 2024/1689. This tool is for informational purposes only and does not constitute legal advice. Intertek expressly disclaims all liability and warranties regarding the accuracy or completeness of the results. The final classification remains the sole responsibility of the user and must be verified by a qualified expert. Use of this tool does not establish a contractual relationship.",
        privacy: 'Privacy Policy',
        legal: 'Legal Disclaimers',
        terms: 'Terms of Service',
        cookie: 'Cookie Policy',
        rights: '© 2024 COMPLIANCE MAPPER. ALL RIGHTS RESERVED.',
        langEn: 'EN',
        langZh: 'ZH',
        errorBackend: 'Backend not running or unreachable (127.0.0.1:8000).',
        errorHttp: 'Backend API error.',
      },
)

const friendlyError = computed(() => {
  const raw = store.error ?? ''
  const lower = raw.toLowerCase()
  if (lower.includes('failed to fetch') || lower.includes('init_failed')) {
    return ui.value.errorBackend
  }
  if (lower.includes('init_http_') || lower.includes('module_http_') || lower.includes('submit_http_')) {
    return ui.value.errorHttp
  }
  return raw
})

async function start() {
  store.reset()
  const module = await store.init()
  if (!module) return
  await router.push({ name: 'module', params: { id: module.id } })
}

async function retry() {
  await store.init()
}

function scrollToSection(sectionId: string) {
  const el = document.getElementById(sectionId)
  if (!el) return
  el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function goHome() {
  scrollToSection('top')
}
</script>

<template>
  <div id="top" class="font-sans antialiased text-[#111111] bg-white">
    <NavBar
      :home-label="ui.navHome"
      :help-label="ui.navHelp"
      :action-label="ui.navStart"
      :action-disabled="store.loading"
      :help-href="helpCenterUrl"
      @home="goHome"
      @action="start"
    />
    <section class="bg-white pt-32 pb-24 text-center relative overflow-hidden">
      <div class="container mx-auto px-6 lg:px-12 flex flex-col items-center max-w-4xl">
        <h1 class="font-serif text-5xl md:text-7xl tracking-tight text-[#111111] mb-6 font-bold">
          {{ ui.heroTitle }} <br />
          <span class="font-serif italic md:not-italic text-[#111111]">{{ ui.heroSubtitle }}</span>
        </h1>
        <p class="text-lg text-[#4B5563] max-w-2xl mx-auto mb-10 font-light leading-relaxed">
          {{ ui.heroDesc }}
        </p>
        <div class="flex flex-col sm:flex-row items-center gap-4 mb-6">
          <button
            type="button"
            class="bg-[#FFCC00] hover:bg-[#E6B800] text-[#111111] font-bold px-10 py-4 rounded-md text-base min-w-[200px] shadow-sm transition-all"
            :disabled="store.loading"
            @click="start"
          >
            {{ ui.startAssessment }}
          </button>
          <button
            type="button"
            class="bg-transparent border border-[#111111] hover:bg-[#111111] hover:text-white text-[#111111] font-semibold px-10 py-4 rounded-md text-base transition-all min-w-[200px]"
            @click="scrollToSection('methodology')"
          >
            {{ ui.readMethodology }}
          </button>
        </div>
        <div v-if="store.loading" class="text-sm text-[#4B5563]">{{ ui.loading }}</div>
        <div v-else-if="store.error" class="text-sm text-red-600">
          {{ ui.loadingFailed }} {{ friendlyError }}
          <button type="button" class="ml-3 underline" @click="retry">{{ ui.retry }}</button>
        </div>
        <div class="flex items-center gap-3 justify-center mt-10">
          <a href="https://www.intertek.com/">
            <img
              alt="Trusted by legal teams"
              class="h-8 w-auto rounded-full"
              src="@/assets/images/logo/673b5ff37cae4f8b28a83e0f972bcc37.png"
            />
          </a>
          <span class="text-sm font-medium text-[#4B5563]">{{ ui.trusted }}</span>
        </div>
      </div>
    </section>
    <section id="about" class="bg-[#F3F4F6] py-24">
      <div id="methodology" class="container mx-auto px-6 lg:px-12">
        <div class="text-center mb-16 max-w-2xl mx-auto">
          <h2 class="font-serif text-[2.5rem] text-[#111111] font-bold mb-6">{{ ui.methodologyTitle }}</h2>
          <p class="text-[#4B5563] text-lg">{{ ui.methodologyDesc }}</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white p-10 rounded-xl shadow-[0_4px_20px_rgba(0,0,0,0.05)] flex flex-col items-start h-full border border-transparent hover:border-[#FFCC00] transition-all">
            <img
              alt="Scope Icon"
              class="w-14 h-14 mb-8"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuCKiTwD4KPSOluy1GRrSZZiiVXg5Kj9kWwBlimAPtw0zhkvexu54x71CBCP2SIeb0sSlgw4C_lkqifcJ3evH_Qeu-FDmeNO5VZIHzhCjhsz6UWMepMbmSeiLbFzXfDSL3AGc4FJGnBZvyFcczJzzl4CUE2bfNk250TPI4yC5jxVgrm4o9vR7aYzhw7nzYMrHlMDG3F7xS-onzAaV9cBzNWnpL6lsVFwYDjHiD_Pmp6xTz4t2pcGWUVJXhPYiGnthh3k5pViQWB70sk"
            />
            <h3 class="font-bold text-xl text-[#111111] mb-4 uppercase tracking-tight">{{ ui.step1Title }}</h3>
            <p class="text-[#4B5563] leading-relaxed text-sm">{{ ui.step1Desc }}</p>
          </div>
          <div class="bg-white p-10 rounded-xl shadow-[0_4px_20px_rgba(0,0,0,0.05)] flex flex-col items-start h-full border border-transparent hover:border-[#FFCC00] transition-all">
            <img
              alt="Classification Icon"
              class="w-14 h-14 mb-8"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuB2z99oufElXo6X7S4-fNI71GvTWiPn1P3sMT1ZGlK7NZ2ML14G4AiMJCXd-nP3dpj3MZNGjKQrCQmEygyAPAYHo7YVfYG8IZMwRZYgqtqJU0FF-60OIV4HGvRTUM4EGhZPrl07xF12z-fr85wDWJ2AsIsQm8R8F7RqdOPdOQBTIZ78dc8iXcAD4-yOIK_QcdTnh1GBYblL7N6O_YiNP37IJFDhOjf8Ty_UL3tEMaWLCB7b64EeYF1nw8Cw2hY4xPn3SXaUD4B5sic"
            />
            <h3 class="font-bold text-xl text-[#111111] mb-4 uppercase tracking-tight">{{ ui.step2Title }}</h3>
            <p class="text-[#4B5563] leading-relaxed text-sm">{{ ui.step2Desc }}</p>
          </div>
          <div class="bg-white p-10 rounded-xl shadow-[0_4px_20px_rgba(0,0,0,0.05)] flex flex-col items-start h-full border border-transparent hover:border-[#FFCC00] transition-all">
            <img
              alt="Risk Icon"
              class="w-14 h-14 mb-8"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuBrtr_s1hfjWS33AgJQBMeRUhd0DVtE6WcGq5DMlyCfVoGsG0ZjFDKWD7JwtzKsqtQj5RveYzrI5yJtwtUoVztsNndEYV87cSddpDO7iKM4lwqMreiomg7i3chn3tfzkvPu7BVep0FPgXxDGcAyMRgNFV70W7vYROghDqDwsnfuRsHoh-KRPyOaEMcqCwVuaNUo56p_iiNq19gBdDN-H0qHcaI25kxvDcI8OTeH3Kp1xnRi16SVkcn-wmtAxUnCJpVk84OdawQzQMA"
            />
            <h3 class="font-bold text-xl text-[#111111] mb-4 uppercase tracking-tight">{{ ui.step3Title }}</h3>
            <p class="text-[#4B5563] leading-relaxed text-sm">{{ ui.step3Desc }}</p>
          </div>
        </div>
      </div>
    </section>
    <section class="bg-white py-24 text-center">
      <div class="container mx-auto px-6">
        <div class="w-20 h-20 mx-auto mb-8 bg-[#F3F4F6] rounded-full flex items-center justify-center">
          <img
            alt="Checklist Icon"
            class="w-10 h-10"
            src="@/assets/images/logo/AISquareimage.png"
          />
        </div>
        <h2 class="font-serif text-[2.5rem] text-[#111111] font-bold mb-4">{{ ui.readyTitle }}</h2>
        <p class="text-[#4B5563] text-lg max-w-2xl mx-auto mb-10">{{ ui.readyDesc }}</p>
        <button
          type="button"
          class="bg-[#FFCC00] hover:bg-[#E6B800] text-[#111111] font-bold px-10 py-4 rounded-md text-lg inline-block shadow-md transition-all"
          :disabled="store.loading"
          @click="start"
        >
          {{ ui.startNow }}
        </button>
      </div>
    </section>
    <section class="bg-white pt-8 pb-12">
      <div class="container mx-auto px-6 lg:px-12">
        <div class="bg-[#F9FAFB] p-8 rounded-lg border border-[#E5E7EB] w-full max-w-6xl mx-auto">
          <p class="text-xs text-[#4B5563] leading-relaxed text-center">{{ ui.disclaimer }}</p>
        </div>
      </div>
    </section>
    <footer id="contact" class="bg-white py-12 border-t border-[#E5E7EB]">
      <div class="container mx-auto px-6 lg:px-12 flex flex-col md:flex-row items-center justify-between gap-8">
        <div class="flex items-center gap-3">

        </div>
        <div class="flex flex-wrap justify-center gap-10 text-xs font-semibold uppercase tracking-widest text-[#4B5563]">
          <a class="hover:text-[#111111] transition-colors" href="https://www.intertek.com/privacy/">{{ ui.privacy }}</a>
          <a class="hover:text-[#111111] transition-colors" href="https://www.intertek.com/disclaimer/">
            {{ ui.legal }}
          </a>
          <a class="hover:text-[#111111] transition-colors" href="https://www.intertek.com/terms/">{{ ui.terms }}</a>
          <a class="hover:text-[#111111] transition-colors" href="https://www.intertek.com/cookie-policy/">{{ ui.cookie }}</a>
        </div>
        <div class="text-xs text-[#4B5563] font-medium">{{ ui.rights }}</div>
      </div>
    </footer>
  </div>
</template>
