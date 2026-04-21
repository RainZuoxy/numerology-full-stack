<script setup lang="ts">
defineProps<{
  open: boolean
  title?: string
}>()
const emit = defineEmits<{
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="mask" @click.self="emit('cancel')">
      <div class="dialog">
        <div class="title">{{ title || '请确认' }}</div>
        <div class="body">
          <slot />
        </div>
        <div class="actions">
          <button class="ghost" type="button" @click="emit('cancel')">取 消</button>
          <button type="button" @click="emit('confirm')">确 认</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.mask {
  position: fixed; inset: 0;
  background: rgba(31, 26, 21, 0.45);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.dialog {
  background: var(--paper);
  border: 1px solid var(--line);
  box-shadow: 0 6px 30px rgba(0,0,0,0.2);
  max-width: 420px;
  width: calc(100% - 48px);
  padding: 22px 24px 18px;
  font-family: var(--font-serif);
}
.title {
  font-size: 18px;
  letter-spacing: 0.3em;
  text-align: center;
  color: var(--ink);
  border-bottom: 1px solid var(--line);
  padding-bottom: 10px;
  margin-bottom: 14px;
}
.body {
  font-size: 15px;
  color: var(--ink);
  line-height: 1.9;
  font-family: var(--font-hand);
}
.actions {
  display: flex; justify-content: flex-end; gap: 12px;
  margin-top: 18px;
}
.actions button { padding: 6px 22px; }
</style>
