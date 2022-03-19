from datetime import datetime
from pydantic import BaseModel

from src.schemas.user_schema import UserSchema

class CreatePostSchema(BaseModel):
    title:str
    content:str
    publised:bool = True


class PostSchema(CreatePostSchema):
    id:int
    created_at:datetime
    owner: UserSchema

    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post:PostSchema
    votes:int

    class Config:
        orm_mode=True
