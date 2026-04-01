# Atoms Demo

AI 驱动的代码生成平台 Demo - 通过自然语言描述需求，自动生成可运行的网页应用。

## 🚀 快速开始

### 方式一：Docker Compose（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 访问应用
# 前端：http://localhost:5173
# 后端：http://localhost:8000
# API 文档：http://localhost:8000/docs

# 停止服务
docker-compose down
```

### 方式二：本地开发

#### 后端

```bash
cd backend

# 使用 uv 创建虚拟环境并安装依赖
uv sync --dev

# 激活虚拟环境
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 启动服务
uvicorn app.main:app --reload --port 8000
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📁 项目结构

```
atoms-demo/
├── backend/                 # Python FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模型
│   │   ├── services/       # 业务服务
│   │   └── main.py         # 应用入口
│   ├── pyproject.toml      # 项目配置和依赖 (uv)
│   ├── .env.example        # 环境变量示例
│   └── Dockerfile
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── components/     # Vue 组件
│   │   ├── config/         # 应用配置
│   │   ├── services/       # API 服务
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── types/          # TypeScript 类型
│   │   └── App.vue         # 主应用
│   ├── .env.development    # 开发环境配置
│   ├── .env.production     # 生产环境配置
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── README.md
└── 产品需求设计文档.md
```

## 🔧 技术栈

### 后端
- **框架**: FastAPI (Python)
- **数据库**: SQLite + SQLAlchemy (异步)
- **AI 服务**: Claude API / Atoms API

### 前端
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI 组件**: Naive UI
- **状态管理**: Pinia
- **HTTP 客户端**: Axios

## 📝 API 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/projects | 获取项目列表 |
| GET | /api/projects/{id} | 获取项目详情 |
| POST | /api/projects | 创建项目 |
| PUT | /api/projects/{id} | 更新项目 |
| DELETE | /api/projects/{id} | 删除项目 |
| POST | /api/generate | 生成代码 |
| POST | /api/sessions | 创建会话 |
| GET | /api/sessions/{id}/messages | 获取会话消息 |

## 🎯 功能特性

- ✅ 自然语言代码生成
- ✅ 实时预览生成的应用
- ✅ 代码编辑与保存
- ✅ 项目历史记录
- ✅ 多设备预览（桌面/平板/手机）
- ✅ 代码导出功能

## ⚙️ 配置

### 后端配置

复制 `.env.example` 为 `.env` 并配置：

```bash
# 后端配置
cd backend
cp .env.example .env

# 编辑 .env 文件，配置 AI API Key（可选）
AI_API_KEY=your-api-key-here
```

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `APP_NAME` | Atoms Demo | 应用名称 |
| `DATABASE_URL` | sqlite+aiosqlite:///./atoms_demo.db | 数据库连接 |
| `AI_API_KEY` | - | AI API 密钥（可选） |
| `AI_MODEL` | claude-sonnet-4-6 | AI 模型 |
| `CORS_ORIGINS` | ["http://localhost:5173"] | 允许的跨域来源 |

### 前端配置

前端支持多环境配置：

| 文件 | 说明 |
|------|------|
| `.env.development` | 开发环境配置 |
| `.env.production` | 生产环境配置 |

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `VITE_API_BASE_URL` | http://localhost:8000 | 后端 API 地址 |
| `VITE_APP_TITLE` | Atoms Demo | 应用标题 |

开发环境下，前端会自动代理 `/api` 请求到后端服务。

## 📸 使用说明

1. 打开浏览器访问 http://localhost:5173
2. 在聊天输入框中描述你想要创建的应用
3. 点击"生成"按钮，等待 AI 生成代码
4. 在代码预览区查看和编辑生成的代码
5. 在应用预览区查看运行效果
6. 可以保存项目到历史记录，随时查看和修改

## 📄 文档

- [产品需求设计文档](产品需求设计文档.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📜 许可证

MIT License
