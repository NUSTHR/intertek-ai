<script setup lang="ts">
import { computed, inject, type ComputedRef } from 'vue'
import logoUrl from '@/assets/images/logo/b9d2336ed590ab1e2a8d517d7f555f72.png'
import { useLocaleStore } from '@/stores/locale'

const props = withDefaults(defineProps<{
  moduleLabel: string
  moduleTitle: string
  moduleDescription?: string
  stepLabel?: string
  stepTotal?: string
  progressWidth?: string
  questionTag: string
  questionText: string
  questionDescription?: string
  error: string | null
  message: string | null
  disableNext: boolean
}>(), {
  stepLabel: '',
  stepTotal: '',
  progressWidth: '',
})

const emit = defineEmits<{
  (e: 'restart'): void
  (e: 'prev'): void
  (e: 'next'): void
}>()

const prevHandler = inject<(() => void) | null>('questionnaire_prev_handler', null)
const progressOverride = inject<ComputedRef<{ stepLabel: string; stepTotal: string; progressWidth: string } | null> | null>(
  'progressOverride',
  null,
)
const stepLabelText = computed(() => progressOverride?.value?.stepLabel ?? '')
const stepTotalText = computed(() => progressOverride?.value?.stepTotal ?? '')
const progressWidthText = computed(() => progressOverride?.value?.progressWidth ?? '')
const locale = useLocaleStore()
const helpCenterUrl = 'https://www.intertekinform.com/en-au/contact-us/'
const ui = computed(() =>
  locale.isZh
    ? {
        home: '首页',
        restart: '重新开始',
        helpCenter: '帮助中心',
        previous: '上一题',
        next: '下一题',
        loadingFailed: '加载失败',
        privacy: '隐私政策',
        terms: '服务条款',
        disclaimer: '合规免责声明',
        contact: '联系支持',
        langEn: 'EN',
        langZh: '中文',
      }
    : {
        home: 'Home',
        restart: 'Restart',
        helpCenter: 'Help',
        previous: 'Previous',
        next: 'Next Question',
        loadingFailed: 'Loading Failed',
        privacy: 'Privacy',
        terms: 'Terms',
        disclaimer: 'Compliance Disclaimer',
        contact: 'Contact Support',
        langEn: 'EN',
        langZh: 'ZH',
      },
)

function onPrev() {
  if (prevHandler) {
    prevHandler()
    return
  }
  emit('prev')
}
</script>

<template>
  <section class="bg-[#f3f4f6] dark:bg-background-dark font-display text-slate-900 dark:text-white min-h-screen flex flex-col intertek-scope">
    <div class="header-accent w-full"></div>
    <header class="flex items-center justify-between md:whitespace-nowrap bg-white dark:bg-slate-900 px-4 md:px-6 py-3 md:py-4 sticky top-0 z-50 shadow-sm">
      <div class="flex items-center gap-6">
        <div class="flex items-center gap-3">
          <a href="https://www.intertek.com/">
            <img alt="Intertek AI² Logo" class="w-8 h-8 rounded-md" :src="logoUrl" />
          </a>
          <h2 class="text-slate-900 dark:text-white text-sm font-extrabold leading-tight tracking-tight uppercase">
            Intertek AI²
          </h2>
        </div>
      </div>
      <div class="flex items-center gap-8">
        <div class="flex items-center bg-slate-100 dark:bg-slate-800 p-0.5 rounded-sm">
          <button
            type="button"
            class="px-3 py-1 text-[10px] font-black shadow-sm"
            :class="locale.isZh ? 'text-slate-400 dark:text-slate-500' : 'bg-white dark:bg-slate-700 text-intertek-dark'"
            @click="locale.setLang('en')"
          >
            {{ ui.langEn }}
          </button>
          <button
            type="button"
            class="px-3 py-1 text-[10px] font-black shadow-sm"
            :class="locale.isZh ? 'bg-white dark:bg-slate-700 text-intertek-dark' : 'text-slate-400 dark:text-slate-500'"
            @click="locale.setLang('zh')"
          >
            {{ ui.langZh }}
          </button>
        </div>
        <div class="flex items-center gap-6">
          <a
            class="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-slate-600 dark:text-slate-400 hover:text-intertek-dark transition-colors"
            href="/"
          >
            <span class="material-symbols-outlined text-lg">home</span>
            <span class="hidden lg:block">{{ ui.home }}</span>
          </a>
          <button
            type="button"
            class="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-slate-600 dark:text-slate-400 hover:text-intertek-dark transition-colors"
            @click="emit('restart')"
          >
            <span class="material-symbols-outlined text-lg">refresh</span>
            <span class="hidden lg:block">{{ ui.restart }}</span>
          </button>
          <a
            class="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-slate-600 dark:text-slate-400 hover:text-intertek-dark transition-colors"
            :href="helpCenterUrl"
          >
            <span class="material-symbols-outlined text-lg">help_center</span>
            <span class="hidden lg:block">{{ ui.helpCenter }}</span>
          </a>
          <div class="h-6 w-px bg-slate-200 dark:bg-slate-700"></div>
        </div>
      </div>
    </header>
    <main class="flex-1 w-full max-w-7xl mx-auto p-4 md:p-10 flex flex-col gap-6 md:gap-10">
      <section class="flex flex-col gap-5 bg-white dark:bg-slate-900 p-6 shadow-sm border border-slate-200 dark:border-slate-800">
        <div class="flex items-center justify-between">
          <div class="flex flex-col gap-1">
            <span class="text-intertek-yellow font-black uppercase tracking-[0.2em] text-[10px]">{{ props.moduleLabel }}</span>
            <h3 class="font-black text-slate-900 dark:text-white text-2xl uppercase italic">{{ props.moduleTitle }}</h3>
            <p v-if="props.moduleDescription" class="text-xs text-slate-500 dark:text-slate-400 font-medium">
              {{ props.moduleDescription }}
            </p>
          </div>
          <div class="text-right">
            <div class="flex items-baseline gap-1">
              <span class="font-black text-2xl text-slate-900 dark:text-white">{{ stepLabelText || props.stepLabel }}</span>
              <span class="text-slate-400 font-bold text-sm uppercase">{{ stepTotalText || props.stepTotal }}</span>
            </div>
          </div>
        </div>
        <div class="w-full bg-slate-100 dark:bg-slate-800 h-2">
          <div class="bg-intertek-yellow h-2 transition-all duration-700" :style="{ width: progressWidthText || props.progressWidth }"></div>
        </div>
      </section>
      <div class="flex flex-col lg:flex-row gap-10 items-start">
        <div class="flex-1 flex flex-col gap-6 md:gap-8 w-full">
          <div class="bg-white dark:bg-slate-900 p-5 md:p-12 shadow-sm border border-slate-200 dark:border-slate-800">
            <div class="mb-10">
              <span class="inline-block px-4 py-1.5 bg-intertek-dark text-white text-[10px] font-black tracking-[0.3em] uppercase mb-6">
                {{ props.questionTag }}
              </span>
              <h1 class="text-3xl md:text-4xl font-extrabold text-slate-900 dark:text-white leading-tight">
                {{ props.questionText }}
              </h1>
              <p v-if="props.questionDescription" class="text-sm text-slate-600 dark:text-slate-400 mt-3 leading-relaxed font-medium">
                {{ props.questionDescription }}
              </p>
            </div>
            <slot></slot>
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 pt-6 md:pt-10 mt-6 md:mt-10 border-t border-slate-100 dark:border-slate-800">
              <button
                type="button"
                class="flex items-center gap-2 px-6 md:px-8 py-3 md:py-4 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-200 font-black uppercase tracking-widest text-[11px] hover:bg-slate-50 dark:hover:bg-slate-800 transition-all"
                @click="onPrev"
              >
                <span class="material-symbols-outlined text-sm">west</span>
                {{ ui.previous }}
              </button>
              <button
                type="button"
                class="flex items-center gap-3 px-10 md:px-12 py-3 md:py-4 bg-intertek-yellow text-black font-black uppercase tracking-[0.2em] text-[11px] hover:bg-intertek-dark hover:text-white transition-all shadow-md active:translate-y-0.5"
                :disabled="props.disableNext"
                @click="emit('next')"
              >
                {{ ui.next }}
                <span class="material-symbols-outlined text-sm">east</span>
              </button>
            </div>
            <div v-if="props.error" class="text-sm text-red-600 mt-6">{{ ui.loadingFailed }} {{ props.error }}</div>
            <div v-if="props.message" class="text-xs text-slate-500 mt-2">{{ props.message }}</div>
          </div>
        </div>
        <aside class="w-full lg:w-[320px] flex-shrink-0">
          <div class="relative md:sticky md:top-28 flex flex-col gap-6">
            <slot name="sidebar"></slot>
            <slot name="tip"></slot>
          </div>
        </aside>
      </div>
    </main>
    <footer class="mt-auto py-10 px-8 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-center md:text-left">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex flex-col gap-2">
          <div class="bg-intertek-yellow inline-block px-2 py-0.5 text-black font-black italic tracking-tighter text-sm leading-none uppercase w-fit mx-auto md:mx-0">
            Intertek AI²
          </div>
          <p class="text-[10px] text-slate-400 font-bold uppercase tracking-[0.2em]">
            © 2024 Intertek Group plc. Total Quality. Assured.
          </p>
        </div>
        <div class="flex flex-wrap justify-center gap-8 text-[10px] text-slate-500 font-black uppercase tracking-widest">
          <a class="hover:text-intertek-dark transition-colors" href="https://www.intertek.com/privacy/">{{ ui.privacy }}</a>
          <a class="hover:text-intertek-dark transition-colors" href="https://www.intertek.com/terms/">{{ ui.terms }}</a>
          <a class="hover:text-intertek-dark transition-colors" href="https://www.intertek.com/disclaimer/">
            {{ ui.disclaimer }}
          </a>
          <a class="hover:text-intertek-dark transition-colors" href="https://www.intertek.com/contact/">
            {{ ui.contact }}
          </a>
        </div>
      </div>
    </footer>
  </section>
</template>

<style>
.option-card:hover {
  border-color: #FFC800;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.option-card.selected {
  border-color: #FFC800;
  background-color: #ffffff;
}

.header-accent {
  background: linear-gradient(to right, #FFC800 0%, #FFC800 100%);
  height: 4px;
}

.intertek-scope .rounded,
.intertek-scope .rounded-lg,
.intertek-scope .rounded-xl {
  border-radius: 0;
}
</style>
