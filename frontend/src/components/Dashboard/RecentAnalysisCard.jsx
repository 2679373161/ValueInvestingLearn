import React from 'react'
import { Card, Typography, Alert, Space, Button } from 'antd'
import { useNavigate } from 'react-router-dom'

const { Title, Text, Paragraph } = Typography

const RecentAnalysisCard = ({ data }) => {
  const navigate = useNavigate()

  if (!data) {
    return (
      <Card title="最新分析结果" className="card-shadow">
        <div className="empty-container">
          <Text type="secondary">暂无分析数据</Text>
        </div>
      </Card>
    )
  }

  const { recommendation, key_indicators, analysis_date } = data

  const getAlertType = (recommendation) => {
    if (recommendation.includes('买入')) return 'success'
    if (recommendation.includes('观望')) return 'warning'
    if (recommendation.includes('谨慎') || recommendation.includes('回避')) return 'error'
    return 'info'
  }

  const handleViewAnalysis = () => {
    navigate('/analysis')
  }

  return (
    <Card
      title="最新分析结果"
      className="card-shadow"
      extra={
        <Button type="link" onClick={handleViewAnalysis}>
          查看详细分析
        </Button>
      }
    >
      <Space direction="vertical" style={{ width: '100%' }} size="middle">
        {/* 投资建议 */}
        <Alert
          message="投资建议"
          description={recommendation}
          type={getAlertType(recommendation)}
          showIcon
        />

        {/* 关键指标 */}
        <div>
          <Title level={5}>关键指标概览</Title>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
            {key_indicators?.pmi && (
              <div>
                <Text type="secondary">PMI</Text>
                <br />
                <Text strong>{key_indicators.pmi}</Text>
              </div>
            )}
            {key_indicators?.cpi && (
              <div>
                <Text type="secondary">CPI</Text>
                <br />
                <Text strong>{key_indicators.cpi}%</Text>
              </div>
            )}
            {key_indicators?.volatility && (
              <div>
                <Text type="secondary">波动率</Text>
                <br />
                <Text strong>{key_indicators.volatility}%</Text>
              </div>
            )}
            {key_indicators?.investor_sentiment && (
              <div>
                <Text type="secondary">投资者情绪</Text>
                <br />
                <Text strong>{key_indicators.investor_sentiment}/100</Text>
              </div>
            )}
          </div>
        </div>

        {/* 分析说明 */}
        <div>
          <Title level={5}>分析说明</Title>
          <Paragraph type="secondary">
            基于{analysis_date}的数据分析，当前择时信号综合考虑了宏观基本面、行业基本面和市场情绪三个维度。
            建议根据择时强度合理配置仓位，并密切关注市场变化。
          </Paragraph>
        </div>
      </Space>
    </Card>
  )
}

export default RecentAnalysisCard