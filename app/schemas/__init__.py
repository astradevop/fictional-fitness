from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Class 
class ClassBase(BaseModel):
    name: str
    start_time: datetime
    duration: int
    total_slots: int

class ClassCreate(ClassBase):
    pass

class ClassOut(ClassBase):
    id: int
    booked_slots: int
    class Config:
        orm_mode = True

# User
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    name: str
    password: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    name: str
    email: str
    class Config:
        orm_mode = True

# Booking
class BookingCreate(BaseModel):
    class_id: int

class BookingOut(BaseModel):
    id: int
    class_id: int
    fitness_class: ClassOut # Return full class details
    class Config:
        orm_mode = True
