from fastapi import FastAPI
from routers import auth
from database import Base, engine

app = FastAPI(title="Auth Service")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")


@app.get("/ping")
def ping():
    return {"status": "ok"}
