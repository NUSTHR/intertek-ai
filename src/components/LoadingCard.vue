<script setup lang="ts">
defineProps<{
  loading: boolean
  errorMessage?: string | null
  loadingText: string
  failedText: string
  retryLabel?: string
}>()
const emit = defineEmits<{
  (e: 'retry'): void
}>()
</script>

<template>
  <div class="bg-white border border-slate-200 shadow-sm px-8 py-6 flex flex-col items-center gap-4 text-center">
    <div class="flex items-center gap-2">
      <span class="h-2 w-2 rounded-full bg-intertek-yellow animate-pulse"></span>
      <span class="h-2 w-2 rounded-full bg-intertek-yellow animate-pulse [animation-delay:150ms]"></span>
      <span class="h-2 w-2 rounded-full bg-intertek-yellow animate-pulse [animation-delay:300ms]"></span>
    </div>
    <div class="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500">
      {{ errorMessage && !loading ? failedText : loadingText }}
    </div>
    <div v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</div>
    <button
      v-if="errorMessage && retryLabel"
      type="button"
      class="px-6 py-2 bg-intertek-yellow text-black font-black uppercase tracking-widest text-[10px] hover:bg-intertek-dark hover:text-white transition-all"
      @click="emit('retry')"
    >
      {{ retryLabel }}
    </button>
  </div>
</template>
