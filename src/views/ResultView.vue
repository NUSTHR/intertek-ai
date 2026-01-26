<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionnaireStore } from '@/stores/questionnaire'
import logoUrl from '@/assets/images/logo/b9d2336ed590ab1e2a8d517d7f555f72.png'
import portraitUrl from '@/assets/images/self-portrait/03ada209733101dff56722826aeaa67f.png'

const router = useRouter()
const store = useQuestionnaireStore()

const conclusion = computed(() => store.conclusion ?? {})
const summaryRows = computed(() => {
  const role = conclusion.value.Role ?? store.parameters.Role ?? ''
  const type = conclusion.value.Type ?? store.parameters.Type ?? ''
  const riskLevel = conclusion.value.Risk_level ?? store.parameters.Risk_level ?? ''
  return [
    { label: 'Role', value: role },
    { label: 'Type', value: type },
    { label: 'Risk_level', value: riskLevel },
  ]
})
const riskLevel = computed(() => conclusion.value.Risk_level ?? store.parameters.Risk_level ?? '')
const statusTitle = computed(() => {
  const raw = String(riskLevel.value ?? '').trim()
  if (!raw) return 'Out of Regulation'
  const lower = raw.toLowerCase()
  if (lower.includes('out of regulation') || lower.includes('outside')) return 'Out of Regulation'
  if (lower.includes('high')) return 'High Risk'
  if (lower.includes('limited')) return 'Limited Risk'
  if (lower.includes('minimal')) return 'Minimal Risk'
  return raw
})
const statusSubtitle = computed(() => {
  if (riskLevel.value) return `Regulatory Classification: ${riskLevel.value}`
  return 'Exclusion Confirmed'
})
onMounted(async () => {
  if (!store.sessionId) {
    await router.replace({ name: 'start' })
    return
  }
  await store.fetchResult()
})

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
    <header class="max-w-7xl mx-auto px-8 py-10 flex justify-between items-center border-b border-gray-100 w-full">
      <div class="flex items-center gap-3">
        <img alt="Intertek AI² Logo" class="w-8 h-8 rounded-md" :src="logoUrl" />
        <span class="text-3xl font-black tracking-tighter uppercase italic leading-none">Intertek AI²</span>
      </div>
      <div class="flex items-center gap-8">
        <nav class="flex items-center gap-6">
          <button
            type="button"
            class="flex items-center gap-2 text-sm font-bold hover:text-[#FAD400] transition-colors group"
            @click="goHome"
          >
            <span class="material-symbols-outlined text-2xl group-hover:scale-110 transition-transform">home</span>
            <span class="uppercase tracking-widest text-[10px]">Home</span>
          </button>
          <a
            class="flex items-center gap-2 text-sm font-bold hover:text-[#FAD400] transition-colors group"
            href="https://www.intertek.com/help/"
          >
            <span class="material-symbols-outlined text-2xl group-hover:scale-110 transition-transform">help_center</span>
            <span class="uppercase tracking-widest text-[10px]">Help Center</span>
          </a>
        </nav>
        <span class="text-[10px] font-black tracking-widest uppercase text-gray-400">Compliance Mapper v2.4</span>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-8 pt-20 pb-32 flex-grow w-full">
      <section class="mb-24">
        <div class="flex flex-col items-start gap-6 mb-12">
          <div class="flex items-center gap-3">
            <span class="h-px w-8 bg-[#FAD400]"></span>
            <span class="text-xs font-black tracking-[0.3em] uppercase text-gray-500">Assessment Complete</span>
          </div>
          <h1 class="text-2xl font-light max-w-2xl leading-relaxed text-gray-600">
            Based on the EU AI Act framework and your technical inputs, your system has been categorized for regulatory
            handling.
          </h1>
          <div v-if="store.error" class="text-sm text-red-600">{{ store.error }}</div>
          <div v-else-if="summaryRows.length === 0" class="text-sm text-gray-500">Loading…</div>
        </div>
        <div class="relative py-4">
          <span class="block text-xs font-black tracking-[0.5em] mb-6 text-[#FAD400] uppercase">Regulatory Status</span>
          <h2 class="text-[clamp(3rem,9vw,10rem)] leading-[0.9] font-black tracking-tighter uppercase mb-4 break-words">
            {{ statusTitle.split(' ').slice(0, 2).join(' ') }}
            <br class="hidden md:block" />
            {{ statusTitle.split(' ').slice(2).join(' ') }}<span class="text-[#FAD400]">.</span>
          </h2>
          <div class="flex items-center gap-4">
            <div class="h-2 bg-black w-32"></div>
            <span class="text-xs font-bold tracking-widest uppercase opacity-40">{{ statusSubtitle }}</span>
          </div>
        </div>
      </section>
      <section
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-16 mb-32 border-t border-gray-100 pt-16"
      >
        <div class="space-y-4">
          <h3 class="font-black text-sm uppercase tracking-widest border-l-4 border-[#FAD400] pl-4">
            System Profile<br /><span class="text-gray-400">Role</span>
          </h3>
          <p class="text-xl font-bold leading-relaxed text-black">{{ summaryRows[0]?.value || 'Unspecified' }}</p>
          <p class="text-sm text-gray-500">
            Entity role classification derived from your responses for this system context.
          </p>
        </div>
        <div class="space-y-4">
          <h3 class="font-black text-sm uppercase tracking-widest border-l-4 border-[#FAD400] pl-4">
            System Profile<br /><span class="text-gray-400">Product Type</span>
          </h3>
          <p class="text-xl font-bold leading-relaxed text-black">{{ summaryRows[1]?.value || 'Unspecified' }}</p>
          <p class="text-sm text-gray-500">
            Product type classification based on the module inputs provided during assessment.
          </p>
        </div>
        <div class="space-y-4">
          <h3 class="font-black text-sm uppercase tracking-widest border-l-4 border-[#FAD400] pl-4">
            Suggestion<br /><span class="text-gray-400">Compliance Mapper's View</span>
          </h3>
           <p class="text-xl font-bold leading-relaxed text-black">For reference</p>
          <p class="text-sm text-gray-500">
            {{ conclusion?.View || '' }}
          </p>
        </div>
      </section>
      <section
        class="bg-white border border-gray-100 rounded-[2.5rem] p-8 md:p-12 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.08)] flex flex-col lg:flex-row items-center gap-16 relative overflow-hidden"
      >
        <div class="flex-1 space-y-10 z-10">
          <div class="space-y-4">
            <span class="inline-block px-4 py-1 bg-gray-100 text-gray-600 text-[10px] font-black tracking-widest uppercase rounded-full">
              Optional Verification
            </span>
            <h3 class="text-4xl md:text-5xl font-black tracking-tight leading-tight">
              Validate Your <br /><span class="relative inline-block before:content-[''] before:absolute before:-bottom-1 before:left-0 before:w-full before:h-2 before:bg-[#FAD400] before:-z-10">Exclusion</span>
            </h3>
            <p class="text-gray-500 text-lg max-w-md">
              While your system appears unregulated, boundaries can be complex. Documentation of exclusion logic is
              recommended.
            </p>
          </div>
          <div class="flex flex-wrap gap-4">
            <button
              type="button"
              class="px-10 py-5 bg-black text-white text-sm font-black uppercase tracking-widest rounded-xl hover:bg-[#FAD400] hover:text-black transition-all flex items-center gap-3"
            >
              Book a Meeting
              <span class="material-symbols-outlined text-lg">calendar_today</span>
            </button>
            <button
              type="button"
              class="px-10 py-5 border border-gray-200 text-black text-sm font-black uppercase tracking-widest rounded-xl hover:border-black transition-colors"
            >
              Download Memo
            </button>
          </div>
        </div>
        <div class="flex-1 flex justify-center lg:justify-end">
          <div class="relative w-full max-w-md bg-white rounded-3xl p-6 border border-gray-100 shadow-xl shadow-gray-100/50">
            <div class="flex flex-col md:flex-row gap-8 items-center">
              <img
                alt="Dr. Elena Rossi, AI Regulatory Specialist"
                class="w-32 h-32 md:w-48 md:h-64 object-cover rounded-2xl shadow-sm grayscale hover:grayscale-0 transition-all duration-500"
                :src="portraitUrl"
              />
              <div class="space-y-3 text-center md:text-left">
                <h4 class="text-2xl font-black leading-tight tracking-tight">Dr. Elena Rossi</h4>
                <p class="text-[#FAD400] font-black text-[10px] tracking-[0.2em] uppercase">EU AI Regulatory Specialist</p>
                <p class="text-gray-500 font-medium text-sm leading-relaxed">
                  Expert in regulatory scope definition, Article 2 exclusions, and compliance strategy.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="mt-40 flex flex-col items-center gap-10 text-center">
        <div class="h-12 w-px bg-gray-200"></div>
        <div class="space-y-3">
          <h2 class="text-2xl font-black uppercase tracking-tight">Evaluate Another System?</h2>
          <p class="text-gray-400 font-medium max-w-sm">
            Clear all current session data and restart the regulatory mapping questionnaire.
          </p>
        </div>
        <button
          type="button"
          class="group flex items-center gap-4 px-10 py-5 bg-[#FAD400] text-black rounded-full font-black text-sm uppercase tracking-widest hover:bg-black hover:text-white transition-all duration-300"
          @click="restart"
        >
          <span class="material-symbols-outlined group-hover:rotate-180 transition-transform duration-700">refresh</span>
          Restart Questionnaire
        </button>
        <div class="w-full max-w-6xl">
          <div class="bg-[#F9FAFB] p-8 rounded-lg border border-[#E5E7EB] w-full">
            <p class="text-xs text-[#4B5563] leading-relaxed text-center">
              The EU AI ACT Compliance Mapper provides automated evaluations for general guidance based on user input.
              It is not legal advice. Intertek disclaims all liability and warranties regarding the accuracy or
              completeness of results. Users are responsible for final classification, which must be verified by expert
              evaluation. Use of this tool creates no contractual relationship. Based on EU Regulation 2024/1689 (July
              2024).
            </p>
          </div>
        </div>
      </section>
    </main>
    <footer class="max-w-7xl mx-auto px-8 py-16 border-t border-gray-100 flex flex-col md:flex-row justify-between items-center gap-8 w-full">
      <div class="flex items-center gap-6">
        <img alt="Intertek AI² Logo" class="w-8 h-8 rounded-md" :src="logoUrl" />
        <span class="text-xl font-black uppercase italic tracking-tighter">Intertek AI²</span>
        <span class="w-px h-4 bg-gray-200"></span>
        <span class="text-gray-400 text-[10px] font-bold tracking-widest">© 2024 COMPLIANCE MAPPER</span>
      </div>
      <div class="flex gap-10 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">
        <a class="hover:text-black transition-colors" href="https://www.intertek.com/privacy/">Privacy Policy</a>
        <a class="hover:text-black transition-colors" href="https://www.intertek.com/terms/">Terms of Service</a>
        <a class="hover:text-black transition-colors" href="https://www.intertek.com/contact/">Support</a>
      </div>
    </footer>
  </div>
</template>
