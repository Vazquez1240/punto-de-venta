from fastapi import APIRouter,Depends, status
from app.token import SECRET_KEY,ALGORITHM
from app.repository.logout import close_session

router = APIRouter(
    prefix="/logout",
    tags=["Logout"]
)

@router.delete("/",status_code=status.HTTP_202_ACCEPTED)
def logout(token:str,username:str):
    
    support = close_session(token,username,SECRET_KEY,ALGORITHM)
    return support