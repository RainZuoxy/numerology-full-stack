<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import ScrollPanel from '@/components/ScrollPanel.vue'
import FormField from '@/components/FormField.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const mode = ref<'login' | 'register'>('login')
const username = ref('')
const password = ref('')
const nickname = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    if (mode.value === 'login') {
      await auth.login(username.value, password.value)
    } else {
      await auth.register(username.value, password.value, nickname.value || undefined)
    }
    const target = (route.query.redirect as string) || '/bazi'
    router.push(target)
  } catch (e: any) {
    error.value = e.message || '操作失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <ScrollPanel title="入门" subtitle="登入 · 注册">
    <div class="login-form">
      <div class="tabs">
        <button
          :class="['tab-btn', { active: mode === 'login' }]"
          type="button"
          @click="mode = 'login'"
        >登 入</button>
        <button
          :class="['tab-btn', { active: mode === 'register' }]"
          type="button"
          @click="mode = 'register'"
        >注 册</button>
      </div>

      <form @submit.prevent="submit">
        <FormField label="用户名">
          <input v-model="username" required autocomplete="username" />
        </FormField>
        <FormField label="密码" hint="至少 6 位字符">
          <input v-model="password" type="password" required autocomplete="current-password" />
        </FormField>
        <FormField v-if="mode === 'register'" label="昵称（可选）">
          <input v-model="nickname" />
        </FormField>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" :disabled="loading" class="submit">
          {{ loading ? '稍候…' : (mode === 'login' ? '登 入' : '注 册') }}
        </button>
      </form>

      <hr class="ink-divider" />
      <p class="wechat-hint">小程序环境请调用 <code>auth.wechatLogin(code)</code>。</p>
    </div>
  </ScrollPanel>
</template>

<style scoped>
.login-form { max-width: 360px; margin: 0 auto; }
.tabs {
  display: flex;
  margin-bottom: 28px;
  border-bottom: 1px solid var(--line);
}
.tab-btn {
  flex: 1;
  padding: 10px 0;
  background: transparent;
  color: var(--muted);
  border: 0;
  border-bottom: 2px solid transparent;
  letter-spacing: 0.4em;
  font-size: 15px;
  border-radius: 0;
}
.tab-btn:hover { color: var(--ink); background: transparent; }
.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }

.submit { width: 100%; padding: 12px 0; font-size: 15px; }
.error { color: var(--accent); font-size: 13px; letter-spacing: 0.1em; }
.wechat-hint { color: var(--muted); font-size: 12px; text-align: center; letter-spacing: 0.1em; }
.wechat-hint code {
  font-family: Menlo, monospace;
  background: var(--bg-soft);
  padding: 1px 6px;
}
</style>
