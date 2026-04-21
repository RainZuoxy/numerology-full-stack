<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import ScrollPanel from '@/components/ScrollPanel.vue'
import QianTongLoader from '@/components/QianTongLoader.vue'
import { useBaziStore } from '@/stores/bazi'
import { useFortuneStore } from '@/stores/fortune'
import { exportElementAsPng } from '@/utils/exportImage'

const router = useRouter()
const bazi = useBaziStore()
const fortune = useFortuneStore()
const { data, loading, error } = storeToRefs(fortune)

const exportArea = ref<HTMLElement | null>(null)
const exporting = ref(false)
const exportErr = ref('')

async function saveAsImage() {
  if (!exportArea.value) return
  exporting.value = true
  exportErr.value = ''
  try {
    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)
    const who = (bazi.form.name || 'fortune').replace(/[^\w\u4e00-\u9fa5-]/g, '_')
    await exportElementAsPng(exportArea.value, `${who}_运势详解_${ts}.png`)
  } catch (e: any) {
    exportErr.value = `导出失败：${e.message || e}`
  } finally {
    exporting.value = false
  }
}

const DIM_ORDER = ['marriage', 'wealth', 'career', 'study', 'health', 'children'] as const
const DIM_FALLBACK: Record<string, string> = {
  marriage: '姻缘', wealth: '财运', career: '事业',
  study: '学业', health: '健康', children: '子嗣',
}
const DIM_ICON: Record<string, string> = {
  marriage: '囍', wealth: '財', career: '業',
  study: '學', health: '康', children: '嗣',
}

const orderedDims = computed(() => {
  if (!data.value) return []
  return DIM_ORDER
    .filter((k) => data.value!.dimensions[k])
    .map((k) => ({ key: k, ...data.value!.dimensions[k] }))
})

function scoreClass(s: number) {
  if (s >= 80) return 'good'
  if (s >= 60) return 'mid'
  if (s >= 40) return 'low'
  return 'warn'
}

async function retry() {
  if (!bazi.result) return
  await fortune.analyze(bazi.result, undefined, true)
}

function back() {
  router.push({ name: 'bazi' })
}

onMounted(async () => {
  if (!bazi.result) {
    router.replace({ name: 'bazi' })
    return
  }
  await fortune.analyze(bazi.result)
})
</script>

<template>
  <ScrollPanel title="运 势 详 解" subtitle="姻缘 · 财运 · 事业 · 学业 · 健康 · 子嗣">
    <div v-if="loading" class="state">
      <QianTongLoader />
    </div>

    <div v-else-if="error" class="state error-state">
      <p class="err">{{ error }}</p>
      <div class="actions">
        <button class="ghost" @click="back">返 回</button>
        <button @click="retry">再 试 一 次</button>
      </div>
    </div>

    <div v-else-if="data" class="result">
      <div ref="exportArea" class="export-area">
      <section class="summary-block">
        <h3>整 体</h3>
        <p>{{ data.summary }}</p>
      </section>

      <div class="dim-grid">
        <article
          v-for="d in orderedDims"
          :key="d.key"
          class="dim-card"
        >
          <header>
            <div class="icon">{{ DIM_ICON[d.key] || '·' }}</div>
            <div class="label">{{ d.label || DIM_FALLBACK[d.key] }}</div>
            <div class="score" :class="scoreClass(d.score)">
              <span class="num">{{ d.score }}</span><span class="unit">分</span>
            </div>
          </header>
          <p class="overall">{{ d.overall }}</p>

          <div v-if="d.insights?.length" class="block">
            <div class="block-title">要 点</div>
            <ul>
              <li v-for="(it, i) in d.insights" :key="'i'+i">{{ it }}</li>
            </ul>
          </div>

          <div v-if="d.suggestions?.length" class="block">
            <div class="block-title">建 议</div>
            <ul>
              <li v-for="(it, i) in d.suggestions" :key="'s'+i">{{ it }}</li>
            </ul>
          </div>

          <div v-if="d.timing" class="block timing">
            <div class="block-title">时 机</div>
            <p>{{ d.timing }}</p>
          </div>
        </article>
      </div>

      <p class="remarks">{{ data.remarks }}</p>
      </div>

      <p v-if="exportErr" class="err-line">{{ exportErr }}</p>
      <div class="actions bottom">
        <button class="ghost" @click="back">返 回 命 盘</button>
        <button class="img-btn" @click="saveAsImage" :disabled="exporting">
          {{ exporting ? '导 出 中…' : '保 存 为 图 片' }}
        </button>
        <button @click="retry" :disabled="loading">重 新 推 演</button>
      </div>
    </div>
  </ScrollPanel>
</template>

<style scoped>
.state {
  min-height: 320px;
  display: flex; align-items: center; justify-content: center;
  flex-direction: column;
}
.error-state .err {
  color: var(--accent);
  font-family: var(--font-hand);
  letter-spacing: 0.2em;
  margin-bottom: 18px;
}
.actions { display: flex; gap: 14px; justify-content: center; }
.actions.bottom { margin: 24px 0 8px; }

.summary-block {
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 18px 22px;
  margin-bottom: 22px;
}
.summary-block h3 {
  margin: 0 0 10px;
  font-family: var(--font-serif);
  letter-spacing: 0.4em;
  font-size: 16px;
  color: var(--ink);
  border-bottom: 1px dashed var(--line);
  padding-bottom: 6px;
}
.summary-block p {
  margin: 0;
  font-family: var(--font-hand);
  font-size: 15px;
  line-height: 1.9;
  color: var(--ink);
  letter-spacing: 0.05em;
}

.dim-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}
.dim-card {
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 16px 18px 18px;
  font-family: var(--font-serif);
  display: flex;
  flex-direction: column;
}
.dim-card header {
  display: flex; align-items: center; gap: 12px;
  border-bottom: 1px solid var(--line);
  padding-bottom: 10px;
  margin-bottom: 10px;
}
.dim-card .icon {
  font-size: 26px;
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  border: 1px solid var(--line);
  color: var(--accent);
  font-family: var(--font-hand);
}
.dim-card .label {
  flex: 1;
  font-size: 18px;
  letter-spacing: 0.4em;
  color: var(--ink);
}
.dim-card .score {
  display: flex; align-items: baseline; gap: 2px;
  font-family: var(--font-hand);
}
.dim-card .score .num { font-size: 24px; letter-spacing: 0.02em; }
.dim-card .score .unit { font-size: 12px; color: var(--muted); }
.score.good .num { color: #3e6b3c; }
.score.mid  .num { color: #a8814b; }
.score.low  .num { color: #7a5a2e; }
.score.warn .num { color: #9b2d20; }

.overall {
  margin: 0 0 10px;
  font-family: var(--font-hand);
  font-size: 14px;
  line-height: 1.9;
  color: var(--ink);
}
.block { margin-top: 8px; }
.block-title {
  font-size: 12px;
  color: var(--muted);
  letter-spacing: 0.4em;
  margin-bottom: 4px;
}
.block ul {
  margin: 0; padding-left: 18px;
  font-family: var(--font-hand);
  font-size: 14px;
  line-height: 1.85;
  color: var(--ink);
}
.block.timing p {
  margin: 0;
  font-family: var(--font-hand);
  font-size: 14px;
  color: var(--ink-soft);
  letter-spacing: 0.05em;
}

.remarks {
  margin: 24px auto 4px;
  text-align: center;
  max-width: 640px;
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0.15em;
}
.export-area {
  background: var(--paper);
  padding: 4px 0;
}
.img-btn {
  background: var(--paper);
  color: var(--ink);
  border-color: var(--ink);
}
.img-btn:hover {
  background: var(--ink);
  color: var(--paper);
}
.err-line {
  text-align: center;
  color: var(--accent);
  font-size: 12px;
  margin: 10px 0 0;
}
</style>
