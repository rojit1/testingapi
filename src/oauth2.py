from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from .schemas.user_schema import TokenData
from .database import get_db
from .models import User
from src.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION = settings.access_token_expire_minutes

# SECRET_KEY = 'apple'
# ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRATION = 60


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise credentials_exception 
        token_data = TokenData(id = user_id)
    except JWTError:
        raise credentials_exception
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid credentials', headers= {'WWW-Authenticate':' Bearer'} )
    token = verify_access_token(token, credentials_exception=credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user