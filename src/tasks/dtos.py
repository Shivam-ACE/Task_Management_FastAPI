from pydantic import BaseModel

class TaskDTO(BaseModel):
    title: str
    description: str
    is_completed: bool = False
    
class TaskResponseDTO(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool