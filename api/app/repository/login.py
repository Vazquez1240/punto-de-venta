from sqlalchemy.orm import Session
from app.db import models
from app.schemas import UpdatePassword
from fastapi import HTTPException,status
from app.hashing import Hash


def login_users(user,db:Session):
    useer = user.dict()
    print(user)
