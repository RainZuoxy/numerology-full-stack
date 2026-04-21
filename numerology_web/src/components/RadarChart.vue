<script setup lang="ts">
import { computed } from 'vue'

interface Item { key: string; label: string; value: number }

const props = withDefaults(
  defineProps<{ items: Item[]; size?: number; max?: number }>(),
  { size: 220, max: 100 },
)

const cx = computed(() => props.size / 2)
const cy = computed(() => props.size / 2)
const R = computed(() => props.size / 2 - 26)

function pointOn(ratio: number, i: number, n: number) {
  const angle = -Math.PI / 2 + (2 * Math.PI * i) / n
  return [cx.value + R.value * ratio * Math.cos(angle), cy.value + R.value * ratio * Math.sin(angle)]
}

const rings = [0.25, 0.5, 0.75, 1]

const axes = computed(() =>
  props.items.map((_, i) => {
    const [x, y] = pointOn(1, i, props.items.length)
    return { x, y }
  }),
)
const labels = computed(() =>
  props.items.map((it, i) => {
    const [x, y] = pointOn(1.15, i, props.items.length)
    return { x, y, label: it.label, value: it.value }
  }),
)
const polygonPoints = computed(() =>
  props.items
    .map((it, i) => {
      const ratio = Math.max(0, Math.min(1, it.value / props.max))
      const [x, y] = pointOn(ratio, i, props.items.length)
      return `${x.toFixed(2)},${y.toFixed(2)}`
    })
    .join(' '),
)
const ringPoints = (ratio: number) =>
  props.items
    .map((_, i) => {
      const [x, y] = pointOn(ratio, i, props.items.length)
      return `${x.toFixed(2)},${y.toFixed(2)}`
    })
    .join(' ')
</script>

<template>
  <svg :width="size" :height="size" class="radar" :viewBox="`0 0 ${size} ${size}`">
    <!-- 环 -->
    <polygon
      v-for="r in rings"
      :key="r"
      :points="ringPoints(r)"
      class="ring"
    />
    <!-- 轴 -->
    <line
      v-for="(a, i) in axes"
      :key="i"
      :x1="cx" :y1="cy"
      :x2="a.x" :y2="a.y"
      class="axis"
    />
    <!-- 数据多边形 -->
    <polygon :points="polygonPoints" class="data" />
    <!-- 标签 -->
    <g v-for="(l, i) in labels" :key="'l'+i">
      <text :x="l.x" :y="l.y" class="axis-label" text-anchor="middle" dominant-baseline="middle">
        {{ l.label }}
      </text>
      <text :x="l.x" :y="l.y + 14" class="axis-value" text-anchor="middle" dominant-baseline="middle">
        {{ l.value }}
      </text>
    </g>
  </svg>
</template>

<style scoped>
.radar { display: block; margin: 0 auto; }
.ring {
  fill: none;
  stroke: var(--line);
  stroke-dasharray: 2 3;
  stroke-width: 1;
  opacity: 0.6;
}
.axis {
  stroke: var(--line);
  stroke-width: 1;
  opacity: 0.5;
}
.data {
  fill: var(--accent);
  fill-opacity: 0.22;
  stroke: var(--accent);
  stroke-width: 1.5;
}
.axis-label {
  font-family: var(--font-hand);
  font-size: 12px;
  letter-spacing: 0.1em;
  fill: var(--ink);
}
.axis-value {
  font-family: var(--font-hand);
  font-size: 11px;
  fill: var(--muted);
}
</style>
