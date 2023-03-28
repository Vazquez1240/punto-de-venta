from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime
from app.hashing import Hash

class User(BaseModel):
    name:str
    surname:str
    username:str
    password:str
    number_phone:str
    mail:str
    rango:str
    creation:datetime = datetime.now()

class SuperAdmin(BaseModel):
    name:str
    surname:str
    username:str
    password:str
    number_phone:str
    mail:str
    rango: str = 'admin'
    creation:datetime = datetime.now()


class ShowUser(BaseModel):
    name:str
    surname:str
    username:str
    mail:str
    class Config():
        orm_mode = True

class ShowAdmin(BaseModel):
    name:str
    password:str
    surname:str
    username:str
    mail:str
    number_phone:str
    class Config():
        orm_mode = True


class UpdateUser(BaseModel):
    username:str = None
    password:str = None
    mail:str = None
    number_phone:str = None
    rango:str = None

class UpdateAdmin(BaseModel):
    username:str = None
    password:str = None
    mail:str = None
    number_phone:str = None

class UpdatePassword(BaseModel):
    password:str
    


class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None