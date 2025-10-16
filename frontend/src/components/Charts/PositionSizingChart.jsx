import React from 'react'
import ReactECharts from 'echarts-for-react'
import { Spin, Empty } from 'antd'

const PositionSizingChart = ({ data, loading }) => {
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
      text: '仓位配置建议',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c}% ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['权益类资产', '债券类资产', '现金储备'],
    },
    series: [
      {
        name: '仓位配置',
        type: 'pie',
        radius: '50%',
        center: ['50%', '60%'],
        data: [
          {
            value: data.equities,
            name: '权益类资产',
            itemStyle: {
              color: '#1890ff',
            },
          },
          {
            value: data.bonds,
            name: '债券类资产',
            itemStyle: {
              color: '#52c41a',
            },
          },
          {
            value: data.cash,
            name: '现金储备',
            itemStyle: {
              color: '#faad14',
            },
          },
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
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

export default PositionSizingChart