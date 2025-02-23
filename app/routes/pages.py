from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
def read_root():
    return FileResponse('public/static/index.html')

@router.get("/login")
def read_login():
    return FileResponse('public/static/auth/login.html')

@router.get("/register")
def read_register():
    return FileResponse('public/static/auth/register.html')

@router.get("/menu")
def read_menu():
    return FileResponse('public/static/menu.html')