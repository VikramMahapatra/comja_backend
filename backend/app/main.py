
from fastapi import FastAPI
from .database import Base, engine
from .routers import auth as auth_router
from .routers import admin as admin_router
from .routers import restaurant as restaurant_router
from .routers import menu as menu_router
from .routers import user as user_router
from .routers import admin_restaurants as admin_restaurants_router
from .routers import google_auth as google_auth_router

from fastapi import Depends
from .dependencies import require_role, get_db
from sqlalchemy.orm import Session
from . import seed

app = FastAPI(
    title="ZenZomato MVP1 Food Delivery App",
    description="A vibrant GenZ food delivery platform. Features: role-based access, restaurant onboarding, menu management, reviews, bookings, and more.",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication and user management"},
        {"name": "admin", "description": "Super admin endpoints"},
        {"name": "restaurant-admin", "description": "Restaurant admin endpoints"},
        {"name": "menu", "description": "Menu management"},
        {"name": "user", "description": "User-facing endpoints"},
    ]
)

# Create tables
Base.metadata.create_all(bind=engine)







app.include_router(auth_router.router)
app.include_router(google_auth_router.router)
app.include_router(admin_router.router)
app.include_router(restaurant_router.router)
app.include_router(menu_router.router)
app.include_router(user_router.router)
app.include_router(admin_restaurants_router.router)


# Debug endpoint to check server responsiveness
@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to ZenZomato MVP1!"}


# Superadmin-only endpoint to seed data
@app.post("/seed", tags=["admin"])
def seed_db(db: Session = Depends(get_db), superadmin=Depends(require_role("superadmin"))):
    seed.seed_data(db)
    return {"message": "Seed data inserted."}