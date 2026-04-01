from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    ApiResponse,
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=ApiResponse)
async def get_projects(db: AsyncSession = Depends(get_db)):
    """获取项目列表"""
    service = ProjectService(db)
    projects = await service.get_projects()
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
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """获取项目详情"""
    service = ProjectService(db)
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

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
    project_data: ProjectCreate, db: AsyncSession = Depends(get_db)
):
    """创建项目"""
    try:
        service = ProjectService(db)
        project = await service.create_project(project_data)

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
):
    """更新项目"""
    service = ProjectService(db)
    project = await service.update_project(project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

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


@router.delete("/{project_id}", response_model=ApiResponse)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """删除项目"""
    service = ProjectService(db)
    success = await service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="项目不存在")
    return ApiResponse(success=True, message="删除成功")
