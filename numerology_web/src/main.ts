import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/main.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)

// 初始化主题（在挂载前应用到 <html>，避免闪烁）
import { useThemeStore } from './stores/theme'
useThemeStore()

app.mount('#app')
