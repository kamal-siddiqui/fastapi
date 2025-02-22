from fastapi import APIRouter, Depends, HTTPException, status
from dependency import get_db
from sqlalchemy.orm import Session
from model import User
from hashing import Hash
from datetime import timedelta
from JwtToken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not Found. Please check credentials.")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token":access_token, "token_type":"bearer"}

