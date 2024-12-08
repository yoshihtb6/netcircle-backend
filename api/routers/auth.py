from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta, datetime
import api.models.user as user_model

import api.cruds.auth as auth_crud
import api.schemas.auth as auth_schema
from api.db import get_db

router = APIRouter()

DbDependency = Annotated[Session, Depends(get_db)]
FormDependency = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]

@router.post("/auth/login", response_model=auth_schema.AuthResponse, status_code=status.HTTP_200_OK)
async def login(db: DbDependency, form_data: FormDependency):
    user = await auth_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = auth_crud.create_access_token(user.name, user.id, user.role, timedelta(minutes=60))
    refresh_token = auth_crud.create_refresh_token({"sub": user.name}, timedelta(days=7))

    # リフレッシュトークンをDBに保存
    user.refresh_token = refresh_token
    user.refresh_token_expiry = datetime.now() + timedelta(days=7)
    db.add(user)
    await db.commit()
    
    if not access_token:
        raise HTTPException(status_code=500, detail="Failed to create access token")
     
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/auth/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    # リフレッシュトークンを検証
    payload = auth_crud.decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # DBでトークンを確認
    result = await db.execute(select(user_model.User).where(user_model.User.name == username))
    user = result.scalars().first()

    if not user or user.refresh_token != refresh_token or user.refresh_token_expiry < datetime.now():
        raise HTTPException(status_code=401, detail="Expired or invalid refresh token")

    # 新しいアクセストークンを作成
    access_token = auth_crud.create_access_token(user.name, user.id, user.role, timedelta(minutes=30))
    return {"access_token": access_token}