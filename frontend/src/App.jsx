import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Layout, ConfigProvider, theme as antdTheme } from 'antd'

import { ThemeProvider, useTheme } from '@contexts/ThemeContext'
import AppHeader from '@components/Layout/AppHeader'
import AppSider from '@components/Layout/AppSider'
import Dashboard from '@pages/Dashboard'
import DataInput from '@pages/DataInput'
import Analysis from '@pages/Analysis'
import Visualization from '@pages/Visualization'
import MarketComparison from '@pages/MarketComparison'

import './App.css'

const { Content } = Layout

const AppContent = () => {
  const { isDark } = useTheme()
  const [collapsed, setCollapsed] = React.useState(false)

  const toggleSider = () => {
    setCollapsed(!collapsed)
  }

  return (
    <ConfigProvider
      theme={{
        algorithm: isDark ? antdTheme.darkAlgorithm : antdTheme.defaultAlgorithm,
        token: {
          colorPrimary: '#1890ff',
        },
      }}
    >
      <Layout className="app-layout">
        <AppSider collapsed={collapsed} />
        <Layout>
          <AppHeader collapsed={collapsed} onToggle={toggleSider} />
          <Content className="app-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/data-input" element={<DataInput />} />
              <Route path="/analysis" element={<Analysis />} />
              <Route path="/visualization" element={<Visualization />} />
              <Route path="/market-comparison" element={<MarketComparison />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  )
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  )
}

export default App