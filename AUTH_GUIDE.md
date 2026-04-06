# 用户认证功能说明

## 功能概述

已成功为用户登录和注册功能，包含以下特性：

- JWT Token 认证
- 密码 bcrypt 加密
- 用户状态管理
- 自动 Token 刷新

## 后端 API

### 1. 用户注册

**接口**: `POST /api/auth/register`

**请求体**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "123456"
}
```

**响应**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "id": 1,
  "is_active": true,
  "created_at": "2026-04-02T16:57:55.028120"
}
```

### 2. 用户登录

**接口**: `POST /api/auth/login`

**请求体**:
```json
{
  "username": "testuser",
  "password": "123456"
}
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. 获取当前用户信息

**接口**: `GET /api/auth/me`

**请求头**:
```
Authorization: Bearer <access_token>
```

**响应**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "id": 1,
  "is_active": true,
  "created_at": "2026-04-02T16:57:55.028120"
}
```

## 前端使用

### 1. 用户状态管理

```typescript
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 检查是否已登录
if (userStore.isAuthenticated) {
  console.log('当前用户:', userStore.user)
}

// 退出登录
userStore.logout()
```

### 2. 登录/注册组件

```vue
<template>
  <AuthModal 
    v-model="showAuthModal" 
    @success="handleLoginSuccess" 
  />
</template>
```

## 安全说明

1. **密码加密**: 使用 bcrypt 算法对用户密码进行加密存储
2. **Token 过期**: JWT Token 有效期为 7 天
3. **SECRET_KEY**: 生产环境必须修改 `.env` 中的 `SECRET_KEY`

## 部署注意事项

1. 生产环境必须修改 `SECRET_KEY`：
   ```bash
   # 生成随机密钥
   openssl rand -hex 32
   ```

2. 在 `.env` 文件中设置：
   ```
   SECRET_KEY=your-random-secret-key-here
   ```

## 数据库

用户信息存储在 `users` 表中，包含以下字段：
- `id`: 用户 ID（主键）
- `username`: 用户名（唯一）
- `email`: 邮箱（唯一）
- `hashed_password`: 密码哈希
- `is_active`: 是否激活
- `created_at`: 创建时间
- `updated_at`: 更新时间

## 相关文件

### 后端
- `backend/app/models/user.py` - 用户模型
- `backend/app/schemas/user.py` - 用户 Schema
- `backend/app/api/auth.py` - 认证 API
- `backend/app/core/security.py` - 安全工具（密码哈希、JWT）

### 前端
- `frontend/src/stores/user.ts` - 用户状态管理
- `frontend/src/components/AuthModal.vue` - 登录/注册模态框
- `frontend/src/services/api.ts` - API 服务（包含认证拦截器）
