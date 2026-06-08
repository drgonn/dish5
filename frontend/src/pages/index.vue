<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { dailyAPI } from '@/api/daily.js'

const today = ref(null)
const loading = ref(true)
const empty = ref(false)
const swappingId = ref(0)

onShow(() => loadToday())

async function loadToday() {
  loading.value = true
  const res = await dailyAPI.today()
  if (res?.data) {
    today.value = res.data
    empty.value = false
  } else {
    today.value = null
    empty.value = true
  }
  loading.value = false
}

async function handleGenerate() {
  uni.showLoading({ title: '生成中...' })
  const res = await dailyAPI.generate()
  uni.hideLoading()
  if (res?.success) {
    uni.showToast({ title: '推荐已生成', icon: 'success' })
    loadToday()
  }
}

async function swapRecipe(recipe) {
  if (swappingId.value) return
  swappingId.value = recipe.id
  try {
    const res = await uni.request({
      url: `/api/v1/daily/today/swap/${recipe.id}`,
      method: 'POST'
    })
    const data = res[1]?.data || res.data
    if (data?.success) {
      uni.showToast({ title: data.detail || '已替换', icon: 'success' })
      loadToday()
    } else {
      uni.showToast({ title: data?.detail || '无可替换菜品', icon: 'none' })
    }
  } catch (e) {
    uni.showToast({ title: '替换失败', icon: 'none' })
  }
  swappingId.value = 0
}

function goDetail(recipe) {
  uni.navigateTo({ url: `/pages/recipe/detail?id=${recipe.id}` })
}
function goShopping() { uni.navigateTo({ url: '/pages/shopping/index' }) }
function goPrep() { uni.navigateTo({ url: '/pages/prep/index' }) }

function getEmoji(dtype) {
  const map = { '硬菜': '🥩', '肉汤': '🍲', '素汤': '🥣', '素菜': '🥬', '半素': '🍳' }
  return map[dtype] || '🍽️'
}
</script>

<template>
  <view class="page">
    <view v-if="loading" class="center">加载中...</view>

    <view v-else-if="empty" class="center">
      <view class="empty-icon">🍳</view>
      <view class="empty-title">今日推荐尚未生成</view>
      <view class="empty-desc">每天 8:00 自动生成，也可手动触发</view>
      <button class="btn-main" @tap="handleGenerate">⚡ 生成今日推荐</button>
    </view>

    <view v-else class="content">
      <view class="date-banner">
        <text class="date-label">今日推荐</text>
        <text class="date-text">{{ today.date }}</text>
      </view>
      <view class="recipe-list">
        <view v-for="r in today.recipes" :key="r.id" class="recipe-card">
          <text class="emoji">{{ getEmoji(r.dtype) }}</text>
          <view class="info" @tap="goDetail(r)">
            <text class="name">{{ r.name }}</text>
            <text class="dtype">{{ r.dtype }}</text>
          </view>
          <button
            class="swap-btn"
            :disabled="swappingId === r.id"
            @tap="swapRecipe(r)"
          >{{ swappingId === r.id ? '⏳' : '🔄' }}</button>
        </view>
      </view>
      <view class="actions">
        <button class="btn orange" @tap="goShopping">🛒 买菜清单</button>
        <button class="btn green" @tap="goPrep">🔪 备菜清单</button>
        <button class="btn outline" @tap="handleGenerate">🔄 换一批</button>
      </view>
    </view>
  </view>
</template>

<style scoped>
.page { min-height: 100vh; }
.center { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 200rpx 40rpx; color: #999; }
.empty-icon { font-size: 120rpx; margin-bottom: 30rpx; }
.empty-title { font-size: 36rpx; font-weight: bold; color: #333; margin-bottom: 16rpx; }
.empty-desc { font-size: 28rpx; color: #999; margin-bottom: 40rpx; }
.btn-main { background: #FF6B35; color: #fff; border: none; border-radius: 100rpx; padding: 20rpx 60rpx; font-size: 32rpx; }
.date-banner { background: linear-gradient(135deg, #FF6B35, #FF8C5A); padding: 50rpx 40rpx; color: #fff; text-align: center; }
.date-label { font-size: 40rpx; font-weight: bold; display: block; }
.date-text { font-size: 26rpx; opacity: .85; margin-top: 6rpx; }
.recipe-list { margin: 20rpx; background: #fff; border-radius: 20rpx; overflow: hidden; }
.recipe-card { display: flex; align-items: center; padding: 24rpx 24rpx; border-bottom: 1rpx solid #f0f0f0; }
.recipe-card:last-child { border-bottom: none; }
.emoji { font-size: 60rpx; margin-right: 20rpx; }
.info { flex: 1; }
.name { font-size: 32rpx; font-weight: bold; display: block; }
.dtype { font-size: 24rpx; color: #999; }
.swap-btn { width: 60rpx; height: 60rpx; border-radius: 50%; border: none; background: #f5f5f5; font-size: 28rpx; display: flex; align-items: center; justify-content: center; padding: 0; line-height: 1; }
.swap-btn[disabled] { opacity: .4; }
.actions { display: flex; gap: 20rpx; padding: 30rpx; flex-wrap: wrap; }
.btn { flex: 1; min-width: 200rpx; text-align: center; border-radius: 100rpx; padding: 24rpx; font-size: 28rpx; border: none; }
.orange { background: #FF6B35; color: #fff; }
.green { background: #4CAF50; color: #fff; }
.outline { background: #fff; color: #FF6B35; border: 2rpx solid #FF6B35; }
</style>
