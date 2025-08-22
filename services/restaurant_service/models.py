from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)
    owner_id = Column(Integer)
    license_number = Column(String, nullable=True)
    license_image = Column(String, nullable=True)  # path or URL
    restaurant_image = Column(String, nullable=True)  # path or URL
    approved = Column(String, default="pending")  # 'pending', 'approved', 'rejected'
    menu_items = relationship("MenuItem", back_populates="restaurant")
    timings = relationship("RestaurantTiming", back_populates="restaurant")


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image = Column(String, nullable=True)  # path or URL
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="menu_items")


class RestaurantTiming(Base):
    __tablename__ = "restaurant_timings"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    day_of_week = Column(String)  # e.g., 'Monday'
    open_time = Column(String)    # e.g., '09:00'
    close_time = Column(String)   # e.g., '22:00'
    restaurant = relationship("Restaurant", back_populates="timings")
