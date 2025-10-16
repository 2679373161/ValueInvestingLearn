import React from 'react'
import { Card, Tabs, Typography, Alert } from 'antd'

import MacroDataForm from '@components/DataInput/MacroDataForm'
import MarketSentimentForm from '@components/DataInput/MarketSentimentForm'
import IndustryDataForm from '@components/DataInput/IndustryDataForm'

const { Title } = Typography
const { TabPane } = Tabs

const DataInput = () => {
  return (
    <div className="page-container">
      <Title level={2}>数据输入</Title>

      <Alert
        message="数据输入说明"
        description="请根据实际情况输入宏观基本面、市场情绪和行业基本面数据。所有数据将用于择时指标计算和AI分析。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Card className="card-shadow">
        <Tabs defaultActiveKey="macro" type="card">
          <TabPane tab="宏观基本面数据" key="macro">
            <MacroDataForm />
          </TabPane>
          <TabPane tab="市场情绪数据" key="sentiment">
            <MarketSentimentForm />
          </TabPane>
          <TabPane tab="行业基本面数据" key="industry">
            <IndustryDataForm />
          </TabPane>
        </Tabs>
      </Card>
    </div>
  )
}

export default DataInput