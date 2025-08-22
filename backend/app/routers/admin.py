from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import require_role, require_roles, get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/restaurant", response_model=schemas.UserOut)
def create_restaurant_admin(user: schemas.UserCreate, db: Session = Depends(get_db), superadmin=Depends(require_role("superadmin"))):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash="",
        role="restaurantadmin"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/restaurant/{id}/approve")
def approve_restaurant(id: int, db: Session = Depends(get_db), superadmin=Depends(require_role("superadmin"))):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant.status = "approved"
    db.commit()
    return {"message": "Restaurant approved"}

@router.post("/restaurant/{id}/reject")
def reject_restaurant(id: int, db: Session = Depends(get_db), superadmin=Depends(require_role("superadmin"))):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant.status = "rejected"
    db.commit()
    return {"message": "Restaurant rejected"}

@router.post("/comment/{id}/approve")
def approve_comment(id: int, db: Session = Depends(get_db), superadmin=Depends(require_role("superadmin"))):
    review = db.query(models.Review).filter(models.Review.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review.status = "approved"
    db.commit()
    return {"message": "Comment approved"}

@router.post("/comment/{id}/reject")
def reject_comment(id: int, db: Session = Depends(get_db), superadmin=Depends(require_role("superadmin"))):
    review = db.query(models.Review).filter(models.Review.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review.status = "rejected"
    db.commit()
    return {"message": "Comment rejected"}

@router.get("/bookings")
def view_bookings(db: Session = Depends(get_db), superadmin=Depends(require_role("superadmin"))):
    bookings = db.query(models.TableBooking).all()
    return bookings
