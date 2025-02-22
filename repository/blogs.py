from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from model import Blog

async def get_blog_list(db: Session):
    db_blog = db.query(Blog).all()
    if not db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No record Found')
    return db_blog

async def get_blog(blog_id: int, db: Session):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id)).first()
    if not db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No record Found')
    return db_blog

async def create_blog(request, db: Session):
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

async def update_blog(blog_id: int, request, db: Session):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.update(request.dict())
    db.commit()
    return {'data':'Updated successfully'}
    
async def delete_blog(blog_id: int, db: Session):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.delete()
    db.commit()
    return {'data':'deleted successfully'}