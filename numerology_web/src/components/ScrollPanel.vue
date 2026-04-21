<script setup lang="ts">
defineProps<{ title?: string; subtitle?: string }>()
</script>

<template>
  <section class="scroll-panel">
    <div class="edge top"></div>
    <div class="body">
      <header v-if="title || subtitle" class="panel-header">
        <h2 v-if="title">{{ title }}</h2>
        <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
      </header>
      <slot />
    </div>
    <div class="edge bottom"></div>
  </section>
</template>

<style scoped>
.scroll-panel {
  background: var(--paper);
  box-shadow: var(--shadow);
  margin: 24px 0;
  position: relative;
}
.edge {
  height: 10px;
  background: linear-gradient(to bottom, var(--gold), #8a673a);
}
.edge.bottom { background: linear-gradient(to top, var(--gold), #8a673a); }
.body {
  padding: 32px 40px;
  border-left: 1px solid var(--line);
  border-right: 1px solid var(--line);
}
.panel-header {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 18px;
  border-bottom: 1px dashed var(--line);
}
.panel-header h2 {
  margin: 0;
  font-family: var(--font-hand);
  font-weight: normal;
  font-size: 24px;
  letter-spacing: 0.6em;
  color: var(--ink);
}
.subtitle {
  margin: 8px 0 0;
  color: var(--muted);
  letter-spacing: 0.3em;
  font-size: 13px;
}
</style>
