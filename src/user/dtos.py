from pydantic import BaseModel

class UserDTO(BaseModel):
    name: str
    username: str
    password: str
    email: str
    
class UserResponseDTO(BaseModel):
    id: int
    name: str
    username: str
    email: str
    
class LoginSchema(BaseModel):
    username: str
    password: str
    