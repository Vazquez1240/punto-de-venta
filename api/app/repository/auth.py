from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException,status
from datetime import datetime, timedelta
from app.hashing import Hash
from app.token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES

def auth_user(user,db:Session):

    useer = db.query(models.User).filter(models.User.username == user.username).first()
    admiin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == user.username).first()
    if(useer == None):
        if(admiin == None):
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe el usuario con el username: {user.username}"
            )
        if(Hash.verify_password(user.password,admiin.password) == False):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Password incorrect"
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    if(Hash.verify_password(user.password,useer.password) == False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password incorrect"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



def auth_email(user,password,db:Session):

    useer = db.query(models.User).filter(models.User.username == user).first()
    admiin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == user).first()
    if(useer == None):
        if(admiin == None):
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe el usuario con el username: {user}"
            )
        if(Hash.verify_password(password,admiin.password) == False):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Password incorrect"
            )
        return {"Succes":True}
    if(Hash.verify_password(password,useer.password) == False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password incorrect"
        )
    
    return {"Succes":True}


def auth_login(user,password,db:Session):
    useer = db.query(models.User).filter(models.User.username == user).first()
    admiin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == user).first()
    if(useer == None):
        if(admiin == None):
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe el usuario con el username: {user}"
            )
        if(Hash.verify_password(password,admiin.password) == False):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Password incorrect"
            )
        return {"Succes":True}
    if(Hash.verify_password(password,useer.password) == False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password incorrect"
        )
    
    return {"Succes":True}


def login_users(user,db:Session):
    usuario = user.dict()
    useer = db.query(models.User).filter(models.User.username == usuario["username"]).first()
    admiin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == usuario["username"]).first()
    
    if(useer == None):
        if(admiin == None):
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe el usuario con el username: {user}"
            )
        if(Hash.verify_password(usuario["password"],admiin.password) == False):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Password incorrect"
            )
        return {"Succes":True}
    if(Hash.verify_password(usuario["password"],useer.password) == False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password incorrect"
        )
    
    return {"Succes":True}