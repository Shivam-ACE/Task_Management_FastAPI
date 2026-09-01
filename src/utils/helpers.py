from fastapi import Request, status, HTTPException ,Depends
from src.utils.settings import settings
from src.utils.db import get_db
from src.user.models import UserModel
from sqlalchemy.orm import Session
import jwt

def is_authenticated(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're unauthorized !!")
    token = token.split(" ")[-1]
    
    try:
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user_id = data.get("_id")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're unauthorized !!")
    
    return user