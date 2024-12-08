from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from api.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    password = Column(String(64), nullable=False)  
    handle_name = Column(String(128), unique=True, nullable=False)
    icon = Column(String(256), nullable=True)
    profile = Column(String(1024), nullable=True)
    role = Column(String(128), nullable=False)
    salt = Column(String(64), nullable=False)
    refresh_token = Column(String(256), nullable=True)  # リフレッシュトークンを保存
    refresh_token_expiry = Column(DateTime, nullable=True)  # 有効期限
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now())

    
