<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import ShichenPicker from './ShichenPicker.vue'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string): void }>()

// 解析 "YYYY-MM-DD HH:MM:SS"
function parse(s: string) {
  const m = s.match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})$/)
  if (!m) {
    const now = new Date()
    return {
      date: `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`,
      hour: now.getHours(),
    }
  }
  return { date: `${m[1]}-${m[2]}-${m[3]}`, hour: +m[4] }
}

const parsed = parse(props.modelValue)
const date = ref(parsed.date)
const hour = ref(parsed.hour)

const combined = computed(() =>
  `${date.value} ${String(hour.value).padStart(2, '0')}:00:00`
)

watch(combined, (v) => {
  if (v !== props.modelValue) emit('update:modelValue', v)
})

watch(() => props.modelValue, (v) => {
  if (v === combined.value) return
  const p = parse(v)
  date.value = p.date
  hour.value = p.hour
})
</script>

<template>
  <div class="dt-picker">
    <div class="date-part">
      <label class="sub-label">阳历日期</label>
      <input type="date" v-model="date" />
    </div>
    <div class="time-part">
      <label class="sub-label">出生时辰</label>
      <ShichenPicker v-model="hour" />
    </div>
  </div>
</template>

<style scoped>
.dt-picker {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 16px;
}
.sub-label {
  display: block;
  font-size: 12px;
  color: var(--muted);
  letter-spacing: 0.3em;
  margin-bottom: 8px;
}
.date-part input[type="date"] {
  width: 100%;
  font-family: var(--font-serif);
  font-size: 15px;
  padding: 8px 10px;
}
</style>
