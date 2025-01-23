# landscape_lab/views/plant_view.py
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.plant import (
    PlantInDB,
    PlantCreate,
    PlantUpdate,
    PlantPublic,
    PlantSearchResult,
    PlantStatistics,
    PlantImage
)
from ..models.user import UserInDB
from ..utils.security import get_current_user
from ..utils.file_utils import save_uploaded_file
from datetime import datetime
import os

router = APIRouter(
    prefix="/api/plants",
    tags=["plants"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=PlantPublic)
def create_plant(
    plant: PlantCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_plant = PlantInDB(**plant.dict(), created_by=current_user.id)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

@router.get("/", response_model=List[PlantSearchResult])
def read_plants(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, min_length=2, max_length=100),
    db: Session = Depends(get_db)
):
    query = db.query(PlantInDB)
    if search:
        query = query.filter(PlantInDB.name.ilike(f"%{search}%"))
    plants = query.offset(skip).limit(limit).all()
    return plants

@router.get("/{plant_id}", response_model=PlantPublic)
def read_plant(
    plant_id: int,
    db: Session = Depends(get_db)
):
    plant = db.query(PlantInDB).filter(PlantInDB.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@router.put("/{plant_id}", response_model=PlantPublic)
def update_plant(
    plant_id: int,
    plant: PlantUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_plant = db.query(PlantInDB).filter(PlantInDB.id == plant_id).first()
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if db_plant.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    update_data = plant.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plant, key, value)
    
    db.commit()
    db.refresh(db_plant)
    return db_plant

@router.delete("/{plant_id}")
def delete_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    plant = db.query(PlantInDB).filter(PlantInDB.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if plant.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    db.delete(plant)
    db.commit()
    return {"message": "Plant deleted successfully"}

@router.get("/statistics/", response_model=PlantStatistics)
def get_plant_statistics(
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    total_plants = db.query(PlantInDB).count()
    
    # 获取植物分类统计
    plant_categories = db.query(
        PlantInDB.category,
        db.func.count(PlantInDB.id).label("count")
    ).group_by(PlantInDB.category).all()
    
    # 获取最近添加的植物
    recent_plants = db.query(PlantInDB).order_by(
        PlantInDB.created_at.desc()
    ).limit(5).all()
    
    return PlantStatistics(
        total_plants=total_plants,
        plant_categories=[{"category": pc[0], "count": pc[1]} for pc in plant_categories],
        recent_additions=recent_plants
    )

@router.post("/{plant_id}/images/", response_model=PlantImage)
def upload_plant_image(
    plant_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    plant = db.query(PlantInDB).filter(PlantInDB.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if plant.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    file_path = save_uploaded_file(file, plant_id)
    db_image = PlantImage(
        plant_id=plant_id,
        file_name=file.filename,
        file_path=file_path,
        uploaded_by=current_user.id
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
