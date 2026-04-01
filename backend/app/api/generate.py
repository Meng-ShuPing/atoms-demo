from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.project import GenerateRequest, ApiResponse, ProjectUpdate
from app.services.ai_service import ai_service
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api", tags=["generate"])


@router.post("/generate", response_model=ApiResponse)
async def generate_code(
    request: GenerateRequest, db: AsyncSession = Depends(get_db)
):
    """
    调用 AI 生成代码

    Args:
        request: 生成请求，包含 prompt、project_id、conversation_history、current_code

    Returns:
        生成的 HTML/CSS/JS 代码
    """
    # 调用 AI 服务生成代码
    code_result = await ai_service.generate_code(
        prompt=request.prompt,
        conversation_history=request.conversation_history,
        current_code=request.current_code
    )

    # 如果提供了 project_id，更新项目
    if request.project_id:
        project_service = ProjectService(db)
        project = await project_service.update_project(
            request.project_id,
            ProjectUpdate(
                html_code=code_result["html"],
                css_code=code_result["css"],
                js_code=code_result["js"],
                user_prompt=request.prompt,
            ),
        )
        if project:
            return ApiResponse(
                success=True,
                data={"code": code_result, "project_id": project.id},
                message="代码生成成功",
            )

    return ApiResponse(
        success=True,
        data={"code": code_result},
        message="代码生成成功",
    )
