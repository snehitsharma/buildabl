from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # lets this build directly from the SQLAlchemy model

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    