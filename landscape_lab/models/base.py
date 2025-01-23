from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from database.db import Base

class BaseModel(Base):
    """所有模型的基类"""
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        """软删除"""
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """恢复删除"""
        self.deleted_at = None
