# landscape_lab/controllers/plant_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
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
    PlantLocation
)
from ..models.user import UserInDB
from ..utils.security import get_current_user

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
    db_plant = PlantInDB(**plant.dict())
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
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    plant = db.query(PlantInDB).filter(PlantInDB.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
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
    
    # 获取植物类型统计
    plant_types = db.query(
        PlantInDB.type,
        db.func.count(PlantInDB.id).label("count")
    ).group_by(PlantInDB.type).all()
    
    # 获取最近添加的植物
    recent_plants = db.query(PlantInDB).order_by(
        PlantInDB.created_at.desc()
    ).limit(5).all()
    
    return PlantStatistics(
        total_plants=total_plants,
        plant_types=[{"type": pt[0], "count": pt[1]} for pt in plant_types],
        recent_additions=recent_plants
    )

@router.post("/locations/", response_model=PlantLocation)
def create_plant_location(
    location: PlantLocation,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_location = PlantLocation(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location
