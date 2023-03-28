from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime
from datetime import datetime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship


'''
class User(BaseModel):
    name:str
    surname:str
    username:str
    password:str
    number_phone:str
    mail:str
    rango:str
'''
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,nullable=False)
    surname = Column(String,nullable=False)
    username = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    number_phone = Column(String,nullable=False)
    mail = Column(String,nullable=False, unique=True)
    rango = Column(String,nullable=False,default="user")
    creation = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    sale = relationship("SaleUser",backref="users",cascade="delete,merge")

'''
class SuperAdmin(BaseModel):
    name:str
    surname:str
    username:str
    password:str
    number_phone:str
    mail:str
    rango:str
    creation:datetime = datetime.now()'''

class SuperAdmin(Base):
    __tablename__ = "superadmin"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    number_phone = Column(String, nullable=False)
    mail = Column(String, nullable=False, unique=True)
    rango = Column(String,nullable=False,default="admin")
    creation = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    sale_admin = relationship("SaleAdmin",backref="superadmin",cascade="delete,merge")

class SaleAdmin(Base):
    __tablename__ = "salesAdmin"
    id = Column(Integer,primary_key=True,autoincrement=True)
    username_id = Column(Integer,ForeignKey("superadmin.id",ondelete="CASCADE"))
    venta = Column(Integer)
    ventas_productos = Column(Integer)

class SaleUser(Base):
    __tablename__ = "salesUser"
    id = Column(Integer,primary_key=True,autoincrement=True)
    username_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    venta = Column(Integer)
    ventas_productos = Column(Integer)
