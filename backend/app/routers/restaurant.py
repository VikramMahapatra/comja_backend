from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import require_role, get_current_user, get_db

router = APIRouter(prefix="/restaurant", tags=["restaurant-admin"])

@router.post("/onboard")
def request_onboarding(
    name: str,
    city: str,
    area: str,
    address: str,
    phone: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("restaurantadmin"))
):
    restaurant = models.Restaurant(
        name=name,
        city=city,
        area=area,
        address=address,
        phone=phone,
        status="pending",
        created_by=user.id
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.put("/update")
def update_restaurant(
    name: str = None,
    city: str = None,
    area: str = None,
    address: str = None,
    phone: str = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("restaurantadmin"))
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.created_by == user.id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if name: restaurant.name = name
    if city: restaurant.city = city
    if area: restaurant.area = area
    if address: restaurant.address = address
    if phone: restaurant.phone = phone
    db.commit()
    db.refresh(restaurant)
    return restaurant
