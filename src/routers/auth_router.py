from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas.user_schema import Token
from ..utils import verify
from .. import oauth2

router = APIRouter(
    # prefix='/auth',
    tags = ['Auth']
)

@router.post('/login' , response_model=Token)
async def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    return {
        "access_token":access_token,
        "token_type": "Bearer"
    } 

