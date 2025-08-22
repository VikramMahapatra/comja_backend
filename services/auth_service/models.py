from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    social_provider = Column(String, nullable=True)
    role = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
