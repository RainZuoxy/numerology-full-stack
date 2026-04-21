<script setup lang="ts">
import PillarCard from './PillarCard.vue'
import type { BaZiResponse } from '@/api/types'

const props = defineProps<{ data: BaZiResponse }>()

const pillars = () => {
  const b = props.data.ba_zi
  const s = props.data.shi_shen
  return [
    { label: '年柱', tg: b.tg_year, dz: b.dz_year, ssTg: s.tg_year,  ssDz: s.dz_year  },
    { label: '月柱', tg: b.tg_month, dz: b.dz_month, ssTg: s.tg_month, ssDz: s.dz_month },
    { label: '日柱', tg: b.tg_day,  dz: b.dz_day,  ssTg: '日主',    ssDz: s.dz_day   },
    { label: '时柱', tg: b.tg_hour, dz: b.dz_hour, ssTg: s.tg_hour,  ssDz: s.dz_hour  },
  ]
}
</script>

<template>
  <div class="bazi-grid">
    <PillarCard
      v-for="p in pillars()"
      :key="p.label"
      :label="p.label"
      :tian-gan="p.tg"
      :di-zhi="p.dz"
      :shi-shen-tg="p.ssTg"
      :shi-shen-dz="p.ssDz"
    />
  </div>
</template>

<style scoped>
.bazi-grid {
  display: flex;
  gap: 12px;
}
</style>
