from pydantic import BaseModel
from typing import Optional

class CreateBlog(BaseModel):
    name: str
    title: str
    no_of_pages: Optional[int] = 0
    description: str