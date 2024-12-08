from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    name: Optional[str] = Field(None, example="jony")
    handle_name: Optional[str] = Field(None, example="じょにー")
    role: Optional[str] = Field(None, example="admin")

class UserCreate(UserBase):
    password: Optional[str] = Field(min_length=8, example="test1234")

class UserCreateResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    icon: Optional[str] = Field(None, example="/asset/")
    profile: Optional[str] = Field(None, example="んほおおお")
    token: Optional[str] = Field(None, example="aaaaaaaa")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(UserCreate):
    icon: Optional[str] = Field(None, example="/asset/")
    profile: Optional[str] = Field(None, example="んほおおお")