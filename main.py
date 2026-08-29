from fastapi import FastAPI, Request
from src.utils.db import Base, engine
from src.tasks.router import task_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management Application", description="This is a sample FastAPI application.", version="1.0.0")

app.include_router(task_routes)
