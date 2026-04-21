import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import {
  archiveApi,
  type ArchiveCreateRequest,
  type ArchiveItem,
  type DailyPredictionResponse,
} from '@/api/archive'

export const useArchiveStore = defineStore('archive', () => {
  const items = ref<ArchiveItem[]>([])
  const maxArchives = ref(5)
  const prediction = ref<DailyPredictionResponse | null>(null)
  const loading = ref(false)
  const predictLoading = ref(false)
  const error = ref('')

  const primary = computed(() => items.value.find((i) => i.is_primary) || null)
  const canCreate = computed(() => items.value.length < maxArchives.value)

  async function refresh() {
    loading.value = true
    error.value = ''
    try {
      const resp = await archiveApi.list()
      items.value = resp.items
      maxArchives.value = resp.max_archives
    } catch (e: any) {
      error.value = e.message || '加载失败'
    } finally {
      loading.value = false
    }
  }

  async function create(req: ArchiveCreateRequest) {
    const item = await archiveApi.create(req)
    await refresh()
    return item
  }

  async function remove(id: number) {
    await archiveApi.remove(id)
    await refresh()
  }

  async function setPrimary(id: number) {
    await archiveApi.setPrimary(id)
    await refresh()
  }

  async function loadToday() {
    try {
      prediction.value = await archiveApi.getToday()
    } catch (e: any) {
      error.value = e.message || '预测加载失败'
    }
  }

  async function predictToday() {
    predictLoading.value = true
    error.value = ''
    try {
      prediction.value = await archiveApi.createToday()
    } catch (e: any) {
      error.value = e.message || '预测失败'
      throw e
    } finally {
      predictLoading.value = false
    }
  }

  function reset() {
    items.value = []
    prediction.value = null
    error.value = ''
  }

  return {
    items, maxArchives, prediction, loading, predictLoading, error,
    primary, canCreate,
    refresh, create, remove, setPrimary, loadToday, predictToday, reset,
  }
})
