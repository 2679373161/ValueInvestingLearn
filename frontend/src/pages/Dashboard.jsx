import React from 'react'
import { Card, Row, Col, Statistic, Typography, Alert, Spin } from 'antd'
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons'

import { useDashboardData } from '@hooks/useDashboardData'
import TimingScoreCard from '@components/Dashboard/TimingScoreCard'
import MarketComparisonCard from '@components/Dashboard/MarketComparisonCard'
import RecentAnalysisCard from '@components/Dashboard/RecentAnalysisCard'

const { Title } = Typography

const Dashboard = () => {
  const { data, loading, error } = useDashboardData()

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-container">
          <Spin size="large" />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="page-container">
        <Alert
          message="数据加载失败"
          description={error.message}
          type="error"
          showIcon
        />
      </div>
    )
  }

  const { analysis, position, marketConfig } = data || {}

  return (
    <div className="page-container">
      <Title level={2}>量化择时仪表盘</Title>

      {/* 关键指标概览 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="择时综合评分"
              value={analysis?.overall_score || 0}
              precision={1}
              valueStyle={{
                color: analysis?.overall_score >= 60 ? '#3f8600' : '#cf1322',
              }}
              prefix={
                analysis?.overall_score >= 60 ? (
                  <ArrowUpOutlined />
                ) : (
                  <ArrowDownOutlined />
                )
              }
              suffix="/100"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="择时强度"
              value={analysis?.strength_level || 'neutral'}
              valueStyle={{
                color: getStrengthLevelColor(analysis?.strength_level),
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="建议仓位比例"
              value={position?.position_percentage || 0}
              precision={1}
              suffix="%"
              valueStyle={{
                color: '#1890ff',
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="建议仓位金额"
              value={position?.position_amount || 0}
              precision={0}
              prefix="¥"
              valueStyle={{
                color: '#52c41a',
              }}
            />
          </Card>
        </Col>
      </Row>

      {/* 择时评分卡片 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={12}>
          <TimingScoreCard data={analysis} />
        </Col>
        <Col xs={24} lg={12}>
          <MarketComparisonCard />
        </Col>
      </Row>

      {/* 最新分析结果 */}
      <Row gutter={[16, 16]}>
        <Col xs={24}>
          <RecentAnalysisCard data={analysis} />
        </Col>
      </Row>
    </div>
  )
}

// 获取择时强度等级对应的颜色
const getStrengthLevelColor = (level) => {
  const colors = {
    very_strong: '#52c41a',
    strong: '#73d13d',
    neutral: '#faad14',
    weak: '#ffa940',
    very_weak: '#ff4d4f',
  }
  return colors[level] || '#d9d9d9'
}

export default Dashboard