from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import get_db, get_current_user

router = APIRouter(tags=["user"])

@router.get("/restaurants")
def list_restaurants(
    city: str = Query(None),
    area: str = Query(None),
    dish: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Restaurant).filter(models.Restaurant.status == "approved")
    if city:
        query = query.filter(models.Restaurant.city.ilike(f"%{city}%"))
    if area:
        query = query.filter(models.Restaurant.area.ilike(f"%{area}%"))
    if dish:
        query = query.join(models.Menu).filter(models.Menu.name.ilike(f"%{dish}%"))
    return query.all()

@router.get("/restaurant/{id}")
def restaurant_detail(id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id, models.Restaurant.status == "approved").first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    menus = db.query(models.Menu).filter(models.Menu.restaurant_id == id).all()
    reviews = db.query(models.Review).filter(models.Review.restaurant_id == id, models.Review.status == "approved").all()
    return {"restaurant": restaurant, "menus": menus, "reviews": reviews}

@router.post("/restaurant/{id}/book")
def book_table(
    id: int,
    booking_date: str,
    booking_time: str,
    guests: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id, models.Restaurant.status == "approved").first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    booking = models.TableBooking(
        restaurant_id=id,
        user_id=user.id,
        booking_date=booking_date,
        booking_time=booking_time,
        guests=guests
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.post("/restaurant/{id}/review")
def post_review(
    id: int,
    menu_id: int = None,
    comment: str = "",
    rating: float = 0,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id, models.Restaurant.status == "approved").first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    review = models.Review(
        restaurant_id=id,
        menu_id=menu_id,
        user_id=user.id,
        comment=comment,
        rating=rating,
        status="pending"
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
