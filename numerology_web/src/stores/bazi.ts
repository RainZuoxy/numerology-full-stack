import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { baziApi, type BaZiRequest } from '@/api/bazi'
import type { BaZiResponse } from '@/api/types'

const FORM_KEY = 'bazi_form'
const RESULT_KEY = 'bazi_result'

const defaultForm: Required<BaZiRequest> = {
  name: '',
  dob_time: '1990-01-19 09:30:00',
  gender: 'male',
  dayun_number: 7,
}

function load<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key)
    return raw ? (JSON.parse(raw) as T) : fallback
  } catch {
    return fallback
  }
}

export const useBaziStore = defineStore('bazi', () => {
  const form = ref<Required<BaZiRequest>>(load(FORM_KEY, defaultForm))
  const result = ref<BaZiResponse | null>(load<BaZiResponse | null>(RESULT_KEY, null))
  const loading = ref(false)
  const error = ref('')

  watch(form, (v) => localStorage.setItem(FORM_KEY, JSON.stringify(v)), { deep: true })
  watch(result, (v) => {
    if (v) localStorage.setItem(RESULT_KEY, JSON.stringify(v))
    else localStorage.removeItem(RESULT_KEY)
  })

  async function generate() {
    error.value = ''
    loading.value = true
    try {
      result.value = await baziApi.generate({
        name: form.value.name || undefined,
        dob_time: form.value.dob_time,
        gender: form.value.gender,
        dayun_number: form.value.dayun_number,
      })
    } catch (e: any) {
      error.value = e.message || '生成失败'
    } finally {
      loading.value = false
    }
  }

  function reset() {
    form.value = { ...defaultForm }
    result.value = null
    error.value = ''
  }

  return { form, result, loading, error, generate, reset }
})
