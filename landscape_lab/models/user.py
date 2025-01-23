from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from database.db import Base
from utils.security import get_password_hash

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    projects = relationship("Project", back_populates="owner")

    def set_password(self, password: str):
        """设置密码"""
        self.hashed_password = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """验证密码"""
        return verify_password(password, self.hashed_password)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
