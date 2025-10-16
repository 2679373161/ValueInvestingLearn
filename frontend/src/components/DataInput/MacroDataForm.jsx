import React from 'react'
import { Form, Input, Button, Select, DatePicker, Row, Col, message } from 'antd'
import { dataInputAPI } from '@services/api'
import dayjs from 'dayjs'

const { Option } = Select

const MacroDataForm = () => {
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
      await dataInputAPI.addMacroData(submitData)

      message.success('宏观数据保存成功')
      form.resetFields()
    } catch (error) {
      console.error('保存宏观数据失败:', error)
      message.error(error.message || '保存宏观数据失败')
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
            label="PMI"
            name="pmi"
            help="采购经理指数，50为荣枯线"
            rules={[
              { type: 'number', min: 0, max: 100, message: 'PMI应在0-100之间' },
            ]}
          >
            <Input
              type="number"
              step="0.1"
              placeholder="例如：50.5"
              suffix="%"
            />
          </Form.Item>
        </Col>

        <Col xs={24} sm={12}>
          <Form.Item
            label="CPI"
            name="cpi"
            help="消费者物价指数"
            rules={[
              { type: 'number', min: -10, max: 50, message: 'CPI应在-10%到50%之间' },
            ]}
          >
            <Input
              type="number"
              step="0.1"
              placeholder="例如：2.1"
              suffix="%"
            />
          </Form.Item>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col xs={24} sm={12}>
          <Form.Item
            label="PPI"
            name="ppi"
            help="生产者物价指数"
            rules={[
              { type: 'number', min: -20, max: 50, message: 'PPI应在-20%到50%之间' },
            ]}
          >
            <Input
              type="number"
              step="0.1"
              placeholder="例如：1.8"
              suffix="%"
            />
          </Form.Item>
        </Col>

        <Col xs={24} sm={12}>
          <Form.Item
            label="M2增速"
            name="m2"
            help="广义货币供应量增速"
            rules={[
              { type: 'number', min: -10, max: 30, message: 'M2增速应在-10%到30%之间' },
            ]}
          >
            <Input
              type="number"
              step="0.1"
              placeholder="例如：8.5"
              suffix="%"
            />
          </Form.Item>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col xs={24} sm={12}>
          <Form.Item
            label="利率"
            name="interest_rate"
            help="基准利率"
            rules={[
              { type: 'number', min: 0, max: 20, message: '利率应在0%到20%之间' },
            ]}
          >
            <Input
              type="number"
              step="0.1"
              placeholder="例如：3.0"
              suffix="%"
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

export default MacroDataForm