from fastapi import FastAPI
import uvicorn
from app.routers import admin,user,auth,passrecovere,recovere_mail,login
from app.db.database import Base,engine
import tracemalloc
tracemalloc.start()

app = FastAPI()

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(passrecovere.router)
app.include_router(recovere_mail.router)
app.include_router(login.router)


if(__name__ == '__main__'):
    uvicorn.run("main:app",port=8000,reload=True)