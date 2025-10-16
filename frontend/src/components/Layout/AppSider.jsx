import React from 'react'
import { Layout, Menu } from 'antd'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  DashboardOutlined,
  FormOutlined,
  BarChartOutlined,
  LineChartOutlined,
  GlobalOutlined,
} from '@ant-design/icons'

const { Sider } = Layout

const menuItems = [
  {
    key: '/dashboard',
    icon: <DashboardOutlined />,
    label: '仪表盘',
  },
  {
    key: '/data-input',
    icon: <FormOutlined />,
    label: '数据输入',
  },
  {
    key: '/analysis',
    icon: <BarChartOutlined />,
    label: '分析结果',
  },
  {
    key: '/visualization',
    icon: <LineChartOutlined />,
    label: '可视化',
  },
  {
    key: '/market-comparison',
    icon: <GlobalOutlined />,
    label: '市场比较',
  },
]

const AppSider = ({ collapsed }) => {
  const navigate = useNavigate()
  const location = useLocation()

  const handleMenuClick = ({ key }) => {
    navigate(key)
  }

  return (
    <Sider
      trigger={null}
      collapsible
      collapsed={collapsed}
      style={{
        background: '#fff',
        boxShadow: '2px 0 8px rgba(0,21,41,.15)',
      }}
    >
      <div
        style={{
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderBottom: '1px solid #f0f0f0',
        }}
      >
        {!collapsed && (
          <div
            style={{
              fontSize: '16px',
              fontWeight: 'bold',
              color: '#1890ff',
            }}
          >
            量化择时
          </div>
        )}
      </div>

      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={handleMenuClick}
        style={{
          border: 'none',
          marginTop: '8px',
        }}
      />
    </Sider>
  )
}

export default AppSider