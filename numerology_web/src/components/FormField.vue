<script setup lang="ts">
defineProps<{ label: string; hint?: string }>()
</script>

<template>
  <div class="form-field">
    <label>{{ label }}</label>
    <slot />
    <p v-if="hint" class="hint">{{ hint }}</p>
  </div>
</template>

<style scoped>
.form-field { margin-bottom: 18px; }
.hint { margin: 6px 0 0; color: var(--muted); font-size: 12px; letter-spacing: 0.1em; }
</style>
