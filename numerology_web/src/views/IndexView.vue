<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

function go(name: string) {
  router.push({ name })
}
</script>

<template>
  <div class="index-wrap">
    <section class="hero">
      <img src="/numerology.png" alt="玄机命理" class="logo" />
      <h1 class="title">玄 机 命 理</h1>
      <p class="subtitle">四 柱 · 六 爻 · 运 势 · 锦 囊</p>
      <p class="tag">以传统术数为形，以现代推演为用。</p>
      <div class="cta">
        <button type="button" @click="go('bazi')">八 字 起 盘</button>
        <button type="button" class="ghost" @click="go('gua')">六 爻 问 卦</button>
        <button v-if="auth.isAuthenticated" type="button" class="ghost" @click="go('me')">
          个 人 中 心
        </button>
        <button v-else type="button" class="ghost" @click="go('login')">登 入</button>
      </div>
    </section>

    <section class="feature-grid">
      <article class="feature">
        <div class="ft-seal">八</div>
        <h3>排 盘</h3>
        <p>阳历生辰 → 四柱十神大运，支持归档保存与图片导出。</p>
      </article>
      <article class="feature">
        <div class="ft-seal">卦</div>
        <h3>卜 卦</h3>
        <p>六爻阴阳序列查询六十四卦，配卦象要旨速览。</p>
      </article>
      <article class="feature">
        <div class="ft-seal">运</div>
        <h3>运 势 详 解</h3>
        <p>姻缘、财运、事业、学业、健康、子嗣六维推断。</p>
      </article>
      <article class="feature">
        <div class="ft-seal">囊</div>
        <h3>今 日 锦 囊</h3>
        <p>主档八字对今日干支，每日一次签评与五维雷达。</p>
      </article>
    </section>

    <p class="disclaim">命理推断基于传统四柱模型，仅作文化参考，不构成决策建议。</p>
  </div>
</template>

<style scoped>
.index-wrap {
  max-width: 960px;
  margin: 0 auto;
  padding: 12px 20px 40px;
}
.hero {
  text-align: center;
  padding: 32px 0 40px;
  border-bottom: 1px dashed var(--line);
}
.logo {
  width: 96px; height: 96px;
  image-rendering: -webkit-optimize-contrast;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.12));
}
.title {
  margin: 16px 0 6px;
  font-family: var(--font-hand);
  font-size: 38px;
  letter-spacing: 0.6em;
  color: var(--ink);
}
.subtitle {
  margin: 0 0 14px;
  font-family: var(--font-hand);
  letter-spacing: 0.5em;
  color: var(--accent);
  font-size: 15px;
}
.tag {
  margin: 0 0 24px;
  font-family: var(--font-serif);
  letter-spacing: 0.2em;
  color: var(--muted);
  font-size: 14px;
}
.cta {
  display: flex; gap: 12px;
  justify-content: center; flex-wrap: wrap;
}
.cta button { padding: 10px 30px; }

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 14px;
  margin: 32px 0;
}
.feature {
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 20px 18px 18px;
  text-align: center;
  font-family: var(--font-serif);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.feature:hover {
  border-color: var(--accent);
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.ft-seal {
  display: inline-flex;
  width: 44px; height: 44px;
  align-items: center; justify-content: center;
  background: var(--accent); color: var(--paper);
  font-family: var(--font-hand);
  font-size: 22px;
  margin-bottom: 12px;
}
.feature h3 {
  margin: 0 0 8px;
  font-family: var(--font-hand);
  letter-spacing: 0.4em;
  color: var(--ink);
  font-size: 16px;
}
.feature p {
  margin: 0;
  font-family: var(--font-hand);
  font-size: 13px;
  line-height: 1.8;
  color: var(--ink-soft);
  letter-spacing: 0.05em;
}

.disclaim {
  text-align: center;
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0.25em;
  margin-top: 24px;
}
</style>
