from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
def read_root():
    return FileResponse('public/index.html')

@router.get("/login")
def read_login():
    return FileResponse('public/auth/login.html')

@router.get("/register")
def read_register():
    return FileResponse('public/auth/register.html')

@router.get("/menu")
def read_menu():
    return FileResponse('public/menu.html')