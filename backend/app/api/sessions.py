from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.project import MessageResponse, ApiResponse
from app.services.project_service import SessionService

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.post("", response_model=ApiResponse)
async def create_session(
    project_id: int, db: AsyncSession = Depends(get_db)
):
    """创建新会话"""
    service = SessionService(db)
    session = await service.create_session(project_id)
    return ApiResponse(success=True, data={"session": session})


@router.get("/{session_id}/messages", response_model=ApiResponse)
async def get_messages(session_id: int, db: AsyncSession = Depends(get_db)):
    """获取会话消息列表"""
    service = SessionService(db)
    session = await service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    messages = await service.get_messages(session_id)
    return ApiResponse(success=True, data={"messages": messages})
