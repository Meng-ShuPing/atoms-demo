from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# User 基础 Schema
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")


# 用户注册请求
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, description="密码")


# 用户登录请求
class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


# 用户响应（不包含密码）
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Token 响应
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Token 数据
class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
