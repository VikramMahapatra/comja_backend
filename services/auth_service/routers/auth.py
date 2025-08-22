from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth_utils, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User registration and login
@router.post("/user/register", response_model=schemas.UserOut)
def user_register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth_utils.get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pw,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/user/login", response_model=schemas.Token)
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username, models.User.role == "user").first()
    if not user or not auth_utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth_utils.create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# Restaurant admin registration and login
@router.post("/restaurant/register", response_model=schemas.UserOut)
def restaurant_register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth_utils.get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pw,
        role="restaurantadmin"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/restaurant/login", response_model=schemas.Token)
def restaurant_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username, models.User.role == "restaurantadmin").first()
    if not user or not auth_utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth_utils.create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# Superadmin registration and login (should be protected in production)
@router.post("/superadmin/register", response_model=schemas.UserOut)
def superadmin_register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth_utils.get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pw,
        role="superadmin"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/superadmin/login", response_model=schemas.Token)
def superadmin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username, models.User.role == "superadmin").first()
    if not user or not auth_utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth_utils.create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth_utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth_utils.create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth_utils.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
