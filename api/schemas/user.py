from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    name: Optional[str] = Field(None, example="admin")
    handle_name: Optional[str] = Field(None, example="管理者")
    role: Optional[str] = Field(None, example="admin")

class UserCreate(UserBase):
    password: Optional[str] = Field(min_length=8, example="test1234")

class UserCreateResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    icon: Optional[str] = Field(None, example="xxxxxx")
    profile: Optional[str] = Field(None, example="＼(^o^)／")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    handle_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    icon: Optional[str] = None
    profile: Optional[str] = None