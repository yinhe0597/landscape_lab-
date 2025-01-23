from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base

class Plant(Base):
    """植物模型"""
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    height = Column(Float, nullable=True)
    spread = Column(Float, nullable=True)
    growth_rate = Column(String, nullable=True)
    sunlight = Column(String, nullable=True)
    water_requirements = Column(String, nullable=True)
    soil_type = Column(String, nullable=True)
    hardiness_zone = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 与项目的多对多关系
    projects = relationship("Project", secondary="project_plants", back_populates="plants")

    def __repr__(self):
        return f"<Plant(id={self.id}, name={self.name})>"
