from datetime import datetime
from typing import Optional, List, TypeVar, Generic
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class ProjectBase(BaseModel):
    """项目基础模型"""
    name: Optional[str] = "未命名项目"
    html_code: Optional[str] = ""
    css_code: Optional[str] = ""
    js_code: Optional[str] = ""
    user_prompt: Optional[str] = ""


class ProjectCreate(ProjectBase):
    """创建项目请求模型"""
    pass


class ProjectUpdate(BaseModel):
    """更新项目请求模型"""
    name: Optional[str] = None
    html_code: Optional[str] = None
    css_code: Optional[str] = None
    js_code: Optional[str] = None
    user_prompt: Optional[str] = None


class ProjectResponse(ProjectBase):
    """项目响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationMessage(BaseModel):
    """对话消息模型"""
    role: str = Field(..., description="角色：user 或 assistant")
    content: str = Field(..., description="消息内容")


class GenerateRequest(BaseModel):
    """代码生成请求模型"""
    prompt: str = Field(..., description="用户需求描述")
    project_id: Optional[int] = None
    conversation_history: Optional[List[ConversationMessage]] = None  # 对话历史
    current_code: Optional[dict] = None  # 当前代码


class GenerateResponse(BaseModel):
    """代码生成响应模型"""
    html: str
    css: str
    js: str


class MessageCreate(BaseModel):
    """创建消息请求模型"""
    role: str
    content: str


class MessageResponse(BaseModel):
    """消息响应模型"""
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# 泛型响应类型
T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """通用 API 响应模型"""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
