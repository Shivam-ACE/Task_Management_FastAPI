from fastapi import HTTPException, status, Request, BackgroundTasks
from src.user.models import UserModel
from src.user.dtos import UserDTO, LoginSchema
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta
from src.utils.mail import send_email


password_hash = PasswordHash.recommended()
def get_password_hash(password):
    return password_hash.hash(password)
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def register(body: UserDTO, bg_task: BackgroundTasks, db: Session):
    body = body.model_dump()
    
    is_user = db.query(UserModel).filter(UserModel.username == body["username"]).first()
    if is_user:
        raise HTTPException(400, detail="Username already exists..")
    
    is_user = db.query(UserModel).filter(UserModel.email == body["email"]).first()
    if is_user:
        raise HTTPException(400, detail="Email already exists..")
    
    hashed_password = get_password_hash(body["password"])
    
    new_user = UserModel(name= body["name"], username= body["username"], hashed_password= hashed_password, email= body["email"])
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    ####send mail
    # res = await send_email([new_user.email])
    # print(res)
    bg_task.add_task(send_email, [new_user.email])
    
    return new_user

def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Username !!")
    
    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password !!")
    
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    
    token = jwt.encode({"_id": user.id, "exp": exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)
            
    return {"token": token}
    
    
def is_authenticated(request: Request, db: Session):
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
    
    ####### no need to validate expire time decode method is handling it itself
    
    # exp_time = data.get("exp")
    
    # curr_time = datetime.now().timestamp()
    # if curr_time > exp_time:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're unauthorized !!")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're unauthorized !!")
    
    return user

def all_users(db: Session):
    users = db.query(UserModel)
    return users