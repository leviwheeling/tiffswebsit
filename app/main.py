from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import logging

# ── LOGGING ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# ── FASTAPI / JINJA SETUP ────────────────────────────────────────────────────
app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["now"] = datetime.now     # enables {{ now().year }}

# ── PAGE ROUTES ──────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", include_in_schema=False)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/services", include_in_schema=False)
async def services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})

@app.get("/new-patients", include_in_schema=False)
@app.get("/new_patients", include_in_schema=False)
async def new_patients(request: Request):
    return templates.TemplateResponse("new_patients.html", {"request": request})

@app.get("/contact", include_in_schema=False)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/location", include_in_schema=False)
async def location(request: Request):
    return templates.TemplateResponse("location.html", {"request": request})

@app.get("/privacy", include_in_schema=False)
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})
