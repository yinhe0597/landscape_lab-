# landscape_lab/controllers/material_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.material import (
    MaterialInDB,
    MaterialCreate,
    MaterialUpdate,
    MaterialPublic,
    MaterialSearchResult,
    MaterialStatistics,
    MaterialUsage
)
from ..models.user import UserInDB
from ..utils.security import get_current_user

router = APIRouter(
    prefix="/api/materials",
    tags=["materials"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=MaterialPublic)
def create_material(
    material: MaterialCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_material = MaterialInDB(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@router.get("/", response_model=List[MaterialSearchResult])
def read_materials(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, min_length=2, max_length=100),
    db: Session = Depends(get_db)
):
    query = db.query(MaterialInDB)
    if search:
        query = query.filter(MaterialInDB.name.ilike(f"%{search}%"))
    materials = query.offset(skip).limit(limit).all()
    return materials

@router.get("/{material_id}", response_model=MaterialPublic)
def read_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    material = db.query(MaterialInDB).filter(MaterialInDB.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.put("/{material_id}", response_model=MaterialPublic)
def update_material(
    material_id: int,
    material: MaterialUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_material = db.query(MaterialInDB).filter(MaterialInDB.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    update_data = material.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_material, key, value)
    
    db.commit()
    db.refresh(db_material)
    return db_material

@router.delete("/{material_id}")
def delete_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    material = db.query(MaterialInDB).filter(MaterialInDB.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db.delete(material)
    db.commit()
    return {"message": "Material deleted successfully"}

@router.get("/statistics/", response_model=MaterialStatistics)
def get_material_statistics(
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    total_materials = db.query(MaterialInDB).count()
    
    # 获取材料类型统计
    material_types = db.query(
        MaterialInDB.category,
        db.func.count(MaterialInDB.id).label("count")
    ).group_by(MaterialInDB.category).all()
    
    # 获取最近添加的材料
    recent_materials = db.query(MaterialInDB).order_by(
        MaterialInDB.created_at.desc()
    ).limit(5).all()
    
    return MaterialStatistics(
        total_materials=total_materials,
        material_types=[{"category": mt[0], "count": mt[1]} for mt in material_types],
        recent_additions=recent_materials
    )

@router.post("/usages/", response_model=MaterialUsage)
def create_material_usage(
    usage: MaterialUsage,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_usage = MaterialUsage(**usage.dict())
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage
