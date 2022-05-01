from flask import Flask


app = Flask(__name__)

from app import routes



# from fastapi import FastAPI, Request, Form
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
#
# app = FastAPI()
#
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates/")
#
# @app.get("/login")
# def login_get(request: Request):
#     return templates.TemplateResponse('login.html', context={ 'request': request })
#
#
# @app.post("/login")
# def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
#     print(f'{username}')
#     print(f'{password}')
#     return templates.TemplateResponse('login.html', context={ 'request': request })
#
# @app.get("/otp")
# def otp_get(request: Request):
#     return templates.TemplateResponse('otp.html', context={ 'request': request })
#
# @app.get("/email")
# def otp_get(request: Request):
#     return templates.TemplateResponse('email.html', context={ 'request': request })
