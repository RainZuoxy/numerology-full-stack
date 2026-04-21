import client from './client'
import type { TokenResponse, UserInfo } from './types'

export const authApi = {
  register: (data: { username: string; password: string; nickname?: string }) =>
    client.post<TokenResponse>('/auth/register', data).then(r => r.data),

  login: (data: { username: string; password: string }) =>
    client.post<TokenResponse>('/auth/login', data).then(r => r.data),

  wechatLogin: (data: { code: string; nickname?: string }) =>
    client.post<TokenResponse>('/auth/wechat', data).then(r => r.data),

  me: () => client.get<UserInfo>('/auth/me').then(r => r.data),
}
