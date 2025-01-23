# landscape_lab/models/plant.py
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
from typing import Optional, List

class Plant(Base):
    """植物模型"""
    __tablename__ = "plants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    scientific_name = Column(String(100))
    description = Column(Text)
    height_min = Column(Float)
    height_max = Column(Float)
    spread_min = Column(Float)
    spread_max = Column(Float)
    growth_rate = Column(String(50))
    sunlight_requirements = Column(String(100))
    water_requirements = Column(String(100))
    soil_type = Column(String(100))
    bloom_time = Column(String(100))
    flower_color = Column(String(50))
    hardiness_zone = Column(String(50))
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="plants")
    
    def __repr__(self):
        return f"<Plant(id={self.id}, name={self.name})>"

class PlantCreate(BaseModel):
    """植物创建模型"""
    name: str
    scientific_name: str
    description: str
    height_min: float
    height_max: float
    spread_min: float
    spread_max: float
    growth_rate: str
    sunlight_requirements: str
    water_requirements: str
    soil_type: str
    bloom_time: str
    flower_color: str
    hardiness_zone: str
    image_url: Optional[str] = None
    project_id: int

class PlantUpdate(BaseModel):
    """植物更新模型"""
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    description: Optional[str] = None
    height_min: Optional[float] = None
    height_max: Optional[float] = None
    spread_min: Optional[float] = None
    spread_max: Optional[float] = None
    growth_rate: Optional[str] = None
    sunlight_requirements: Optional[str] = None
    water_requirements: Optional[str] = None
    soil_type: Optional[str] = None
    bloom_time: Optional[str] = None
    flower_color: Optional[str] = None
    hardiness_zone: Optional[str] = None
    image_url: Optional[str] = None

class PlantInDB(BaseModel):
    """数据库中的植物模型"""
    id: int
    name: str
    scientific_name: str
    description: str
    height_min: float
    height_max: float
    spread_min: float
    spread_max: float
    growth_rate: str
    sunlight_requirements: str
    water_requirements: str
    soil_type: str
    bloom_time: str
    flower_color: str
    hardiness_zone: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Config:
        orm_mode = True
