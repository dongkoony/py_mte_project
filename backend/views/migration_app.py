from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    # 로그인 로직 처리
    return {"message": "Logged in successfully"}

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(email: str = Form(...), password: str = Form(...)):
    # 회원가입 로직 처리
    return {"message": "Registered successfully"}

@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/ssh-connect")
def ssh_connect(host: str = Form(...), username: str = Form(...), password: str = Form(...), port: int = Form(22)):
    # SSH 접속 및 데이터 추출 로직 처리
    return {"message": "Data extracted successfully"}

@app.get("/download-template")
def download_template():
    # Terraform 템플릿 다운로드 로직 처리
    return {"message": "Template downloaded successfully"}

@app.get("/mypage")
def mypage(request: Request):
    return templates.TemplateResponse("mypage.html", {"request": request})
