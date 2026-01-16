import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type {
  AnswerRequest,
  AnswerResponse,
  AnswerValue,
  EvaluateResponse,
  Question,
  QuestionResponse,
  Result,
  ResultResponse,
  ResultsResponse,
  StartResponse,
  TreeResponse,
} from '@/types/questionnaire'

const STORAGE_KEY = 'aiq:answers:v2'

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((v) => typeof v === 'string')
}

function loadPersistedAnswers(): Record<string, AnswerValue> {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) return {}
  try {
    const data = JSON.parse(raw) as Record<string, unknown>
    if (!data || typeof data !== 'object') return {}
    const out: Record<string, AnswerValue> = {}
    for (const [k, v] of Object.entries(data)) {
      if (typeof v === 'string') out[k] = v
      else if (isStringArray(v)) out[k] = v
    }
    return out
  } catch {
    return {}
  }
}

function persistAnswers(answers: Record<string, AnswerValue>) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(answers))
}

export const useQuestionnaireStore = defineStore('questionnaire', () => {
  const startId = ref<string>('q1')
  const questionsById = ref<Record<string, Question>>({})
  const resultsById = ref<Record<string, Result>>({})
  const loaded = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const answers = ref<Record<string, AnswerValue>>(loadPersistedAnswers())
  const lastEvaluation = ref<EvaluateResponse | null>(null)

  const questions = computed(() => Object.values(questionsById.value))

  async function load() {
    if (loaded.value || loading.value) return
    loading.value = true
    error.value = null
    try {
      const startRes = await fetch('/api/start')
      if (startRes.ok) {
        const start = (await startRes.json()) as StartResponse
        startId.value = start.start
        questionsById.value = { ...questionsById.value, [start.question.id]: start.question }
        loaded.value = true
        return
      }

      const [treeRes, resultsRes] = await Promise.all([fetch('/api/tree'), fetch('/api/results')])
      if (!treeRes.ok) throw new Error(`tree_http_${treeRes.status}`)
      if (!resultsRes.ok) throw new Error(`results_http_${resultsRes.status}`)

      const tree = (await treeRes.json()) as TreeResponse
      const results = (await resultsRes.json()) as ResultsResponse

      startId.value = tree.start
      questionsById.value = Object.fromEntries(tree.questions.map((q) => [q.id, q]))
      resultsById.value = Object.fromEntries(results.results.map((r) => [r.id, r]))
      loaded.value = true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'load_failed'
      loaded.value = false
    } finally {
      loading.value = false
    }
  }

  function reset() {
    answers.value = {}
    persistAnswers(answers.value)
    lastEvaluation.value = null
  }

  function setAnswer(questionId: string, value: AnswerValue) {
    answers.value = { ...answers.value, [questionId]: value }
    persistAnswers(answers.value)
  }

  function getNext(questionId: string, value: AnswerValue) {
    const q = questionsById.value[questionId]
    if (!q || q.kind !== 'single') return null
    if (typeof value !== 'string') return null
    const opt = q.options.find((o) => o.value === value)
    return opt?.next ?? null
  }

  async function fetchQuestion(questionId: string): Promise<Question | null> {
    if (questionsById.value[questionId]) return questionsById.value[questionId]
    const res = await fetch(`/api/question/${encodeURIComponent(questionId)}`)
    if (!res.ok) return null
    const data = (await res.json()) as QuestionResponse
    questionsById.value = { ...questionsById.value, [data.question.id]: data.question }
    return data.question
  }

  async function fetchResult(resultId: string): Promise<Result | null> {
    const existing = resultsById.value[resultId as Result['id']]
    if (existing) return existing
    const res = await fetch(`/api/result/${encodeURIComponent(resultId)}`)
    if (!res.ok) return null
    const data = (await res.json()) as ResultResponse
    resultsById.value = { ...resultsById.value, [data.result.id]: data.result }
    return data.result
  }

  async function answer(questionId: string, value: AnswerValue): Promise<AnswerResponse | null> {
    const payload: AnswerRequest = { question_id: questionId, value, answers: answers.value }
    const res = await fetch('/api/answer', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (!res.ok) return null
    const data = (await res.json()) as AnswerResponse
    if (data.question) {
      questionsById.value = { ...questionsById.value, [data.question.id]: data.question }
    }
    if (data.result) {
      resultsById.value = { ...resultsById.value, [data.result.id]: data.result }
      lastEvaluation.value = { result_id: data.result.id, path: data.path, result: data.result }
    }
    return data
  }

  async function evaluate(): Promise<EvaluateResponse> {
    const res = await fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ answers: answers.value }),
    })
    if (!res.ok) {
      const detail = await res.json().catch(() => null)
      throw new Error(JSON.stringify(detail ?? { status: res.status }))
    }
    const data = (await res.json()) as EvaluateResponse
    lastEvaluation.value = data
    return data
  }

  return {
    startId,
    questionsById,
    resultsById,
    questions,
    loaded,
    loading,
    error,
    answers,
    lastEvaluation,
    load,
    reset,
    setAnswer,
    getNext,
    fetchQuestion,
    fetchResult,
    answer,
    evaluate,
  }
})
