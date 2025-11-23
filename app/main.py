import os
import segno
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from shortuuid import uuid
from .database import database
from .models import qrs
from . import crud

# Initialize app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_qr(request: Request, url: str = Form(...), title: str = Form(None)):
    short_code = uuid()[:8]
    qr = segno.make(url)
    qr_path = f"static/qr/{short_code}.png"
    os.makedirs("static/qr", exist_ok=True)
    qr.save(qr_path, scale=10)
    
    await crud.create_qr(short_code=short_code, url=url, title=title or "My QR")
    
    full_url = str(request.url_for('redirect', short_code=short_code))
    qr_url = f"{request.base_url}static/qr/{short_code}.png"
    
    return templates.TemplateResponse("created.html", {
        "request": request,
        "short_url": full_url,
        "qr_image": qr_url,
        "title": title or "My QR Code"
    })

@app.get("/{short_code}", name="redirect")
async def redirect(short_code: str, request: Request):
    client_ip = request.client.host
    qr = await crud.get_qr_by_code(short_code)
    if not qr:
        raise HTTPException(404)
    
    # Simple unique click detection using IP (you can improve with cookies)
    await crud.increment_clicks(short_code, client_ip)
    return RedirectResponse(qr.url)

@app.get("/stats/{short_code}", response_class=HTMLResponse)
async def stats(request: Request, short_code: str):
    qr = await crud.get_qr_by_code(short_code)
    if not qr:
        raise HTTPException(404)
    return templates.TemplateResponse("stats.html", {
        "request": request,
        "qr": qr,
        "qr_image": f"{request.base_url}static/qr/{short_code}.png"
    })