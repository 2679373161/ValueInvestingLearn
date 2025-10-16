import React from 'react'
import ReactECharts from 'echarts-for-react'
import { Spin, Empty } from 'antd'

const MarketComparisonChart = ({ data, loading }) => {
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
      text: '市场比较分析',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      formatter: function (params) {
        const param = params[0]
        return `${param.name}<br/>择时评分: ${param.value}分`
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: ['A股市场', '港股市场', '美股市场'],
    },
    yAxis: {
      type: 'value',
      name: '评分',
      min: 0,
      max: 100,
      axisLabel: {
        formatter: '{value} 分',
      },
    },
    series: [
      {
        name: '择时评分',
        type: 'bar',
        barWidth: '60%',
        data: [
          {
            value: data.a_share,
            itemStyle: {
              color: function (params) {
                const score = params.value
                if (score >= 80) return '#52c41a'
                if (score >= 60) return '#faad14'
                return '#ff4d4f'
              },
            },
          },
          {
            value: data.hong_kong,
            itemStyle: {
              color: function (params) {
                const score = params.value
                if (score >= 80) return '#52c41a'
                if (score >= 60) return '#faad14'
                return '#ff4d4f'
              },
            },
          },
          {
            value: data.nasdaq,
            itemStyle: {
              color: function (params) {
                const score = params.value
                if (score >= 80) return '#52c41a'
                if (score >= 60) return '#faad14'
                return '#ff4d4f'
              },
            },
          },
        ],
        label: {
          show: true,
          position: 'top',
          formatter: '{c}分',
          color: '#333',
          fontWeight: 'bold',
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

export default MarketComparisonChart