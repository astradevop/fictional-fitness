from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List

import models
import schemas
from database import SessionLocal, engine

# database create
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Studio Booking API")

# Configuration
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# --- Endpoints ---

@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, name=user.name, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/classes", response_model=schemas.ClassOut)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
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

@app.get("/classes", response_model=List[schemas.ClassOut])
def get_classes(db: Session = Depends(get_db)):
    return db.query(models.FitnessClass).all()

@app.post("/book", response_model=schemas.BookingOut)
def book_class(booking_data: schemas.BookingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
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

@app.get("/bookings", response_model=List[schemas.BookingOut])
def get_bookings(current_user: models.User = Depends(get_current_user)):
    return current_user.bookings
