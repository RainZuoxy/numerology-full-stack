<script setup lang="ts">
import { computed } from 'vue'

// 12 时辰与时间范围。hour 用中点代表，提交给后端。
// 子时跨日：23:00–01:00，这里用 00:00 作为代表时间。
const SHICHEN = [
  { name: '子时', range: '23:00 – 01:00', hour: 0 },
  { name: '丑时', range: '01:00 – 03:00', hour: 2 },
  { name: '寅时', range: '03:00 – 05:00', hour: 4 },
  { name: '卯时', range: '05:00 – 07:00', hour: 6 },
  { name: '辰时', range: '07:00 – 09:00', hour: 8 },
  { name: '巳时', range: '09:00 – 11:00', hour: 10 },
  { name: '午时', range: '11:00 – 13:00', hour: 12 },
  { name: '未时', range: '13:00 – 15:00', hour: 14 },
  { name: '申时', range: '15:00 – 17:00', hour: 16 },
  { name: '酉时', range: '17:00 – 19:00', hour: 18 },
  { name: '戌时', range: '19:00 – 21:00', hour: 20 },
  { name: '亥时', range: '21:00 – 23:00', hour: 22 },
] as const

const props = defineProps<{ modelValue: number }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: number): void }>()

// 把当前 hour 映射到某个时辰 index
const activeIndex = computed(() => {
  const h = props.modelValue
  // 23 或 0 → 子(0)；1-2 → 丑(1); 3-4 → 寅(2) ...
  return Math.floor(((h + 1) % 24) / 2)
})

function select(i: number) {
  emit('update:modelValue', SHICHEN[i].hour)
}
</script>

<template>
  <div class="shichen">
    <div class="grid">
      <button
        v-for="(s, i) in SHICHEN"
        :key="s.name"
        type="button"
        class="cell"
        :class="{ active: i === activeIndex }"
        @click="select(i)"
      >
        <span class="name">{{ s.name }}</span>
        <span class="range">{{ s.range }}</span>
      </button>
    </div>
    <p class="hint">按阳历出生时间对应时段选择；若不确定可依据中间一小时判断。</p>
  </div>
</template>

<style scoped>
.shichen {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}
.cell {
  background: var(--paper);
  border: 1px solid var(--line);
  color: var(--ink);
  padding: 10px 6px;
  cursor: pointer;
  font-family: var(--font-hand);
  border-radius: 2px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  transition: all 0.15s;
  letter-spacing: normal;
}
.cell:hover {
  border-color: var(--accent-soft);
  color: var(--accent);
  background: var(--paper);
}
.cell.active {
  background: var(--accent);
  border-color: var(--accent);
  color: var(--paper);
}
.cell .name {
  font-size: 18px;
  letter-spacing: 0.2em;
}
.cell .range {
  font-size: 11px;
  font-family: Menlo, monospace;
  letter-spacing: 0.05em;
  opacity: 0.8;
}
.hint {
  margin: 0;
  text-align: center;
  font-size: 12px;
  color: var(--muted);
  letter-spacing: 0.1em;
}

@media (max-width: 520px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
</style>
