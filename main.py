from fastapi import FastAPI, Depends, status, Response, HTTPException
from schema import CreateBlog
from database import Base, engine
from dependency import get_db
from sqlalchemy.orm import Session
from model import Blog

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/blog/list", status_code=status.HTTP_200_OK)
async def get_blog_list(db: Session = Depends(get_db)):
    db_blog = db.query(Blog).all()
    return db_blog

@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK)
async def get_blog(blog_id: int, response:Response, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id)).first()
    if not db_blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': 'No record Found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No record Found')
    return db_blog

@app.post("/create/blog", status_code=status.HTTP_201_CREATED)
async def create_blog(request: CreateBlog, db: Session = Depends(get_db)):
    db_data = Blog(
        name=request.name,
        title=request.title,
        no_of_pages=request.no_of_pages,
        description=request.description
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.put("/update/{blog_id}", status_code=status.HTTP_200_OK)
async def update_blog(blog_id: int, request: CreateBlog, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.update(request)
    db.commit()
    return {'data':'Updated successfully'}
    
@app.delete("/delete/{blog_id}", status_code=status.HTTP_200_OK)
async def create_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.delete()
    db.commit()
    return {'data':'deleted successfully'}