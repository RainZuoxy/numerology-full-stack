<script setup lang="ts">
import { computed } from 'vue'
import YaoLine from './YaoLine.vue'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string): void }>()

const lines = computed(() => props.modelValue.split('').map(c => c === '1'))

function toggle(i: number) {
  const arr = props.modelValue.split('')
  arr[i] = arr[i] === '1' ? '0' : '1'
  emit('update:modelValue', arr.join(''))
}
</script>

<template>
  <div class="trigram-editor">
    <!-- 从上到下：上爻 → 初爻 -->
    <div class="side-label">上</div>
    <div class="lines">
      <div v-for="i in [5,4,3,2,1,0]" :key="i" class="row">
        <span class="idx">{{ ['初','二','三','四','五','上'][i] }}</span>
        <YaoLine :yang="lines[i]" clickable @toggle="toggle(i)" />
        <span class="yy">{{ lines[i] ? '阳' : '阴' }}</span>
      </div>
    </div>
    <div class="side-label">下</div>
  </div>
</template>

<style scoped>
.trigram-editor {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 0;
  font-family: var(--font-hand);
}
.side-label {
  color: var(--muted);
  letter-spacing: 0.4em;
  margin: 6px 0;
  font-size: 13px;
}
.lines { display: flex; flex-direction: column; }
.row { display: flex; align-items: center; gap: 12px; }
.idx { width: 24px; text-align: right; color: var(--muted); font-size: 13px; }
.yy { width: 24px; color: var(--ink-soft); font-size: 13px; }
</style>
