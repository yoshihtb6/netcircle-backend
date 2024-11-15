from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    name: Optional[str] = Field(None, example="jony")
    handle_name: Optional[str] = Field(None, example="じょにー")    

class UserCreate(UserBase):
    pass

class UserCreateResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int
    icon: Optional[str] = Field(None, example="/asset/")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True