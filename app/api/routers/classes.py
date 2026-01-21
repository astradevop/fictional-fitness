from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.api import deps

router = APIRouter()

@router.post("/classes", response_model=schemas.ClassOut)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    new_class = models.FitnessClass(
        name=class_data.name,
        start_time=class_data.start_time,
        duration=class_data.duration,
        total_slots=class_data.total_slots
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@router.get("/classes", response_model=List[schemas.ClassOut])
def get_classes(db: Session = Depends(deps.get_db)):
    return db.query(models.FitnessClass).all()
