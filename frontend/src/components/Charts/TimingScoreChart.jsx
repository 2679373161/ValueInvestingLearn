import React from 'react'
import ReactECharts from 'echarts-for-react'
import { Spin, Empty } from 'antd'

const TimingScoreChart = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
      </div>
    )
  }

  if (!data || data.length === 0) {
    return <Empty description="暂无数据" />
  }

  const option = {
    title: {
      text: '择时评分趋势',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'axis',
      formatter: function (params) {
        const param = params[0]
        return `${param.axisValue}<br/>择时评分: ${param.value}分`
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
      data: data.map(item => item.date),
      axisLabel: {
        rotate: 45,
      },
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
        type: 'line',
        data: data.map(item => item.score),
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#1890ff',
        },
        itemStyle: {
          color: '#1890ff',
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              {
                offset: 0,
                color: 'rgba(24, 144, 255, 0.3)',
              },
              {
                offset: 1,
                color: 'rgba(24, 144, 255, 0.05)',
              },
            ],
          },
        },
        markLine: {
          data: [
            {
              name: '优秀线',
              yAxis: 80,
              lineStyle: {
                color: '#52c41a',
                type: 'dashed',
              },
              label: {
                formatter: '优秀',
                position: 'end',
              },
            },
            {
              name: '及格线',
              yAxis: 60,
              lineStyle: {
                color: '#faad14',
                type: 'dashed',
              },
              label: {
                formatter: '及格',
                position: 'end',
              },
            },
          ],
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

export default TimingScoreChart