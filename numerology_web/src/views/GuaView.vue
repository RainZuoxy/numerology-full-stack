<script setup lang="ts">
import { storeToRefs } from 'pinia'
import ScrollPanel from '@/components/ScrollPanel.vue'
import TrigramEditor from '@/components/TrigramEditor.vue'
import TrigramResult from '@/components/TrigramResult.vue'
import { useGuaStore } from '@/stores/gua'

const store = useGuaStore()
const { series, result, loading, error } = storeToRefs(store)
</script>

<template>
  <ScrollPanel title="起 卦" subtitle="按爻取象 · 六十四卦">
    <div class="gua-layout">
      <TrigramEditor v-model="series" />
      <div class="side">
        <p class="series-text">{{ series }}</p>
        <div class="btns">
          <button @click="store.query()" :disabled="loading">{{ loading ? '卜算中…' : '起 卦' }}</button>
          <button class="ghost" @click="store.reset()">清 空</button>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </div>
  </ScrollPanel>

  <ScrollPanel v-if="result" title="卦 象">
    <TrigramResult :data="result" />
  </ScrollPanel>
</template>

<style scoped>
.gua-layout {
  display: flex;
  justify-content: center;
  gap: 48px;
  align-items: center;
}
.side { display: flex; flex-direction: column; align-items: center; gap: 14px; }
.series-text {
  font-family: Menlo, monospace;
  font-size: 18px;
  letter-spacing: 0.6em;
  color: var(--ink-soft);
  margin: 0;
}
.btns { display: flex; gap: 12px; }
.error { color: var(--accent); font-size: 13px; }
</style>
