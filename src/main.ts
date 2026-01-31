import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const logLevel = import.meta.env.VITE_LOG_LEVEL ?? (import.meta.env.DEV ? 'info' : 'error')
const logEnabled = (level: 'info' | 'error') => {
  if (level === 'error') return true
  return logLevel === 'info' || logLevel === 'debug'
}
const logInfo = (...args: unknown[]) => {
  if (logEnabled('info')) console.info(...args)
}
const logError = (...args: unknown[]) => {
  console.error(...args)
}

app.use(createPinia())
app.use(router)

app.config.errorHandler = (err, instance, info) => {
  logError('ui_error', { err, info, instance })
}

window.addEventListener('error', (event) => {
  logError('window_error', { message: event.message, filename: event.filename, lineno: event.lineno, colno: event.colno })
})

window.addEventListener('unhandledrejection', (event) => {
  logError('unhandled_rejection', { reason: event.reason })
})

router.beforeEach((to, from) => {
  logInfo('route_change_start', { from: from.fullPath, to: to.fullPath })
  return true
})

router.afterEach((to, from) => {
  logInfo('route_change_end', { from: from.fullPath, to: to.fullPath })
})

app.mount('#app')
