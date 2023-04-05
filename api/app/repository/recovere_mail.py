from sqlalchemy.orm import Session
from app.db import models
from app.schemas import UpdatePassword
from fastapi import HTTPException,status

def recovere_mail(username, updateEmail ,db:Session):
    support_user = db.query(models.User).filter(models.User.username == username)
    support_admin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == username)
    if(support_user.first() is None):
        if(support_admin.first() is None):
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"username not exist"
        )
        support_admin.update(updateEmail.dict(exclude_unset=True))
        db.commit()
        return {"Success":"Email actualizado correctamente"}
    
    support_user.update(updateEmail.dict(exclude_unset=True))
    db.commit()
    return {"Success":"Email actualizado correctamente"}
