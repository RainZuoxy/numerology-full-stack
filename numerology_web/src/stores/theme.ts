import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export interface ThemeDef {
  id: string
  name: string
  subtitle: string
  swatches: string[]   // 4 种代表色，用于 UI 预览
}

export const THEMES: ThemeDef[] = [
  {
    id: 'inkwash',
    name: '水墨宣纸',
    subtitle: '墨色 · 朱砂 · 竹纹',
    swatches: ['#1f1a15', '#9b2d20', '#c9b89a', '#f3ece1'],
  },
  {
    id: 'zuihuayin',
    name: '醉花荫',
    subtitle: '桃珊 · 叶青 · 暖杏',
    swatches: ['#EC776E', '#FEB48E', '#92A470', '#FFBC8F'],
  },
  {
    id: 'qinyuanchun',
    name: '沁园春',
    subtitle: '烟波 · 天水 · 桃腮',
    swatches: ['#205064', '#76A4B3', '#D7E8F8', '#ECA7A7'],
  },
  {
    id: 'qingyuan',
    name: '青玉案',
    subtitle: '松烟 · 苔色 · 新篁',
    swatches: ['#367349', '#97CA9B', '#92AE71', '#86A993'],
  },
]

const KEY = 'ui_theme'
const DEFAULT_ID = 'inkwash'

function apply(id: string) {
  document.documentElement.dataset.theme = id
}

export const useThemeStore = defineStore('theme', () => {
  const current = ref<string>(localStorage.getItem(KEY) || DEFAULT_ID)
  apply(current.value)

  watch(current, (v) => {
    localStorage.setItem(KEY, v)
    apply(v)
  })

  function setTheme(id: string) {
    if (!THEMES.find((t) => t.id === id)) return
    current.value = id
  }

  return { current, setTheme, themes: THEMES }
})
