<script setup lang="ts">
import type { MainDestinyChart } from '@/api/types'

defineProps<{ data: MainDestinyChart }>()

function dzList(dz: (string | null)[]): string[] {
  return dz.filter((x): x is string => !!x)
}
</script>

<template>
  <ul class="destiny-list">
    <li v-for="item in data.items" :key="item.origin_item.name">
      <div class="age">{{ item.schedule[0] }} - {{ item.schedule[1] }}</div>
      <div class="gz">
        <span>{{ item.origin_item.tian_gan.type }}</span>
        <span>{{ item.origin_item.di_zhi.type }}</span>
      </div>
      <hr class="mini-divider" />
      <div class="ss-group">
        <!-- 天干十神 -->
        <div class="ss-col tg">
          <span v-for="(ch, i) in item.shi_shen[0].split('')" :key="'tg'+i">{{ ch }}</span>
        </div>
        <span v-if="dzList(item.shi_shen[1]).length" class="ss-sep">·</span>
        <!-- 地支藏干十神：每个气一列 -->
        <div
          v-for="(term, idx) in dzList(item.shi_shen[1])"
          :key="'dz'+idx"
          class="ss-col dz"
        >
          <span v-for="(ch, i) in term.split('')" :key="i">{{ ch }}</span>
        </div>
      </div>
    </li>
  </ul>
</template>

<style scoped>
.destiny-list {
  list-style: none;
  margin: 0; padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(92px, 1fr));
  gap: 10px;
}
.destiny-list li {
  text-align: center;
  padding: 14px 6px;
  background: var(--paper);
  border: 1px solid var(--line);
  font-family: var(--font-hand);
}
.age { color: var(--muted); font-size: 12px; letter-spacing: 0.15em; }
.gz {
  font-size: 26px;
  margin: 8px 0 4px;
  color: var(--ink);
  display: flex;
  justify-content: center;
  gap: 2px;
}
.mini-divider {
  border: 0;
  border-top: 1px dashed var(--line);
  margin: 6px 14px;
}
.ss-group {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
  padding-top: 4px;
}
/* 藏干列之间稍紧一点 */
.ss-col.dz + .ss-col.dz { margin-left: 2px; }
/* 竖排单列 */
.ss-col {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
  font-size: 13px;
  letter-spacing: 0.05em;
}
.ss-col.tg { color: var(--ink-soft); }
.ss-col.dz { color: var(--ink-soft); }
.ss-sep {
  color: var(--line);
  font-size: 14px;
  line-height: 1;
  margin: 0 -1px;
}
</style>
