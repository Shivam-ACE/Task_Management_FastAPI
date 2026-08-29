from src.tasks.dtos import TaskDTO
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def create_task(body: TaskDTO, db: Session):
    data = body.model_dump()
    new_task = TaskModel(title=data['title'], description=data['description'], is_completed=data['is_completed'])
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # return {"status": "Task created successfully...", "data": new_task}
    return new_task

def get_all_tasks(db: Session):
    tasks = db.query(TaskModel).all()
    # return {"status": "Success", "data": tasks}
    return tasks

def get_task_by_id(task_id: int, db: Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(404, detail="Task id is invalid")
    return task

def delete_task_by_id(task_id: int, db: Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(404, detail="Task id is invalid")
    
    db.delete(task)
    db.commit()
    
    return None

def update_task(task_id: int, body: TaskDTO, db: Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(404, detail="Task id is invalid")
    
    # task.title = body.title
    # task.description = body.description
    # task.is_completed = body.is_completed
    body = body.model_dump()
    for field, value in body.items():
        setattr(task, field, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task
    