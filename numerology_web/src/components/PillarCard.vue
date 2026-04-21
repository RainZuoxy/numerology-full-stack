<script setup lang="ts">
import type { BaseStem } from '@/api/types'

defineProps<{
  label: string
  tianGan: BaseStem
  diZhi: BaseStem
  shiShenTg?: string
  shiShenDz?: (string | null)[]
}>()

function elementClass(e: string) {
  const map: Record<string, string> = {
    '金': 'metal', '木': 'wood', '水': 'water', '火': 'fire', '土': 'earth'
  }
  return map[e] || ''
}
</script>

<template>
  <div class="pillar-card">
    <div class="pillar-label">{{ label }}</div>
    <div v-if="shiShenTg" class="ss top">{{ shiShenTg }}</div>
    <div class="char tg" :class="elementClass(tianGan.element)">
      {{ tianGan.type }}
    </div>
    <div class="char dz" :class="elementClass(diZhi.element)">
      {{ diZhi.type }}
    </div>
    <div v-if="shiShenDz && shiShenDz.length" class="ss bottom">
      <div
        v-for="(s, i) in shiShenDz"
        :key="i"
        class="qi-col"
      >
        <template v-if="s">
          <span v-for="(ch, j) in s.split('')" :key="j">{{ ch }}</span>
        </template>
        <span v-else class="placeholder">·</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pillar-card {
  flex: 1;
  min-width: 90px;
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 16px 8px 14px;
  text-align: center;
  font-family: var(--font-hand);
}
.pillar-label {
  font-size: 15px;
  font-weight: bold;
  color: var(--ink);
  letter-spacing: 0.4em;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--line);
}
.char {
  font-size: 40px;
  line-height: 1.2;
  color: var(--ink);
  margin: 2px 0;
}
.char.tg { border-bottom: 1px dashed var(--line); padding-bottom: 6px; margin-bottom: 6px; }

/* 五行色 */
.metal  { color: #a8814b; }
.wood   { color: #3e6b3c; }
.water  { color: #1f3a5f; }
.fire   { color: #9b2d20; }
.earth  { color: #7a5a2e; }

.ss { font-size: 12px; color: var(--ink-soft); letter-spacing: 0.2em; }
.ss.top { margin-bottom: 8px; }
.ss.bottom {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  gap: 10px;
  letter-spacing: normal;
}
.qi-col {
  display: flex;
  flex-direction: column;
  line-height: 1.25;
  font-size: 13px;
  opacity: 0.9;
}
.qi-col .placeholder { color: var(--line); }
</style>
