<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import DateTimePicker from '@/components/DateTimePicker.vue'
import FormField from '@/components/FormField.vue'
import RadarChart from '@/components/RadarChart.vue'
import { useArchiveStore } from '@/stores/archive'
import { useAuthStore } from '@/stores/auth'
import { useBaziStore } from '@/stores/bazi'
import { useFortuneStore } from '@/stores/fortune'
import { useThemeStore } from '@/stores/theme'

const router = useRouter()
const bazi = useBaziStore()
const fortune = useFortuneStore()
const theme = useThemeStore()

const archive = useArchiveStore()
const auth = useAuthStore()
const { items, maxArchives, prediction, predictLoading, error } = storeToRefs(archive)

type TabKey = 'archives' | 'account' | 'settings' | 'about'
const tab = ref<TabKey>('archives')

const newForm = ref({
  name: '',
  gender: 'male' as 'male' | 'female',
  dob_time: '1990-01-19 09:30:00',
})
const creating = ref(false)
const localError = ref('')

const primary = computed(() => items.value.find((i) => i.is_primary) || null)
const todayStr = computed(() => new Date().toISOString().slice(0, 10))

async function createArchive() {
  localError.value = ''
  if (!newForm.value.name.trim()) {
    localError.value = '请填写姓名'
    return
  }
  if (items.value.length >= maxArchives.value) {
    localError.value = `最多只能创建 ${maxArchives.value} 个归档`
    return
  }
  creating.value = true
  try {
    await archive.create({
      name: newForm.value.name.trim(),
      gender: newForm.value.gender,
      dob_time: newForm.value.dob_time,
    })
    newForm.value.name = ''
  } catch (e: any) {
    localError.value = e.message || '创建失败'
  } finally {
    creating.value = false
  }
}

async function removeArchive(id: number) {
  if (!confirm('确定删除该归档？')) return
  try {
    await archive.remove(id)
  } catch (e: any) {
    localError.value = e.message || '删除失败'
  }
}

async function makePrimary(id: number) {
  try {
    await archive.setPrimary(id)
  } catch (e: any) {
    localError.value = e.message || '设置失败'
  }
}

async function runPrediction() {
  if (!primary.value) {
    localError.value = '请先设置主档'
    return
  }
  try {
    await archive.predictToday()
  } catch {
    // error 由 store 暴露
  }
}

onMounted(async () => {
  await archive.refresh()
  await archive.loadToday()
})

function scoreClass(s: number) {
  if (s >= 80) return 'good'
  if (s >= 60) return 'mid'
  if (s >= 40) return 'low'
  return 'warn'
}

const DIM_MINI: Record<string, string> = {
  marriage: '姻', wealth: '财', career: '事', study: '学', health: '康', children: '嗣',
}
function miniLabel(k: string) { return DIM_MINI[k] || k }

const DAILY_DIM_ORDER = ['wealth', 'love', 'career', 'health', 'study'] as const
const DAILY_DIM_LABEL: Record<string, string> = {
  wealth: '财富', love: '爱情', career: '事业', health: '健康', study: '学业',
}
const radarItems = computed(() => {
  const dims = prediction.value?.payload?.dimensions
  if (!dims) return []
  return DAILY_DIM_ORDER.map((k) => ({
    key: k,
    label: DAILY_DIM_LABEL[k],
    value: (dims as any)[k] ?? 0,
  }))
})
const SIGN_CLASS: Record<string, string> = {
  '上上签': 'sign-top',
  '上签':   'sign-good',
  '中平签': 'sign-mid',
  '下签':   'sign-low',
  '下下签': 'sign-bad',
}
function signClass(s?: string) { return s ? SIGN_CLASS[s] || '' : '' }

function goFortune() {
  if (!fortune.hasCache) return
  if (!bazi.result) {
    localError.value = '命盘已失效，请先到八字页重新起盘。'
    return
  }
  router.push({ name: 'fortune' })
}
</script>

<template>
  <div class="personal-layout">
    <!-- 侧边栏 -->
    <aside class="side">
      <section class="card prediction-card">
        <div class="card-title">今 日 锦 囊</div>
        <div v-if="prediction" class="pred-body">
          <div class="pred-head">
            <div class="archive-name">{{ prediction.archive_name }}</div>
            <div class="sign" :class="signClass(prediction.payload.sign)">
              {{ prediction.payload.sign }}
            </div>
          </div>
          <div class="score-line" :class="scoreClass(prediction.payload.score)">
            综 合 <span class="num">{{ prediction.payload.score }}</span><span class="unit">分</span>
          </div>
          <RadarChart :items="radarItems" :size="220" />
          <p class="pred-overall">{{ prediction.payload.overall }}</p>
          <div class="pred-row"><span>宜</span><strong>{{ prediction.payload.highlight }}</strong></div>
          <div class="pred-row"><span>忌</span><strong>{{ prediction.payload.caution }}</strong></div>
          <div class="pred-row"><span>色</span><strong>{{ prediction.payload.lucky_color }}</strong></div>
          <div class="pred-row"><span>方</span><strong>{{ prediction.payload.lucky_direction }}</strong></div>
          <p class="pred-advice">{{ prediction.payload.advice }}</p>
          <div v-if="prediction.day_pillar" class="pred-pillar">{{ prediction.day_pillar }}</div>
          <div class="pred-date">日期：{{ prediction.predict_date }}</div>
        </div>
        <div v-else class="pred-empty">
          <p v-if="!primary">请先在"归档管理"中创建并设置主档。</p>
          <p v-else>今日（{{ todayStr }}）锦囊尚未拆启。</p>
          <button
            type="button"
            @click="runPrediction"
            :disabled="!primary || predictLoading"
            class="pred-btn"
          >
            {{ predictLoading ? '推 演 中…' : '拆 开 今 日 锦 囊' }}
          </button>
          <p class="hint">每账户每日仅可开启一次，以主档八字对今日干支。</p>
        </div>
      </section>

      <section v-if="fortune.hasCache" class="card fortune-card" @click="goFortune">
        <div class="card-title">上 次 运 势 详 解</div>
        <div class="fortune-body">
          <p class="fortune-summary">{{ (fortune.data?.summary || '').slice(0, 42) }}…</p>
          <div class="fortune-mini">
            <span v-for="k in ['marriage','wealth','career','study','health','children']" :key="k" class="mini-chip">
              <span class="mini-label">{{ miniLabel(k) }}</span>
              <span class="mini-score">{{ fortune.data?.dimensions?.[k]?.score ?? '—' }}</span>
            </span>
          </div>
          <div class="fortune-cta">点 击 查 看 完 整 详 解 →</div>
        </div>
      </section>

      <section class="card placeholder-card">
        <div class="card-title">每 日 签 到</div>
        <div class="placeholder">
          <div class="check-seal">待 开 放</div>
          <p>连续签到、积分、小福袋…敬请期待。</p>
        </div>
      </section>
    </aside>

    <!-- 主内容 -->
    <main class="main">
      <nav class="tabs">
        <button :class="{ active: tab === 'archives' }" @click="tab = 'archives'">归档管理</button>
        <button :class="{ active: tab === 'account' }"  @click="tab = 'account'">用户管理</button>
        <button :class="{ active: tab === 'settings' }" @click="tab = 'settings'">系统设置</button>
        <button :class="{ active: tab === 'about' }"    @click="tab = 'about'">版本信息</button>
      </nav>

      <section v-if="tab === 'archives'" class="panel">
        <header class="panel-head">
          <h2>归 档 管 理</h2>
          <div class="meter">{{ items.length }} / {{ maxArchives }}</div>
        </header>

        <div v-if="items.length" class="archive-list">
          <article
            v-for="a in items"
            :key="a.archive_id"
            class="archive-card"
            :class="{ 'is-primary': a.is_primary }"
          >
            <div class="a-top">
              <div class="a-name">{{ a.name }}</div>
              <span v-if="a.is_primary" class="badge">主档</span>
            </div>
            <div class="a-meta">
              <div><span>性别</span><strong>{{ a.gender === 'female' ? '女' : '男' }}</strong></div>
              <div><span>生辰</span><strong>{{ a.dob_time }}</strong></div>
            </div>
            <div class="a-actions">
              <button
                type="button"
                class="ghost"
                :disabled="a.is_primary"
                @click="makePrimary(a.archive_id)"
              >
                {{ a.is_primary ? '当前主档' : '设为主档' }}
              </button>
              <button type="button" class="danger" @click="removeArchive(a.archive_id)">删除</button>
            </div>
          </article>
        </div>
        <p v-else class="empty">尚无归档。请在下方创建。</p>

        <section class="new-block" v-if="items.length < maxArchives">
          <h3>新 增 归 档</h3>
          <div class="grid-2">
            <FormField label="姓名">
              <input v-model="newForm.name" placeholder="如 张三" maxlength="32" />
            </FormField>
            <FormField label="性别">
              <select v-model="newForm.gender">
                <option value="male">男</option>
                <option value="female">女</option>
              </select>
            </FormField>
          </div>
          <FormField label="阳历生辰">
            <DateTimePicker v-model="newForm.dob_time" />
          </FormField>
          <div class="submit">
            <button type="button" @click="createArchive" :disabled="creating">
              {{ creating ? '保 存 中…' : '保 存 归 档' }}
            </button>
          </div>
        </section>
        <p v-else class="limit">已达上限，请先删除一条再创建。</p>

        <p v-if="localError || error" class="err">{{ localError || error }}</p>
      </section>

      <section v-else-if="tab === 'account'" class="panel">
        <h2>用 户 管 理</h2>
        <div class="kv">
          <div><span>账号</span><strong>{{ auth.user?.username }}</strong></div>
          <div><span>昵称</span><strong>{{ auth.user?.nickname || '—' }}</strong></div>
          <div><span>用户 ID</span><strong>{{ auth.user?.user_id }}</strong></div>
          <div><span>来源</span><strong>{{ auth.user?.openid ? '微信' : '密码' }}</strong></div>
        </div>
        <div class="submit">
          <button type="button" class="danger" @click="auth.logout()">退 出 登 录</button>
        </div>
        <p class="hint">更多资料编辑、密码修改等功能将在后续版本开放。</p>
      </section>

      <section v-else-if="tab === 'settings'" class="panel">
        <h2>系 统 设 置</h2>

        <div class="theme-block">
          <div class="block-head">
            <strong>界面主题</strong>
            <p>切换后立即生效，会在本机记住偏好。</p>
          </div>
          <div class="theme-grid">
            <button
              v-for="t in theme.themes"
              :key="t.id"
              type="button"
              class="theme-card"
              :class="{ active: theme.current === t.id }"
              @click="theme.setTheme(t.id)"
            >
              <div class="swatches">
                <span
                  v-for="(c, i) in t.swatches"
                  :key="i"
                  class="swatch"
                  :style="{ background: c }"
                />
              </div>
              <div class="t-name">{{ t.name }}</div>
              <div class="t-sub">{{ t.subtitle }}</div>
              <span v-if="theme.current === t.id" class="t-mark">当前</span>
            </button>
          </div>
        </div>

        <div class="settings-list">
          <div class="row">
            <div><strong>通知提醒</strong><p>每日锦囊拆启后提示（待开放）</p></div>
            <span class="tag">待开放</span>
          </div>
          <div class="row">
            <div><strong>语言</strong><p>简体中文</p></div>
            <span class="tag">默认</span>
          </div>
        </div>
      </section>

      <section v-else-if="tab === 'about'" class="panel">
        <h2>版 本 信 息</h2>
        <div class="kv">
          <div><span>前端版本</span><strong>1.0.0</strong></div>
          <div><span>API 版本</span><strong>v1</strong></div>
          <div><span>协议</span><strong>仅供参考</strong></div>
          <div><span>构建</span><strong>{{ todayStr }}</strong></div>
        </div>
        <p class="hint">命理推断基于传统四柱模型，仅作文化参考，不构成任何决策建议。</p>
      </section>
    </main>
  </div>
</template>

<style scoped>
.personal-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 22px;
  max-width: 1120px;
  margin: 0 auto;
  padding: 24px 20px 40px;
}
.side { display: flex; flex-direction: column; gap: 16px; }
.card {
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 16px 18px;
  font-family: var(--font-serif);
}
.card-title {
  font-size: 15px;
  letter-spacing: 0.5em;
  color: var(--ink);
  border-bottom: 1px solid var(--line);
  padding-bottom: 8px;
  margin-bottom: 12px;
  text-align: center;
}
.pred-head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px;
}
.archive-name {
  font-family: var(--font-hand);
  letter-spacing: 0.2em;
  font-size: 16px;
  color: var(--ink);
}
.score { display: flex; align-items: baseline; gap: 2px; font-family: var(--font-hand); }
.score .num { font-size: 26px; }
.score .unit { font-size: 12px; color: var(--muted); }

.sign {
  font-family: var(--font-hand);
  font-size: 18px;
  letter-spacing: 0.3em;
  padding: 4px 14px;
  border: 1px solid currentColor;
  background: var(--paper);
}
.sign.sign-top  { color: #c0392b; background: #fff1ef; }
.sign.sign-good { color: #a8814b; }
.sign.sign-mid  { color: var(--ink-soft); }
.sign.sign-low  { color: #7a5a2e; }
.sign.sign-bad  { color: #5a4a4a; background: #eee7e3; }

.score-line {
  text-align: center;
  font-family: var(--font-hand);
  letter-spacing: 0.3em;
  font-size: 13px;
  color: var(--muted);
  margin: 4px 0 6px;
}
.score-line .num { font-size: 22px; letter-spacing: 0; margin: 0 2px; }
.score-line .unit { font-size: 12px; color: var(--muted); }
.score-line.good .num { color: #3e6b3c; }
.score-line.mid  .num { color: #a8814b; }
.score-line.low  .num { color: #7a5a2e; }
.score-line.warn .num { color: #9b2d20; }
.score.good .num { color: #3e6b3c; }
.score.mid  .num { color: #a8814b; }
.score.low  .num { color: #7a5a2e; }
.score.warn .num { color: #9b2d20; }

.pred-overall {
  margin: 6px 0 10px;
  font-family: var(--font-hand);
  font-size: 13px;
  line-height: 1.8;
  color: var(--ink);
}
.pred-row {
  display: flex; gap: 10px;
  font-family: var(--font-hand);
  font-size: 13px;
  line-height: 1.9;
  border-top: 1px dashed var(--line);
  padding-top: 4px;
}
.pred-row span {
  flex: 0 0 22px;
  color: var(--muted);
  letter-spacing: 0.2em;
}
.pred-row strong { font-weight: normal; color: var(--ink); }
.pred-advice {
  margin: 10px 0 4px;
  font-family: var(--font-hand);
  font-size: 13px;
  color: var(--ink-soft);
  line-height: 1.8;
}
.pred-pillar {
  text-align: center;
  font-family: var(--font-hand);
  font-size: 12px;
  color: var(--muted);
  margin-top: 6px;
}
.pred-date { text-align: right; font-size: 11px; color: var(--muted); margin-top: 4px; }

.pred-empty { text-align: center; }
.pred-empty p { margin: 6px 0 12px; color: var(--ink-soft); font-size: 13px; }
.pred-btn { width: 100%; }
.pred-empty .hint { color: var(--muted); font-size: 11px; margin-top: 8px; letter-spacing: 0.1em; }

.fortune-card {
  cursor: pointer;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.fortune-card:hover {
  border-color: var(--accent);
  box-shadow: 0 2px 10px rgba(155, 45, 32, 0.12);
}
.fortune-summary {
  margin: 0 0 10px;
  font-family: var(--font-hand);
  font-size: 13px;
  line-height: 1.8;
  color: var(--ink);
}
.fortune-mini {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px 8px;
  margin-bottom: 10px;
}
.mini-chip {
  display: flex; align-items: baseline; gap: 4px;
  border: 1px dashed var(--line);
  padding: 4px 6px;
  font-family: var(--font-hand);
  justify-content: center;
}
.mini-label { color: var(--muted); font-size: 11px; letter-spacing: 0.1em; }
.mini-score { color: var(--accent); font-size: 14px; }
.fortune-cta {
  text-align: right;
  font-size: 12px;
  color: var(--accent);
  letter-spacing: 0.1em;
  font-family: var(--font-hand);
}

.placeholder-card .placeholder {
  text-align: center;
  padding: 10px 4px 4px;
}
.check-seal {
  display: inline-block;
  padding: 8px 22px;
  border: 1px dashed var(--line);
  color: var(--muted);
  font-family: var(--font-hand);
  letter-spacing: 0.5em;
  margin-bottom: 8px;
}
.placeholder p { margin: 0; font-size: 12px; color: var(--muted); letter-spacing: 0.1em; }

.main {
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 0;
  display: flex;
  flex-direction: column;
  min-height: 560px;
}
.tabs {
  display: flex;
  border-bottom: 1px solid var(--line);
  background: linear-gradient(to bottom, rgba(243,236,225,0.8), transparent);
}
.tabs button {
  flex: 1;
  background: transparent;
  border: none;
  border-right: 1px solid var(--line);
  padding: 14px 0;
  font-family: var(--font-hand);
  font-size: 15px;
  letter-spacing: 0.4em;
  color: var(--ink-soft);
  cursor: pointer;
}
.tabs button:last-child { border-right: none; }
.tabs button.active {
  color: var(--accent);
  background: var(--paper);
  border-bottom: 2px solid var(--accent);
}
.panel { padding: 22px 26px 28px; }
.panel h2 {
  margin: 0 0 18px;
  font-family: var(--font-hand);
  letter-spacing: 0.5em;
  font-size: 20px;
  color: var(--ink);
  text-align: center;
}
.panel-head {
  display: flex; align-items: baseline; justify-content: space-between;
  margin-bottom: 14px;
}
.panel-head h2 { margin: 0; text-align: left; }
.meter {
  font-family: var(--font-hand);
  color: var(--muted);
  letter-spacing: 0.2em;
  font-size: 13px;
}

.archive-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 12px;
}
.archive-card {
  border: 1px solid var(--line);
  padding: 12px 14px;
  background: #fbf6ea;
}
.archive-card.is-primary {
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent) inset;
}
.a-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.a-name { font-family: var(--font-hand); font-size: 17px; letter-spacing: 0.2em; color: var(--ink); }
.badge {
  background: var(--accent); color: var(--paper);
  font-size: 11px; letter-spacing: 0.2em;
  padding: 2px 8px;
}
.a-meta { font-family: var(--font-hand); font-size: 13px; line-height: 1.9; color: var(--ink); }
.a-meta span { display: inline-block; width: 40px; color: var(--muted); letter-spacing: 0.15em; }
.a-meta strong { font-weight: normal; }
.a-actions { display: flex; gap: 8px; margin-top: 10px; }
.a-actions button { flex: 1; padding: 6px 0; font-size: 13px; }
.danger { color: var(--accent); border-color: var(--accent); background: var(--paper); }

.new-block { margin-top: 24px; border-top: 1px dashed var(--line); padding-top: 16px; }
.new-block h3 {
  margin: 0 0 12px;
  font-family: var(--font-hand);
  letter-spacing: 0.4em;
  font-size: 15px;
  color: var(--ink);
}
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.submit { text-align: center; margin-top: 14px; }
.submit button { padding: 8px 32px; }
.empty, .limit { text-align: center; color: var(--muted); font-size: 13px; margin: 20px 0; letter-spacing: 0.15em; }
.err { color: var(--accent); text-align: center; margin-top: 10px; font-size: 13px; }

.kv {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 30px;
  font-family: var(--font-hand);
  font-size: 14px;
  max-width: 520px;
  margin: 0 auto 18px;
}
.kv div { border-bottom: 1px dashed var(--line); padding: 6px 0; }
.kv span { display: inline-block; width: 78px; color: var(--muted); letter-spacing: 0.2em; }
.kv strong { font-weight: normal; color: var(--ink); }

.theme-block {
  max-width: 640px;
  margin: 0 auto 24px;
}
.block-head { margin-bottom: 12px; font-family: var(--font-hand); }
.block-head strong { color: var(--ink); letter-spacing: 0.2em; font-weight: normal; font-size: 15px; }
.block-head p { margin: 4px 0 0; color: var(--muted); font-size: 12px; letter-spacing: 0.1em; }

.theme-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}
.theme-card {
  position: relative;
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 14px 14px 12px;
  text-align: left;
  cursor: pointer;
  font-family: var(--font-hand);
  letter-spacing: normal;
  color: var(--ink);
  transition: all 0.2s;
}
.theme-card:hover {
  border-color: var(--accent);
  background: var(--paper);
  color: var(--ink);
}
.theme-card.active {
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent) inset;
  background: var(--paper);
  color: var(--ink);
}
.theme-card .swatches {
  display: flex; gap: 4px;
  margin-bottom: 10px;
}
.theme-card .swatch {
  flex: 1;
  height: 22px;
  border: 1px solid rgba(0,0,0,0.08);
}
.theme-card .t-name {
  font-size: 16px; letter-spacing: 0.25em;
  color: var(--ink);
}
.theme-card .t-sub {
  margin-top: 2px;
  font-size: 12px; color: var(--muted);
  letter-spacing: 0.15em;
}
.theme-card .t-mark {
  position: absolute;
  top: 8px; right: 8px;
  font-size: 10px;
  letter-spacing: 0.2em;
  color: var(--paper);
  background: var(--accent);
  padding: 2px 6px;
}

.settings-list { max-width: 560px; margin: 0 auto; }
.settings-list .row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 2px; border-bottom: 1px dashed var(--line);
  font-family: var(--font-hand);
}
.settings-list .row:last-child { border-bottom: none; }
.settings-list .row strong { font-weight: normal; color: var(--ink); letter-spacing: 0.15em; }
.settings-list .row p { margin: 4px 0 0; color: var(--muted); font-size: 12px; letter-spacing: 0.1em; }
.tag {
  font-size: 11px;
  padding: 2px 10px;
  border: 1px solid var(--line);
  color: var(--muted);
  letter-spacing: 0.2em;
}
.hint { text-align: center; color: var(--muted); font-size: 12px; letter-spacing: 0.15em; margin-top: 18px; }

@media (max-width: 860px) {
  .personal-layout { grid-template-columns: 1fr; }
}
</style>
