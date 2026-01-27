export type AnswerScalar = string | number | boolean
export type AnswerValue = AnswerScalar | AnswerScalar[]

export type ModuleOption = {
  label: string
  value: AnswerScalar
  description?: string
  cite?: string
  exclusive?: boolean
}

export type ModuleQuestion = {
  id: string
  text: string
  ref?: string
  description?: string
  type: 'single_choice' | 'multi_choice' | 'multiple_choice' | 'boolean'
  options?: ModuleOption[]
}

export type Module = {
  id: string
  title: string
  description?: string
  questions: ModuleQuestion[]
}

export type StartResponse = {
  session_id: string
  module: Module
}

export type ModuleResponse = {
  module: Module
}

export type QuestionResponse = {
  question: ModuleQuestion
}

export type SubmitRequest = {
  session_id: string
  module_id?: string | null
  answers: Record<string, AnswerValue>
  replace?: boolean
}

export type NextAction = {
  type: 'module' | 'result'
  module_id?: string | null
  message?: string | null
}

export type SubmitResponse = {
  session_id: string
  parameters: Record<string, AnswerValue>
  next: NextAction
  module_complete: boolean
  module?: Module | null
  conclusion?: Record<string, unknown> | null
}

export type ResultResponse = {
  parameters: Record<string, AnswerValue>
  conclusion?: Record<string, unknown> | null
}
