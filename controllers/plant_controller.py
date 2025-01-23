# landscape_lab/controllers/plant_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from models.plant import PlantInDB, create_plant, get_plant_by_id, get_plants, update_plant, delete_plant
from models.user import UserInDB
from controllers.user_controller import get_current_user

router = APIRouter()

class PlantCreate(BaseModel):
    name: str
    scientific_name: str
    description: str
    growth_conditions: str
    maintenance_requirements: str
    image_url: Optional[str] = None

class PlantUpdate(BaseModel):
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    description: Optional[str] = None
    growth_conditions: Optional[str] = None
    maintenance_requirements: Optional[str] = None
    image_url: Optional[str] = None

@router.post("/plants", response_model=PlantInDB)
async def create_new_plant(
    plant: PlantCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """创建新植物"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以创建植物")
    
    created_plant = create_plant(plant)
    if not created_plant:
        raise HTTPException(status_code=500, detail="创建植物失败")
    return created_plant

@router.get("/plants", response_model=List[PlantInDB])
async def get_all_plants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    name: Optional[str] = None,
    scientific_name: Optional[str] = None
):
    """获取植物列表"""
    plants = get_plants(skip=skip, limit=limit, name=name, scientific_name=scientific_name)
    return plants

@router.get("/plants/{plant_id}", response_model=PlantInDB)
async def get_plant_details(plant_id: int):
    """获取植物详细信息"""
    plant = get_plant_by_id(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="植物未找到")
    return plant

@router.put("/plants/{plant_id}", response_model=PlantInDB)
async def update_plant_info(
    plant_id: int,
    plant: PlantUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """更新植物信息"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以更新植物信息")
    
    updated_plant = update_plant(plant_id, plant)
    if not updated_plant:
        raise HTTPException(status_code=500, detail="更新植物信息失败")
    return updated_plant

@router.delete("/plants/{plant_id}")
async def delete_plant_record(
    plant_id: int,
    current_user: UserInDB = Depends(get_current_user)
):
    """删除植物记录"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以删除植物")
    
    success = delete_plant(plant_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除植物失败")
    return {"message": "植物删除成功"}

@router.get("/plants/search", response_model=List[PlantInDB])
async def search_plants(
    query: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000)
):
    """搜索植物"""
    plants = get_plants(skip=skip, limit=limit, search_query=query)
    return plants
