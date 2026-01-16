export type AnswerValue = string | string[]

export type NextNode =
  | { type: 'question'; id: string }
  | { type: 'result'; id: string }

export type SingleOption = {
  label: string
  value: string
  next: NextNode
}

export type MultiOption = {
  label: string
  value: string
  exclusive?: boolean
}

export type QuestionBase = {
  id: string
  title: string
  description: string | null
  bullets: string[] | null
}

export type SingleQuestion = QuestionBase & {
  kind: 'single'
  options: SingleOption[]
}

export type MultiQuestion = QuestionBase & {
  kind: 'multi'
  options: MultiOption[]
  next_any: NextNode
  next_none: NextNode
}

export type Question = SingleQuestion | MultiQuestion

export type Result = {
  id: string
  title: string
  description: string
  bullets: string[] | null
}

export type TreeResponse = {
  start: string
  questions: Question[]
}

export type ResultsResponse = {
  results: Result[]
}

export type EvaluateResponse = {
  result_id: Result['id']
  path: string[]
  result: Result
}

export type StartResponse = {
  start: string
  question: Question
}

export type QuestionResponse = {
  question: Question
}

export type ResultResponse = {
  result: Result
}

export type AnswerRequest = {
  question_id: string
  value: AnswerValue
  answers: Record<string, AnswerValue>
}

export type AnswerResponse = {
  next: NextNode
  path: string[]
  question?: Question | null
  result?: Result | null
}
