import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { TokenResponse, UserInfo } from '@/api/types'
import router from '@/router'

const TOKEN_KEY = 'access_token'
const USER_KEY = 'user_info'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<UserInfo | null>(null)
  const isAuthenticated = computed(() => !!token.value)

  function hydrate() {
    if (token.value) return
    const t = localStorage.getItem(TOKEN_KEY)
    const u = localStorage.getItem(USER_KEY)
    if (t) token.value = t
    if (u) user.value = JSON.parse(u)
  }

  function applyToken(resp: TokenResponse) {
    token.value = resp.access_token
    user.value = resp.user
    localStorage.setItem(TOKEN_KEY, resp.access_token)
    localStorage.setItem(USER_KEY, JSON.stringify(resp.user))
  }

  async function login(username: string, password: string) {
    applyToken(await authApi.login({ username, password }))
  }

  async function register(username: string, password: string, nickname?: string) {
    applyToken(await authApi.register({ username, password, nickname }))
  }

  async function wechatLogin(code: string, nickname?: string) {
    applyToken(await authApi.wechatLogin({ code, nickname }))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    // 清理业务数据缓存，避免跨用户泄露
    localStorage.removeItem('bazi_form')
    localStorage.removeItem('bazi_result')
    localStorage.removeItem('gua_series')
    localStorage.removeItem('gua_result')
    localStorage.removeItem('fortune_result')
    localStorage.removeItem('fortune_sig')
    router.push({ name: 'login' })
  }

  return { token, user, isAuthenticated, hydrate, login, register, wechatLogin, logout }
})
