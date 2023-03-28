from fastapi import APIRouter,Depends, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.schemas import SuperAdmin,ShowAdmin,UpdateAdmin
from app.repository import admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/obtener_admins",response_model=List[ShowAdmin],status_code=status.HTTP_200_OK)
def obtener_admins(db:Session = Depends(get_db)):
    support = admin.get_admins(db)
    return support

@router.post("/create_admin",status_code=status.HTTP_201_CREATED)
def create_admin(admiin:SuperAdmin,db:Session = Depends(get_db)):
    support = admin.create_admin(admiin,db)
    return support

@router.get("/{user_admin}",response_model=ShowAdmin)
def obtener_admin(user_admin:str,db:Session = Depends(get_db)):
    support = admin.get_admin(user_admin,db)
    return support

@router.delete("/{username_admin}")
def delete_admin(username_admin:str,db:Session = Depends(get_db)):
    support = admin.delete_admin(username_admin,db)
    return support


@router.patch("/{user_admin}")
def update_admin(user_admin:str,updateAdmin:UpdateAdmin,db:Session = Depends(get_db)):
    support = admin.update_admin(user_admin,db,updateAdmin)
    return support