# landscape_lab/views/material_view.py
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
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
    MaterialImage
)
from ..models.user import UserInDB
from ..utils.security import get_current_user
from ..utils.file_utils import save_uploaded_file
from datetime import datetime
import os

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
    db_material = MaterialInDB(**material.dict(), created_by=current_user.id)
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
    if db_material.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
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
    material = db.query(MaterialInDB).filter(MaterialInDB.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    if material.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
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
    
    # 获取材料分类统计
    material_categories = db.query(
        MaterialInDB.category,
        db.func.count(MaterialInDB.id).label("count")
    ).group_by(MaterialInDB.category).all()
    
    # 获取最近添加的材料
    recent_materials = db.query(MaterialInDB).order_by(
        MaterialInDB.created_at.desc()
    ).limit(5).all()
    
    return MaterialStatistics(
        total_materials=total_materials,
        material_categories=[{"category": mc[0], "count": mc[1]} for mc in material_categories],
        recent_additions=recent_materials
    )

@router.post("/{material_id}/images/", response_model=MaterialImage)
def upload_material_image(
    material_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    material = db.query(MaterialInDB).filter(MaterialInDB.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    if material.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    file_path = save_uploaded_file(file, material_id)
    db_image = MaterialImage(
        material_id=material_id,
        file_name=file.filename,
        file_path=file_path,
        uploaded_by=current_user.id
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
