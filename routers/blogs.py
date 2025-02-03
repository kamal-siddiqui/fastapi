from fastapi import APIRouter, status, Response, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schema import CreateBlog, showBlog
from dependency import get_db
from model import Blog

router = APIRouter(
    tags=["Blog"],
    prefix='/blog'
)

@router.get("/blog/list", status_code=status.HTTP_200_OK, response_model=List[showBlog], tags=["Blog"])
async def get_blog_list(db: Session = Depends(get_db)):
    db_blog = db.query(Blog).all()
    if not db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No record Found')
    return db_blog

@router.get("/blog/{blog_id}", status_code=status.HTTP_200_OK, response_model=showBlog, tags=["Blog"])
async def get_blog(blog_id: int, response:Response, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id)).first()
    if not db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No record Found')
    return db_blog

@router.post("/create/blog", status_code=status.HTTP_201_CREATED, response_model=showBlog, tags=["Blog"])
async def create_blog(request: CreateBlog, db: Session = Depends(get_db)):
    db_data = Blog(
        name=request.name,
        title=request.title,
        no_of_pages=request.no_of_pages,
        description=request.description,
        user_id=request.user_id
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.put("/update/{blog_id}", status_code=status.HTTP_200_OK, tags=["Blog"])
async def update_blog(blog_id: int, request: CreateBlog, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.update(request.dict())
    db.commit()
    return {'data':'Updated successfully'}
    
@router.delete("/delete/{blog_id}", status_code=status.HTTP_200_OK, tags=["Blog"])
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.delete()
    db.commit()
    return {'data':'deleted successfully'}

