<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { dishAPI } from '@/api/dishes.js'

const dishes = ref([])
const total = ref(0)
const page = ref(1)
const keyword = ref('')
const dtypeFilter = ref('')
const loading = ref(false)
const dtypes = ['硬菜', '肉汤', '素汤', '素菜', '半素']

onShow(() => loadDishes())

async function loadDishes(reset = false) {
  if (reset) page.value = 1
  loading.value = true
  const params = { current: page.value, pageSize: 15, sort_field: 'eats', sort_order: 'asc' }
  if (keyword.value) params.name = keyword.value
  if (dtypeFilter.value) params.dtype = dtypeFilter.value
  const res = await dishAPI.list(params)
  if (res?.data) {
    dishes.value = res.data
    total.value = res.total
  }
  loading.value = false
}

function onSearch() {
  loadDishes(true)
}

function goDetail(id) {
  uni.navigateTo({ url: `/pages/recipe/detail?id=${id}` })
}

function getEmoji(dtype) {
  const map = { '硬菜': '🥩', '肉汤': '🍲', '素汤': '🥣', '素菜': '🥬', '半素': '🍳' }
  return map[dtype] || '🍽️'
}

function changePage(p) {
  page.value = p
  loadDishes()
}
</script>

<template>
  <view class="page">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <input class="search-input" v-model="keyword" placeholder="搜索菜名..." confirm-type="search" @confirm="onSearch" />
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-chips">
          <view
            :class="['chip', !dtypeFilter && 'chip-active']"
            @tap="dtypeFilter = ''; loadDishes(true)"
          >全部</view>
          <view
            v-for="dt in dtypes" :key="dt"
            :class="['chip', dtypeFilter === dt && 'chip-active']"
            @tap="dtypeFilter = dt; loadDishes(true)"
          >{{ dt }}</view>
        </view>
      </scroll-view>
    </view>

    <!-- 列表 -->
    <view v-if="loading" class="loading">加载中...</view>
    <view v-else-if="dishes.length === 0" class="empty">暂无菜品</view>
    <view v-else>
      <view v-for="dish in dishes" :key="dish.id" class="dish-card" @tap="goDetail(dish.id)">
        <view class="dish-emoji">{{ getEmoji(dish.dtype) }}</view>
        <view class="dish-info">
          <text class="dish-name">{{ dish.name }}</text>
          <view class="dish-tags">
            <text class="tag">{{ dish.dtype }}</text>
            <text class="tag tag-sub">{{ dish.ftype }}</text>
            <text class="tag tag-time">{{ dish.cooking_time }}分钟</text>
          </view>
          <text class="dish-season">{{ dish.start_month }}-{{ dish.end_month }}月 应季</text>
        </view>
        <text class="arrow">›</text>
      </view>
    </view>

    <!-- 分页 -->
    <view v-if="total > 15" class="pagination">
      <button :disabled="page <= 1" @tap="changePage(page - 1)">上一页</button>
      <text class="page-num">{{ page }} / {{ Math.ceil(total / 15) }}</text>
      <button :disabled="page >= Math.ceil(total / 15)" @tap="changePage(page + 1)">下一页</button>
    </view>
  </view>
</template>

<style scoped>
.page { padding-bottom: 30rpx; }
.search-bar { background: #fff; padding: 20rpx; position: sticky; top: 0; z-index: 10; }
.search-input { background: #f5f5f5; border-radius: 50rpx; padding: 16rpx 30rpx; font-size: 28rpx; }
.filter-scroll { white-space: nowrap; margin-top: 16rpx; }
.filter-chips { display: flex; gap: 16rpx; padding: 0 10rpx; }
.chip { padding: 10rpx 28rpx; border-radius: 100rpx; font-size: 24rpx; background: #f0f0f0; display: inline-block; }
.chip-active { background: #FF6B35; color: #fff; }
.loading, .empty { text-align: center; padding: 200rpx 40rpx; color: #999; }
.dish-card { display: flex; align-items: center; padding: 24rpx 30rpx; background: #fff; margin: 10rpx 20rpx; border-radius: 16rpx; }
.dish-emoji { font-size: 56rpx; margin-right: 20rpx; }
.dish-info { flex: 1; }
.dish-name { font-size: 30rpx; font-weight: bold; }
.dish-tags { display: flex; gap: 10rpx; margin-top: 8rpx; }
.tag { font-size: 22rpx; background: #FFF3E0; color: #FF6B35; padding: 4rpx 12rpx; border-radius: 6rpx; }
.tag-sub { background: #E8F5E9; color: #388E3C; }
.tag-time { background: #E3F2FD; color: #1976D2; }
.dish-season { font-size: 22rpx; color: #999; margin-top: 4rpx; }
.arrow { font-size: 40rpx; color: #ccc; }
.pagination { display: flex; justify-content: center; align-items: center; gap: 30rpx; padding: 30rpx; }
.page-num { font-size: 28rpx; color: #666; }
</style>
