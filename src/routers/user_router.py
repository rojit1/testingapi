from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas.user_schema import CreateUserSchema, UserSchema
from ..utils import hash

router = APIRouter(
    prefix='/users',
    tags = ['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def register_user(user:CreateUserSchema, db:Session=Depends(get_db)):
    user.password = hash(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/:id', response_model=UserSchema)
async def profile_user(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

