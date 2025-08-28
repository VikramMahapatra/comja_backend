from fastapi import FastAPI
from routers import auth
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auth Service")

# Enable CORS so restaurant_service Swagger UI can talk to auth_service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:8000"] if only frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")


@app.get("/ping")
def ping():
    return {"status": "ok"}
