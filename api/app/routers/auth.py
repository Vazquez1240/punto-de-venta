from fastapi import APIRouter,Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List
from app.schemas import Login
from app.repository import auth
from fastapi.security import OAuth2PasswordRequestForm

active_tokens = {}
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/",status_code=status.HTTP_200_OK)
def login(login:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    print(login.grant_type)
    support = auth.auth_user(login,db)

    active_tokens[f"tokens{login.username}"] = support["access_token"]

    #"tokens":support["access_token"]

    return support