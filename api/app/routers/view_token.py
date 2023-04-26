from fastapi import APIRouter,Depends, status
from app.routers import auth


router = APIRouter(
    prefix="/view_token",
    tags=["View Token"]
)

@router.post("/")
def view():
    a = auth.active_tokens
    return a