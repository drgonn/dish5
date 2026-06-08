// 冰箱状态管理
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fridgeAPI } from '@/api/fridge.js'

export const useFridgeStore = defineStore('fridge', () => {
  const items = ref([])
  const loading = ref(false)

  const categories = computed(() => {
    const map = {}
    for (const item of items.value) {
      const cat = item.category || '其他'
      if (!map[cat]) map[cat] = []
      map[cat].push(item)
    }
    // 有库存排前面
    for (const cat of Object.keys(map)) {
      map[cat].sort((a, b) => (b.quantity ? 1 : 0) - (a.quantity ? 1 : 0))
    }
    return map
  })

  const hasItems = computed(() => items.value.length > 0)

  async function fetch() {
    loading.value = true
    const res = await fridgeAPI.list()
    items.value = res?.data || []
    loading.value = false
  }

  async function add(name, category, quantity) {
    const res = await fridgeAPI.add(name, category, quantity)
    if (res?.success) await fetch()
    return res
  }

  async function remove(name) {
    const res = await fridgeAPI.remove(name)
    if (res?.success) await fetch()
    return res
  }

  return { items, loading, categories, hasItems, fetch, add, remove }
})
