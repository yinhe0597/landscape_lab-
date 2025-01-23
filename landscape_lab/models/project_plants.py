from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base

project_plants = Table(
    "project_plants",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("plant_id", Integer, ForeignKey("plants.id"), primary_key=True)
)
