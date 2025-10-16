import React from 'react'
import { Layout, Button, Space, Typography, Switch } from 'antd'
import { MenuFoldOutlined, MenuUnfoldOutlined, BulbOutlined } from '@ant-design/icons'
import { useTheme } from '@contexts/ThemeContext'

const { Header } = Layout
const { Title } = Typography

const AppHeader = ({ collapsed, onToggle }) => {
  const { theme, toggleTheme, isDark } = useTheme()

  return (
    <Header
      style={{
        padding: '0 24px',
        background: 'var(--header-bg, #fff)',
        boxShadow: '0 1px 4px rgba(0,21,41,.08)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}
    >
      <Space>
        <Button
          type="text"
          icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
          onClick={onToggle}
          style={{
            fontSize: '16px',
            width: 64,
            height: 64,
          }}
        />
        <Title level={4} style={{ margin: 0, color: 'var(--primary-color, #1890ff)' }}>
          量化择时指标应用
        </Title>
      </Space>

      <Space>
        <span style={{ color: 'var(--text-secondary, #666)' }}>
          基于多维度择时框架的量化分析工具
        </span>

        <Space>
          <BulbOutlined style={{ color: isDark ? '#ffd666' : '#faad14' }} />
          <Switch
            checked={isDark}
            onChange={toggleTheme}
            checkedChildren="暗色"
            unCheckedChildren="亮色"
          />
        </Space>
      </Space>
    </Header>
  )
}

export default AppHeader