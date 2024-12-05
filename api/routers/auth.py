from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta

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
    
    token = auth_crud.create_access_token(user.name, user.id, timedelta(minutes=20))
    
    if not token:
        raise HTTPException(status_code=500, detail="Failed to create access token")
     
    return {"access_token": token, "token_type": "bearer"}