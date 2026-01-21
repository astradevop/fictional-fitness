from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.api import deps

router = APIRouter()

@router.post("/book", response_model=schemas.BookingOut)
def book_class(booking_data: schemas.BookingCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    # Check class existence
    fitness_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking_data.class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check slots
    if fitness_class.booked_slots >= fitness_class.total_slots:
        raise HTTPException(status_code=400, detail="Class is full")
    
    # Check already booked status
    existing_booking = db.query(models.Booking).filter(
        models.Booking.user_id == current_user.id,
        models.Booking.class_id == booking_data.class_id
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="You have already booked this class")

    # Book it
    new_booking = models.Booking(user_id=current_user.id, class_id=booking_data.class_id)
    fitness_class.booked_slots += 1
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/bookings", response_model=List[schemas.BookingOut])
def get_bookings(current_user: models.User = Depends(deps.get_current_user)):
    return current_user.bookings
