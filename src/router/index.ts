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
      path: '/q/:id',
      name: 'question',
      component: () => import('@/views/QuestionView.vue'),
      props: true,
    },
    {
      path: '/result/:id',
      name: 'result',
      component: () => import('@/views/ResultView.vue'),
      props: true,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

export default router
