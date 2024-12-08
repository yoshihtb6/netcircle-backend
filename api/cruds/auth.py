from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional, Annotated
from sqlalchemy import select
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import api.models.user as user_model
import api.schemas.auth as auth_schema
import hashlib

ALGORITHM = "HS256"
SECRET_KEY = "5458f58237051cf825168eb23792c5037b5e15da0f4906325b8063362d02c93f"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[user_model.User]:
    result = await db.execute(
        select(user_model.User).filter(user_model.User.name == username)
    )
    user = result.scalars().first()

    # ユーザーが存在しない場合
    if not user:
        return None

    # パスワードをハッシュ化して検証
    salt = user.salt.encode()
    hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 1000).hex()
    if user.password != hashed_password:
        return None

    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    expires = datetime.now() + expires_delta
    payload = {"username": username, "id": user_id, "role": role, "exp": expires}
    encoded_jwt = jwt.encode(payload, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        user_id = payload.get("id")
        role = payload.get("role")
        if username is None or user_id is None:
            return None
        return auth_schema.DecodedToken(username = username, user_id = user_id, role = role)
    except JWTError:
        raise JWTError
    
def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None