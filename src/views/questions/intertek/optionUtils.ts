import type { AnswerScalar, ModuleQuestion } from '@/types/questionnaire'

type FallbackOption = {
  value: AnswerScalar
  title: string
  description?: string
  icon?: string
  label?: string
  cite?: string
  exclusive?: boolean
  span?: string
}

type BuiltOption = {
  value: AnswerScalar
  title: string
  description?: string
  icon?: string
  label?: string
  cite?: string
  exclusive?: boolean
  span?: string
}

export function buildOptions(question: ModuleQuestion, fallbackOptions: FallbackOption[]): BuiltOption[] {
  const backendOptions = question.options ?? []
  if (!backendOptions.length) return fallbackOptions
  return backendOptions.map((opt, index) => {
    const base = fallbackOptions[index]
    const title = opt.label ?? base?.title ?? String(opt.value)
    const label = base?.label ?? (opt.label ? opt.label.toUpperCase() : String(opt.value).toUpperCase())
    return {
      value: opt.value,
      title,
      description: opt.description ?? base?.description ?? '',
      icon: base?.icon ?? 'help',
      label,
      cite: opt.cite ?? base?.cite,
      exclusive: opt.exclusive ?? base?.exclusive,
      span: base?.span,
    }
  })
}
