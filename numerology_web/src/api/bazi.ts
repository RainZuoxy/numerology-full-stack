import client from './client'
import type { BaZiResponse } from './types'

export interface BaZiRequest {
  name?: string
  dob_time: string
  gender: 'male' | 'female'
  dayun_number?: number
}

export const baziApi = {
  generate: (data: BaZiRequest) =>
    client.post<BaZiResponse>('/bazi', data).then(r => r.data),
}
