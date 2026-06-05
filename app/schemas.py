from pydantic import BaseModel, EmailStr
from datetime import datetime


class TravelCreate(BaseModel):
    name: str
    city: str
    duration: int
    cost: int


class TravelResponse(TravelCreate):
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True