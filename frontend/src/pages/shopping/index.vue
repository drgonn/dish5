<script setup>
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { dailyAPI } from '@/api/daily.js'
import { shoppingAPI } from '@/api/shopping.js'

const recommend = ref(null)
const loading = ref(true)

onShow(() => loadData())

async function loadData() {
  const today = new Date().toISOString().split('T')[0]
  const res = await dailyAPI.getDate(today)
  if (res?.data) recommend.value = res.data
  loading.value = false
}

// 按 type 分组：main / side / seasoning
const mainItems = computed(() => (recommend.value?.shopping_list || []).filter(i => i.type === 'main'))
const sideItems = computed(() => (recommend.value?.shopping_list || []).filter(i => i.type === 'side'))
const seasoningItems = computed(() => (recommend.value?.shopping_list || []).filter(i => i.type === 'seasoning'))

async function toggleBought(item) {
  item.bought = !item.bought
  const today = new Date().toISOString().split('T')[0]
  const allItems = recommend.value.shopping_list.map(i => ({
    name: i.name, amount: i.amount, bought: i.bought
  }))
  await shoppingAPI.update(today, allItems)
}
</script>

<template>
  <view class="page">
    <view v-if="loading" class="center">加载中...</view>
    <view v-else-if="!recommend" class="center">
      <view class="empty-icon">🛒</view>
      <text>暂无推荐，请先生成今日推荐</text>
    </view>
    <view v-else>
      <view class="banner">📅 {{ recommend.date }} 买菜清单</view>

      <!-- 主材 -->
      <view class="section" v-if="mainItems.length">
        <view class="section-title">🥩 主材</view>
        <view v-for="item in mainItems" :key="item.name" class="item" @tap="toggleBought(item)">
          <view :class="['check', item.bought && 'checked']">{{ item.bought ? '✅' : '⬜' }}</view>
          <view class="info">
            <text :class="['name', item.bought && 'done']">{{ item.name }}</text>
            <text class="amount" v-if="item.amount">{{ item.amount }}</text>
          </view>
        </view>
      </view>

      <!-- 辅料 -->
      <view class="section" v-if="sideItems.length">
        <view class="section-title">🥬 辅料</view>
        <view v-for="item in sideItems" :key="item.name" class="item item-side" @tap="toggleBought(item)">
          <view :class="['check', 'check-sm', item.bought && 'checked']">{{ item.bought ? '✅' : '⬜' }}</view>
          <view class="info">
            <text :class="['name', 'name-sm', item.bought && 'done']">{{ item.name }}</text>
            <text class="amount" v-if="item.amount">{{ item.amount }}</text>
          </view>
        </view>
      </view>

      <!-- 佐料 -->
      <view class="section" v-if="seasoningItems.length">
        <view class="section-title section-title-sm">🧂 佐料</view>
        <view class="seasoning-chips">
          <view
            v-for="item in seasoningItems" :key="item.name"
            :class="['chip', item.bought && 'chip-done']"
            @tap="toggleBought(item)"
          >
            {{ item.name }}
            <text class="chip-amount" v-if="item.amount">{{ item.amount }}</text>
          </view>
        </view>
      </view>

      <view v-if="!recommend.shopping_list?.length" class="center">清单为空</view>
    </view>
  </view>
</template>

<style scoped>
.page { padding-bottom: 40rpx; }
.center { text-align: center; padding: 200rpx 40rpx; color: #999; }
.empty-icon { font-size: 80rpx; margin-bottom: 20rpx; }
.banner { background: #4CAF50; color: #fff; padding: 30rpx; font-size: 32rpx; font-weight: bold; text-align: center; }
.section { background: #fff; margin: 16rpx 20rpx; border-radius: 16rpx; overflow: hidden; }
.section-title { font-size: 28rpx; font-weight: bold; padding: 20rpx 24rpx 8rpx; color: #333; }
.section-title-sm { font-size: 24rpx; color: #999; padding-bottom: 12rpx; }

/* 主材 — 醒目 */
.item { display: flex; align-items: center; padding: 18rpx 24rpx; border-bottom: 1rpx solid #f8f8f8; }
.item:last-child { border-bottom: none; }
.check { font-size: 44rpx; margin-right: 18rpx; width: 50rpx; text-align: center; }
.checked { opacity: .5; }
.name { font-size: 32rpx; font-weight: 500; }
.done { text-decoration: line-through; color: #ccc; }
.amount { font-size: 26rpx; color: #999; margin-left: 14rpx; }

/* 辅料 — 稍小 */
.item-side { padding: 14rpx 24rpx; }
.check-sm { font-size: 36rpx; margin-right: 14rpx; width: 44rpx; }
.name-sm { font-size: 28rpx; }

/* 佐料 — chips */
.seasoning-chips { display: flex; flex-wrap: wrap; gap: 12rpx; padding: 0 24rpx 20rpx; }
.chip { font-size: 22rpx; background: #f5f5f5; color: #999; padding: 6rpx 16rpx; border-radius: 20rpx; }
.chip-done { text-decoration: line-through; opacity: .5; }
.chip-amount { margin-left: 4rpx; }
</style>
