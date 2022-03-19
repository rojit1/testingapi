from typing import Optional
from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    email:EmailStr
    password:str


class UserSchema(BaseModel):
    id:int
    email:EmailStr
    
    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[str] = None