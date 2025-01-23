# landscape_lab/models/project.py
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel
from typing import Optional, List

class Project(Base):
    """项目模型"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    location = Column(String(200))
    area_size = Column(Float)
    design_style = Column(String(100))
    status = Column(String(50), default="draft")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")
    
    plants = relationship("Plant", back_populates="project")
    materials = relationship("Material", back_populates="project")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"

class ProjectCreate(BaseModel):
    """项目创建模型"""
    name: str
    description: str
    location: str
    area_size: float
    design_style: str
    owner_id: int

class ProjectUpdate(BaseModel):
    """项目更新模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    area_size: Optional[float] = None
    design_style: Optional[str] = None
    status: Optional[str] = None

class ProjectInDB(BaseModel):
    """数据库中的项目模型"""
    id: int
    name: str
    description: str
    location: str
    area_size: float
    design_style: str
    status: str
    created_at: datetime
    updated_at: datetime
    owner_id: int
    plants: List["PlantInDB"] = []
    materials: List["MaterialInDB"] = []

    class Config:
        orm_mode = True
