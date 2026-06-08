// API 请求封装 — dish5
// H5 开发环境通过 Vite proxy 转发到 localhost:8010，无需完整 URL
// 小程序/生产环境需替换为实际地址
const BASE_URL = '/api/v1'

const request = async (url, options = {}) => {
  const config = {
    url: BASE_URL + url,
    method: options.method || 'GET',
    header: {
      'Content-Type': 'application/json',
      ...options.header,
    },
    timeout: 15000,
    ...options,
  }

  if (options.body) {
    config.data = options.body
  }
  if (options.params) {
    const qs = Object.entries(options.params)
      .filter(([, v]) => v != null && v !== '')
      .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
      .join('&')
    if (qs) config.url += '?' + qs
  }

  try {
    const res = await uni.request(config)
    const data = res[1]?.data || res.data
    if (data?.success === false) {
      uni.showToast({ title: data.detail || '请求失败', icon: 'none' })
    }
    return data
  } catch (e) {
    uni.showToast({ title: '网络异常，请检查连接', icon: 'none' })
    console.error('[API]', url, e)
    return null
  }
}

export default request
export { BASE_URL }
