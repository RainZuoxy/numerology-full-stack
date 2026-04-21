import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'index', component: () => import('@/views/IndexView.vue') },
    { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
    { path: '/bazi', name: 'bazi', component: () => import('@/views/BaZiView.vue'), meta: { requiresAuth: true } },
    { path: '/gua',  name: 'gua',  component: () => import('@/views/GuaView.vue'),  meta: { requiresAuth: true } },
    { path: '/fortune', name: 'fortune', component: () => import('@/views/FortuneView.vue'), meta: { requiresAuth: true } },
    { path: '/me', name: 'me', component: () => import('@/views/PersonalView.vue'), meta: { requiresAuth: true } },
  ]
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  auth.hydrate()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})

export default router
