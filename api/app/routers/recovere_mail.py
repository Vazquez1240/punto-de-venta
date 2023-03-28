from fastapi import APIRouter,Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List
from app.schemas import UpdateMail
from app.repository import passrecovere
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/recoverer-email",
    tags=["Recoverer-Email"]
)

@router.patch("/{username}/{password}")
def recover_mail(username:str, password:str,updateMail:UpdateMail,db:Session = Depends(get_db)):
    return {"Esto es":f"{username}{password}"}