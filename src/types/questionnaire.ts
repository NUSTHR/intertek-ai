export type AnswerValue = 'yes' | 'no'

export type NextNode =
  | { type: 'question'; id: string }
  | { type: 'result'; id: 'A' | 'B' | 'C' | 'D' | 'E' }

export type Option = {
  label: string
  value: AnswerValue
  next: NextNode
}

export type Question = {
  id: string
  title: string
  description: string | null
  bullets: string[] | null
  options: Option[]
}

export type Result = {
  id: 'A' | 'B' | 'C' | 'D' | 'E'
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

