from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from src.user import controller
from src.user.dtos import UserDTO, UserResponseDTO, LoginSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session

user_routes = APIRouter(prefix="/users")

@user_routes.post("/register", response_model= UserResponseDTO, status_code= status.HTTP_201_CREATED)
async def register(body: UserDTO, bg_task: BackgroundTasks, db: Session = Depends(get_db)):
    return await controller.register(body, bg_task, db)

@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)

@user_routes.get("/is_auth", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
def is_auth(request: Request, db: Session = Depends(get_db)):
    return controller.is_authenticated(request, db)

@user_routes.get("/all", response_model= list[UserResponseDTO], status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)):
    return controller.all_users(db)