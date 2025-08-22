from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    social_provider = Column(String, nullable=True)
    role = Column(String)  # "superadmin", "restaurantadmin", "user"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    area = Column(String)
    address = Column(String)
    phone = Column(String)
    status = Column(String)  # "pending", "approved", "rejected"
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(String)
    rating = Column(Float)
    status = Column(String)  # "pending", "approved", "rejected"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TableBooking(Base):
    __tablename__ = "table_bookings"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    booking_date = Column(String)
    booking_time = Column(String)
    guests = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
