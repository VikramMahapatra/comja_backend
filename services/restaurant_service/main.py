from fastapi import FastAPI
from routers import restaurant
import models, database

app = FastAPI(
    title="Restaurant Service",
    description="CRUD operations for restaurants, menus, licenses with JWT auth",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)

app.include_router(restaurant.router, prefix="/restaurant", tags=["Restaurant"])

@app.get("/ping")
def ping():
    return {"message": "Restaurant Service is running"}
