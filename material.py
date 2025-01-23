# landscape_lab/models/material.py
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Material(Base):
    """材料模型"""
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    material_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    unit = Column(String(20), nullable=False)
    unit_price = Column(Float, nullable=False)
    supplier = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="materials")

    def __repr__(self):
        return f"<Material(id={self.id}, name={self.name})>"
