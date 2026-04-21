<script setup lang="ts">
import type { GuaResponse } from '@/api/types'

defineProps<{ data: GuaResponse }>()
</script>

<template>
  <div class="result">
    <div class="icon">{{ data.value.icon }}</div>
    <div class="meta">
      <h3>{{ data.value.name }}</h3>
      <p class="no">第 {{ data.value.index }} 卦</p>
      <dl>
        <div>
          <dt>上卦</dt>
          <dd>{{ data.value.up_trigram.icon }} {{ data.value.up_trigram.name }}</dd>
        </div>
        <div>
          <dt>下卦</dt>
          <dd>{{ data.value.down_trigram.icon }} {{ data.value.down_trigram.name }}</dd>
        </div>
      </dl>
    </div>
  </div>
</template>

<style scoped>
.result {
  display: flex;
  gap: 32px;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
}
.icon {
  font-size: 96px;
  color: var(--accent);
  line-height: 1;
}
.meta h3 {
  font-family: var(--font-hand);
  font-weight: normal;
  font-size: 26px;
  letter-spacing: 0.4em;
  margin: 0 0 4px;
  color: var(--ink);
}
.no {
  color: var(--muted);
  letter-spacing: 0.2em;
  font-size: 13px;
  margin: 0 0 14px;
}
dl { margin: 0; display: flex; flex-direction: column; gap: 6px; }
dl div { display: flex; gap: 14px; }
dt { color: var(--muted); letter-spacing: 0.2em; font-size: 13px; width: 36px; }
dd { margin: 0; font-family: var(--font-hand); font-size: 16px; color: var(--ink); }
</style>
