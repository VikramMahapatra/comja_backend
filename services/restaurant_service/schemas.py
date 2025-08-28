from pydantic import BaseModel
from typing import List, Optional


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None  # URL or path


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemOut(MenuItemBase):
    id: int
    class Config:
        from_attributes = True


class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    license_number: Optional[str] = None
    license_image: Optional[str] = None
    restaurant_image: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantTimingBase(BaseModel):
    day_of_week: str
    open_time: str
    close_time: str

class RestaurantTimingCreate(RestaurantTimingBase):
    pass

class RestaurantTimingOut(RestaurantTimingBase):
    id: int
    class Config:
        from_attributes = True

class RestaurantOut(RestaurantBase):
    id: int
    owner_id:Optional[int]= None
    approved: Optional[str] = None
    menu_items: List[MenuItemOut] = []
    timings: List[RestaurantTimingOut] = []
    class Config:
        from_attributes = True

# For admin approval
class RestaurantApproval(BaseModel):
    approved: str  # 'approved' or 'rejected'
