<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import ScrollPanel from '@/components/ScrollPanel.vue'
import FormField from '@/components/FormField.vue'
import BaZiChart from '@/components/BaZiChart.vue'
import MainDestinyList from '@/components/MainDestinyList.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { useBaziStore } from '@/stores/bazi'
import { useFortuneStore } from '@/stores/fortune'
import { useArchiveStore } from '@/stores/archive'
import { exportElementAsPng } from '@/utils/exportImage'
import { formatDobDisplay } from '@/utils/shichen'

const router = useRouter()
const fortune = useFortuneStore()
const archive = useArchiveStore()
const store = useBaziStore()
const { form, result, loading, error } = storeToRefs(store)

const archiveOpen = ref(false)
const archiving = ref(false)
const archiveMsg = ref('')

async function openArchive() {
  archiveMsg.value = ''
  if (!archive.items.length && !archive.loading) {
    await archive.refresh()
  }
  archiveOpen.value = true
}
function cancelArchive() { archiveOpen.value = false; archiveMsg.value = '' }
async function confirmArchive() {
  if (!form.value.name?.trim()) {
    archiveMsg.value = '姓名不能为空，请先在上方填写。'
    return
  }
  if (!archive.canCreate) {
    archiveMsg.value = `归档已达上限（${archive.maxArchives}），请到个人中心删除后再试。`
    return
  }
  archiving.value = true
  try {
    await archive.create({
      name: form.value.name.trim(),
      gender: form.value.gender,
      dob_time: form.value.dob_time,
    })
    archiveOpen.value = false
    router.push({ name: 'me' })
  } catch (e: any) {
    archiveMsg.value = e.message || '归档失败'
  } finally {
    archiving.value = false
  }
}

const confirmOpen = ref(false)
const confirmInfo = computed(() => {
  const f = form.value
  return {
    name: f.name || '（未填写）',
    gender: f.gender === 'female' ? '女' : '男',
    dob: f.dob_time,
  }
})

const hasFortuneCache = computed(() => fortune.matches(result.value))

function openFortune() { confirmOpen.value = true }
function cancelFortune() { confirmOpen.value = false }
function confirmFortune() {
  confirmOpen.value = false
  if (!result.value) return
  // 若当前命盘与缓存不一致，清掉旧缓存；一致则直接复用
  if (!fortune.matches(result.value)) fortune.reset()
  router.push({ name: 'fortune' })
}
function viewCachedFortune() {
  if (!result.value) return
  router.push({ name: 'fortune' })
}

const chartArea = ref<HTMLElement | null>(null)
const exporting = ref(false)

async function saveAsImage() {
  if (!chartArea.value) return
  exporting.value = true
  try {
    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)
    const name = (form.value.name || 'bazi').replace(/[^\w\u4e00-\u9fa5-]/g, '_')
    await exportElementAsPng(chartArea.value, `${name}_${ts}.png`)
  } catch (e: any) {
    error.value = `导出失败：${e.message || e}`
  } finally {
    exporting.value = false
  }
}
</script>

<template>
  <ScrollPanel title="排 盘" subtitle="四柱 · 十神 · 大运">
    <form class="inputs" @submit.prevent="store.generate()">
      <div class="grid-2">
        <FormField label="姓名">
          <input v-model="form.name" placeholder="（可选）" />
        </FormField>
        <FormField label="性别">
          <select v-model="form.gender">
            <option value="male">男</option>
            <option value="female">女</option>
          </select>
        </FormField>
      </div>
      <FormField label="阳历生辰">
        <DateTimePicker v-model="form.dob_time" />
      </FormField>
      <FormField label="大运数量">
        <input v-model.number="form.dayun_number" type="number" min="1" max="20" />
      </FormField>
      <div class="submit-wrap">
        <button type="submit" :disabled="loading">{{ loading ? '推演中…' : '起 盘' }}</button>
        <button type="button" class="ghost" @click="store.reset()">清 空</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </ScrollPanel>

  <div ref="chartArea">
    <ScrollPanel v-if="result" title="命 盘">
      <div class="summary">
        <div v-if="form.name"><span>姓名</span><strong>{{ form.name }}</strong></div>
        <div><span>生肖</span><strong>{{ result.chinese_zodiac }}</strong></div>
        <div><span>日主</span><strong>{{ result.day_master.type }}</strong></div>
        <div><span>起运</span><strong>{{ result.standard_start_age }}</strong></div>
      </div>
      <hr class="ink-divider" />
      <BaZiChart :data="result" />
    </ScrollPanel>

    <ScrollPanel v-if="result" title="大 运">
      <MainDestinyList :data="result.main_destiny" />
    </ScrollPanel>
  </div>

  <div v-if="result" class="export-bar">
    <button type="button" @click="saveAsImage" :disabled="exporting">
      {{ exporting ? '导出中…' : '保存为图片' }}
    </button>
    <button type="button" class="archive-btn" @click="openArchive">
      归 档 保 存
    </button>
    <button
      v-if="hasFortuneCache"
      type="button"
      class="cached-btn"
      @click="viewCachedFortune"
    >
      查 看 上 次 运 势
    </button>
    <button type="button" class="fortune-btn" @click="openFortune">
      {{ hasFortuneCache ? '重 新 推 演' : '运 势 详 解' }}
    </button>
  </div>

  <ConfirmDialog
    :open="archiveOpen"
    title="确认归档此命主信息"
    @confirm="confirmArchive"
    @cancel="cancelArchive"
  >
    <div class="confirm-info">
      <div><span>姓名</span><strong>{{ form.name || '（未填写）' }}</strong></div>
      <div><span>性别</span><strong>{{ form.gender === 'female' ? '女' : '男' }}</strong></div>
      <div><span>阳历生辰</span><strong>{{ formatDobDisplay(form.dob_time) }}</strong></div>
    </div>
    <p class="confirm-hint">
      当前已存 {{ archive.items.length }} / {{ archive.maxArchives }}，
      归档后可在"个人中心"设为主档。
    </p>
    <p v-if="archiveMsg" class="err-line">{{ archiveMsg }}</p>
    <p v-if="archiving" class="hint-line">保存中…</p>
  </ConfirmDialog>

  <ConfirmDialog
    :open="confirmOpen"
    title="请核对出生信息"
    @confirm="confirmFortune"
    @cancel="cancelFortune"
  >
    <div class="confirm-info">
      <div><span>姓名</span><strong>{{ confirmInfo.name }}</strong></div>
      <div><span>性别</span><strong>{{ confirmInfo.gender }}</strong></div>
      <div><span>阳历生辰</span><strong>{{ confirmInfo.dob }}</strong></div>
    </div>
    <p class="confirm-hint">确认无误后将调用命理推演，约需 30 秒。</p>
  </ConfirmDialog>
</template>

<style scoped>
.inputs { max-width: 640px; margin: 0 auto; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
.submit-wrap { text-align: center; margin-top: 10px; display: flex; gap: 12px; justify-content: center; }
.submit-wrap button { padding: 10px 36px; }
.error { color: var(--accent); text-align: center; margin-top: 10px; }

.summary {
  display: flex;
  justify-content: center;
  gap: 48px;
  font-family: var(--font-hand);
  flex-wrap: wrap;
}
.summary div { text-align: center; }
.summary span {
  display: block;
  color: var(--muted);
  letter-spacing: 0.3em;
  font-size: 13px;
  margin-bottom: 6px;
}
.summary strong {
  font-weight: normal;
  font-size: 22px;
  color: var(--accent);
  letter-spacing: 0.2em;
}

.export-bar {
  text-align: center;
  margin: 16px 0 32px;
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}
.fortune-btn {
  background: var(--accent);
  color: var(--paper);
  border-color: var(--accent);
}
.archive-btn {
  background: var(--paper);
  color: var(--ink);
  border-color: var(--ink);
}
.archive-btn:hover {
  background: var(--ink);
  color: var(--paper);
}
.cached-btn {
  background: var(--paper);
  color: var(--accent);
  border-color: var(--accent);
}
.cached-btn:hover {
  background: var(--accent);
  color: var(--paper);
}
.err-line { color: var(--accent); text-align: center; font-size: 12px; margin: 6px 0 0; }
.hint-line { color: var(--muted); text-align: center; font-size: 12px; margin: 6px 0 0; }
.confirm-info {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 6px 18px;
  padding: 4px 6px 12px;
}
.confirm-info div {
  display: contents;
}
.confirm-info span {
  color: var(--muted);
  letter-spacing: 0.3em;
  font-size: 13px;
}
.confirm-info strong {
  font-weight: normal;
  color: var(--ink);
  font-size: 16px;
  letter-spacing: 0.1em;
}
.confirm-hint {
  margin: 6px 0 0;
  font-size: 12px;
  color: var(--muted);
  letter-spacing: 0.15em;
  text-align: center;
}
</style>
