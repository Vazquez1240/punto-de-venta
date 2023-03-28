from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException,status
from app.hashing import Hash

def get_users(db:Session):
    data = db.query(models.User).all()
    return data

def create_user(user,db:Session):
    useer = user.dict()
    try:
        new_user = models.User(
            name=useer["name"],
            surname=useer["surname"],
            username=useer["username"],
            password=Hash.hash_password(useer["password"]),
            number_phone=useer["number_phone"],
            mail=useer["mail"]
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User or mail already in use"
        )
    return {"Success":"User create whit exit!"}


def get_user(user_username,db:Session):
    useer = db.query(models.User).filter(models.User.username == user_username).first()
    if (not useer):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el usuario {user_username}"
        )
    return useer


def delete_user(user_username,db:Session):
    useer = db.query(models.User).filter(models.User.username == user_username)
    if (not useer.first()):
        return {"Error": f"El usuario con el username: {user_username} no existe"}
    useer.delete(synchronize_session=False)
    db.commit()
    return {"Exito":"Usuario eliminado correctamente"}


def update_user(user_username,db:Session,updateUser):
    useer = db.query(models.User).filter(models.User.username == user_username)
    if (not useer.first()):
        return {"Error": f"El usuario con el username: {user_username} no existe"}
    useer.update(updateUser.dict(exclude_unset=True))
    db.commit()
    return {"Exito":"Usuario actualizado correctamente"}