from fastapi import FastAPI
from app import models
from app.db.session import engine
from app.api.routers import users, auth, classes, bookings

# database create
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Studio Booking API")

app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(classes.router, tags=["Classes"])
app.include_router(bookings.router, tags=["Bookings"])
