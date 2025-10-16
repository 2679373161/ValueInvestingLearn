import axios from 'axios'

// 获取API基础URL
const getBaseURL = () => {
  // 开发环境使用代理，生产环境使用环境变量
  if (import.meta.env.DEV) {
    return '/api'
  }
  return import.meta.env.VITE_API_BASE_URL || '/api'
}

// 创建axios实例
const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API请求错误:', error)

    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response
      const message = data?.message || `请求失败: ${status}`

      return Promise.reject({
        code: status,
        message,
        data: data?.data,
      })
    } else if (error.request) {
      // 请求发送失败
      return Promise.reject({
        code: 'NETWORK_ERROR',
        message: '网络连接错误，请检查网络连接',
      })
    } else {
      // 其他错误
      return Promise.reject({
        code: 'UNKNOWN_ERROR',
        message: '未知错误',
      })
    }
  }
)

// 数据输入相关API
export const dataInputAPI = {
  // 宏观数据
  addMacroData: (data) => api.post('/data/macro', data),
  getMacroData: (params) => api.get('/data/macro', { params }),

  // 市场情绪数据
  addMarketSentiment: (data) => api.post('/data/market-sentiment', data),
  getMarketSentiment: (params) => api.get('/data/market-sentiment', { params }),

  // 行业数据
  addIndustryData: (data) => api.post('/data/industry', data),
  getIndustryData: (params) => api.get('/data/industry', { params }),
}

// 分析相关API
export const analysisAPI = {
  // 择时指标计算
  calculateTimingIndicators: (data) => api.post('/analysis/timing-indicators', data),
  getTimingIndicators: (params) => api.get('/analysis/timing-indicators', { params }),

  // AI分析
  getAIAnalysis: (data) => api.post('/analysis/ai-analysis', data),

  // 仓位计算
  calculatePositionSizing: (data) => api.post('/analysis/position-sizing', data),

  // 市场比较
  compareMarkets: (params) => api.get('/analysis/market-comparison', { params }),

  // 分析摘要
  getAnalysisSummary: (params) => api.get('/analysis/summary', { params }),
}

// 可视化相关API
export const visualizationAPI = {
  // 择时评分趋势
  getTimingScoreTrend: (params) => api.get('/visualization/timing-score-trend', { params }),

  // 市场比较图表
  getMarketComparisonChart: (params) => api.get('/visualization/market-comparison-chart', { params }),

  // 指标分解
  getIndicatorBreakdown: (params) => api.get('/visualization/indicator-breakdown', { params }),

  // 仓位配置图表
  getPositionSizingChart: (params) => api.get('/visualization/position-sizing-chart', { params }),

  // 市场情绪分析
  getSentimentAnalysis: (params) => api.get('/visualization/sentiment-analysis', { params }),

  // 宏观指标
  getMacroIndicators: (params) => api.get('/visualization/macro-indicators', { params }),

  // 仪表盘摘要
  getDashboardSummary: (params) => api.get('/visualization/dashboard-summary', { params }),
}

// 健康检查
export const healthAPI = {
  checkDataService: () => api.get('/data/health'),
  checkAnalysisService: () => api.get('/analysis/health'),
  checkVisualizationService: () => api.get('/visualization/health'),
}

export default api