# 量化择时指标应用

基于多维度择时框架的专业投资分析工具，通过整合宏观基本面、行业基本面、市场情绪三个维度的指标，结合AI分析生成每日择时评分和投资建议。

## 🎯 项目特色

- **多维度择时框架**: 宏观基本面 + 行业基本面 + 市场情绪
- **AI智能分析**: 集成DeepSeek API，提供专家级择时建议
- **实时数据支持**: 支持手动输入和实时数据获取双模式
- **多市场覆盖**: A股主要指数、港股、纳指全面跟踪
- **科学仓位建议**: 基于择时强度的仓位配置建议
- **自然语言解释**: AI生成的择时信号专业解读

## 📊 核心功能

### 1. 数据管理
- 宏观基本面数据手动输入（PMI、CPI、PPI等）
- 市场情绪数据双模式输入（手动/实时配置）
- 本地JSON文件数据存储
- 数据验证和清洗

### 2. 指标计算
- 宏观基本面评分计算
- 行业基本面评分（基于自由现金流）
- 市场情绪评分计算
- 综合择时评分（加权平均）

### 3. AI分析
- DeepSeek API集成
- 组合指标智能分析
- 择时建议生成
- 自然语言解释

### 4. 可视化展示
- 择时评分趋势图
- 多维度指标雷达图
- 仓位建议柱状图
- 多市场并行显示

## 🛠️ 技术架构

### 后端技术栈
- **框架**: Flask 3.1.2
- **数据处理**: pandas, numpy
- **AI集成**: OpenAI客户端（DeepSeek API）
- **API文档**: Flask-Swagger-UI
- **测试**: pytest

### 前端技术栈
- **框架**: React 18 + Vite
- **UI组件**: Ant Design
- **图表**: ECharts
- **构建工具**: Vite
- **代码质量**: ESLint, Prettier

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js 16+
- Git

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/ValueInvestingLearn.git
   cd ValueInvestingLearn
   ```

2. **设置Python环境**
   ```bash
   # 使用conda
   conda create -n quant-timing python=3.9 -y
   conda activate quant-timing

   # 安装Python依赖
   pip install -r requirements.txt
   ```

3. **设置前端环境**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **验证环境**
   ```bash
   python scripts/dev_setup.py
   ```

### 运行应用

1. **启动后端服务**
   ```bash
   python app/main.py
   ```
   后端服务将在 http://localhost:5000 启动

2. **启动前端服务**
   ```bash
   cd frontend
   npm run dev
   ```
   前端服务将在 http://localhost:3000 启动

## 📁 项目结构

```
ValueInvestingLearn/
├── app/                    # 后端应用
│   ├── main.py            # Flask主应用
│   ├── routes/            # API路由
│   ├── services/          # 业务逻辑服务
│   ├── models/            # 数据模型
│   └── utils/             # 工具函数
├── frontend/              # 前端应用
│   ├── src/
│   │   ├── components/    # React组件
│   │   ├── services/      # API调用服务
│   │   └── App.js         # 主应用组件
│   └── package.json       # 前端依赖
├── tests/                 # 测试代码
├── config/                # 配置文件
├── data/                  # 数据存储
├── docs/                  # 项目文档
├── scripts/               # 开发脚本
└── tasks/                 # 开发任务管理
```

## 🔧 开发指南

### 代码规范
- Python代码使用Black格式化
- 使用Flake8进行代码检查
- 前端代码使用Prettier格式化
- 提交信息遵循约定式提交规范

### 开发命令

```bash
# Python代码格式化
black app/ tests/

# Python代码检查
flake8 app/ tests/

# 运行测试
pytest

# 前端代码格式化
cd frontend && npm run format

# 前端代码检查
cd frontend && npm run lint
```

### 开发环境配置
项目包含VSCode工作区配置，推荐安装以下扩展：
- Python
- Pylance
- Black Formatter
- ESLint
- Prettier

## 📈 择时框架

### 三个维度指标

1. **宏观基本面**
   - PMI采购经理指数
   - CPI消费者价格指数
   - PPI生产者价格指数
   - M2货币供应量
   - 利率水平

2. **行业基本面**
   - 自由现金流指标
   - 行业景气度
   - 估值水平

3. **市场情绪**
   - 市场波动率
   - 投资者情绪指数
   - 技术指标

### 择时评分
- 每个维度独立评分（0-100）
- 加权计算综合择时评分
- AI分析生成最终建议

## 🤝 贡献指南

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 Apache 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目主页: [ValueInvestingLearn](https://github.com/your-username/ValueInvestingLearn)
- 问题反馈: [Issues](https://github.com/your-username/ValueInvestingLearn/issues)

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

---

**注意**: 本工具仅供投资分析参考，不构成投资建议。投资有风险，入市需谨慎。