import React from 'react'
import ReactECharts from 'echarts-for-react'
import { Spin, Empty } from 'antd'

const IndicatorBreakdownChart = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
      </div>
    )
  }

  if (!data) {
    return <Empty description="暂无数据" />
  }

  const option = {
    title: {
      text: '指标分解分析',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c}分 ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['宏观基本面', '行业基本面', '市场情绪'],
    },
    series: [
      {
        name: '指标分解',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 18,
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data: [
          {
            value: data.macro,
            name: '宏观基本面',
            itemStyle: {
              color: '#1890ff',
            },
          },
          {
            value: data.industry,
            name: '行业基本面',
            itemStyle: {
              color: '#52c41a',
            },
          },
          {
            value: data.sentiment,
            name: '市场情绪',
            itemStyle: {
              color: '#faad14',
            },
          },
        ],
      },
    ],
  }

  return (
    <ReactECharts
      option={option}
      style={{ height: 400 }}
      opts={{ renderer: 'canvas' }}
    />
  )
}

export default IndicatorBreakdownChart