import axios, { AxiosError } from 'axios'
import { useAuthStore } from '@/stores/auth'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api/v1',
  timeout: 15000
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (resp) => resp,
  (err: AxiosError<any>) => {
    if (err.response?.status === 401) {
      const auth = useAuthStore()
      auth.logout()
    }
    const detail = (err.response?.data as any)?.detail
    return Promise.reject(new Error(typeof detail === 'string' ? detail : err.message))
  }
)

export default client
