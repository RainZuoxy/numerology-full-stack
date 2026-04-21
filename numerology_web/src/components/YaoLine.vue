<script setup lang="ts">
defineProps<{
  yang: boolean
  clickable?: boolean
}>()
const emit = defineEmits<{ (e: 'toggle'): void }>()
</script>

<template>
  <div
    class="yao"
    :class="{ clickable }"
    @click="clickable && emit('toggle')"
  >
    <template v-if="yang">
      <div class="bar"></div>
    </template>
    <template v-else>
      <div class="bar half"></div>
      <div class="gap"></div>
      <div class="bar half"></div>
    </template>
  </div>
</template>

<style scoped>
.yao {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 14px;
  margin: 7px 0;
  width: 120px;
}
.yao.clickable { cursor: pointer; }
.yao.clickable:hover .bar { background: var(--accent); }
.bar {
  flex: 1;
  height: 7px;
  background: var(--ink);
  transition: background 0.2s;
}
.bar.half { flex: 0 0 calc(50% - 8px); }
.gap { flex: 0 0 16px; }
</style>
