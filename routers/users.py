from fastapi import APIRouter, status, Response, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schema import CreateBlog, showBlog, CreateUser, ShowUser
from dependency import get_db
from model import Blog, User
from passlib.context import CryptContext

router = APIRouter(
    tags=["User"],
    prefix='/user'
)

pass_cnt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get('/get', status_code=status.HTTP_200_OK, response_model=List[ShowUser])
async def all_user(db: Session = Depends(get_db)):
    db_data = db.query(User).all()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    return db_data

@router.get('/get/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser)
async def user(id:int, db: Session = Depends(get_db)):
    db_data = db.query(User).filter(User.id==id).first()
    if not db_data:
        raise HTTPException(detail="No Data Found", status_code=status.HTTP_404_NOT_FOUND)
    return db_data

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ShowUser)
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

@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
async def edit(id:int, request:CreateUser, db: Session = Depends(get_db)):
    db_data = db.query(User).filter(User.id==int(id))
    if not db_data.first():
        raise HTTPException(detail="No data Found", status_code=status.HTTP_400_BAD_REQUEST)
    db_data.update(request.dict())
    db.commit()
    return {'data':'Updated successfully'}

@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, db: Session = Depends(get_db)):
    db_blog = db.query(User).filter(User.id==int(id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.delete()
    db.commit()
    return {'data':'deleted successfully'}