// 冰箱 API
import request from './request.js'

export const fridgeAPI = {
  list(category) {
    return request('/fridge', { params: category ? { category } : {} })
  },
  add(ingredient_name, category = '其他', quantity = '') {
    return request('/fridge', { method: 'POST', params: { ingredient_name, category, quantity } })
  },
  batchAdd(names) {
    return request('/fridge/batch', { method: 'POST', body: names })
  },
  remove(ingredient_name) {
    return request(`/fridge/${encodeURIComponent(ingredient_name)}`, { method: 'DELETE' })
  },
  match() {
    return request('/fridge/match')
  },
}
