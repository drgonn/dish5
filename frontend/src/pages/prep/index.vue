<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { dailyAPI } from '@/api/daily.js'

const recommend = ref(null)
const loading = ref(true)
const prepSteps = ref([])
const cooks = ref([])

onShow(() => loadData())

async function loadData() {
  const today = new Date().toISOString().split('T')[0]
  const res = await dailyAPI.getDate(today)
  if (res?.data?.aggregated) {
    recommend.value = res.data
    prepSteps.value = res.data.aggregated.prep_steps || []
    cooks.value = res.data.aggregated.cooking_steps || []
  }
  loading.value = false
}

function getActLabel(act) {
  const map = { '腌': '🧂 腌制', '泡': '💧 泡发', '发': '🌱 发酵', '洗': '🚿 清洗', '切': '🔪 切配', '备': '📋 备料' }
  return map[act] || `📌 ${act}`
}

function getActColor(act) {
  if (['腌', '泡', '发'].includes(act)) return '#E65100'
  if (act === '洗') return '#1976D2'
  if (act === '切') return '#388E3C'
  return '#666'
}
</script>

<template>
  <view class="page">
    <view v-if="loading" class="center">加载中...</view>
    <view v-else-if="!recommend" class="center">
      <text>暂无今日推荐</text>
    </view>
    <view v-else>
      <view class="banner">🔪 {{ recommend.date }} 备菜清单</view>

      <!-- 耗时步骤优先 -->
      <view v-for="step in prepSteps" :key="step.act" class="prep-section">
        <view class="prep-header" :style="{ borderLeftColor: getActColor(step.act) }">
          <text class="prep-title">{{ getActLabel(step.act) }}</text>
          <text v-if="step.time_minutes" class="prep-time">⏱ {{ step.time_minutes }}分钟</text>
        </view>
        <view class="prep-items">
          <view v-for="item in step.items" :key="item.name" class="prep-item">
            <text class="prep-dot">·</text>
            <text>{{ item.name }}</text>
            <text v-if="item.amount" class="prep-amount">{{ item.amount }}</text>
            <text v-if="item.shape" class="prep-shape">{{ item.shape }}</text>
          </view>
        </view>
        <view v-if="step.notes?.length" class="prep-notes">
          <text v-for="n in step.notes" :key="n" class="note">💡 {{ n }}</text>
        </view>
      </view>

      <!-- 烹饪步骤 -->
      <view v-for="c in cooks" :key="c.name" class="cook-section">
        <view class="cook-header">
          <text class="cook-name">{{ c.name }}</text>
          <text class="cook-time">🕐 {{ c.cooking_time }}分钟</text>
        </view>
        <view v-for="(s, i) in c.steps" :key="i" class="cook-step">
          <view class="step-num">{{ i + 1 }}</view>
          <text>{{ s }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<style scoped>
.page { padding-bottom: 40rpx; }
.center { text-align: center; padding: 200rpx; color: #999; }
.banner { background: #388E3C; color: #fff; padding: 30rpx; font-size: 32rpx; font-weight: bold; text-align: center; }
.prep-section { margin: 20rpx; background: #fff; border-radius: 16rpx; padding: 24rpx; }
.prep-header { border-left: 6rpx solid #FF6B35; padding-left: 20rpx; margin-bottom: 16rpx; display: flex; justify-content: space-between; align-items: center; }
.prep-title { font-size: 30rpx; font-weight: bold; }
.prep-time { font-size: 24rpx; background: #FFF3E0; color: #E65100; padding: 4rpx 14rpx; border-radius: 10rpx; }
.prep-item { display: flex; padding: 10rpx 0; font-size: 28rpx; align-items: center; }
.prep-dot { margin-right: 8rpx; color: #FF6B35; font-weight: bold; }
.prep-amount { color: #999; margin-left: 10rpx; font-size: 24rpx; }
.prep-shape { background: #E8F5E9; color: #388E3C; padding: 2rpx 12rpx; border-radius: 6rpx; font-size: 22rpx; margin-left: 10rpx; }
.prep-notes { margin-top: 12rpx; }
.note { display: block; font-size: 24rpx; color: #E65100; padding: 4rpx 0; }
.cook-section { margin: 20rpx; background: #fff; border-radius: 16rpx; padding: 24rpx; }
.cook-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; padding-bottom: 16rpx; border-bottom: 1rpx solid #f0f0f0; }
.cook-name { font-size: 32rpx; font-weight: bold; }
.cook-time { font-size: 24rpx; color: #999; }
.cook-step { display: flex; padding: 12rpx 0; font-size: 28rpx; line-height: 1.6; }
.step-num { background: #4CAF50; color: #fff; width: 36rpx; height: 36rpx; border-radius: 50%; text-align: center; line-height: 36rpx; font-size: 22rpx; margin-right: 14rpx; flex-shrink: 0; margin-top: 6rpx; }
</style>
