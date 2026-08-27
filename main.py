from fastapi import FastAPI, Request
from src.utils.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management Application", description="This is a sample FastAPI application.", version="1.0.0")

