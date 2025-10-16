import React from 'react'
import { Card, Typography, Alert, Row, Col, Statistic, Tag, Progress, Button, Space, Table } from 'antd'
import { analysisAPI } from '@services/api'

const { Title, Text } = Typography

const Analysis = () => {
  const [loading, setLoading] = React.useState(false)
  const [analysisData, setAnalysisData] = React.useState(null)

  const loadAnalysisData = async () => {
    try {
      setLoading(true)
      const response = await analysisAPI.getAnalysisSummary()
      setAnalysisData(response.data)
    } catch (error) {
      console.error('加载分析数据失败:', error)
    } finally {
      setLoading(false)
    }
  }

  React.useEffect(() => {
    loadAnalysisData()
  }, [])

  // 模拟数据
  const mockAnalysisData = {
    timingScore: 78,
    market: 'a_share',
    date: '2024-01-15',
    indicators: {
      macro: {
        score: 85,
        breakdown: {
          pmi: 82,
          cpi: 75,
          ppi: 88,
          m2: 90,
          interest_rate: 80
        }
      },
      industry: {
        score: 72,
        breakdown: {
          free_cash_flow: 70,
          industry_sentiment: 74
        }
      },
      sentiment: {
        score: 77,
        breakdown: {
          volatility: 80,
          investor_sentiment: 75,
          rsi: 78,
          macd: 76,
          bollinger_bands: 74
        }
      }
    },
    aiAnalysis: {
      summary: '当前市场整体处于中性偏乐观状态，宏观基本面稳健，市场情绪温和，建议适度增加仓位。',
      recommendations: [
        '关注科技和消费行业的投资机会',
        '建议配置60%的权益类资产',
        '保持20%的现金储备应对市场波动',
        '建议关注政策面的变化'
      ],
      riskLevel: '中等'
    },
    positionSizing: {
      suggestedPosition: 60,
      maxPosition: 80,
      minPosition: 40,
      allocation: {
        equities: 60,
        bonds: 20,
        cash: 20
      }
    }
  }

  const data = analysisData || mockAnalysisData

  const getScoreColor = (score) => {
    if (score >= 80) return '#52c41a'
    if (score >= 60) return '#faad14'
    return '#ff4d4f'
  }

  const getRiskLevelColor = (level) => {
    switch (level) {
      case '低': return '#52c41a'
      case '中等': return '#faad14'
      case '高': return '#ff4d4f'
      default: return '#d9d9d9'
    }
  }

  const indicatorColumns = [
    {
      title: '指标类型',
      dataIndex: 'type',
      key: 'type',
    },
    {
      title: '评分',
      dataIndex: 'score',
      key: 'score',
      render: (score) => (
        <Progress
          percent={score}
          size="small"
          strokeColor={getScoreColor(score)}
          format={(percent) => `${percent}分`}
        />
      ),
    },
    {
      title: '权重',
      dataIndex: 'weight',
      key: 'weight',
      render: (weight) => `${weight}%`,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === '良好' ? 'green' : status === '一般' ? 'orange' : 'red'}>
          {status}
        </Tag>
      ),
    },
  ]

  // 确保数据存在后再计算indicatorData
  const indicatorData = data && data.indicators ? [
    {
      key: '1',
      type: '宏观基本面',
      score: data.indicators.macro.score,
      weight: 40,
      status: data.indicators.macro.score >= 80 ? '良好' : data.indicators.macro.score >= 60 ? '一般' : '较差',
    },
    {
      key: '2',
      type: '行业基本面',
      score: data.indicators.industry.score,
      weight: 30,
      status: data.indicators.industry.score >= 80 ? '良好' : data.indicators.industry.score >= 60 ? '一般' : '较差',
    },
    {
      key: '3',
      type: '市场情绪',
      score: data.indicators.sentiment.score,
      weight: 30,
      status: data.indicators.sentiment.score >= 80 ? '良好' : data.indicators.sentiment.score >= 60 ? '一般' : '较差',
    },
  ] : []

  // 如果数据不存在，显示加载状态
  if (!data) {
    return (
      <div className="page-container">
        <Title level={2}>分析结果</Title>
        <Alert
          message="数据加载中..."
          description="正在获取分析数据，请稍候。"
          type="info"
          showIcon
        />
      </div>
    )
  }

  return (
    <div className="page-container">
      <Title level={2}>分析结果</Title>

      <Alert
        message="分析结果说明"
        description="基于多维度择时框架的综合分析结果，包含择时指标评分、AI智能分析和仓位配置建议。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      {/* 综合评分卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={8}>
          <Card className="card-shadow">
            <Statistic
              title="综合择时评分"
              value={data.timingScore}
              suffix="/100"
              valueStyle={{ color: getScoreColor(data.timingScore) }}
            />
            <div style={{ marginTop: 16 }}>
              <Text type="secondary">市场: {data.market === 'a_share' ? 'A股' : data.market === 'hong_kong' ? '港股' : '美股'}</Text>
              <br />
              <Text type="secondary">日期: {data.date}</Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card className="card-shadow">
            <Statistic
              title="AI分析风险等级"
              value={data?.aiAnalysis?.riskLevel || '未知'}
              valueStyle={{ color: getRiskLevelColor(data?.aiAnalysis?.riskLevel || '未知') }}
            />
            <div style={{ marginTop: 16 }}>
              <Text type="secondary">基于深度学习和市场数据</Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card className="card-shadow">
            <Statistic
              title="建议仓位"
              value={data?.positionSizing?.suggestedPosition || 0}
              suffix="%"
              valueStyle={{ color: '#1890ff' }}
            />
            <div style={{ marginTop: 16 }}>
              <Text type="secondary">范围: {data?.positionSizing?.minPosition || 0}% - {data?.positionSizing?.maxPosition || 0}%</Text>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 择时指标分析 */}
      <Card title="择时指标分析" className="card-shadow" style={{ marginBottom: 24 }}>
        <Table
          columns={indicatorColumns}
          dataSource={indicatorData}
          pagination={false}
          loading={loading}
        />

        <div style={{ marginTop: 24 }}>
          <Title level={5}>指标分解详情</Title>
          <Row gutter={16}>
            <Col xs={24} sm={8}>
              <Card size="small" title="宏观指标" style={{ marginBottom: 16 }}>
                {data?.indicators?.macro?.breakdown && Object.entries(data.indicators.macro.breakdown).map(([key, value]) => (
                  <div key={key} style={{ marginBottom: 8, display: 'flex', justifyContent: 'space-between' }}>
                    <Text>{key.toUpperCase()}</Text>
                    <Text strong style={{ color: getScoreColor(value) }}>
                      {value}分
                    </Text>
                  </div>
                ))}
              </Card>
            </Col>
            <Col xs={24} sm={8}>
              <Card size="small" title="行业指标" style={{ marginBottom: 16 }}>
                {data?.indicators?.industry?.breakdown && Object.entries(data.indicators.industry.breakdown).map(([key, value]) => (
                  <div key={key} style={{ marginBottom: 8, display: 'flex', justifyContent: 'space-between' }}>
                    <Text>{key === 'free_cash_flow' ? '自由现金流' : '行业情绪'}</Text>
                    <Text strong style={{ color: getScoreColor(value) }}>
                      {value}分
                    </Text>
                  </div>
                ))}
              </Card>
            </Col>
            <Col xs={24} sm={8}>
              <Card size="small" title="情绪指标" style={{ marginBottom: 16 }}>
                {data?.indicators?.sentiment?.breakdown && Object.entries(data.indicators.sentiment.breakdown).map(([key, value]) => (
                  <div key={key} style={{ marginBottom: 8, display: 'flex', justifyContent: 'space-between' }}>
                    <Text>{key.toUpperCase()}</Text>
                    <Text strong style={{ color: getScoreColor(value) }}>
                      {value}分
                    </Text>
                  </div>
                ))}
              </Card>
            </Col>
          </Row>
        </div>
      </Card>

      {/* AI分析结果 */}
      <Card title="AI智能分析" className="card-shadow" style={{ marginBottom: 24 }}>
        <Alert
          message="分析摘要"
          description={data?.aiAnalysis?.summary || '暂无分析摘要'}
          type="info"
          style={{ marginBottom: 16 }}
        />

        <Title level={5}>投资建议</Title>
        <ul style={{ paddingLeft: 20 }}>
          {data?.aiAnalysis?.recommendations?.map((recommendation, index) => (
            <li key={index} style={{ marginBottom: 8 }}>
              <Text>{recommendation}</Text>
            </li>
          ))}
        </ul>

        <div style={{ marginTop: 16 }}>
          <Space>
            <Button type="primary">查看详细分析</Button>
            <Button>导出分析报告</Button>
          </Space>
        </div>
      </Card>

      {/* 仓位配置建议 */}
      <Card title="仓位配置建议" className="card-shadow">
        <Row gutter={16}>
          <Col xs={24} sm={12}>
            <div style={{ marginBottom: 16 }}>
              <Text strong>建议仓位: </Text>
              <Text style={{ color: '#1890ff', fontSize: '18px', fontWeight: 'bold' }}>
                {data?.positionSizing?.suggestedPosition || 0}%
              </Text>
            </div>

            <Progress
              percent={data?.positionSizing?.suggestedPosition || 0}
              strokeColor={{
                '0%': '#108ee9',
                '100%': '#87d068',
              }}
              format={(percent) => `${percent}%`}
            />

            <div style={{ marginTop: 16 }}>
              <Text type="secondary">
                建议仓位范围: {data?.positionSizing?.minPosition || 0}% - {data?.positionSizing?.maxPosition || 0}%
              </Text>
            </div>
          </Col>

          <Col xs={24} sm={12}>
            <Title level={5}>资产配置建议</Title>
            {data?.positionSizing?.allocation && Object.entries(data.positionSizing.allocation).map(([asset, percentage]) => (
              <div key={asset} style={{ marginBottom: 12, display: 'flex', justifyContent: 'space-between' }}>
                <Text>
                  {asset === 'equities' ? '权益类资产' :
                   asset === 'bonds' ? '债券类资产' : '现金储备'}
                </Text>
                <Text strong style={{ color: '#1890ff' }}>
                  {percentage}%
                </Text>
              </div>
            ))}
          </Col>
        </Row>
      </Card>
    </div>
  )
}

export default Analysis