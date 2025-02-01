from fastapi import FastAPI, Depends, status, Response, HTTPException
from schema import CreateBlog, showBlog, CreateUser, ShowUser
from database import Base, engine
from dependency import get_db
from sqlalchemy.orm import Session
from model import Blog, User
from typing import List
from passlib.context import CryptContext

app = FastAPI()

Base.metadata.create_all(engine)

pass_cnt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/blog/list", status_code=status.HTTP_200_OK, response_model=List[showBlog], tags=["Blog"])
async def get_blog_list(db: Session = Depends(get_db)):
    db_blog = db.query(Blog).all()
    return db_blog

@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK, tags=["Blog"])
async def get_blog(blog_id: int, response:Response, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id)).first()
    if not db_blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': 'No record Found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No record Found')
    return db_blog

@app.post("/create/blog", status_code=status.HTTP_201_CREATED, tags=["Blog"])
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

@app.put("/update/{blog_id}", status_code=status.HTTP_200_OK, tags=["Blog"])
async def update_blog(blog_id: int, request: CreateBlog, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.update(request)
    db.commit()
    return {'data':'Updated successfully'}
    
@app.delete("/delete/{blog_id}", status_code=status.HTTP_200_OK, tags=["Blog"])
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id==int(blog_id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.delete()
    db.commit()
    return {'data':'deleted successfully'}

@app.post('/create/user', status_code=status.HTTP_201_CREATED, response_model=List[ShowUser], tags=["User"])
async def create_user(request:CreateUser, db: Session = Depends(get_db)):
    db_data = User(
        name = request.name,
        email = request.email,
        password = pass_cnt.hash(request.password)
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.get('/get/user', status_code=status.HTTP_200_OK, response_model=List[ShowUser], tags=["User"])
async def get_all_user(db: Session = Depends(get_db)):
    db_data = db.query(User).all()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    return db_data

@app.get('/get/user/{id}', status_code=status.HTTP_200_OK, tags=["User"])
async def get_user(id:int, db: Session = Depends(get_db)):
    db_data = db.query(User).filter(User.id==id).first()
    if not db_data:
        raise HTTPException(detail="No Data Found", status_code=status.HTTP_404_NOT_FOUND)
    return db_data

@app.put('/edit/user/{id}', status_code=status.HTTP_200_OK, tags=["User"])
async def edit_user(id:int, request:CreateUser, db: Session = Depends(get_db)):
    db_data = db.query(User).filter(User.id==int(id))
    if not db_data.first():
        raise HTTPException(detail="No data Found", status_code=status.HTTP_400_BAD_REQUEST)
    db_data.update(request)
    db.commit()
    return {'data':'Updated successfully'}

@app.delete("/delete/user/{id}", status_code=status.HTTP_200_OK, tags=["User"])
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_blog = db.query(User).filter(User.id==int(id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.delete()
    db.commit()
    return {'data':'deleted successfully'}
