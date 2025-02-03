from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session
from model import User
from passlib.context import CryptContext

pass_cnt = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def all_user(db: Session):
    db_data = db.query(User).all()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    return db_data

async def user(id:int, db: Session):
    db_data = db.query(User).filter(User.id==id).first()
    if not db_data:
        raise HTTPException(detail="No Data Found", status_code=status.HTTP_404_NOT_FOUND)
    return db_data

async def create_user(request, db: Session):
    db_data = User(
        name = request.name,
        email = request.email,
        password = pass_cnt.hash(request.password)
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

async def edit(id:int, request, db: Session):
    db_data = db.query(User).filter(User.id==int(id))
    if not db_data.first():
        raise HTTPException(detail="No data Found", status_code=status.HTTP_400_BAD_REQUEST)
    db_data.update(request.dict())
    db.commit()
    return {'data':'Updated successfully'}

async def delete(id: int, db: Session):
    db_blog = db.query(User).filter(User.id==int(id))
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Records not found')
    db_blog.delete()
    db.commit()
    return {'data':'deleted successfully'}