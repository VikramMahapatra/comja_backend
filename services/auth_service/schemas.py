from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# Used for admin creation endpoint
class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str  # 'superadmin' or 'restaurantadmin'

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
