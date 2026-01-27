<script setup lang="ts">
import { computed } from 'vue'
import type { AnswerValue, Module, ModuleQuestion } from '@/types/questionnaire'
import { useLocaleStore } from '@/stores/locale'

defineProps<{
  module: Module
  answers: Record<string, AnswerValue | undefined>
  error: string | null
  message: string | null
  canSubmit: boolean
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update-answer', payload: { id: string; value: AnswerValue }): void
  (e: 'toggle-multi', payload: { id: string; value: AnswerValue }): void
  (e: 'submit'): void
  (e: 'restart'): void
  (e: 'prev'): void
}>()

const locale = useLocaleStore()
const ui = computed(() =>
  locale.isZh
    ? {
        yes: '是',
        no: '否',
        loadingFailed: '加载失败',
        prev: '上一题',
        restart: '重新开始',
        next: '继续',
      }
    : {
        yes: 'Yes',
        no: 'No',
        loadingFailed: 'Loading Failed',
        prev: 'Previous',
        restart: 'Restart',
        next: 'Continue',
      },
)

function onSingleChange(question: ModuleQuestion, value: AnswerValue) {
  emit('update-answer', { id: question.id, value })
}

function onBooleanChange(question: ModuleQuestion, value: boolean) {
  emit('update-answer', { id: question.id, value })
}

function onMultiToggle(question: ModuleQuestion, value: AnswerValue) {
  emit('toggle-multi', { id: question.id, value })
}
</script>

<template>
  <section class="card">
    <h2>{{ module.title }}</h2>
    <p v-if="module.description" class="muted">{{ module.description }}</p>

    <div v-for="question in module.questions" :key="question.id" class="question">
      <h3 class="question-title">{{ question.text }}</h3>

      <div v-if="question.type === 'boolean'" class="options">
        <label class="option">
          <input
            type="radio"
            :name="question.id"
            :checked="answers[question.id] === true"
            @change="onBooleanChange(question, true)"
          />
          <span>{{ ui.yes }}</span>
        </label>
        <label class="option">
          <input
            type="radio"
            :name="question.id"
            :checked="answers[question.id] === false"
            @change="onBooleanChange(question, false)"
          />
          <span>{{ ui.no }}</span>
        </label>
      </div>

      <div v-else-if="question.type === 'single_choice'" class="options">
        <label v-for="opt in question.options" :key="String(opt.value)" class="option">
          <input
            type="radio"
            :name="question.id"
            :checked="answers[question.id] === opt.value"
            @change="onSingleChange(question, opt.value as AnswerValue)"
          />
          <span>{{ opt.label }}</span>
        </label>
      </div>

      <div v-else-if="question.type === 'multi_choice' || question.type === 'multiple_choice'" class="options">
        <label v-for="opt in question.options" :key="String(opt.value)" class="option">
          <input
            type="checkbox"
            :name="question.id"
            :checked="Array.isArray(answers[question.id]) && (answers[question.id] as AnswerValue[]).includes(opt.value)"
            @change="onMultiToggle(question, opt.value as AnswerValue)"
          />
          <span>{{ opt.label }}</span>
        </label>
      </div>
    </div>

    <div v-if="error" class="error">{{ ui.loadingFailed }} {{ error }}</div>
    <div v-if="message" class="muted">{{ message }}</div>

    <div class="actions">
      <button type="button" @click="emit('prev')">{{ ui.prev }}</button>
      <button type="button" @click="emit('restart')">{{ ui.restart }}</button>
      <button type="button" :disabled="!canSubmit || loading" @click="emit('submit')">{{ ui.next }}</button>
    </div>
  </section>
</template>
