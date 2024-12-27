from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as user_model
import api.schemas.user as user_schema
import hashlib
import base64
import os
from typing import List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result


async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreate
) -> user_model.User:
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac("sha256", user_create.password.encode(), salt, 1000).hex()

    user = user_model.User(
        name = user_create.name,
        handle_name = user_create.handle_name,
        password = hashed_password,
        salt = salt.decode(),
        role = user_create.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_all_users(db: AsyncSession) -> List[Tuple[int]]:
    result: Result = await (
        db.execute(select(
            user_model.User.id,
            user_model.User.name,
            user_model.User.handle_name,
            user_model.User.icon,
            user_model.User.profile,
            user_model.User.role,
            user_model.User.created_at,
            user_model.User.updated_at    
        ))
    )
    return result.all()

async def get_user(db: AsyncSession, user_id: int) -> Optional[user_model.User]:
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.id == user_id)
    )
    user: Optional[Tuple[user_model.User]] = result.first()
    return user[0] if user is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


async def update_user(
    db: AsyncSession, user_update: user_schema.UserUpdate, original: user_model.User
) -> user_model.User:
    if user_update.name is not None:
        original.name = user_update.name
        
    if user_update.password is not None:
        # salt を original インスタンスから取得
        salt = original.salt.encode()
        original.password = hashlib.pbkdf2_hmac(
            "sha256", user_update.password.encode(), salt, 1000
        ).hex()
    
    if user_update.handle_name is not None:
        original.handle_name = user_update.handle_name
    
    if user_update.icon is not None:
        original.icon = user_update.icon
    
    if user_update.role is not None:
        original.role = user_update.role
    
    if user_update.profile is not None:
        original.profile = user_update.profile
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_user(db: AsyncSession, original: user_model.User) -> None:
    await db.delete(original)
    await db.commit()
