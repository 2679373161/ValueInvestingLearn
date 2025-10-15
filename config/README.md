# 配置管理

## 配置文件说明

### config.template.json
配置模板文件，包含所有可配置项的默认值和说明。

### config.json
实际使用的配置文件（需要手动创建）。系统会在首次运行时自动基于模板创建。

### .env.example
环境变量示例文件，用于敏感信息的配置。

## 配置结构

### 应用配置 (app)
- `name`: 应用名称
- `version`: 应用版本
- `environment`: 运行环境 (development/production)
- `debug`: 调试模式
- `secret_key`: 应用密钥

### 服务器配置 (server)
- `host`: 服务器主机
- `port`: 服务器端口
- `cors_origins`: CORS允许的源

### AI配置 (ai)
- `provider`: AI提供商 (deepseek)
- `api_key`: API密钥
- `base_url`: API基础URL
- `model`: 使用的模型
- `max_tokens`: 最大token数
- `temperature`: 生成温度

### 择时指标配置 (timing_indicators)
- `weights`: 各维度权重配置
- `macro_indicators`: 宏观指标配置
- `industry_indicators`: 行业指标配置
- `market_sentiment_indicators`: 市场情绪指标配置

### 市场配置 (markets)
- `a_share`: A股市场配置
- `hong_kong`: 港股市场配置
- `nasdaq`: 纳指配置

### 数据源配置 (data_sources)
- `macro_data`: 宏观数据配置
- `market_sentiment`: 市场情绪数据配置

### 仓位配置 (position_sizing)
- 基于择时评分的仓位建议配置

## 配置优先级

1. 环境变量 (最高优先级)
2. config.json 文件
3. 默认值 (最低优先级)

## 敏感信息配置

对于API密钥等敏感信息，建议使用环境变量：

1. 复制 `.env.example` 为 `.env`
2. 在 `.env` 中填写实际值
3. 确保 `.env` 文件在 `.gitignore` 中

## 配置验证

系统会在启动时自动验证配置：

- 检查必需配置项
- 验证权重总和
- 检查API密钥
- 验证数据目录

## 配置更新

配置可以在运行时动态更新，但需要调用 `save_config()` 方法保存到文件。