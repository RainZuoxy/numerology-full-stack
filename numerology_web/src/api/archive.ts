import client from './client'

export interface ArchiveItem {
  archive_id: number
  name: string
  gender: 'male' | 'female'
  dob_time: string
  is_primary: boolean
  created_at: string
}

export interface ArchiveListResponse {
  items: ArchiveItem[]
  max_archives: number
}

export interface ArchiveCreateRequest {
  name: string
  gender: 'male' | 'female'
  dob_time: string
}

export type SignLevel = '上上签' | '上签' | '中平签' | '下签' | '下下签'

export interface DailyDimensions {
  wealth: number
  love: number
  career: number
  health: number
  study: number
}

export interface DailyPredictionPayload {
  sign: SignLevel
  score: number
  dimensions: DailyDimensions
  overall: string
  highlight: string
  caution: string
  lucky_color: string
  lucky_direction: string
  advice: string
}

export interface DailyPredictionResponse {
  predict_date: string
  archive_id: number
  archive_name: string
  day_pillar?: string | null
  payload: DailyPredictionPayload
  created_at: string
}

export const archiveApi = {
  async list(): Promise<ArchiveListResponse> {
    return (await client.get<ArchiveListResponse>('/archives')).data
  },
  async create(req: ArchiveCreateRequest): Promise<ArchiveItem> {
    return (await client.post<ArchiveItem>('/archives', req)).data
  },
  async remove(id: number): Promise<void> {
    await client.delete(`/archives/${id}`)
  },
  async setPrimary(id: number): Promise<ArchiveItem> {
    return (await client.post<ArchiveItem>(`/archives/${id}/primary`)).data
  },
  async getToday(): Promise<DailyPredictionResponse | null> {
    const resp = await client.get<DailyPredictionResponse | null>('/archives/predictions/today')
    return resp.data
  },
  async createToday(): Promise<DailyPredictionResponse> {
    const resp = await client.post<DailyPredictionResponse>(
      '/archives/predictions/today',
      {},
      { timeout: 120000 },
    )
    return resp.data
  },
}
