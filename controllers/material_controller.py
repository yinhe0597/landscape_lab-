# landscape_lab/controllers/material_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from models.material import MaterialInDB, create_material, get_material_by_id, get_materials, update_material, delete_material
from models.user import UserInDB
from controllers.user_controller import get_current_user

router = APIRouter()

class MaterialCreate(BaseModel):
    name: str
    material_type: str
    description: str
    specifications: str
    unit_price: float
    image_url: Optional[str] = None

class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    material_type: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[str] = None
    unit_price: Optional[float] = None
    image_url: Optional[str] = None

@router.post("/materials", response_model=MaterialInDB)
async def create_new_material(
    material: MaterialCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """创建新材料"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以创建材料")
    
    created_material = create_material(material)
    if not created_material:
        raise HTTPException(status_code=500, detail="创建材料失败")
    return created_material

@router.get("/materials", response_model=List[MaterialInDB])
async def get_all_materials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    name: Optional[str] = None,
    material_type: Optional[str] = None
):
    """获取材料列表"""
    materials = get_materials(skip=skip, limit=limit, name=name, material_type=material_type)
    return materials

@router.get("/materials/{material_id}", response_model=MaterialInDB)
async def get_material_details(material_id: int):
    """获取材料详细信息"""
    material = get_material_by_id(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="材料未找到")
    return material

@router.put("/materials/{material_id}", response_model=MaterialInDB)
async def update_material_info(
    material_id: int,
    material: MaterialUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """更新材料信息"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以更新材料信息")
    
    updated_material = update_material(material_id, material)
    if not updated_material:
        raise HTTPException(status_code=500, detail="更新材料信息失败")
    return updated_material

@router.delete("/materials/{material_id}")
async def delete_material_record(
    material_id: int,
    current_user: UserInDB = Depends(get_current_user)
):
    """删除材料记录"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以删除材料")
    
    success = delete_material(material_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除材料失败")
    return {"message": "材料删除成功"}

@router.get("/materials/search", response_model=List[MaterialInDB])
async def search_materials(
    query: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000)
):
    """搜索材料"""
    materials = get_materials(skip=skip, limit=limit, search_query=query)
    return materials
