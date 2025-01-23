# landscape_lab/views/project_view.py
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
from models.project import ProjectInDB, create_project, get_project_by_id, get_projects, update_project, delete_project
from models.user import UserInDB
from controllers.user_controller import get_current_user
from utils.file_utils import save_project_file
from datetime import datetime

router = APIRouter()

class ProjectCreate(BaseModel):
    name: str
    description: str
    location: str
    area_size: float
    budget: float
    start_date: datetime
    end_date: datetime
    status: str

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    area_size: Optional[float] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None

@router.post("/projects", response_model=ProjectInDB)
async def create_new_project(
    project: ProjectCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """创建新项目"""
    created_project = create_project(project, current_user.id)
    if not created_project:
        raise HTTPException(status_code=500, detail="创建项目失败")
    return created_project

@router.get("/projects", response_model=List[ProjectInDB])
async def get_all_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    name: Optional[str] = None,
    status: Optional[str] = None
):
    """获取项目列表"""
    projects = get_projects(skip=skip, limit=limit, name=name, status=status)
    return projects

@router.get("/projects/{project_id}", response_model=ProjectInDB)
async def get_project_details(project_id: int):
    """获取项目详细信息"""
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目未找到")
    return project

@router.put("/projects/{project_id}", response_model=ProjectInDB)
async def update_project_info(
    project_id: int,
    project: ProjectUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """更新项目信息"""
    updated_project = update_project(project_id, project, current_user.id)
    if not updated_project:
        raise HTTPException(status_code=500, detail="更新项目信息失败")
    return updated_project

@router.delete("/projects/{project_id}")
async def delete_project_record(
    project_id: int,
    current_user: UserInDB = Depends(get_current_user)
):
    """删除项目记录"""
    success = delete_project(project_id, current_user.id)
    if not success:
        raise HTTPException(status_code=500, detail="删除项目失败")
    return {"message": "项目删除成功"}

@router.post("/projects/{project_id}/upload-file")
async def upload_project_file(
    project_id: int,
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user)
):
    """上传项目文件"""
    try:
        file_path = save_project_file(project_id, file)
        return {"message": "文件上传成功", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.get("/projects/search", response_model=List[ProjectInDB])
async def search_projects(
    query: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000)
):
    """搜索项目"""
    projects = get_projects(skip=skip, limit=limit, search_query=query)
    return projects

@router.get("/projects/{project_id}/statistics")
async def get_project_statistics(project_id: int):
    """获取项目统计信息"""
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目未找到")
    
    # TODO: 实现项目统计逻辑
    return {
        "plant_count": 0,
        "material_count": 0,
        "total_cost": 0,
        "progress": 0
    }
