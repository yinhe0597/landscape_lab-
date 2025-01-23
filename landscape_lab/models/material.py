# landscape_lab/models/material.py
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel
from typing import Optional

class Material(Base):
    """材料模型"""
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    category = Column(String(100))
    description = Column(Text)
    unit = Column(String(50))
    unit_price = Column(Float)
    density = Column(Float, nullable=True)
    strength = Column(Float, nullable=True)
    color = Column(String(50), nullable=True)
    texture = Column(String(100), nullable=True)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="materials")
    
    def __repr__(self):
        return f"<Material(id={self.id}, name={self.name})>"

class MaterialCreate(BaseModel):
    """材料创建模型"""
    name: str
    category: str
    description: str
    unit: str
    unit_price: float
    density: Optional[float] = None
    strength: Optional[float] = None
    color: Optional[str] = None
    texture: Optional[str] = None
    image_url: Optional[str] = None
    project_id: int

class MaterialUpdate(BaseModel):
    """材料更新模型"""
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    density: Optional[float] = None
    strength: Optional[float] = None
    color: Optional[str] = None
    texture: Optional[str] = None
    image_url: Optional[str] = None

class MaterialInDB(BaseModel):
    """数据库中的材料模型"""
    id: int
    name: str
    category: str
    description: str
    unit: str
    unit_price: float
    density: Optional[float] = None
    strength: Optional[float] = None
    color: Optional[str] = None
    texture: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Config:
        orm_mode = True
