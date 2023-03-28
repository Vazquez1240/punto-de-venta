from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException,status
from app.hashing import Hash

def get_admins(db:Session):
    data = db.query(models.SuperAdmin).all()
    return data

def create_admin(user_admin,db:Session):
    try:
        admiin = user_admin.dict()
        new_admin = models.SuperAdmin(
            name = admiin["name"],
            surname = admiin["surname"],
            username = admiin["username"],
            password = Hash.hash_password(admiin["password"]),
            number_phone = admiin["number_phone"],
            mail = admiin["mail"]
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or mail already in use"
        )
    return {"Success":"Admin create with exit!"}

def get_admin(user_admin, db:Session):
    admiin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == user_admin).first()
    if(not admiin):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username does not exist: {user_admin}"
        )
    return admiin


def delete_admin(user_admin, db:Session):
    admiin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == user_admin)
    if(not admiin.first()):
        return {"Error":f"El administrador con el username {user_admin} no existe"}
    admiin.delete(synchronize_session=False)
    db.commit()
    return {"Success":"Usuario eliminado correctamente"}


def update_admin(user_admin, db:Session,updateAdmin):
    admiin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == user_admin)
    if(not admiin.first()):
        return {"Error":f"The user whit username {user_admin} not exist"}
    admiin.update(updateAdmin.dict(exclude_unset=True))
    db.commit()
    return {"Success":"User actualizado correctamente"}

