<script setup lang="ts">
import type { AnswerScalar, AnswerValue } from '@/types/questionnaire'

type Option = {
  value: AnswerScalar
  title: string
  description?: string
  icon?: string
  cite?: string
}

const props = defineProps<{
  options: Option[]
  modelValue: AnswerValue | undefined
  inputName: string
  labelId: string
  containerClass?: string
  titleRowClass?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: AnswerValue): void
}>()
</script>

<template>
  <div role="radiogroup" :aria-labelledby="props.labelId" :class="['flex flex-col gap-4', props.containerClass]">
    <label
      v-for="opt in props.options"
      :key="String(opt.value)"
      class="option-card cursor-pointer relative flex items-start p-6 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 transition-all duration-200 group"
      :class="{ selected: props.modelValue === opt.value }"
    >
      <input
        class="peer sr-only"
        :name="props.inputName"
        type="radio"
        :value="opt.value"
        :checked="props.modelValue === opt.value"
        @change="emit('update:modelValue', opt.value as AnswerValue)"
      />
      <div class="flex-shrink-0 mr-6">
        <div class="size-14 bg-white dark:bg-slate-800 flex items-center justify-center text-slate-400 group-hover:bg-intertek-yellow group-hover:text-black transition-colors shadow-sm">
          <span class="material-symbols-outlined text-3xl">{{ opt.icon }}</span>
        </div>
      </div>
      <div class="flex-1">
        <div :class="['flex justify-between items-center', props.titleRowClass ?? 'mb-2']">
          <h3 class="text-lg font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ opt.title }}</h3>
          <div class="flex items-center gap-3">
            <div v-if="opt.cite" class="relative group/info">
              <span class="material-symbols-outlined text-base text-slate-400 group-hover/info:text-intertek-yellow transition-colors">info</span>
              <div class="absolute right-0 top-6 z-10 w-72 rounded bg-slate-900 text-white text-[10px] leading-relaxed px-3 py-2 shadow-lg opacity-0 invisible group-hover/info:visible group-hover/info:opacity-100 transition-opacity">
                {{ opt.cite }}
              </div>
            </div>
            <div class="size-6 border-2 border-slate-200 dark:border-slate-700 peer-checked:border-intertek-yellow peer-checked:bg-intertek-yellow flex items-center justify-center opacity-0 peer-checked:opacity-100 transition-all">
              <span class="material-symbols-outlined text-black font-black text-lg">check</span>
            </div>
          </div>
        </div>
        <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed max-w-xl font-medium">
          {{ opt.description }}
        </p>
      </div>
      <div class="absolute inset-0 border-2 border-intertek-yellow opacity-0 peer-checked:opacity-100 pointer-events-none transition-opacity"></div>
    </label>
  </div>
</template>
