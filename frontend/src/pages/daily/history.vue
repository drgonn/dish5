<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { dailyAPI } from '@/api/daily.js'

const history = ref([])
const loading = ref(true)

onShow(() => loadHistory())

async function loadHistory() {
  loading.value = true
  const res = await dailyAPI.history(1, 30)
  history.value = res?.data || []
  loading.value = false
}
</script>

<template>
  <view class="page">
    <view v-if="loading" class="center">加载中...</view>
    <view v-else-if="!history.length" class="center">暂无推荐历史</view>
    <view v-else>
      <view v-for="item in history" :key="item.date" class="card">
        <view class="card-header">
          <text class="date">📅 {{ item.date }}</text>
          <text :class="['status', item.notified ? 'green' : 'grey']">{{ item.notified ? '已推送 ✅' : '未推送' }}</text>
        </view>
        <view class="recipes">
          <text v-for="r in item.recipes" :key="r.id" class="recipe-tag">{{ r.name }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<style scoped>
.page { padding: 20rpx; }
.center { text-align: center; padding: 200rpx; color: #999; }
.card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 16rpx; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
.date { font-size: 28rpx; font-weight: bold; }
.status { font-size: 24rpx; }
.green { color: #4CAF50; }
.grey { color: #999; }
.recipes { display: flex; flex-wrap: wrap; gap: 10rpx; }
.recipe-tag { background: #FFF3E0; color: #FF6B35; padding: 6rpx 18rpx; border-radius: 20rpx; font-size: 24rpx; }
</style>
