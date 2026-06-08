// 菜品 API
import request from './request.js'

export const dishAPI = {
  list(params) {
    return request('/dishes', { params })
  },
  get(id) {
    return request(`/dishes/${id}`)
  },
  create(data) {
    return request('/dishes', { method: 'POST', body: data })
  },
  update(id, data) {
    return request(`/dishes/${id}`, { method: 'PATCH', body: data })
  },
  delete(id) {
    return request(`/dishes/${id}`, { method: 'DELETE' })
  },
  findByIngredient(name) {
    return request('/dishes/by-ingredient', { params: { name } })
  },
  aggregate(ids) {
    return request('/dishes/aggregate', { params: { ids: ids.join(',') } })
  },
}
