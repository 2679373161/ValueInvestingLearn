# 量化择时指标应用 - 用户使用指南

## 概述

量化择时指标应用是一个基于多维度择时框架的量化分析工具，帮助投资者进行投资时机分析和决策。该应用支持A股、港股、美股市场的择时分析，并提供AI辅助决策功能。

## 快速开始

### 1. 环境要求

- Python 3.8+
- Node.js 14+ (前端开发)
- Conda (推荐用于环境管理)

### 2. 安装和配置

#### 后端服务安装

```bash
# 克隆项目
git clone <repository-url>
cd ValueInvestingLearn

# 创建conda环境
conda create -n value_investing python=3.9
conda activate value_investing

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp config/config.example.json config/config.json
# 编辑config.json文件，配置API密钥等参数
```

#### 前端服务安装

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 3. 启动应用

#### 启动后端服务

```bash
# 在项目根目录
python run.py
```

后端服务将在 `http://localhost:5000` 启动

#### 启动前端服务

```bash
# 在前端目录
cd frontend
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

## 功能使用

### 1. 数据管理

#### 添加宏观数据

通过API或前端界面添加宏观数据：

```bash
POST /api/data/macro
```

请求体示例：
```json
{
  "date": "2024-01-15",
  "market": "a_share",
  "pmi": 50.5,
  "cpi": 2.1,
  "ppi": 1.8,
  "m2": 8.5,
  "interest_rate": 3.0
}
```

#### 添加市场情绪数据

```bash
POST /api/data/market-sentiment
```

请求体示例：
```json
{
  "date": "2024-01-15",
  "market": "a_share",
  "volatility": 15.5,
  "investor_sentiment": 65.0,
  "technical_indicators": {
    "rsi": 55.0,
    "macd": 2.5,
    "bollinger_bands": 1.2
  }
}
```

#### 添加行业数据

```bash
POST /api/data/industry
```

请求体示例：
```json
{
  "date": "2024-01-15",
  "market": "a_share",
  "industry": "technology",
  "free_cash_flow": 120.5,
  "industry_sentiment": 70.0
}
```

### 2. 择时分析

#### 计算择时指标

```bash
POST /api/analysis/timing-indicators
```

请求体示例：
```json
{
  "market": "a_share",
  "date": "2024-01-15"
}
```

响应示例：
```json
{
  "timing_score": 78,
  "indicators": {
    "macro": {
      "score": 85,
      "breakdown": {
        "pmi": 82,
        "cpi": 75,
        "ppi": 88,
        "m2": 90,
        "interest_rate": 80
      }
    },
    "industry": {
      "score": 72,
      "breakdown": {
        "free_cash_flow": 70,
        "industry_sentiment": 74
      }
    },
    "sentiment": {
      "score": 77,
      "breakdown": {
        "volatility": 80,
        "investor_sentiment": 75,
        "rsi": 78,
        "macd": 76,
        "bollinger_bands": 74
      }
    }
  }
}
```

#### AI分析

```bash
POST /api/analysis/ai-analysis
```

请求体示例：
```json
{
  "market": "a_share",
  "timing_indicators": {
    "macro_score": 85,
    "industry_score": 72,
    "sentiment_score": 77
  }
}
```

响应示例：
```json
{
  "summary": "当前市场整体处于中性偏乐观状态...",
  "recommendations": [
    "关注科技和消费行业的投资机会",
    "建议配置60%的权益类资产"
  ],
  "risk_level": "中等"
}
```

#### 仓位计算

```bash
POST /api/analysis/position-sizing
```

请求体示例：
```json
{
  "market": "a_share",
  "timing_score": 78,
  "risk_tolerance": "中等"
}
```

响应示例：
```json
{
  "suggested_position": 60,
  "max_position": 80,
  "min_position": 40,
  "allocation": {
    "equities": 60,
    "bonds": 20,
    "cash": 20
  }
}
```

### 3. 可视化分析

#### 择时评分趋势

```bash
GET /api/visualization/timing-score-trend?market=a_share&start_date=2024-01-01&end_date=2024-01-31
```

#### 市场比较

```bash
GET /api/visualization/market-comparison-chart
```

#### 指标分解

```bash
GET /api/visualization/indicator-breakdown?market=a_share&date=2024-01-15
```

#### 仪表盘摘要

```bash
GET /api/visualization/dashboard-summary?market=a_share&date=2024-01-15
```

## 使用示例

### Python客户端示例

```python
import requests

BASE_URL = "http://localhost:5000"

# 添加宏观数据
def add_macro_data():
    data = {
        "date": "2024-01-15",
        "market": "a_share",
        "pmi": 50.5,
        "cpi": 2.1,
        "ppi": 1.8,
        "m2": 8.5,
        "interest_rate": 3.0
    }

    response = requests.post(f"{BASE_URL}/api/data/macro", json=data)
    return response.json()

# 获取择时分析
def get_timing_analysis():
    data = {
        "market": "a_share",
        "date": "2024-01-15"
    }

    response = requests.post(f"{BASE_URL}/api/analysis/timing-indicators", json=data)
    return response.json()

# 获取AI分析建议
def get_ai_analysis():
    data = {
        "market": "a_share",
        "timing_indicators": {
            "macro_score": 85,
            "industry_score": 72,
            "sentiment_score": 77
        }
    }

    response = requests.post(f"{BASE_URL}/api/analysis/ai-analysis", json=data)
    return response.json()
```

### JavaScript客户端示例

```javascript
const BASE_URL = 'http://localhost:5000';

// 获取择时评分趋势
async function getTimingScoreTrend(market, startDate, endDate) {
  const params = new URLSearchParams({
    market,
    start_date: startDate,
    end_date: endDate
  });

  const response = await fetch(`${BASE_URL}/api/visualization/timing-score-trend?${params}`);
  return await response.json();
}

// 添加市场情绪数据
async function addMarketSentiment(data) {
  const response = await fetch(`${BASE_URL}/api/data/market-sentiment`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });

  return await response.json();
}

// 计算仓位配置
async function calculatePositionSizing(market, timingScore, riskTolerance) {
  const data = {
    market,
    timing_score: timingScore,
    risk_tolerance: riskTolerance
  };

  const response = await fetch(`${BASE_URL}/api/analysis/position-sizing`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });

  return await response.json();
}
```

## 配置说明

### AI配置

在 `config/config.json` 中配置AI服务：

```json
{
  "ai": {
    "api_key": "your-deepseek-api-key-here",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "max_tokens": 2000,
    "temperature": 0.7,
    "cache_enabled": true,
    "cache_ttl_minutes": 60
  }
}
```

### 市场配置

```json
{
  "markets": {
    "a_share": {
      "name": "A股市场",
      "currency": "CNY",
      "timezone": "Asia/Shanghai"
    },
    "hong_kong": {
      "name": "港股市场",
      "currency": "HKD",
      "timezone": "Asia/Hong_Kong"
    },
    "nasdaq": {
      "name": "美股市场",
      "currency": "USD",
      "timezone": "America/New_York"
    }
  }
}
```

### 择时权重配置

```json
{
  "timing_weights": {
    "macro_fundamental": 0.4,
    "industry_fundamental": 0.3,
    "market_sentiment": 0.3
  }
}
```

## 故障排除

### 常见问题

1. **AI功能无法使用**
   - 检查 `config.json` 中的AI API密钥配置
   - 确认网络连接正常
   - 查看日志文件了解详细错误信息

2. **数据保存失败**
   - 检查数据目录权限
   - 验证数据格式是否符合要求
   - 查看后端日志了解具体错误

3. **前端无法连接后端**
   - 确认后端服务正在运行
   - 检查CORS配置
   - 验证端口配置

4. **测试失败**
   - 运行 `python run_tests.py` 查看详细错误
   - 检查测试数据文件是否存在
   - 确认依赖包已正确安装

### 日志查看

后端日志位于控制台输出，包含以下信息：
- 应用启动状态
- API请求和响应
- 错误和异常信息
- AI服务调用状态

前端日志位于浏览器开发者工具控制台。

## 技术支持

如有问题或建议，请通过以下方式联系：

- 项目GitHub Issues: [项目地址]
- 开发团队邮箱: [联系邮箱]

## 版本历史

- **v1.0.0** (2024-01-15): 初始版本发布
  - 数据管理功能
  - 择时指标计算
  - AI分析功能
  - 可视化图表
  - 完整的API文档

---

**注意**: 本应用仅供学习和研究使用，不构成投资建议。投资有风险，决策需谨慎。