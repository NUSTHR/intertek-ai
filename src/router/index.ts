import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'start',
      component: () => import('@/views/StartView.vue'),
    },
    {
      path: '/module/9',
      redirect: '/result',
    },
    {
      path: '/module/:id',
      name: 'module',
      component: () => import('@/views/QuestionView.vue'),
      props: true,
    },
    {
      path: '/result',
      name: 'result',
      component: () => import('@/views/ResultView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

let lastPosition = Number(window.history.state?.position ?? 0)

router.beforeEach((to, from) => {
  const currentPosition = Number(window.history.state?.position ?? lastPosition)
  const isBack = currentPosition < lastPosition
  if (isBack && (from.name === 'module' || from.name === 'result') && to.name !== 'start') {
    return { name: 'start', replace: true }
  }
  return true
})

router.afterEach(() => {
  lastPosition = Number(window.history.state?.position ?? lastPosition)
})

export default router
