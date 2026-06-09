// 推荐偏好状态管理
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { prefAPI } from '@/api/preferences.js'

export const usePrefStore = defineStore('preferences', () => {
  const preferences = ref({ meat_count: 1, vegetable_count: 2, soup_count: 1, prefer_healthy: false })

  async function fetch() {
    const res = await prefAPI.get()
    if (res?.data) {
      preferences.value = {
        meat_count: res.data.meat_count,
        vegetable_count: res.data.vegetable_count,
        soup_count: res.data.soup_count,
        prefer_healthy: res.data.prefer_healthy ?? false,
      }
    }
  }

  async function save() {
    const res = await prefAPI.update(preferences.value)
    if (res?.success) {
      uni.showToast({ title: '偏好已保存', icon: 'success' })
    }
  }

  return { preferences, fetch, save }
})
