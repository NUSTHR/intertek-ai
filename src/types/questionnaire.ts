export type AnswerScalar = string | number | boolean
export type AnswerValue = AnswerScalar | AnswerScalar[]

export type ModuleOption = {
  label: string
  value: AnswerScalar
  exclusive?: boolean
}

export type ModuleQuestion = {
  id: string
  text: string
  ref?: string
  description?: string
  type: 'single_choice' | 'multi_choice' | 'boolean'
  options?: ModuleOption[]
}

export type Module = {
  id: string
  title: string
  description?: string
  questions: ModuleQuestion[]
}

export type InitResponse = {
  session_id: string
  module: Module
}

export type ModuleResponse = {
  module: Module
}

export type SubmitRequest = {
  session_id: string
  module_id: string
  answers: Record<string, AnswerValue>
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
}

export type ResultResponse = {
  parameters: Record<string, AnswerValue>
}
