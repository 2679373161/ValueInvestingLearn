import React from 'react'
import { Form, Input, Button, Select, DatePicker, Row, Col, message } from 'antd'
import { dataInputAPI } from '@services/api'
import dayjs from 'dayjs'

const { Option } = Select

const IndustryDataForm = () => {
  const [form] = Form.useForm()
  const [loading, setLoading] = React.useState(false)

  const onFinish = async (values) => {
    try {
      setLoading(true)

      // 格式化数据
      const submitData = {
        ...values,
        date: values.date.format('YYYY-MM-DD'),
      }

      // 调用API
      await dataInputAPI.addIndustryData(submitData)

      message.success('行业数据保存成功')
      form.resetFields()
    } catch (error) {
      console.error('保存行业数据失败:', error)
      message.error(error.message || '保存行业数据失败')
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

      <Row gutter={16}>
        <Col xs={24} sm={12}>
          <Form.Item
            label="行业"
            name="industry"
            rules={[{ required: true, message: '请选择行业' }]}
          >
            <Select placeholder="选择行业">
              <Option value="technology">科技</Option>
              <Option value="finance">金融</Option>
              <Option value="healthcare">医疗保健</Option>
              <Option value="consumer">消费</Option>
              <Option value="energy">能源</Option>
              <Option value="real_estate">房地产</Option>
              <Option value="materials">原材料</Option>
              <Option value="industrial">工业</Option>
            </Select>
          </Form.Item>
        </Col>

        <Col xs={24} sm={12}>
          <Form.Item
            label="自由现金流（亿元）"
            name="free_cash_flow"
            help="行业自由现金流，正值表示现金流入"
            rules={[
              { type: 'number', min: -10000, max: 10000, message: '自由现金流应在-10000到10000亿元之间' },
            ]}
          >
            <Input
              type="number"
              step="0.1"
              placeholder="例如：120.5"
            />
          </Form.Item>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col xs={24} sm={12}>
          <Form.Item
            label="行业情绪"
            name="industry_sentiment"
            help="行业情绪指数，0-100"
            rules={[
              { type: 'number', min: 0, max: 100, message: '行业情绪应在0-100之间' },
            ]}
          >
            <Input
              type="number"
              min={0}
              max={100}
              step="1"
              placeholder="例如：70"
              suffix="/100"
            />
          </Form.Item>
        </Col>
      </Row>

      <Form.Item>
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

export default IndustryDataForm