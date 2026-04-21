import client from './client'
import type { GuaResponse } from './types'

export const guaApi = {
  query: (trigram_series: string) =>
    client.post<GuaResponse>('/gua', { trigram_series }).then(r => r.data),
}
