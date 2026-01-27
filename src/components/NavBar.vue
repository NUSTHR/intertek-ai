<script setup lang="ts">
import { useLocaleStore } from '@/stores/locale'
import logoUrl from '@/assets/images/logo/b9d2336ed590ab1e2a8d517d7f555f72.png'

const props = defineProps<{
  homeLabel: string
  helpLabel: string
  actionLabel: string
  actionDisabled?: boolean
  helpHref: string
}>()

const emit = defineEmits<{
  (e: 'home'): void
  (e: 'action'): void
}>()

const locale = useLocaleStore()
</script>

<template>
  <header class="bg-white w-full py-6 border-b border-[#E5E7EB]">
    <div class="container mx-auto px-6 lg:px-12 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="https://www.intertek.com/">
          <img alt="Intertek AI² Logo" class="w-8 h-8 rounded-md" :src="logoUrl" />
        </a>
        <span class="text-[#111111] font-bold text-lg tracking-wide uppercase">Intertek AI²</span>
      </div>
      <div class="hidden md:flex items-center gap-8">
        <div class="flex items-center bg-[#F3F4F6] p-1 rounded-md">
          <button
            type="button"
            class="px-3 py-1 text-xs font-bold"
            :class="locale.isZh ? 'text-[#6B7280]' : 'bg-white rounded-md shadow-sm text-[#111111]'"
            @click="locale.setLang('en')"
          >
            EN
          </button>
          <button
            type="button"
            class="px-3 py-1 text-xs font-bold"
            :class="locale.isZh ? 'bg-white rounded-md shadow-sm text-[#111111]' : 'text-[#6B7280]'"
            @click="locale.setLang('zh')"
          >
            中文
          </button>
        </div>
        <nav class="flex items-center gap-6 text-sm font-medium text-[#111111]">
          <button
            type="button"
            class="flex items-center gap-2 font-bold hover:text-[#4B5563] transition-colors"
            @click="emit('home')"
          >
            <span class="material-symbols-outlined text-xl">home</span>
            {{ props.homeLabel }}
          </button>
          <a class="flex items-center gap-2 font-bold hover:text-[#4B5563] transition-colors" :href="props.helpHref">
            <span class="material-symbols-outlined text-xl">help_center</span>
            {{ props.helpLabel }}
          </a>
        </nav>
        <button
          type="button"
          class="bg-[#FFCC00] hover:bg-[#E6B800] text-[#111111] font-bold text-sm px-6 py-3 rounded-md transition-colors"
          :disabled="props.actionDisabled"
          @click="emit('action')"
        >
          {{ props.actionLabel }}
        </button>
      </div>
      <button type="button" class="md:hidden text-[#111111]">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
        </svg>
      </button>
    </div>
  </header>
</template>
