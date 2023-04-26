from fastapi import FastAPI
import uvicorn
from app.routers import admin,user,auth,passrecovere,recovere_mail,logout,view_token
from app.db.database import Base,engine
import tracemalloc
from fastapi.middleware.cors import CORSMiddleware


tracemalloc.start()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500"
]

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(passrecovere.router)
app.include_router(recovere_mail.router)
app.include_router(logout.router)
app.include_router(view_token.router)


#if(__name__ == '__main__'):
#    uvicorn.run("main:app",port=8000,reload=True)