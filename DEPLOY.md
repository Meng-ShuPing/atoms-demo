# Atoms Demo 部署指南

## 服务器配置要求

### 最低配置（个人开发/测试）

| 资源 | 配置 | 说明 |
|------|------|------|
| **CPU** | 1 核 | 可运行但并发能力有限 |
| **内存** | 512MB + 1GB Swap | 后端约 150MB，前端约 100MB，数据库约 50MB |
| **存储** | 5GB | 镜像 + 依赖 + 数据库 + 日志 |
| **带宽** | 1Mbps | 仅 API 传输，无大文件 |

### 推荐配置（小型团队/演示）

| 资源 | 配置 | 说明 |
|------|------|------|
| **CPU** | 2 核 | 可同时处理多个请求 |
| **内存** | 2GB | 流畅运行，有一定缓冲 |
| **存储** | 10GB | 充足空间存储项目和日志 |
| **带宽** | 5Mbps | 更快的响应速度 |

### 生产环境配置

| 资源 | 配置 | 说明 |
|------|------|------|
| **CPU** | 4 核+ | 高并发支持 |
| **内存** | 4GB+ | 稳定运行，支持缓存 |
| **存储** | 20GB+ SSD | 快速读写，充足空间 |
| **带宽** | 10Mbps+ | 低延迟响应 |

---

## 资源占用分析

### 后端服务
- **基础内存**: ~150MB (FastAPI + Python 运行时)
- **AI 调用**: ~50MB (httpx 异步客户端)
- **数据库**: ~50MB (SQLite + aiosqlite)
- **峰值内存**: ~300MB

### 前端服务
- **开发模式**: ~150MB (Vite + Node.js)
- **生产模式**: ~30MB (静态文件，Nginx)

### 数据库
- **SQLite**: ~50MB (适合小型项目)
- **建议升级**: PostgreSQL (生产环境)

---

## 部署方式

### 方式 1: Docker Compose (推荐)

```bash
# 1. 克隆项目
git clone <repo-url>
cd atoms-demo

# 2. 配置环境变量
cp .env.example .env
vim .env  # 填入 AI_API_KEY

# 3. 启动服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f

# 5. 访问服务
# 前端：http://your-server:5173
# 后端：http://your-server:8000
```

### 方式 2: 直接部署

#### 后端部署

```bash
cd backend

# 1. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install uv
uv pip install -r pyproject.toml

# 3. 配置环境变量
cp .env.example .env
vim .env

# 4. 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 前端部署

```bash
cd frontend

# 1. 安装依赖
npm install

# 2. 构建生产版本
npm run build

# 3. 使用 Nginx 托管
# 将 dist/ 目录内容放到 Nginx 根目录
```

### 方式 3: 云平台部署

#### 阿里云函数计算 (Serverless)
- 按需付费，适合低频率使用
- 无需管理服务器

#### 阿里云 ECS
- 按上述 Docker Compose 方式部署
- 推荐使用 2 核 2G 配置

#### Vercel/Netlify (前端) + Railway/Render (后端)
- 前端部署到 Vercel/Netlify
- 后端部署到 Railway/Render
- 免费额度够用

---

## Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## systemd 服务配置 (Linux)

### 后端服务

```ini
# /etc/systemd/system/atoms-backend.service
[Unit]
Description=Atoms Demo Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/atoms-demo/backend
Environment="AI_API_KEY=sk-your-key-here"
Environment="AI_MODEL=qwen3.5-plus"
ExecStart=/path/to/atoms-demo/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable atoms-backend
sudo systemctl start atoms-backend
sudo systemctl status atoms-backend
```

---

## 数据库迁移 (生产环境)

当前使用 SQLite，生产环境建议迁移到 PostgreSQL：

1. 修改 `.env`:
```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/atoms_demo
```

2. 安装依赖:
```bash
pip install asyncpg
```

3. 创建数据库:
```bash
createdb atoms_demo
```

---

## 监控和日志

### 日志配置

修改 `backend/app/main.py` 添加日志：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 健康检查端点

- `GET /health` - 健康检查
- `GET /` - 应用信息

---

## 安全建议

1. **API Key 管理**
   - 不要将 `.env` 提交到 Git
   - 使用云平台密钥管理服务

2. **HTTPS**
   - 使用 Let's Encrypt 免费证书
   - 强制 HTTPS 重定向

3. **CORS 配置**
   - 生产环境限制允许的源

4. **速率限制**
   - 添加 API 请求频率限制

5. **定期备份**
   - 备份 SQLite 数据库文件
   - 备份环境变量

---

## 常见问题

### Q: 内存不足怎么办？
A: 增加 Swap 空间或升级服务器配置

### Q: 如何查看日志？
A: `docker-compose logs -f` 或 `journalctl -u atoms-backend`

### Q: 如何备份数据？
A: 复制 `atoms_demo.db` 文件到安全位置
