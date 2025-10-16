import React from 'react'
import { Form, Input, Button, Select, DatePicker, Row, Col, message, Card } from 'antd'
import { dataInputAPI } from '@services/api'
import dayjs from 'dayjs'

const { Option } = Select

const MarketSentimentForm = () => {
  const [form] = Form.useForm()
  const [loading, setLoading] = React.useState(false)

  const onFinish = async (values) => {
    try {
      setLoading(true)

      // 格式化数据
      const submitData = {
        ...values,
        date: values.date.format('YYYY-MM-DD'),
        technical_indicators: {
          rsi: values.rsi,
          macd: values.macd,
          bollinger_bands: values.bollinger_bands,
        },
      }

      // 删除原始的技术指标字段
      delete submitData.rsi
      delete submitData.macd
      delete submitData.bollinger_bands

      // 调用API
      await dataInputAPI.addMarketSentiment(submitData)

      message.success('市场情绪数据保存成功')
      form.resetFields()
    } catch (error) {
      console.error('保存市场情绪数据失败:', error)
      message.error(error.message || '保存市场情绪数据失败')
    } finally {
      setLoading(false)
    }
  }

  const onReset = () => {
    form.resetFields()
  }

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      style={{ maxWidth: 600 }}
    >
      <Row gutter={16}>
        <Col xs={24} sm={12}>
          <Form.Item
            label="日期"
            name="date"
            rules={[{ required: true, message: '请选择日期' }]}
          >
            <DatePicker
              style={{ width: '100%' }}
              disabledDate={(current) => current && current > dayjs().endOf('day')}
            />
          </Form.Item>
        </Col>

        <Col xs={24} sm={12}>
          <Form.Item
            label="市场"
            name="market"
            rules={[{ required: true, message: '请选择市场' }]}
          >
            <Select placeholder="选择市场">
              <Option value="a_share">A股市场</Option>
              <Option value="hong_kong">港股市场</Option>
              <Option value="nasdaq">美股市场</Option>
            </Select>
          </Form.Item>
        </Col>
      </Row>

      <Card title="市场情绪指标" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col xs={24} sm={12}>
            <Form.Item
              label="波动率"
              name="volatility"
              help="市场波动率，越低越好"
              rules={[
                { type: 'number', min: 0, max: 100, message: '波动率应在0-100%之间' },
              ]}
            >
              <Input
                type="number"
                step="0.1"
                placeholder="例如：15.5"
                suffix="%"
              />
            </Form.Item>
          </Col>

          <Col xs={24} sm={12}>
            <Form.Item
              label="投资者情绪"
              name="investor_sentiment"
              help="投资者情绪指数，0-100"
              rules={[
                { type: 'number', min: 0, max: 100, message: '投资者情绪应在0-100之间' },
              ]}
            >
              <Input
                type="number"
                min={0}
                max={100}
                step="1"
                placeholder="例如：65"
                suffix="/100"
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="技术指标">
        <Row gutter={16}>
          <Col xs={24} sm={8}>
            <Form.Item
              label="RSI"
              name="rsi"
              help="相对强弱指数，30-70为合理区间"
              rules={[
                { type: 'number', min: 0, max: 100, message: 'RSI应在0-100之间' },
              ]}
            >
              <Input
                type="number"
                min={0}
                max={100}
                step="0.1"
                placeholder="例如：55.0"
              />
            </Form.Item>
          </Col>

          <Col xs={24} sm={8}>
            <Form.Item
              label="MACD"
              name="macd"
              help="移动平均收敛散度，正值为看涨"
              rules={[
                { type: 'number', min: -10, max: 10, message: 'MACD应在-10到10之间' },
              ]}
            >
              <Input
                type="number"
                step="0.1"
                placeholder="例如：2.5"
              />
            </Form.Item>
          </Col>

          <Col xs={24} sm={8}>
            <Form.Item
              label="布林带位置"
              name="bollinger_bands"
              help="价格在布林带中的位置，绝对值越小越好"
              rules={[
                { type: 'number', min: -3, max: 3, message: '布林带位置应在-3到3之间' },
              ]}
            >
              <Input
                type="number"
                step="0.1"
                placeholder="例如：1.2"
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Form.Item style={{ marginTop: 24 }}>
        <Button type="primary" htmlType="submit" loading={loading}>
          保存数据
        </Button>
        <Button style={{ marginLeft: 8 }} onClick={onReset}>
          重置
        </Button>
      </Form.Item>
    </Form>
  )
}

export default MarketSentimentForm