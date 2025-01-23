# landscape_lab/controllers/project_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.project import (
    ProjectInDB,
    ProjectCreate,
    ProjectUpdate,
    ProjectPublic,
    ProjectSearchResult,
    ProjectStatistics,
    ProjectFile,
    ProjectVersion
)
from ..models.user import UserInDB
from ..utils.security import get_current_user
from ..utils.file_utils import save_uploaded_file
from datetime import datetime
import os

router = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ProjectPublic)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_project = ProjectInDB(**project.dict(), owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[ProjectSearchResult])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, min_length=2, max_length=100),
    db: Session = Depends(get_db)
):
    query = db.query(ProjectInDB)
    if search:
        query = query.filter(ProjectInDB.name.ilike(f"%{search}%"))
    projects = query.offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectPublic)
def read_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(ProjectInDB).filter(ProjectInDB.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectPublic)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_project = db.query(ProjectInDB).filter(ProjectInDB.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if db_project.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    project = db.query(ProjectInDB).filter(ProjectInDB.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

@router.get("/statistics/", response_model=ProjectStatistics)
def get_project_statistics(
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    total_projects = db.query(ProjectInDB).count()
    
    # 获取项目状态统计
    project_statuses = db.query(
        ProjectInDB.status,
        db.func.count(ProjectInDB.id).label("count")
    ).group_by(ProjectInDB.status).all()
    
    # 获取最近创建的项目
    recent_projects = db.query(ProjectInDB).order_by(
        ProjectInDB.created_at.desc()
    ).limit(5).all()
    
    return ProjectStatistics(
        total_projects=total_projects,
        project_statuses=[{"status": ps[0], "count": ps[1]} for ps in project_statuses],
        recent_additions=recent_projects
    )

@router.post("/{project_id}/files/", response_model=ProjectFile)
def upload_project_file(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    project = db.query(ProjectInDB).filter(ProjectInDB.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    file_path = save_uploaded_file(file, project_id)
    db_file = ProjectFile(
        project_id=project_id,
        file_name=file.filename,
        file_path=file_path,
        uploaded_by=current_user.id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@router.post("/{project_id}/versions/", response_model=ProjectVersion)
def create_project_version(
    project_id: int,
    version: str,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    project = db.query(ProjectInDB).filter(ProjectInDB.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    db_version = ProjectVersion(
        project_id=project_id,
        version=version,
        created_by=current_user.id
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version
