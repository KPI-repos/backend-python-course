from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    return FileResponse('public/index.html')
@app.get("/login")
def read_root():
    return FileResponse('public/auth/login.html')
@app.get("/register")
def read_root():
    return FileResponse('public/auth/register.html')
@app.get("/menu")
def read_root():
    return FileResponse('public/menu.html')