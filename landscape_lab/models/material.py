from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base

class Material(Base):
    """材料模型"""
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    unit = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    density = Column(Float, nullable=True)
    strength = Column(Float, nullable=True)
    color = Column(String, nullable=True)
    texture_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 与项目的多对多关系
    projects = relationship("Project", secondary="project_materials", back_populates="materials")

    def __repr__(self):
        return f"<Material(id={self.id}, name={self.name})>"
