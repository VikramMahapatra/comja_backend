import requests
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import models, auth, database
from ..schemas import Token, UserOut
from ..dependencies import get_db
import os

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

@router.post("/social-login/google", response_model=Token)
def google_login(id_token: str, db: Session = Depends(get_db)):
    # Verify token with Google
    google_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    resp = requests.get(google_url)
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    payload = resp.json()
    if payload.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Invalid Google client ID")
    email = payload.get("email")
    name = payload.get("name", email.split("@")[0])
    # Find or create user
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            name=name,
            email=email,
            password_hash="",
            social_provider="google",
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    # Return JWT
    access_token = auth.create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
