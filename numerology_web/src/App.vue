<script setup lang="ts">
import { RouterView } from 'vue-router'
import SiteHeader from '@/components/SiteHeader.vue'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const auth = useAuthStore()
onMounted(() => auth.hydrate())
</script>

<template>
  <div class="app-shell">
    <SiteHeader />
    <main class="container">
      <RouterView />
    </main>
    <footer class="site-footer">
      <span>—— 玄机命理 · 为学习研究所用 ——</span>
    </footer>
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
main { flex: 1; }
.site-footer {
  text-align: center;
  padding: 24px 0;
  color: var(--muted);
  font-size: 13px;
  letter-spacing: 0.3em;
}
</style>
