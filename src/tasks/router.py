from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import TaskDTO, TaskResponseDTO
from src.utils.db import get_db
from src.utils.helpers import is_authenticated
from src.user.models import UserModel
from sqlalchemy.orm import Session

task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create", response_model= TaskResponseDTO, status_code= status.HTTP_201_CREATED)
def create_task(body: TaskDTO, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.create_task(body, db, user)

@task_routes.get("/all", response_model= list[TaskResponseDTO], status_code= status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_all_tasks(db, user)

@task_routes.get("/{task_id}", response_model= TaskResponseDTO, status_code= status.HTTP_200_OK)
def get_task_by_id(task_id: int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_task_by_id(task_id, db, user)

@task_routes.delete("/delete/{task_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_task_by_id(task_id: int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.delete_task_by_id(task_id, db, user)

@task_routes.put("/update/{task_id}", response_model= TaskResponseDTO, status_code= status.HTTP_201_CREATED)
def update_task(task_id: int, body: TaskDTO, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.update_task(task_id, body, db, user)