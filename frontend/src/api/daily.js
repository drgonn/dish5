// 每日推荐 API
import request from './request.js'

export const dailyAPI = {
  today() {
    return request('/daily/today')
  },
  getDate(date) {
    return request(`/daily/${date}`)
  },
  generate(date) {
    const params = date ? { target_date: date } : {}
    return request('/daily/generate', { method: 'POST', params })
  },
  history(page = 1, pageSize = 20) {
    return request('/daily/history/list', { params: { page, page_size: pageSize } })
  },
}
