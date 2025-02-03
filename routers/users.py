from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schema import CreateUser, ShowUser
from dependency import get_db
from repository import users

router = APIRouter(
    tags=["User"],
    prefix='/user'
)

@router.get('/get', status_code=status.HTTP_200_OK, response_model=List[ShowUser])
async def all_user(db: Session = Depends(get_db)):
    res = await users.all_user(db)
    return res

@router.get('/get/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser)
async def get(id:int, db: Session = Depends(get_db)):
    res = await users.user(id, db)
    return res

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create(request:CreateUser, db: Session = Depends(get_db)):
    res = await users.create_user(request, db)
    return res

@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
async def edit(id:int, request:CreateUser, db: Session = Depends(get_db)):
    res = await users.edit(id, request, db)
    return res

@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, db: Session = Depends(get_db)):
    res = await users.delete(id, db)
    return res