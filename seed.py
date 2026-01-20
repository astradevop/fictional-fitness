from database import SessionLocal, engine
import models
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Create tables
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def seed():
    # 1. Create a sample user
    if not db.query(models.User).filter(models.User.email == "test@example.com").first():
        user = models.User(
            name="Test User", 
            email="test@example.com", 
            password=pwd_context.hash("password123")
        )
        db.add(user)
        print("Created user: test@example.com / password123")
    
    # 2. Create classes
    if db.query(models.FitnessClass).count() == 0:
        c1 = models.FitnessClass(
            name="Yoga Flow", 
            start_time=datetime.now() + timedelta(days=1, hours=2), 
            duration=60, 
            total_slots=10
        )
        c2 = models.FitnessClass(
            name="HIIT Blast", 
            start_time=datetime.now() + timedelta(days=2, hours=4), 
            duration=45, 
            total_slots=15
        )
        c3 = models.FitnessClass(
            name="Meditation", 
            start_time=datetime.now() + timedelta(days=3, hours=1), 
            duration=30, 
            total_slots=5
        )
        db.add_all([c1, c2, c3])
        print("Created 3 fitness classes.")

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
