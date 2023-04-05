from fastapi import APIRouter,Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import UpdateMail
from app.db import models
from app.repository import auth
from app.repository import recovere_mail


router = APIRouter(
    prefix="/recoverer-email",
    tags=["Recoverer-Email"]
)

@router.patch("/{username}")
def recover_mail(username:str, password:str,updateMail:UpdateMail,db:Session = Depends(get_db)):
    support = auth.auth_email(username,password,db)
    if(support):
        support = recovere_mail.recovere_mail(username,updateMail,db)
        return support