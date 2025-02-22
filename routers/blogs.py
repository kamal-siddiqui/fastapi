from fastapi import APIRouter, status, Response, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schema import CreateBlog, showBlog, CreateUser
from dependency import get_db
from repository import blogs
from oauth2 import get_current_user

router = APIRouter(
    tags=["Blog"],
    prefix='/blog'
)

@router.get("/list", status_code=status.HTTP_200_OK, response_model=List[showBlog])
async def get_all(db: Session = Depends(get_db), get_current_user: CreateUser = Depends(get_current_user)):
    res = await blogs.get_blog_list(db)
    return res

@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=showBlog)
async def get(blog_id: int, db: Session = Depends(get_db)):
    res = await blogs.get_blog(blog_id, db)
    return res

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=showBlog)
async def create(request: CreateBlog, db: Session = Depends(get_db), get_current_user: CreateUser = Depends(get_current_user)): 
    res = await blogs.create_blog(request, db)
    return res

@router.put("/update/{blog_id}", status_code=status.HTTP_200_OK)
async def update(blog_id: int, request: CreateBlog, db: Session = Depends(get_db), get_current_user: CreateUser = Depends(get_current_user)):
    res = await blogs.update_blog(blog_id, request, db)
    return res
    
@router.delete("/delete/{blog_id}", status_code=status.HTTP_200_OK)
async def delete(blog_id: int, db: Session = Depends(get_db), get_current_user: CreateUser = Depends(get_current_user)):
    res = await blogs.delete_blog(blog_id, db)
    return res

