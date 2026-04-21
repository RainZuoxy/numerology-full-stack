import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'
import { fortuneApi, type FortuneResponse } from '@/api/fortune'
import type { BaZiResponse } from '@/api/types'

const RESULT_KEY = 'fortune_result'
const KEY_SIG = 'fortune_sig'

function load<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key)
    return raw ? (JSON.parse(raw) as T) : fallback
  } catch {
    return fallback
  }
}

function sigOf(bazi: BaZiResponse): string {
  const b = bazi.ba_zi
  return [
    b.tg_year.type, b.dz_year.type,
    b.tg_month.type, b.dz_month.type,
    b.tg_day.type, b.dz_day.type,
    b.tg_hour.type, b.dz_hour.type,
  ].join('')
}

export const useFortuneStore = defineStore('fortune', () => {
  const data = ref<FortuneResponse | null>(load<FortuneResponse | null>(RESULT_KEY, null))
  const signature = ref<string>(load<string>(KEY_SIG, ''))
  const loading = ref(false)
  const error = ref('')

  watch(data, (v) => {
    if (v) localStorage.setItem(RESULT_KEY, JSON.stringify(v))
    else localStorage.removeItem(RESULT_KEY)
  })
  watch(signature, (v) => {
    if (v) localStorage.setItem(KEY_SIG, JSON.stringify(v))
    else localStorage.removeItem(KEY_SIG)
  })

  async function analyze(bazi: BaZiResponse, question?: string, force = false) {
    const sig = sigOf(bazi) + '|' + (question || '')
    if (!force && data.value && signature.value === sig) return
    error.value = ''
    loading.value = true
    try {
      data.value = await fortuneApi.analyze({ bazi, question })
      signature.value = sig
    } catch (e: any) {
      error.value = e.message || '推演失败'
      data.value = null
    } finally {
      loading.value = false
    }
  }

  function reset() {
    data.value = null
    signature.value = ''
    error.value = ''
  }

  function matches(bazi: BaZiResponse | null, question?: string): boolean {
    if (!bazi || !data.value) return false
    return signature.value === sigOf(bazi) + '|' + (question || '')
  }

  const hasCache = computed(() => !!data.value && !!signature.value)

  return { data, signature, loading, error, hasCache, analyze, reset, matches }
})
