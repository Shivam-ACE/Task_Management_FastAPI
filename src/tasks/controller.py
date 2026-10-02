# from src.tasks.dtos import TaskDTO
# from sqlalchemy.orm import Session
# from src.tasks.models import TaskModel
# from src.user.models import UserModel
# from fastapi import HTTPException

# def create_task(body: TaskDTO, db: Session, user: UserModel):
#     data = body.model_dump()
#     new_task = TaskModel(title=data['title'], description=data['description'], is_completed=data['is_completed'], user_id = user.id)
    
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
    
#     # return {"status": "Task created successfully...", "data": new_task}
#     return new_task

# def get_all_tasks(db: Session, user: UserModel):
#     tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id)
#     # return {"status": "Success", "data": tasks}
#     return tasks

# def get_task_by_id(task_id: int, db: Session, user: UserModel):
#     task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
#     if not task:
#         raise HTTPException(404, detail="Task id is invalid")
#     return task

# def delete_task_by_id(task_id: int, db: Session, user: UserModel):
#     task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
#     if not task:
#         raise HTTPException(404, detail="Task id is invalid")
    
#     db.delete(task)
#     db.commit()
    
#     return None

# def update_task(task_id: int, body: TaskDTO, db: Session, user: UserModel):
#     task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
#     if not task:
#         raise HTTPException(404, detail="Task id is invalid")
    
#     # task.title = body.title
#     # task.description = body.description
#     # task.is_completed = body.is_completed
#     body = body.model_dump()
#     for field, value in body.items():
#         setattr(task, field, value)
    
#     db.add(task)
#     db.commit()
#     db.refresh(task)
    
#     return task
    
from src.tasks.dtos import TaskDTO
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.user.models import UserModel
from fastapi import HTTPException
from src.utils.cache import cache_get, cache_set, cache_delete


def _cache_key(user: UserModel) -> str:
    return f"tasks:user:{user.id}"


def _to_dict(task: TaskModel) -> dict:
    d = dict(task.__dict__)
    d.pop("_sa_instance_state", None)
    return d


def create_task(body: TaskDTO, db: Session, user: UserModel):
    data = body.model_dump()
    new_task = TaskModel(title=data['title'], description=data['description'],
                         is_completed=data['is_completed'], user_id=user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    cache_delete(_cache_key(user))
    return new_task


def get_all_tasks(db: Session, user: UserModel):
    key = _cache_key(user)
    cached = cache_get(key)
    if cached is not None:
        return cached

    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    data = [_to_dict(t) for t in tasks]
    cache_set(key, data, ttl=60)
    return data


def get_task_by_id(task_id: int, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(404, detail="Task id is invalid")
    return task


def delete_task_by_id(task_id: int, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(404, detail="Task id is invalid")

    db.delete(task)
    db.commit()

    cache_delete(_cache_key(user))
    return None


def update_task(task_id: int, body: TaskDTO, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(404, detail="Task id is invalid")

    body = body.model_dump()
    for field, value in body.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    cache_delete(_cache_key(user))
    return task
