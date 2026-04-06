from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.core.database import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    ApiResponse,
)
from app.services.project_service import ProjectService
from app.models.user import User
from app.core.security import decode_access_token

router = APIRouter(prefix="/api/projects", tags=["projects"])

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前登录用户（强制要求认证）"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未认证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账号已被禁用"
        )

    return user


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """获取当前用户（可选，允许匿名用户）"""
    if not token:
        return None

    payload = decode_access_token(token)
    if payload is None:
        return None

    user_id = payload.get("user_id")
    if not user_id:
        return None

    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


@router.get("", response_model=ApiResponse)
async def get_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目列表（需要登录）"""
    service = ProjectService(db)
    projects = await service.get_projects_by_user(current_user.id)
    # 转换为字典
    projects_data = [
        {
            "id": p.id,
            "name": p.name,
            "html_code": p.html_code,
            "css_code": p.css_code,
            "js_code": p.js_code,
            "user_prompt": p.user_prompt,
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat(),
        }
        for p in projects
    ]
    return ApiResponse(success=True, data={"projects": projects_data})


@router.get("/{project_id}", response_model=ApiResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目详情（需要登录）"""
    service = ProjectService(db)
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    # 验证项目所有权
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问该项目")

    project_data = {
        "id": project.id,
        "name": project.name,
        "html_code": project.html_code,
        "css_code": project.css_code,
        "js_code": project.js_code,
        "user_prompt": project.user_prompt,
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat(),
    }
    return ApiResponse(success=True, data={"project": project_data})


@router.post("", response_model=ApiResponse)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建项目（需要登录）"""
    try:
        service = ProjectService(db)
        # 关联 user_id
        project_data_dict = project_data.model_dump()
        project_data_dict['user_id'] = current_user.id
        from app.models.project import Project
        project = Project(**project_data_dict)
        db.add(project)
        await db.flush()
        await db.refresh(project)

        project_response = {
            "id": project.id,
            "name": project.name,
            "html_code": project.html_code,
            "css_code": project.css_code,
            "js_code": project.js_code,
            "user_prompt": project.user_prompt,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
        }
        return ApiResponse(success=True, data={"project": project_response})
    except Exception as e:
        import traceback
        print(f"Error creating project: {e}")
        print(traceback.format_exc())
        raise


@router.put("/{project_id}", response_model=ApiResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新项目（需要登录）"""
    service = ProjectService(db)
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    # 验证项目所有权
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改该项目")

    updated_project = await service.update_project(project_id, project_data)
    project_response = {
        "id": updated_project.id,
        "name": updated_project.name,
        "html_code": updated_project.html_code,
        "css_code": updated_project.css_code,
        "js_code": updated_project.js_code,
        "user_prompt": updated_project.user_prompt,
        "created_at": updated_project.created_at.isoformat(),
        "updated_at": updated_project.updated_at.isoformat(),
    }
    return ApiResponse(success=True, data={"project": project_response})


@router.delete("/{project_id}", response_model=ApiResponse)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除项目（需要登录）"""
    service = ProjectService(db)
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    # 验证项目所有权
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除该项目")

    success = await service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="项目不存在")
    return ApiResponse(success=True, message="删除成功")
