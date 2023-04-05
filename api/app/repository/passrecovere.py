from sqlalchemy.orm import Session
from app.db import models
from app.schemas import UpdatePassword
from fastapi import HTTPException,status
from app.hashing import Hash
from app.send_email import send_email
import tracemalloc
tracemalloc.start()


def recovere_password(username,updatePassword ,db:Session):
    support_admin = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == username)
    support_user = db.query(models.User).filter(models.User.username == username)
    if(support_user.first() is None):
        if(support_admin.first() is None):
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"username not exist"
        )
        query = db.query(models.SuperAdmin).filter(models.SuperAdmin.username == username).first()
        
        new_password = updatePassword.dict()
        
        haseo = Hash.hash_password(new_password["password"])

        password = UpdatePassword(password=haseo)

        print(query.mail)
        
        support_admin.update(password.dict(exclude_unset=True))
        db.commit()
        
        return {"Success":"password actualizada correctamente"}
    

    new_password = updatePassword.dict()

    haseo = Hash.hash_password(new_password["password"])

    password = UpdatePassword(password=haseo)
    
    support_user.update(password.dict(exclude_unset=True))
    
    print(support_user)
    db.commit()
    return {"Success":"password actualizada correctamente"} 