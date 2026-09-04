from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Role(BaseModel):
    name: str
    permissions: List[str] = Field(default_factory=list)

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    roles: List[Role] = Field(default_factory=list)
    created_at: datetime
    
    class Config:
        from_attributes = True
