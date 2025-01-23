# landscape_lab/views/plant_view.py
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
from models.plant import PlantInDB, create_plant, get_plant_by_id, get_plants, update_plant, delete_plant
from models.user import UserInDB
from controllers.user_controller import get_current_user
from utils.file_utils import save_plant_image
from datetime import datetime

router = APIRouter()

class PlantCreate(BaseModel):
    name: str
    scientific_name: str
    description: str
    category: str
    growth_cycle: str
    water_requirements: str
    sunlight_requirements: str
    soil_type: str
    maintenance_level: str

class PlantUpdate(BaseModel):
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    growth_cycle: Optional[str] = None
    water_requirements: Optional[str] = None
    sunlight_requirements: Optional[str] = None
    soil_type: Optional[str] = None
    maintenance_level: Optional[str] = None

@router.post("/plants", response_model=PlantInDB)
async def create_new_plant(
    plant: PlantCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """创建新植物"""
    created_plant = create_plant(plant, current_user.id)
    if not created_plant:
        raise HTTPException(status_code=500, detail="创建植物失败")
    return created_plant

@router.get("/plants", response_model=List[PlantInDB])
async def get_all_plants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    name: Optional[str] = None,
    category: Optional[str] = None
):
    """获取植物列表"""
    plants = get_plants(skip=skip, limit=limit, name=name, category=category)
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
    updated_plant = update_plant(plant_id, plant, current_user.id)
    if not updated_plant:
        raise HTTPException(status_code=500, detail="更新植物信息失败")
    return updated_plant

@router.delete("/plants/{plant_id}")
async def delete_plant_record(
    plant_id: int,
    current_user: UserInDB = Depends(get_current_user)
):
    """删除植物记录"""
    success = delete_plant(plant_id, current_user.id)
    if not success:
        raise HTTPException(status_code=500, detail="删除植物失败")
    return {"message": "植物删除成功"}

@router.post("/plants/{plant_id}/upload-image")
async def upload_plant_image(
    plant_id: int,
    image: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user)
):
    """上传植物图片"""
    try:
        image_path = save_plant_image(plant_id, image)
        return {"message": "图片上传成功", "image_path": image_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片上传失败: {str(e)}")

@router.get("/plants/search", response_model=List[PlantInDB])
async def search_plants(
    query: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000)
):
    """搜索植物"""
    plants = get_plants(skip=skip, limit=limit, search_query=query)
    return plants
