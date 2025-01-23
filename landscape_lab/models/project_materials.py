from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base

project_materials = Table(
    "project_materials",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("material_id", Integer, ForeignKey("materials.id"), primary_key=True)
)
