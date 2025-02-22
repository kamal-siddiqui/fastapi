from pydantic import BaseModel
from typing import Optional, List

class CreateBlog(BaseModel):
    name: str
    title: str
    no_of_pages: Optional[int] = 0
    description: str
    user_id: int

    class Config:
        orm_config = True

class ShowUser(BaseModel):
    name: str
    email: str
    blog_details: List[CreateBlog]

    class Config:
        orm_config = True

class CreateUser(BaseModel):
    name: str
    email: str
    password: str

class showBlog(BaseModel):
    name: str
    title: str
    description: str
    user_id: int
    user_details: CreateUser
    
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    email: Optional[str] = None



 