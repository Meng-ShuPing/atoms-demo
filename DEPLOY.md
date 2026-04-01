# 部署指南

## 环境变量配置

### 后端环境变量

后端服务需要以下环境变量：

| 变量名 | 说明 | 默认值 | 是否必须 |
|--------|------|--------|----------|
| `AI_API_KEY` | 阿里云 DashScope API Key | 无 | 是 |
| `AI_MODEL` | AI 模型名称 | qwen3.5-plus | 否 |
| `DATA<br/>BASE_URL` | 数据库连接 URL | sqlite+aiosqlite:///./atoms_demo.db | 否 |
| `DEBUG` | 调试模式 | True | 否 |
| `CORS_ORIGINS` | CORS 允许的源 | ["http://localhost:5173"] | 否 |

### 配置方式

#### 方式 1：使用 .env 文件

在 `backend/` 目录下创建 `.env` 文件：

```bash
# 复制示例配置
cp backend/.env.example backend/.env

# 编辑 .env 文件，填入你的 API Key
vim backend/.env
```

`.env` 文件内容：
```bash
AI_API_KEY=sk-your-actual-api-key-here
AI_MODEL=qwen3.5-plus
```

#### 方式 2：使用系统环境变量

```bash
# Linux/Mac
export AI_API_KEY=sk-your-api-key-here
export AI_MODEL=qwen3.5-plus

# Windows PowerShell
$env:AI_API_KEY="sk-your-api-key-here"
$env:AI_MODEL="qwen3.5-plus"
```

#### 方式 3：Docker Compose 部署

在项目根目录创建 `.env` 文件：

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
vim .env
```

然后启动服务：
```bash
docker-compose up -d
```

## 获取 API Key

1. 访问阿里云 DashScope 控制台：https://dashscope.console.aliyun.com/
2. 注册/登录账号
3. 创建 API Key
4. 将 API Key 复制到配置文件中

## 安全提示

- **永远不要**将 `.env` 文件提交到 Git 仓库
- 项目已配置 `.gitignore` 忽略 `.env` 文件
- 在生产环境中使用环境变量管理服务（如 AWS Secrets Manager、HashiCorp Vault 等）
- 定期轮换 API Key

## 验证配置

启动后端服务后，访问以下端点验证配置：

```bash
# 健康检查
curl http://localhost:8000/health

# 测试代码生成
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "创建一个按钮"}'
```
