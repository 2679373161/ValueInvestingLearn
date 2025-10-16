import { useState, useEffect } from 'react'
import { visualizationAPI } from '@services/api'

const useDashboardData = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        setError(null)

        // 获取仪表盘摘要数据
        const dashboardData = await visualizationAPI.getDashboardSummary({
          market: 'a_share',
          date: new Date().toISOString().split('T')[0],
        })

        setData(dashboardData.data)
      } catch (err) {
        console.error('获取仪表盘数据失败:', err)
        setError(err)

        // 提供默认数据用于演示
        setData({
          analysis: {
            market: 'a_share',
            analysis_date: new Date().toISOString().split('T')[0],
            overall_score: 65.5,
            strength_level: 'strong',
            component_scores: {
              macro: 70.0,
              industry: 65.0,
              sentiment: 60.0,
            },
            key_indicators: {
              pmi: 51.2,
              cpi: 2.3,
              volatility: 14.5,
              investor_sentiment: 68.0,
            },
            recommendation: '建议买入 - 择时信号强劲',
          },
          position: {
            market: 'a_share',
            date: new Date().toISOString().split('T')[0],
            timing_score: 65.5,
            strength_level: 'strong',
            position_percentage: 60.0,
            position_amount: 60000.0,
            available_capital: 100000.0,
            risk_per_trade_percentage: 2.0,
            risk_amount: 2000.0,
          },
          market_config: {
            enabled: true,
            indices: ['沪深300', '创业板', '红利指数'],
            update_frequency: 'daily',
          },
        })
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  return { data, loading, error }
}

export { useDashboardData }