import React from 'react';
import { Layout, Typography } from 'antd';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

function App() {
  return (
    <Layout className="app-layout">
      <Header className="app-header">
        <Title level={2} style={{ color: 'white', margin: 0 }}>
          量化择时指标分析系统
        </Title>
      </Header>

      <Content className="app-content">
        <div className="content-wrapper">
          <h1>欢迎使用量化择时指标分析系统</h1>
          <p>基于多维度择时框架的专业投资分析工具</p>
          <p>系统正在开发中...</p>
        </div>
      </Content>

      <Footer className="app-footer">
        ValueInvestingLearn ©2025 - 量化择时指标应用
      </Footer>
    </Layout>
  );
}

export default App;