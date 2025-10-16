import React from 'react'
import { Card, Row, Col, Statistic, Table, Tag } from 'antd'
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons'

const MarketComparison = () => {
  // 模拟市场比较数据
  const marketData = [
    {
      key: '1',
      market: 'A股市场',
      timingScore: 78,
      trend: 'up',
      strength: 'strong',
      recommendation: '买入',
      riskLevel: '中等'
    },
    {
      key: '2',
      market: '港股市场',
      timingScore: 65,
      trend: 'neutral',
      strength: 'moderate',
      recommendation: '观望',
      riskLevel: '中等'
    },
    {
      key: '3',
      market: '美股市场',
      timingScore: 72,
      trend: 'up',
      strength: 'moderate',
      recommendation: '适度买入',
      riskLevel: '中等'
    }
  ]

  const columns = [
    {
      title: '市场',
      dataIndex: 'market',
      key: 'market',
    },
    {
      title: '择时评分',
      dataIndex: 'timingScore',
      key: 'timingScore',
      render: (score) => (
        <Statistic
          value={score}
          precision={0}
          valueStyle={{ color: score >= 70 ? '#3f8600' : score >= 50 ? '#cf1322' : '#cf1322' }}
          prefix={score >= 70 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
          suffix="/100"
        />
      )
    },
    {
      title: '趋势',
      dataIndex: 'trend',
      key: 'trend',
      render: (trend) => (
        <Tag color={trend === 'up' ? 'green' : trend === 'down' ? 'red' : 'orange'}>
          {trend === 'up' ? '上涨' : trend === 'down' ? '下跌' : '中性'}
        </Tag>
      )
    },
    {
      title: '择时强度',
      dataIndex: 'strength',
      key: 'strength',
      render: (strength) => (
        <Tag color={
          strength === 'strong' ? 'green' :
          strength === 'moderate' ? 'blue' :
          strength === 'weak' ? 'red' : 'orange'
        }>
          {strength === 'strong' ? '强劲' :
           strength === 'moderate' ? '中等' :
           strength === 'weak' ? '疲弱' : '中性'}
        </Tag>
      )
    },
    {
      title: '投资建议',
      dataIndex: 'recommendation',
      key: 'recommendation',
      render: (recommendation) => (
        <Tag color={
          recommendation.includes('买入') ? 'green' :
          recommendation.includes('卖出') ? 'red' : 'orange'
        }>
          {recommendation}
        </Tag>
      )
    },
    {
      title: '风险等级',
      dataIndex: 'riskLevel',
      key: 'riskLevel',
      render: (riskLevel) => (
        <Tag color={
          riskLevel === '低' ? 'green' :
          riskLevel === '中等' ? 'orange' : 'red'
        }>
          {riskLevel}
        </Tag>
      )
    }
  ]

  return (
    <div className="market-comparison">
      <h1>多市场择时比较</h1>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="最佳市场"
              value="A股市场"
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="平均择时评分"
              value={71.7}
              precision={1}
              valueStyle={{ color: '#3f8600' }}
              prefix={<ArrowUpOutlined />}
              suffix="/100"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="市场数量"
              value={3}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="市场择时对比分析" bordered={false}>
        <Table
          columns={columns}
          dataSource={marketData}
          pagination={false}
          size="middle"
        />
      </Card>

      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col span={12}>
          <Card title="分析说明" bordered={false}>
            <p><strong>A股市场</strong>：择时信号强劲，宏观基本面表现良好，建议积极配置。</p>
            <p><strong>港股市场</strong>：择时信号中性，市场存在不确定性，建议观望。</p>
            <p><strong>美股市场</strong>：择时信号中等，技术指标偏积极，可适度配置。</p>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="投资策略建议" bordered={false}>
            <p>• <strong>重点配置</strong>：A股市场（择时评分78）</p>
            <p>• <strong>适度配置</strong>：美股市场（择时评分72）</p>
            <p>• <strong>谨慎观望</strong>：港股市场（择时评分65）</p>
            <p>• <strong>总体仓位</strong>：建议配置60-70%权益类资产</p>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default MarketComparison