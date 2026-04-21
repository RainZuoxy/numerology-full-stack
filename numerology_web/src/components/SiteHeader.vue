<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useFortuneStore } from '@/stores/fortune'

const auth = useAuthStore()
const fortune = useFortuneStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="site-header">
    <RouterLink to="/" class="brand" title="回到首页">
      <img src="/numerology.png" alt="logo" class="brand-logo" />
      <span class="title">玄机命理</span>
    </RouterLink>
    <nav v-if="auth.isAuthenticated">
      <RouterLink to="/bazi">八字</RouterLink>
      <span class="dot">·</span>
      <RouterLink to="/gua">卦象</RouterLink>
      <template v-if="fortune.hasCache">
        <span class="dot">·</span>
        <RouterLink to="/fortune">运势</RouterLink>
      </template>
      <span class="dot">·</span>
      <RouterLink to="/me">个人中心</RouterLink>
    </nav>
    <div class="user">
      <template v-if="auth.isAuthenticated">
        <span class="who">{{ auth.user?.nickname || auth.user?.username }}</span>
        <button class="ghost" @click="handleLogout">退出</button>
      </template>
      <template v-else>
        <RouterLink to="/login">登入</RouterLink>
      </template>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  display: flex;
  align-items: center;
  padding: 18px 36px;
  border-bottom: 1px solid var(--line);
  background: linear-gradient(to bottom, rgba(251, 246, 234, 0.9), transparent);
}
.brand {
  display: flex; align-items: center; gap: 12px; flex: 0 0 auto;
  color: inherit;
}
.brand:hover { color: inherit; }
.brand-logo {
  width: 38px; height: 38px;
  object-fit: contain;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15));
}
.title { font-family: var(--font-hand); font-size: 22px; letter-spacing: 0.4em; }

nav {
  flex: 1;
  text-align: center;
  letter-spacing: 0.4em;
  font-size: 15px;
}
nav a { color: var(--ink-soft); }
nav a.router-link-active { color: var(--accent); }
.dot { color: var(--line); margin: 0 12px; }

.user { display: flex; align-items: center; gap: 14px; font-size: 14px; }
.who { color: var(--ink-soft); letter-spacing: 0.1em; }
</style>
