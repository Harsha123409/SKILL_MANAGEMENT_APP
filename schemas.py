from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "Employee"

class UserLogin(BaseModel):
    email: str
    password: str

class SkillCreate(BaseModel):
    name: str
    level: str

