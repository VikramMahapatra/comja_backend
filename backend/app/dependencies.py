from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from . import auth
from .routers.auth import oauth2_scheme
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_role(role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

def require_roles(roles: list):
    def roles_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return roles_checker
