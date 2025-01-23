# landscape_lab/models/plant.py
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Plant(Base):
    """植物模型"""
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    scientific_name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    height_min = Column(Float, nullable=True)
    height_max = Column(Float, nullable=True)
    spread_min = Column(Float, nullable=True)
    spread_max = Column(Float, nullable=True)
    growth_rate = Column(String(50), nullable=True)
    sunlight_requirements = Column(String(100), nullable=True)
    water_requirements = Column(String(100), nullable=True)
    soil_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="plants")

    def __repr__(self):
        return f"<Plant(id={self.id}, name={self.name})>"
