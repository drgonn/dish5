<script setup>
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useFridgeStore } from '@/store/fridge.js'

const store = useFridgeStore()
const checklist = ref([])
const generating = ref(false)

onShow(() => loadChecklist())

async function loadChecklist() {
  const res = await uni.request({ url: '/api/v1/fridge/checklist' })
  checklist.value = (res[1]?.data || res.data)?.data || []
}

async function toggle(item) {
  const res = await uni.request({
    url: `/api/v1/fridge/toggle?ingredient_name=${encodeURIComponent(item.name)}`,
    method: 'POST'
  })
  const data = res[1]?.data || res.data
  if (data?.success) {
    item.lit = data.data?.lit ?? !item.lit
  }
}

async function generateFromFridge() {
  const lit = checklist.value.filter(i => i.lit)
  if (!lit.length) {
    uni.showToast({ title: '请先点亮食材', icon: 'none' })
    return
  }
  generating.value = true
  uni.showLoading({ title: '生成推荐...' })
  const res = await uni.request({
    url: '/api/v1/fridge/generate-recommend',
    method: 'POST'
  })
  uni.hideLoading()
  generating.value = false
  const data = res[1]?.data || res.data
  if (data?.success) {
    uni.showToast({ title: '已生成！', icon: 'success' })
    uni.switchTab({ url: '/pages/index' })
  }
}

const litCount = computed(() => checklist.value.filter(i => i.lit).length)
</script>

<template>
  <view class="page">
    <!-- 状态条 -->
    <view class="status-bar">
      <text class="status-text">
        🧊 已点亮 {{ litCount }}/{{ checklist.length }} 种食材
      </text>
    </view>

    <!-- 图鉴网格 -->
    <view class="grid">
      <view
        v-for="item in checklist" :key="item.name"
        :class="['card', item.lit ? 'card-lit' : 'card-off']"
        @tap="toggle(item)"
      >
        <text class="card-emoji">{{ item.emoji }}</text>
        <text :class="['card-name', item.lit && 'card-name-lit']">{{ item.name }}</text>
      </view>
    </view>

    <!-- 生成按钮 -->
    <view class="bottom-bar">
      <button
        class="gen-btn"
        :disabled="litCount === 0 || generating"
        @tap="generateFromFridge"
      >
        🍳 用这 {{ litCount }} 种食材生成推荐
      </button>
    </view>
  </view>
</template>

<style scoped>
.page { padding-bottom: 120rpx; }
.status-bar { padding: 24rpx 30rpx; background: #fff; margin-bottom: 10rpx; }
.status-text { font-size: 28rpx; color: #666; }
.grid { display: flex; flex-wrap: wrap; gap: 16rpx; padding: 16rpx; }
.card {
  width: calc(25% - 12rpx);
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 16rpx;
  transition: all .2s;
}
.card-lit { background: #fff; box-shadow: 0 2rpx 12rpx rgba(255,107,53,.15); }
.card-off { background: #f0f0f0; opacity: .5; }
.card-emoji { font-size: 56rpx; }
.card-name { font-size: 22rpx; margin-top: 6rpx; color: #999; }
.card-name-lit { color: #333; font-weight: 500; }
.bottom-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 20rpx 30rpx 40rpx; background: #fff; border-top: 1rpx solid #f0f0f0; }
.gen-btn { background: #FF6B35; color: #fff; border: none; border-radius: 100rpx; padding: 24rpx; font-size: 30rpx; width: 100%; }
.gen-btn[disabled] { opacity: .4; }
</style>
