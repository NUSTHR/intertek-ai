export function computeQuestionTag(id: string, isZh: boolean): string {
  if (!id) return ''
  const num = id.replace(/^q/i, '').toUpperCase()
  return isZh ? `问题 ${num}` : `Question ${num}`
}
