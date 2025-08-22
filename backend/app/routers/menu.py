from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import require_role, get_current_user, get_db

router = APIRouter(prefix="/restaurant/menu", tags=["menu"])

@router.post("/", response_model=schemas.UserOut)
def add_menu_item(
    name: str,
    description: str,
    price: float,
    image_url: str = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("restaurantadmin"))
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.created_by == user.id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    menu = models.Menu(
        restaurant_id=restaurant.id,
        name=name,
        description=description,
        price=price,
        image_url=image_url
    )
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu

@router.put("/{menu_id}")
def edit_menu_item(
    menu_id: int,
    name: str = None,
    description: str = None,
    price: float = None,
    image_url: str = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("restaurantadmin"))
):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu item not found")
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == menu.restaurant_id).first()
    if restaurant.created_by != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if name: menu.name = name
    if description: menu.description = description
    if price: menu.price = price
    if image_url: menu.image_url = image_url
    db.commit()
    db.refresh(menu)
    return menu

@router.delete("/{menu_id}")
def delete_menu_item(menu_id: int, db: Session = Depends(get_db), user=Depends(require_role("restaurantadmin"))):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu item not found")
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == menu.restaurant_id).first()
    if restaurant.created_by != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(menu)
    db.commit()
    return {"message": "Menu item deleted"}
