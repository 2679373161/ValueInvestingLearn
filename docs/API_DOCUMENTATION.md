# 量化择时指标应用 API 文档

## 概述

量化择时指标应用提供基于多维度择时框架的量化分析工具API。该API支持数据输入、指标计算、AI分析和可视化功能。

**基础URL**: `http://localhost:5000`

## 快速开始

### 1. 健康检查
```bash
GET /health
```

### 2. API文档
```bash
GET /api/docs
```

## API端点

### 数据管理模块

#### 宏观数据

**添加宏观数据**
```bash
POST /api/data/macro
```

**请求体**:
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

**获取宏观数据**
```bash
GET /api/data/macro?market=a_share&start_date=2024-01-01&end_date=2024-01-31
```

#### 市场情绪数据

**添加市场情绪数据**
```bash
POST /api/data/market-sentiment
```

**请求体**:
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

#### 行业数据

**添加行业数据**
```bash
POST /api/data/industry
```

**请求体**:
```json
{
  "date": "2024-01-15",
  "market": "a_share",
  "industry": "technology",
  "free_cash_flow": 120.5,
  "industry_sentiment": 70.0
}
```

### 分析模块

#### 择时指标计算

**计算择时指标**
```bash
POST /api/analysis/timing-indicators
```

**请求体**:
```json
{
  "market": "a_share",
  "date": "2024-01-15"
}
```

**响应**:
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

**获取AI分析**
```bash
POST /api/analysis/ai-analysis
```

**请求体**:
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

**响应**:
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

**计算仓位配置**
```bash
POST /api/analysis/position-sizing
```

**请求体**:
```json
{
  "market": "a_share",
  "timing_score": 78,
  "risk_tolerance": "中等"
}
```

**响应**:
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

#### 市场比较

**获取市场比较**
```bash
GET /api/analysis/market-comparison
```

**查询参数**:
- `date`: 日期 (可选)

**响应**:
```json
{
  "a_share": 78,
  "hong_kong": 72,
  "nasdaq": 85
}
```

#### 分析摘要

**获取分析摘要**
```bash
GET /api/analysis/summary
```

**查询参数**:
- `market`: 市场类型
- `date`: 日期 (可选)

### 可视化模块

#### 择时评分趋势

**获取择时评分趋势**
```bash
GET /api/visualization/timing-score-trend
```

**查询参数**:
- `market`: 市场类型
- `start_date`: 开始日期
- `end_date`: 结束日期

**响应**:
```json
[
  {"date": "2024-01-01", "score": 65},
  {"date": "2024-01-02", "score": 68},
  {"date": "2024-01-03", "score": 72}
]
```

#### 市场比较图表

**获取市场比较图表数据**
```bash
GET /api/visualization/market-comparison-chart
```

**查询参数**:
- `date`: 日期 (可选)

#### 指标分解

**获取指标分解数据**
```bash
GET /api/visualization/indicator-breakdown
```

**查询参数**:
- `market`: 市场类型
- `date`: 日期 (可选)

#### 仓位配置图表

**获取仓位配置数据**
```bash
GET /api/visualization/position-sizing-chart
```

**查询参数**:
- `market`: 市场类型
- `date`: 日期 (可选)

#### 市场情绪分析

**获取市场情绪分析数据**
```bash
GET /api/visualization/sentiment-analysis
```

#### 宏观指标

**获取宏观指标数据**
```bash
GET /api/visualization/macro-indicators
```

#### 仪表盘摘要

**获取仪表盘摘要数据**
```bash
GET /api/visualization/dashboard-summary
```

## 错误处理

所有API端点都遵循统一的错误响应格式：

```json
{
  "error": "错误类型",
  "message": "错误描述"
}
```

### 常见HTTP状态码

- `200`: 请求成功
- `201`: 创建成功
- `400`: 请求参数错误
- `404`: 资源未找到
- `500`: 服务器内部错误

## 数据格式

### 市场类型
- `a_share`: A股市场
- `hong_kong`: 港股市场
- `nasdaq`: 美股市场

### 行业类型
- `technology`: 科技
- `finance`: 金融
- `healthcare`: 医疗保健
- `consumer`: 消费
- `energy`: 能源
- `real_estate`: 房地产
- `materials`: 原材料
- `industrial`: 工业

### 风险等级
- `低`: 低风险
- `中等`: 中等风险
- `高`: 高风险

## 使用示例

### Python示例

```python
import requests

# 基础URL
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

# 获取分析摘要
def get_analysis_summary():
    params = {
        "market": "a_share",
        "date": "2024-01-15"
    }

    response = requests.get(f"{BASE_URL}/api/analysis/summary", params=params)
    return response.json()
```

### JavaScript示例

```javascript
// 使用fetch API
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
```

## 版本历史

- **v1.0.0** (2024-01-15): 初始版本发布
  - 数据管理API
  - 分析计算API
  - 可视化数据API

## 技术支持

如有问题或建议，请联系开发团队。