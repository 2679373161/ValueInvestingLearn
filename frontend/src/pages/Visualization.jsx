import React from 'react'
import { Card, Typography, Alert, Row, Col, Tabs, Select, DatePicker } from 'antd'
import { visualizationAPI } from '@services/api'
import TimingScoreChart from '@components/Charts/TimingScoreChart'
import IndicatorBreakdownChart from '@components/Charts/IndicatorBreakdownChart'
import PositionSizingChart from '@components/Charts/PositionSizingChart'
import MarketComparisonChart from '@components/Charts/MarketComparisonChart'

const { Title } = Typography
const { TabPane } = Tabs
const { Option } = Select
const { RangePicker } = DatePicker

const Visualization = () => {
  const [loading, setLoading] = React.useState(false)
  const [market, setMarket] = React.useState('a_share')
  const [dateRange, setDateRange] = React.useState(null)

  const handleMarketChange = (value) => {
    setMarket(value)
  }

  const handleDateRangeChange = (dates) => {
    setDateRange(dates)
  }

  // 模拟数据
  const mockChartData = {
    timingScoreTrend: [
      { date: '2024-01-01', score: 65 },
      { date: '2024-01-02', score: 68 },
      { date: '2024-01-03', score: 72 },
      { date: '2024-01-04', score: 70 },
      { date: '2024-01-05', score: 75 },
      { date: '2024-01-06', score: 78 },
      { date: '2024-01-07', score: 76 },
    ],
    indicatorBreakdown: {
      macro: 85,
      industry: 72,
      sentiment: 77,
    },
    positionSizing: {
      equities: 60,
      bonds: 20,
      cash: 20,
    },
    marketComparison: {
      a_share: 78,
      hong_kong: 72,
      nasdaq: 85,
    },
  }

  return (
    <div className="page-container">
      <Title level={2}>可视化</Title>

      <Alert
        message="可视化分析"
        description="通过图表直观展示择时评分趋势、指标分解、仓位配置和市场比较等关键信息。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      {/* 筛选条件 */}
      <Card className="card-shadow" style={{ marginBottom: 24 }}>
        <Row gutter={16} align="middle">
          <Col xs={24} sm={8}>
            <div>
              <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>
                选择市场
              </label>
              <Select
                value={market}
                onChange={handleMarketChange}
                style={{ width: '100%' }}
              >
                <Option value="a_share">A股市场</Option>
                <Option value="hong_kong">港股市场</Option>
                <Option value="nasdaq">美股市场</Option>
              </Select>
            </div>
          </Col>
          <Col xs={24} sm={8}>
            <div>
              <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>
                时间范围
              </label>
              <RangePicker
                style={{ width: '100%' }}
                onChange={handleDateRangeChange}
              />
            </div>
          </Col>
        </Row>
      </Card>

      <Tabs defaultActiveKey="trend" type="card">
        <TabPane tab="择时评分趋势" key="trend">
          <Card className="card-shadow">
            <TimingScoreChart
              data={mockChartData.timingScoreTrend}
              loading={loading}
            />
          </Card>
        </TabPane>

        <TabPane tab="指标分解" key="breakdown">
          <Card className="card-shadow">
            <IndicatorBreakdownChart
              data={mockChartData.indicatorBreakdown}
              loading={loading}
            />
          </Card>
        </TabPane>

        <TabPane tab="仓位配置" key="position">
          <Card className="card-shadow">
            <PositionSizingChart
              data={mockChartData.positionSizing}
              loading={loading}
            />
          </Card>
        </TabPane>

        <TabPane tab="市场比较" key="comparison">
          <Card className="card-shadow">
            <MarketComparisonChart
              data={mockChartData.marketComparison}
              loading={loading}
            />
          </Card>
        </TabPane>
      </Tabs>
    </div>
  )
}

export default Visualization