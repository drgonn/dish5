<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { dishAPI } from '@/api/dishes.js'

const dish = ref(null)
const id = ref(0)

onLoad((options) => {
  id.value = parseInt(options.id)
  loadDish()
})

async function loadDish() {
  const res = await dishAPI.get(id.value)
  dish.value = res?.data
  if (!dish.value) uni.showToast({ title: '菜品不存在', icon: 'none' })
}
</script>

<template>
  <view class="page" v-if="dish">
    <view class="header">
      <text class="name">{{ dish.name }}</text>
      <view class="tags">
        <text class="tag">{{ dish.dtype }}</text>
        <text class="tag tag-sub">{{ dish.ftype }}</text>
        <text class="tag tag-time">🕐 {{ dish.cooking_time }}分钟</text>
        <text class="tag tag-diff">{{ dish.difficulty }}</text>
      </view>
      <text class="season">📅 {{ dish.start_month }}-{{ dish.end_month }}月 应季 · 已做 {{ dish.eats }} 次</text>
    </view>

    <view class="section" v-if="dish.main_ingredients?.length">
      <view class="section-title">🥩 主料</view>
      <view class="ing-list">
        <view v-for="ing in dish.main_ingredients" :key="ing.name" class="ing-item">
          <text class="dot">·</text>{{ ing.name }} <text class="amount">{{ ing.amount }}</text>
        </view>
      </view>
    </view>

    <view class="section" v-if="dish.side_ingredients?.length">
      <view class="section-title">🥬 辅料</view>
      <view class="ing-list">
        <view v-for="ing in dish.side_ingredients" :key="ing.name" class="ing-item">
          <text class="dot">·</text>{{ ing.name }} <text class="amount">{{ ing.amount }}</text>
        </view>
      </view>
    </view>

    <view class="section" v-if="dish.seasonings?.length">
      <view class="section-title">🧂 调料</view>
      <view class="ing-list">
        <view v-for="ing in dish.seasonings" :key="ing.name" class="ing-item">
          <text class="dot">·</text>{{ ing.name }} <text class="amount">{{ ing.amount }}</text>
        </view>
      </view>
    </view>

    <view class="section" v-if="dish.cooking_steps?.length">
      <view class="section-title">📝 烹饪步骤</view>
      <view v-for="(s, i) in dish.cooking_steps" :key="i" class="step">
        <view class="step-num">{{ i + 1 }}</view>
        <text>{{ s.name || s }}</text>
      </view>
    </view>

    <view class="section" v-if="dish.attentions?.length">
      <view class="section-title">⚠️ 注意事项</view>
      <view v-for="a in dish.attentions" :key="a.name" class="attention">
        {{ a.name || a }}
      </view>
    </view>

    <view class="section" v-if="dish.prep_steps?.length">
      <view class="section-title">🔪 备菜步骤</view>
      <view v-for="(p, i) in dish.prep_steps" :key="i" class="prep">
        <text class="prep-act">{{ p.act }}</text>
        <text v-if="p.items?.length">{{ p.items.map(it => it.name).join('、') }}</text>
        <text v-else>{{ p.name }}</text>
      </view>
    </view>
  </view>
  <view v-else class="center">加载中...</view>
</template>

<style scoped>
.page { padding-bottom: 60rpx; }
.header { background: #fff; padding: 40rpx 30rpx; margin-bottom: 20rpx; }
.name { font-size: 44rpx; font-weight: bold; display: block; }
.tags { display: flex; gap: 14rpx; margin-top: 16rpx; flex-wrap: wrap; }
.tag { font-size: 24rpx; padding: 6rpx 16rpx; border-radius: 8rpx; background: #FFF3E0; color: #FF6B35; }
.tag-sub { background: #E8F5E9; color: #388E3C; }
.tag-time { background: #E3F2FD; color: #1976D2; }
.tag-diff { background: #F3E5F5; color: #7B1FA2; }
.season { font-size: 24rpx; color: #999; margin-top: 12rpx; display: block; }
.section { background: #fff; margin: 0 20rpx 20rpx; padding: 30rpx; border-radius: 16rpx; }
.section-title { font-size: 30rpx; font-weight: bold; margin-bottom: 20rpx; }
.ing-item { padding: 8rpx 0; font-size: 28rpx; }
.dot { margin-right: 8rpx; color: #FF6B35; }
.amount { color: #999; margin-left: 10rpx; }
.step { display: flex; align-items: flex-start; padding: 12rpx 0; font-size: 28rpx; line-height: 1.6; }
.step-num { background: #FF6B35; color: #fff; width: 40rpx; height: 40rpx; border-radius: 50%; text-align: center; line-height: 40rpx; font-size: 24rpx; margin-right: 16rpx; flex-shrink: 0; margin-top: 4rpx; }
.attention { padding: 10rpx 0; font-size: 26rpx; color: #E65100; }
.prep { padding: 10rpx 0; font-size: 28rpx; }
.prep-act { background: #FF6B35; color: #fff; padding: 2rpx 12rpx; border-radius: 6rpx; font-size: 22rpx; margin-right: 16rpx; }
.center { text-align: center; padding: 200rpx; color: #999; }
</style>
