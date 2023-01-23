from pydantic import BaseModel

class Credentials(BaseModel):
    
    login: str
    password: str

class UserCreate(BaseModel):
    
    login: str
    password: str
    email: str
    first_name: str
    last_name: str
    middle_name: str