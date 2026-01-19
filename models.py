from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    bookings = relationship("Booking", back_populates="user")

class FitnessClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_time = Column(DateTime)
    duration = Column(Integer)
    total_slots = Column(Integer)
    booked_slots = Column(Integer, default=0)

    bookings = relationship("Booking", back_populates="fitness_class")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    
    user = relationship("User", back_populates="bookings")
    fitness_class = relationship("FitnessClass", back_populates="bookings")
