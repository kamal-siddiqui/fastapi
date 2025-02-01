from pydantic import BaseModel
from typing import Optional

class CreateBlog(BaseModel):
    name: str
    title: str
    no_of_pages: Optional[int] = 0
    description: str
    
class showBlog(BaseModel):
    name: str
    title: str
    description: str
    
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_config = True 