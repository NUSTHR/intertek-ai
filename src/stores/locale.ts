import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const LOCALE_KEY = 'questionnaire_lang'

type Locale = 'en' | 'zh'

export const useLocaleStore = defineStore('locale', () => {
  const lang = ref<Locale>((localStorage.getItem(LOCALE_KEY) as Locale) || 'en')

  const apiLang = computed(() => (lang.value === 'zh' ? 'cn' : 'en'))
  const isZh = computed(() => lang.value === 'zh')

  function setLang(next: Locale) {
    lang.value = next
    localStorage.setItem(LOCALE_KEY, next)
  }

  return {
    lang,
    apiLang,
    isZh,
    setLang,
  }
})
