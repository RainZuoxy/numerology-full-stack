import client from './client'
import type { BaZiResponse } from './types'

export interface DimensionAnalysis {
  label: string
  score: number
  overall: string
  insights: string[]
  suggestions: string[]
  timing?: string | null
}

export interface FortuneResponse {
  summary: string
  dimensions: Record<string, DimensionAnalysis>
  remarks: string
}

export interface FortuneRequest {
  bazi: BaZiResponse
  question?: string
}

export const fortuneApi = {
  async analyze(payload: FortuneRequest): Promise<FortuneResponse> {
    const resp = await client.post<FortuneResponse>('/fortune/analyze', payload, {
      timeout: 120000,
    })
    return resp.data
  },
}
