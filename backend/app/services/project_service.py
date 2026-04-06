from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.project import Project, Session, Message
from app.schemas.project import ProjectCreate, ProjectUpdate
from datetime import datetime


class ProjectService:
    """项目服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_project(self, project_id: int) -> Optional[Project]:
        """获取项目详情"""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_projects(self, limit: int = 20, offset: int = 0) -> List[Project]:
        """获取项目列表"""
        result = await self.db.execute(
            select(Project)
            .order_by(Project.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_projects_by_user(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Project]:
        """获取指定用户的项目列表"""
        result = await self.db.execute(
            select(Project)
            .where(Project.user_id == user_id)
            .order_by(Project.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_project(self, project_data: ProjectCreate) -> Project:
        """创建项目"""
        project = Project(**project_data.model_dump())
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def update_project(
        self, project_id: int, project_data: ProjectUpdate
    ) -> Optional[Project]:
        """更新项目"""
        project = await self.get_project(project_id)
        if not project:
            return None

        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        project.updated_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete_project(self, project_id: int) -> bool:
        """删除项目"""
        project = await self.get_project(project_id)
        if not project:
            return False

        await self.db.delete(project)
        await self.db.flush()
        return True

    async def get_project_code(self, project_id: int) -> Optional[dict]:
        """获取项目代码"""
        project = await self.get_project(project_id)
        if not project:
            return None

        return {
            "html": project.html_code,
            "css": project.css_code,
            "js": project.js_code,
        }


class SessionService:
    """会话服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, project_id: int) -> Session:
        """创建会话"""
        session = Session(project_id=project_id)
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)
        return session

    async def get_session(self, session_id: int) -> Optional[Session]:
        """获取会话"""
        result = await self.db.execute(
            select(Session).where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def get_messages(self, session_id: int) -> List[Message]:
        """获取会话消息"""
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.asc())
        )
        return result.scalars().all()

    async def add_message(
        self, session_id: int, role: str, content: str
    ) -> Message:
        """添加消息"""
        message = Message(session_id=session_id, role=role, content=content)
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message
