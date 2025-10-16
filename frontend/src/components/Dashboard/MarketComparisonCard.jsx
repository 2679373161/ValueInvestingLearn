import React from 'react'
import { Card, List, Tag, Typography, Button } from 'antd'
import { useNavigate } from 'react-router-dom'

const { Title, Text } = Typography

const MarketComparisonCard = () => {
  const navigate = useNavigate()

  // 模拟数据
  const marketData = [
    {
      market: 'A股市场',
      score: 75.5,
      strength: 'strong',
      trend: 'up',
    },
    {
      market: '港股市场',
      score: 65.0,
      strength: 'neutral',
      trend: 'stable',
    },
    {
      market: '美股市场',
      score: 70.2,
      strength: 'strong',
      trend: 'up',
    },
  ]

  const getStrengthColor = (strength) => {
    const colors = {
      very_strong: 'success',
      strong: 'processing',
      neutral: 'warning',
      weak: 'default',
      very_weak: 'error',
    }
    return colors[strength] || 'default'
  }

  const getStrengthText = (strength) => {
    const texts = {
      very_strong: '非常强劲',
      strong: '强劲',
      neutral: '中性',
      weak: '偏弱',
      very_weak: '非常弱',
    }
    return texts[strength] || '未知'
  }

  const handleViewDetails = () => {
    navigate('/market-comparison')
  }

  return (
    <Card
      title="多市场比较"
      className="card-shadow"
      extra={
        <Button type="link" onClick={handleViewDetails}>
          查看详情
        </Button>
      }
    >
      <List
        dataSource={marketData}
        renderItem={(item) => (
          <List.Item
            actions={[
              <Text key="score" strong style={{ color: '#1890ff' }}>
                {item.score}分
              </Text>,
            ]}
          >
            <List.Item.Meta
              title={
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Text>{item.market}</Text>
                  <Tag color={getStrengthColor(item.strength)}>
                    {getStrengthText(item.strength)}
                  </Tag>
                </div>
              }
              description={
                <Text type="secondary">
                  {item.trend === 'up' ? '📈 上升趋势' :
                   item.trend === 'down' ? '📉 下降趋势' : '➡️ 平稳趋势'}
                </Text>
              }
            />
          </List.Item>
        )}
      />
    </Card>
  )
}

export default MarketComparisonCard