from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import models, schemas, database
import auth_utils
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.RestaurantOut)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    if user["role"] != "restaurantadmin":
        raise HTTPException(status_code=403, detail="Only restaurant admins can create restaurants")
    db_restaurant = models.Restaurant(name=restaurant.name, address=restaurant.address, owner_id=user["user_id"])
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.get("/", response_model=list[schemas.RestaurantOut])
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(models.Restaurant).all()

@router.get("/{restaurant_id}", response_model=schemas.RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.put("/{restaurant_id}/license", response_model=schemas.RestaurantOut)
def update_license(restaurant_id: int, license_number: str = Form(...), license_image: UploadFile = File(None), db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant or restaurant.owner_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    restaurant.license_number = license_number
    if license_image:
        file_path = os.path.join(UPLOAD_DIR, f"license_{restaurant_id}_{license_image.filename}")
        with open(file_path, "wb") as f:
            f.write(license_image.file.read())
        restaurant.license_image = file_path
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.put("/{restaurant_id}/image", response_model=schemas.RestaurantOut)
def update_restaurant_image(restaurant_id: int, restaurant_image: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant or restaurant.owner_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    file_path = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}_{restaurant_image.filename}")
    with open(file_path, "wb") as f:
        f.write(restaurant_image.file.read())
    restaurant.restaurant_image = file_path
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.post("/{restaurant_id}/menu", response_model=schemas.MenuItemOut)
def create_menu_item(restaurant_id: int, name: str = Form(...), price: float = Form(...), description: str = Form(None), image: UploadFile = File(None), db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant or restaurant.owner_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    image_path = None
    if image:
        image_path = os.path.join(UPLOAD_DIR, f"menu_{restaurant_id}_{image.filename}")
        with open(image_path, "wb") as f:
            f.write(image.file.read())
    db_item = models.MenuItem(name=name, price=price, description=description, image=image_path, restaurant_id=restaurant_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{restaurant_id}/menu", response_model=list[schemas.MenuItemOut])
def list_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()

@router.get("/{restaurant_id}/menu/{item_id}", response_model=schemas.MenuItemOut)
def get_menu_item(restaurant_id: int, item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id, models.MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.put("/{restaurant_id}/menu/{item_id}", response_model=schemas.MenuItemOut)
def update_menu_item(restaurant_id: int, item_id: int, item: schemas.MenuItemCreate, db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id, models.MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if user["role"] != "restaurantadmin" or db_restaurant.owner_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update menu items for this restaurant")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{restaurant_id}/menu/{item_id}")
def delete_menu_item(restaurant_id: int, item_id: int, db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id, models.MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if user["role"] != "restaurantadmin" or db_restaurant.owner_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete menu items for this restaurant")
    db.delete(db_item)
    db.commit()
    return {"detail": "Menu item deleted"}

@router.put("/{restaurant_id}/timings", response_model=list[schemas.RestaurantTimingOut])
def set_timings(restaurant_id: int, timings: list[schemas.RestaurantTimingCreate], db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant or restaurant.owner_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Remove old timings
    db.query(models.RestaurantTiming).filter(models.RestaurantTiming.restaurant_id == restaurant_id).delete()
    # Add new timings
    for t in timings:
        db_timing = models.RestaurantTiming(restaurant_id=restaurant_id, **t.dict())
        db.add(db_timing)
    db.commit()
    return db.query(models.RestaurantTiming).filter(models.RestaurantTiming.restaurant_id == restaurant_id).all()

# Super admin endpoints
@router.get("/admin/restaurants/pending", response_model=list[schemas.RestaurantOut])
def list_pending_restaurants(db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    if user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can view pending restaurants")
    return db.query(models.Restaurant).filter(models.Restaurant.approved == "pending").all()

@router.post("/admin/restaurants/{restaurant_id}/approve", response_model=schemas.RestaurantOut)
def approve_restaurant(restaurant_id: int, db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    if user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can approve")
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant.approved = "approved"
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.post("/admin/restaurants/{restaurant_id}/reject", response_model=schemas.RestaurantOut)
def reject_restaurant(restaurant_id: int, db: Session = Depends(get_db), user=Depends(auth_utils.get_current_user)):
    if user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can reject")
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant.approved = "rejected"
    db.commit()
    db.refresh(restaurant)
    return restaurant
