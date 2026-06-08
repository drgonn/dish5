// 购物清单 API
import request from './request.js'

export const shoppingAPI = {
  get(date) {
    return request(`/shopping/${date}`)
  },
  update(date, items) {
    return request(`/shopping/${date}`, { method: 'PUT', body: items })
  },
}
