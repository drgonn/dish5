// 推荐偏好 API
import request from './request.js'

export const prefAPI = {
  get() {
    return request('/preferences')
  },
  update(data) {
    return request('/preferences', { method: 'PUT', body: data })
  },
}
