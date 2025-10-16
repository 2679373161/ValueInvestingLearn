## 相关文件

- `app/__init__.py` - 应用主模块初始化
- `app/main.py` - Flask/FastAPI主应用文件
- `app/routes/__init__.py` - 路由模块
- `app/routes/data_input.py` - 数据输入API路由
- `app/routes/analysis.py` - 分析API路由
- `app/routes/visualization.py` - 可视化API路由
- `app/services/__init__.py` - 服务层模块
- `app/services/data_service.py` - 数据管理服务
- `app/services/indicator_service.py` - 指标计算服务
- `app/services/ai_service.py` - AI分析服务
- `app/models/__init__.py` - 数据模型
- `app/models/timing_models.py` - 择时数据模型
- `app/utils/__init__.py` - 工具模块
- `app/utils/config.py` - 配置管理
- `app/utils/calculations.py` - 计算工具
- `frontend/src/App.js` - 前端主应用组件
- `frontend/src/components/DataInput.js` - 数据输入组件
- `frontend/src/components/Dashboard.js` - 仪表盘组件
- `frontend/src/components/Visualization.js` - 可视化组件
- `frontend/src/services/api.js` - API调用服务
- `tests/test_data_service.py` - 数据服务单元测试
- `tests/test_indicator_service.py` - 指标计算单元测试
- `tests/test_ai_service.py` - AI服务单元测试
- `tests/test_routes.py` - API路由测试
- `config/config.json` - 应用配置文件
- `data/` - 数据存储目录
- `requirements.txt` - Python依赖
- `package.json` - 前端依赖

### 说明

- 单元测试通常放在与被测试代码相同的目录中（例如 `MyComponent.tsx` 和 `MyComponent.test.tsx` 在同一目录）
- 使用 `pytest [可选/测试文件路径]` 运行测试。不带路径运行将执行Jest配置找到的所有测试

## 任务

- [x] 1.0 项目基础架构搭建
  - [x] 1.1 创建Python虚拟环境并安装基础依赖
  - [x] 1.2 设置项目目录结构（后端、前端、测试、配置）
  - [x] 1.3 配置开发环境（IDE设置、代码格式化工具）
  - [x] 1.4 创建requirements.txt和package.json依赖管理文件
  - [x] 1.5 设置Git版本控制和.gitignore配置
  - [x] 1.6 创建基础配置文件（config.json）

- [x] 2.0 后端核心服务开发
  - [x] 2.1 搭建Flask/FastAPI应用框架
  - [x] 2.2 实现基础API路由结构
  - [x] 2.3 创建错误处理和日志系统
  - [x] 2.4 实现配置管理模块
  - [x] 2.5 添加CORS支持用于前后端通信
  - [ ] 2.6 创建API文档（Swagger/OpenAPI）

- [x] 3.0 数据管理模块实现
  - [x] 3.1 设计数据模型（宏观数据、市场数据、择时结果）
  - [x] 3.2 实现本地JSON文件数据存储
  - [x] 3.3 创建数据输入API接口（宏观基本面手动输入）
  - [x] 3.4 实现市场情绪数据双模式输入（手动/实时配置）
  - [x] 3.5 添加数据验证和清洗功能
  - [x] 3.6 实现数据查询和更新接口
  - [x] 3.7 创建数据备份和恢复机制

- [x] 4.0 指标计算引擎开发
  - [x] 4.1 实现宏观基本面评分计算逻辑
  - [x] 4.2 实现行业基本面评分计算（基于自由现金流）
  - [x] 4.3 实现市场情绪评分计算
  - [x] 4.4 设计指标权重配置系统
  - [x] 4.5 实现综合择时评分计算（加权平均）
  - [x] 4.6 创建指标标准化和归一化处理
  - [x] 4.7 实现多市场指数并行计算
  - [x] 4.8 添加指标计算缓存机制

- [x] 5.0 AI分析集成
  - [x] 5.1 集成DeepSeek API客户端
  - [x] 5.2 设计AI分析提示词模板
  - [x] 5.3 实现组合指标AI分析功能
  - [x] 5.4 开发择时建议生成逻辑
  - [x] 5.5 实现自然语言解释功能
  - [x] 5.6 创建基于择时强度的仓位建议算法
  - [x] 5.7 添加AI分析结果缓存
  - [x] 5.8 实现API密钥安全管理

- [ ] 6.0 Web前端开发
  - [ ] 6.1 搭建React/Vue.js前端项目结构
  - [ ] 6.2 创建数据输入表单组件
  - [ ] 6.3 实现仪表盘主界面
  - [ ] 6.4 集成ECharts/Chart.js可视化图表
  - [ ] 6.5 开发择时评分显示组件
  - [ ] 6.6 实现AI建议展示组件
  - [ ] 6.7 创建多市场切换功能
  - [ ] 6.8 添加响应式布局和主题切换
  - [ ] 6.9 实现前端API调用服务

- [ ] 7.0 系统集成与测试
  - [ ] 7.1 集成前后端通信
  - [ ] 7.2 实现端到端功能测试
  - [ ] 7.3 编写单元测试（数据服务、指标计算、AI服务）
  - [ ] 7.4 创建集成测试用例
  - [ ] 7.5 进行性能测试和优化
  - [ ] 7.6 完善错误处理和用户提示
  - [ ] 7.7 创建用户使用文档
  - [ ] 7.8 部署和运行验证