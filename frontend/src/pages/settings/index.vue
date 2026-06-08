<script setup>
import { onShow } from '@dcloudio/uni-app'
import { usePrefStore } from '@/store/preferences.js'

const store = usePrefStore()

onShow(() => store.fetch())

function inc(field) {
  if (store.preferences[field] < 10) store.preferences[field]++
}
function dec(field) {
  if (store.preferences[field] > 0) store.preferences[field]--
}
</script>

<template>
  <view class="page">
    <view class="section">
      <view class="section-title">⚙️ 每日推荐数量</view>
      <view class="desc">每天推荐菜品的类型和数量</view>

      <view class="row">
        <text class="label">🥩 荤菜</text>
        <view class="stepper">
          <button class="step-btn" @tap="dec('meat_count')">−</button>
          <text class="step-val">{{ store.preferences.meat_count }}</text>
          <button class="step-btn" @tap="inc('meat_count')">+</button>
        </view>
      </view>

      <view class="row">
        <text class="label">🥬 素菜</text>
        <view class="stepper">
          <button class="step-btn" @tap="dec('vegetable_count')">−</button>
          <text class="step-val">{{ store.preferences.vegetable_count }}</text>
          <button class="step-btn" @tap="inc('vegetable_count')">+</button>
        </view>
      </view>

      <view class="row">
        <text class="label">🍲 汤</text>
        <view class="stepper">
          <button class="step-btn" @tap="dec('soup_count')">−</button>
          <text class="step-val">{{ store.preferences.soup_count }}</text>
          <button class="step-btn" @tap="inc('soup_count')">+</button>
        </view>
      </view>

      <button class="save-btn" @tap="store.save()">💾 保存偏好</button>
    </view>

    <view class="section">
      <view class="section-title">📋 其他</view>
      <view class="link" @tap="uni.navigateTo({ url: '/pages/daily/history' })">
        <text>📅 推荐历史</text>
        <text class="arrow">›</text>
      </view>
      <view class="link" @tap="uni.navigateTo({ url: '/pages/shopping/index' })">
        <text>🛒 买菜清单</text>
        <text class="arrow">›</text>
      </view>
      <view class="link" @tap="uni.navigateTo({ url: '/pages/prep/index' })">
        <text>🔪 备菜清单</text>
        <text class="arrow">›</text>
      </view>
    </view>
  </view>
</template>

<style scoped>
.page { padding: 20rpx; }
.section { background: #fff; border-radius: 16rpx; padding: 30rpx; margin-bottom: 20rpx; }
.section-title { font-size: 32rpx; font-weight: bold; margin-bottom: 8rpx; }
.desc { font-size: 24rpx; color: #999; margin-bottom: 24rpx; }
.row { display: flex; justify-content: space-between; align-items: center; padding: 20rpx 0; border-bottom: 1rpx solid #f5f5f5; }
.label { font-size: 30rpx; }
.stepper { display: flex; align-items: center; gap: 20rpx; }
.step-btn { width: 56rpx; height: 56rpx; border-radius: 50%; border: 2rpx solid #FF6B35; background: #fff; color: #FF6B35; font-size: 32rpx; text-align: center; line-height: 52rpx; padding: 0; }
.step-val { font-size: 36rpx; font-weight: bold; min-width: 50rpx; text-align: center; }
.save-btn { background: #FF6B35; color: #fff; border: none; border-radius: 100rpx; padding: 20rpx; margin-top: 30rpx; font-size: 30rpx; }
.link { display: flex; justify-content: space-between; align-items: center; padding: 22rpx 0; border-bottom: 1rpx solid #f5f5f5; font-size: 28rpx; }
.link:last-child { border-bottom: none; }
.arrow { color: #ccc; font-size: 36rpx; }
</style>
