# 开发环境配置指南

## 环境要求

- Python 3.9+
- Node.js 16+ (前端开发)
- Git

## 快速开始

### 1. 激活开发环境

```bash
# 激活conda环境
conda activate quant-timing

# 或者使用完整路径
conda.bat activate quant-timing
```

### 2. 安装Python依赖

```bash
# 使用conda安装核心依赖
conda install -n quant-timing flask pandas numpy requests -y

# 或者使用pip安装完整依赖
pip install -r requirements.txt
```

### 3. 验证开发环境

```bash
python scripts/dev_setup.py
```

## 开发工具配置

### 代码格式化

项目使用以下工具进行代码格式化：

- **Black**: Python代码格式化
- **Flake8**: Python代码检查
- **isort**: Python导入排序
- **Prettier**: 前端代码格式化

### VSCode配置

项目包含VSCode工作区配置：

- 自动格式化保存
- Python环境路径设置
- 代码检查配置
- 推荐的扩展列表

安装推荐的扩展：
```bash
# 在VSCode中按 Ctrl+Shift+P
# 输入 "Extensions: Show Recommended Extensions"
# 安装所有推荐的扩展
```

## 开发命令

### Python后端

```bash
# 运行开发服务器
python app/main.py

# 运行测试
pytest

# 代码格式化
black app/ tests/

# 代码检查
flake8 app/ tests/

# 导入排序
isort app/ tests/
```

### 前端开发

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 项目结构

```
ValueInvestingLearn/
├── app/              # Python后端
├── frontend/         # React前端
├── tests/            # 测试代码
├── config/           # 配置文件
├── data/             # 数据存储
├── scripts/          # 开发脚本
└── docs/             # 项目文档
```

## 开发规范

1. **代码风格**: 遵循Black和Flake8规范
2. **提交信息**: 使用约定式提交格式
3. **测试**: 新功能必须包含测试
4. **文档**: 重要功能需要更新文档

## 故障排除

### 常见问题

1. **Python环境问题**
   ```bash
   # 重新创建环境
   conda env remove -n quant-timing
   conda create -n quant-timing python=3.9 -y
   ```

2. **依赖安装失败**
   ```bash
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. **VSCode无法识别Python环境**
   - 重启VSCode
   - 手动选择解释器: Ctrl+Shift+P → "Python: Select Interpreter"

## 联系方式

如有问题，请参考项目文档或联系开发团队。