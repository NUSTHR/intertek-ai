import { ref } from 'vue'
import { defineStore } from 'pinia'
import type {
  AnswerValue,
  Module,
  ModuleResponse,
  ResultResponse,
  StartResponse,
  SubmitRequest,
  SubmitResponse,
} from '@/types/questionnaire'

const API_BASE = import.meta.env.VITE_API_BASE ?? (import.meta.env.DEV ? '/api' : '')
const SESSION_KEY = 'questionnaire_session_id'

export const useQuestionnaireStore = defineStore('questionnaire', () => {
  const sessionId = ref<string>(localStorage.getItem(SESSION_KEY) ?? '')
  const currentModule = ref<Module | null>(null)
  const parameters = ref<Record<string, AnswerValue>>({})
  const answers = ref<Record<string, AnswerValue>>({})
  const lastAction = ref<SubmitResponse['next'] | null>(null)
  const lastMessage = ref<string | null>(null)
  const conclusion = ref<Record<string, unknown> | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function init(): Promise<Module | null> {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API_BASE}/start`, { method: 'POST' })
      if (!res.ok) throw new Error(`init_http_${res.status}`)
      const data = (await res.json()) as StartResponse
      sessionId.value = data.session_id
      localStorage.setItem(SESSION_KEY, data.session_id)
      currentModule.value = data.module
      parameters.value = {}
      answers.value = {}
      lastAction.value = null
      lastMessage.value = null
      conclusion.value = null
      return data.module
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'init_failed'
      return null
    } finally {
      loading.value = false
    }
  }

  async function loadModule(moduleId: string): Promise<Module | null> {
    if (!sessionId.value) return null
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API_BASE}/module/${encodeURIComponent(moduleId)}?session_id=${sessionId.value}`)
      if (!res.ok) throw new Error(`module_http_${res.status}`)
      const data = (await res.json()) as ModuleResponse
      currentModule.value = data.module
      return data.module
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'module_failed'
      return null
    } finally {
      loading.value = false
    }
  }

  async function submit(moduleId: string, payloadAnswers: Record<string, AnswerValue>): Promise<SubmitResponse | null> {
    if (!sessionId.value) return null
    loading.value = true
    error.value = null
    try {
      const payload: SubmitRequest = {
        session_id: sessionId.value,
        module_id: moduleId,
        answers: payloadAnswers,
        replace: true,
      }
      const res = await fetch(`${API_BASE}/submit-answer`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!res.ok) {
        const detail = await res.json().catch(() => null)
        throw new Error(JSON.stringify(detail ?? { status: res.status }))
      }
      const data = (await res.json()) as SubmitResponse
      parameters.value = data.parameters
      lastAction.value = data.next
      lastMessage.value = data.next?.message ?? null
      answers.value = { ...payloadAnswers }
      if (data.module) currentModule.value = data.module
      if (data.conclusion !== undefined) conclusion.value = data.conclusion ?? null
      return data
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'submit_failed'
      return null
    } finally {
      loading.value = false
    }
  }

  async function fetchResult(): Promise<Record<string, AnswerValue> | null> {
    if (!sessionId.value) return null
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API_BASE}/result?session_id=${sessionId.value}`)
      if (!res.ok) throw new Error(`result_http_${res.status}`)
      const data = (await res.json()) as ResultResponse
      parameters.value = data.parameters
      conclusion.value = data.conclusion ?? null
      return data.parameters
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'result_failed'
      return null
    } finally {
      loading.value = false
    }
  }

  function reset() {
    sessionId.value = ''
    localStorage.removeItem(SESSION_KEY)
    currentModule.value = null
    parameters.value = {}
    answers.value = {}
    lastAction.value = null
    lastMessage.value = null
    conclusion.value = null
    error.value = null
  }

  return {
    sessionId,
    currentModule,
    parameters,
    answers,
    lastAction,
    lastMessage,
    conclusion,
    loading,
    error,
    init,
    loadModule,
    submit,
    fetchResult,
    reset,
  }
})
