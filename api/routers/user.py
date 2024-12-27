from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import api.cruds.user as user_crud
import api.schemas.user as user_schema
import api.cruds.auth as auth_crud
from api.schemas.auth import DecodedToken
from api.db import get_db

router = APIRouter()

UserDependency = Annotated[DecodedToken, Depends(auth_crud.get_current_user)]


@router.get("/users", response_model=List[user_schema.UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all_users(db)

@router.post("/users", response_model=user_schema.UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_crud.create_user(db, user_body)

@router.put("/users/{user_id}", response_model=user_schema.UserResponse)
async def update_user(token: UserDependency, user_id: int, user_body: user_schema.UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.update_user(db, user_body, original=user)


@router.delete("/users/{user_id}", response_model=None)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.delete_user(db, original=user)