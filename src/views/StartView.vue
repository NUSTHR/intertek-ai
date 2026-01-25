<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'
import logoUrl from '@/assets/images/logo/b9d2336ed590ab1e2a8d517d7f555f72.png'

const router = useRouter()
const store = useQuestionnaireStore()

const friendlyError = computed(() => {
  const raw = store.error ?? ''
  const lower = raw.toLowerCase()
  if (lower.includes('failed to fetch') || lower.includes('init_failed')) {
    return '后端未启动或不可达（127.0.0.1:8000）'
  }
  if (lower.includes('init_http_') || lower.includes('module_http_') || lower.includes('submit_http_')) {
    return '后端接口返回异常'
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
</script>

<template>
  <div id="top" class="font-sans antialiased text-[#111111] bg-white">
    <header class="bg-white w-full py-6 border-b border-[#E5E7EB]">
      <div class="container mx-auto px-6 lg:px-12 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <img
            alt="Intertek AI² Logo"
            class="w-8 h-8 rounded-md"
            :src="logoUrl"
          />
          <span class="text-[#111111] font-bold text-lg tracking-wide uppercase">Intertek AI²</span>
        </div>
        <div class="hidden md:flex items-center gap-8">
          <nav class="flex items-center gap-6 text-sm font-medium text-[#111111]">
            <a class="flex items-center gap-2 font-bold hover:text-[#4B5563] transition-colors" href="#top">
              <span class="material-symbols-outlined text-xl">home</span>
              Home
            </a>
            <a class="flex items-center gap-2 font-bold hover:text-[#4B5563] transition-colors" href="https://www.intertek.com/help/">
              <span class="material-symbols-outlined text-xl">help_center</span>
              Help Center
            </a>
          </nav>
          <button
            type="button"
            class="bg-[#FFCC00] hover:bg-[#E6B800] text-[#111111] font-bold text-sm px-6 py-3 rounded-md transition-colors"
            :disabled="store.loading"
            @click="start"
          >
            Start Assessment
          </button>
        </div>
        <button type="button" class="md:hidden text-[#111111]">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
        </button>
      </div>
    </header>
    <section class="bg-white pt-32 pb-24 text-center relative overflow-hidden">
      <div class="container mx-auto px-6 lg:px-12 flex flex-col items-center max-w-4xl">
        <h1 class="font-serif text-5xl md:text-7xl tracking-tight text-[#111111] mb-6 font-bold">
          EU AI Act <br />
          <span class="font-serif italic md:not-italic text-[#111111]">Compliance Mapper</span>
        </h1>
        <p class="text-lg text-[#4B5563] max-w-2xl mx-auto mb-10 font-light leading-relaxed">
          Determine your regulatory obligations with precision. The authoritative tool for technical and legal teams
          navigating the complexities of the European AI Act.
        </p>
        <div class="flex flex-col sm:flex-row items-center gap-4 mb-6">
          <button
            type="button"
            class="bg-[#FFCC00] hover:bg-[#E6B800] text-[#111111] font-bold px-10 py-4 rounded-md text-base min-w-[200px] shadow-sm transition-all"
            :disabled="store.loading"
            @click="start"
          >
            Start Assessment
          </button>
          <button
            type="button"
            class="bg-transparent border border-[#111111] hover:bg-[#111111] hover:text-white text-[#111111] font-semibold px-10 py-4 rounded-md text-base transition-all min-w-[200px]"
            @click="scrollToSection('methodology')"
          >
            Read Methodology
          </button>
        </div>
        <div v-if="store.loading" class="text-sm text-[#4B5563]">Loading…</div>
        <div v-else-if="store.error" class="text-sm text-red-600">
          Loading Failed{{ friendlyError }}
          <button type="button" class="ml-3 underline" @click="retry">重试</button>
        </div>
        <div class="flex items-center gap-3 justify-center mt-10">
          <img
            alt="Trusted by legal teams"
            class="h-8 w-auto rounded-full grayscale"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3blJImmlOBw_Wm0MwN_hqL23N_wYdQkAYyYlDXYVksY0YLKXfNgI5Lg-IQIYlymKTn8hd0xLrypR2yIDvgzhN94KpreaXmTh3ExRpMsrOcfx1VCU4nk66Unkdgef9sYQMIItgUW_iMayh_xEI3NlIHf0CyqiXjhK-c5M6nmB9ZDIJNKdhRcjCQ55KAcFUnnnBLopv6QWG8T0DqHx0HcDgB98fQloxD74vrPDKqaRaHhqt3yoJAB3UVtdC59NHPqm4CEyO9zzd3n4"
          />
          <span class="text-sm font-medium text-[#4B5563]">Intertek is trusted by 1000+ global enterprises</span>
        </div>
      </div>
    </section>
    <section id="about" class="bg-[#F3F4F6] py-24">
      <div id="methodology" class="container mx-auto px-6 lg:px-12">
        <div class="text-center mb-16 max-w-2xl mx-auto">
          <h2 class="font-serif text-[2.5rem] text-[#111111] font-bold mb-6">How the Compliance Mapper Works</h2>
          <p class="text-[#4B5563] text-lg">
            Follow our systematic three-step process to ensure your AI systems meet strict EU regulatory standards.
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white p-10 rounded-xl shadow-[0_4px_20px_rgba(0,0,0,0.05)] flex flex-col items-start h-full border border-transparent hover:border-[#FFCC00] transition-all">
            <img
              alt="Scope Icon"
              class="w-14 h-14 mb-8"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuCKiTwD4KPSOluy1GRrSZZiiVXg5Kj9kWwBlimAPtw0zhkvexu54x71CBCP2SIeb0sSlgw4C_lkqifcJ3evH_Qeu-FDmeNO5VZIHzhCjhsz6UWMepMbmSeiLbFzXfDSL3AGc4FJGnBZvyFcczJzzl4CUE2bfNk250TPI4yC5jxVgrm4o9vR7aYzhw7nzYMrHlMDG3F7xS-onzAaV9cBzNWnpL6lsVFwYDjHiD_Pmp6xTz4t2pcGWUVJXhPYiGnthh3k5pViQWB70sk"
            />
            <h3 class="font-bold text-xl text-[#111111] mb-4 uppercase tracking-tight">1. Scope Determination</h3>
            <p class="text-[#4B5563] leading-relaxed text-sm">
              Identify if your AI system falls under the jurisdiction of the EU AI Act based on its market placement
              and usage.
            </p>
          </div>
          <div class="bg-white p-10 rounded-xl shadow-[0_4px_20px_rgba(0,0,0,0.05)] flex flex-col items-start h-full border border-transparent hover:border-[#FFCC00] transition-all">
            <img
              alt="Classification Icon"
              class="w-14 h-14 mb-8"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuB2z99oufElXo6X7S4-fNI71GvTWiPn1P3sMT1ZGlK7NZ2ML14G4AiMJCXd-nP3dpj3MZNGjKQrCQmEygyAPAYHo7YVfYG8IZMwRZYgqtqJU0FF-60OIV4HGvRTUM4EGhZPrl07xF12z-fr85wDWJ2AsIsQm8R8F7RqdOPdOQBTIZ78dc8iXcAD4-yOIK_QcdTnh1GBYblL7N6O_YiNP37IJFDhOjf8Ty_UL3tEMaWLCB7b64EeYF1nw8Cw2hY4xPn3SXaUD4B5sic"
            />
            <h3 class="font-bold text-xl text-[#111111] mb-4 uppercase tracking-tight">2. Classification & Role</h3>
            <p class="text-[#4B5563] leading-relaxed text-sm">
              Determine if you act as a Provider, Deployer, Importer or Distributor to clarify your specific legal
              liabilities.
            </p>
          </div>
          <div class="bg-white p-10 rounded-xl shadow-[0_4px_20px_rgba(0,0,0,0.05)] flex flex-col items-start h-full border border-transparent hover:border-[#FFCC00] transition-all">
            <img
              alt="Risk Icon"
              class="w-14 h-14 mb-8"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuBrtr_s1hfjWS33AgJQBMeRUhd0DVtE6WcGq5DMlyCfVoGsG0ZjFDKWD7JwtzKsqtQj5RveYzrI5yJtwtUoVztsNndEYV87cSddpDO7iKM4lwqMreiomg7i3chn3tfzkvPu7BVep0FPgXxDGcAyMRgNFV70W7vYROghDqDwsnfuRsHoh-KRPyOaEMcqCwVuaNUo56p_iiNq19gBdDN-H0qHcaI25kxvDcI8OTeH3Kp1xnRi16SVkcn-wmtAxUnCJpVk84OdawQzQMA"
            />
            <h3 class="font-bold text-xl text-[#111111] mb-4 uppercase tracking-tight">3. Risk Assessment</h3>
            <p class="text-[#4B5563] leading-relaxed text-sm">
              Map specific regulatory obligations based on your system's risk tier (Unacceptable, High, Limited, or
              Minimal).
            </p>
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
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuBdLzTHBR-w4pTfm2InE0qABKZOfeUh3qpSNAbGFr5PH1bY7GbDhnTfXDM_2a0hf84Sg7EjtREmJlsDzLlQVgSokM4bAxjUmnIM3ynbYBOfzgoWpf5EBgCJ9u1CyIKXUPOMHpxQglnhQUfNOFiQk8Y9CDd8Ckad3qcMcMBONCXFlilsEFghyPJxtyf8ZWr_UjcGSyb0qwKdG9GHTlJcsbd3ef2umy2mTS2We9lEOXgObBPxy0C4Pp8GtCGvJpdnCJ37pMFlfq3vyUg"
          />
        </div>
        <h2 class="font-serif text-[2.5rem] text-[#111111] font-bold mb-4">Ready to ensure compliance?</h2>
        <p class="text-[#4B5563] text-lg max-w-2xl mx-auto mb-10">
          Start your preliminary assessment today and get a clear roadmap for your AI governance strategy.
        </p>
        <button
          type="button"
          class="bg-[#FFCC00] hover:bg-[#E6B800] text-[#111111] font-bold px-10 py-4 rounded-md text-lg inline-block shadow-md transition-all"
          :disabled="store.loading"
          @click="start"
        >
          Start Assessment Now
        </button>
      </div>
    </section>
    <section class="bg-white pt-8 pb-12">
      <div class="container mx-auto px-6 lg:px-12">
        <div class="bg-[#F9FAFB] p-8 rounded-lg border border-[#E5E7EB] w-full max-w-6xl mx-auto">
          <p class="text-xs text-[#4B5563] leading-relaxed text-center">
            The EU AI ACT Compliance Mapper provides automated evaluations for general guidance based on user input. It
            is not legal advice. Intertek disclaims all liability and warranties regarding the accuracy or completeness
            of results. Users are responsible for final classification, which must be verified by expert evaluation.
            Use of this tool creates no contractual relationship. Based on EU Regulation 2024/1689 (July 2024).
          </p>
        </div>
      </div>
    </section>
    <footer id="contact" class="bg-white py-12 border-t border-[#E5E7EB]">
      <div class="container mx-auto px-6 lg:px-12 flex flex-col md:flex-row items-center justify-between gap-8">
        <div class="flex items-center gap-3">
          <img
            alt="Compliance Mapper Logo"
            class="w-8 h-8 rounded-md"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDJQkfX8__-vf6rmrZyDztGJ217awHv7KHQ9hL1cz7NKnWe-hKVU3sieSrtMU9tGLWb5y-c11Kvson0CeKQguDZkM5sJrSkw1l5Fb4z93OOu-uLbLjWYK2lazw6x3OHFiL_E3A9an-rYVE6DnVkDysbr09F5OE4gJL-9QH84kMesk6k_QApRVuTkVPF1vmslFatgi-6Bw_uXAWg0kAl7XAn_KVD7Ak4ZrkNhWtxSFQE5u8a9H6x4SlWA9GrmWhAWkHWqL07nFOv75Y"
          />
          <span class="text-[#111111] font-bold text-sm uppercase tracking-wider">Compliance Mapper</span>
        </div>
        <div class="flex flex-wrap justify-center gap-10 text-xs font-semibold uppercase tracking-widest text-[#4B5563]">
          <a class="hover:text-[#111111] transition-colors" href="https://www.intertek.com/privacy/">Privacy Policy</a>
          <a class="hover:text-[#111111] transition-colors" href="https://www.intertek.com/disclaimer/">
            Legal Disclaimers
          </a>
          <a class="hover:text-[#111111] transition-colors" href="https://www.intertek.com/terms/">
            Terms of Service
          </a>
        </div>
        <div class="text-xs text-[#4B5563] font-medium">© 2024 COMPLIANCE MAPPER. ALL RIGHTS RESERVED.</div>
      </div>
    </footer>
  </div>
</template>
