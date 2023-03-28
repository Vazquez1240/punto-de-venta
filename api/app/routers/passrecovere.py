from fastapi import APIRouter,Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List
from app.schemas import UpdatePassword
from app.repository import passrecovere
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/recoverer-password",
    tags=["Recoverer-Password"]
)

@router.patch("/{username}")
def recover_password(username:str,updatePassword:UpdatePassword,db:Session = Depends(get_db)):
    support = passrecovere.recovere_password(username,updatePassword,db)
    return support