export interface UserInfo {
  user_id: string
  username: string
  nickname?: string | null
  openid?: string | null
}

export interface TokenResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: UserInfo
}

export interface BaseStem {
  type: string
  yin_yang: string
  sequence: number
  element: string
}

export interface GanZhiChart {
  tg_year: BaseStem; dz_year: BaseStem
  tg_month: BaseStem; dz_month: BaseStem
  tg_day: BaseStem; dz_day: BaseStem
  tg_hour: BaseStem; dz_hour: BaseStem
}

export type ShiShenTuple = [string, string | null, string | null]

export interface ShiShenChart {
  tg_year: string; dz_year: ShiShenTuple
  tg_month: string; dz_month: ShiShenTuple
  dz_day: ShiShenTuple
  tg_hour: string; dz_hour: ShiShenTuple
}

export interface MainDestinyItem {
  schedule: [number, number]
  origin_item: { name: string; tian_gan: BaseStem; di_zhi: BaseStem }
  shi_shen: [string, [string | null, string | null, string | null]]
}

export interface MainDestinyChart {
  num: number
  items: MainDestinyItem[]
}

export interface BaZiResponse {
  standard_start_age: string
  chinese_zodiac: string
  day_master: BaseStem
  main_destiny: MainDestinyChart
  ba_zi: GanZhiChart
  shi_shen: ShiShenChart
}

export interface BaseTrigramItem {
  name: string
  icon: string
  lines: { value: boolean }[]
}

export interface Trigram64Item {
  name: string
  index: number
  icon: string
  up_trigram: BaseTrigramItem
  down_trigram: BaseTrigramItem
}

export interface GuaResponse {
  name: string
  value: Trigram64Item
}
