import React from 'react'
import { Card, Progress, Row, Col, Typography, Space } from 'antd'

const { Title, Text } = Typography

const TimingScoreCard = ({ data }) => {
  if (!data) {
    return (
      <Card title="择时评分" className="card-shadow">
        <div className="empty-container">
          <Text type="secondary">暂无数据</Text>
        </div>
      </Card>
    )
  }

  const { overall_score, component_scores, strength_level } = data

  const getProgressStatus = (score) => {
    if (score >= 80) return 'success'
    if (score >= 60) return 'active'
    if (score >= 40) return 'normal'
    return 'exception'
  }

  const getStrengthLevelText = (level) => {
    const texts = {
      very_strong: '非常强劲',
      strong: '强劲',
      neutral: '中性',
      weak: '偏弱',
      very_weak: '非常弱',
    }
    return texts[level] || '未知'
  }

  return (
    <Card title="择时评分" className="card-shadow">
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        {/* 综合评分 */}
        <div>
          <Row align="middle" gutter={16}>
            <Col>
              <Progress
                type="circle"
                percent={overall_score}
                status={getProgressStatus(overall_score)}
                format={(percent) => `${percent}分`}
                size={80}
              />
            </Col>
            <Col flex={1}>
              <Title level={4} style={{ margin: 0 }}>
                综合择时评分
              </Title>
              <Text type="secondary">
                择时强度: {getStrengthLevelText(strength_level)}
              </Text>
            </Col>
          </Row>
        </div>

        {/* 各维度评分 */}
        <div>
          <Title level={5}>各维度评分</Title>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={8}>
              <div>
                <Text>宏观基本面</Text>
                <Progress
                  percent={component_scores?.macro || 0}
                  status={getProgressStatus(component_scores?.macro)}
                  size="small"
                />
              </div>
            </Col>
            <Col xs={24} sm={8}>
              <div>
                <Text>行业基本面</Text>
                <Progress
                  percent={component_scores?.industry || 0}
                  status={getProgressStatus(component_scores?.industry)}
                  size="small"
                />
              </div>
            </Col>
            <Col xs={24} sm={8}>
              <div>
                <Text>市场情绪</Text>
                <Progress
                  percent={component_scores?.sentiment || 0}
                  status={getProgressStatus(component_scores?.sentiment)}
                  size="small"
                />
              </div>
            </Col>
          </Row>
        </div>
      </Space>
    </Card>
  )
}

export default TimingScoreCard