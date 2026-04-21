const SHICHEN = [
  { name: '子时', range: '23:00 – 01:00' },
  { name: '丑时', range: '01:00 – 03:00' },
  { name: '寅时', range: '03:00 – 05:00' },
  { name: '卯时', range: '05:00 – 07:00' },
  { name: '辰时', range: '07:00 – 09:00' },
  { name: '巳时', range: '09:00 – 11:00' },
  { name: '午时', range: '11:00 – 13:00' },
  { name: '未时', range: '13:00 – 15:00' },
  { name: '申时', range: '15:00 – 17:00' },
  { name: '酉时', range: '17:00 – 19:00' },
  { name: '戌时', range: '19:00 – 21:00' },
  { name: '亥时', range: '21:00 – 23:00' },
]

export function shichenOfHour(hour: number): { name: string; range: string } {
  const idx = Math.floor(((hour + 1) % 24) / 2)
  return SHICHEN[idx]
}

export function formatDobDisplay(dob: string): string {
  const m = dob.match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):\d{2}:\d{2}$/)
  if (!m) return dob
  const [, y, mo, d, h] = m
  const sc = shichenOfHour(+h)
  return `${y}-${mo}-${d}  ${sc.name}（${sc.range}）`
}
