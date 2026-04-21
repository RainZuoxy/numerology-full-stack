import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { guaApi } from '@/api/gua'
import type { GuaResponse } from '@/api/types'

const SERIES_KEY = 'gua_series'
const RESULT_KEY = 'gua_result'

function load<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key)
    return raw ? (JSON.parse(raw) as T) : fallback
  } catch {
    return fallback
  }
}

export const useGuaStore = defineStore('gua', () => {
  const series = ref<string>(load(SERIES_KEY, '010111'))
  const result = ref<GuaResponse | null>(load<GuaResponse | null>(RESULT_KEY, null))
  const loading = ref(false)
  const error = ref('')

  watch(series, (v) => localStorage.setItem(SERIES_KEY, v))
  watch(result, (v) => {
    if (v) localStorage.setItem(RESULT_KEY, JSON.stringify(v))
    else localStorage.removeItem(RESULT_KEY)
  })

  async function query() {
    error.value = ''
    loading.value = true
    try {
      result.value = await guaApi.query(series.value)
    } catch (e: any) {
      error.value = e.message || '查询失败'
    } finally {
      loading.value = false
    }
  }

  function reset() {
    series.value = '010111'
    result.value = null
    error.value = ''
  }

  return { series, result, loading, error, query, reset }
})
