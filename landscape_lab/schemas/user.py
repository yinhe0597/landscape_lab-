from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """用户更新模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

class UserInDB(UserBase):
    """数据库用户模型"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    """用户登录模型"""
    username: str
    password: str

class Token(BaseModel):
    """Token模型"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token数据模型"""
    username: Optional[str] = None
