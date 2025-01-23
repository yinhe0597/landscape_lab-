from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from .base import Base

class Project(Base):
    """项目模型"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    area = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="planning")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 与用户的关系
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")

    # 与植物的多对多关系
    plants = relationship("Plant", secondary="project_plants", back_populates="projects")

    # 与材料的多对多关系
    materials = relationship("Material", secondary="project_materials", back_populates="projects")

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"
