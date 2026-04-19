from fastapi import FastAPI, Request
from fastapi.responses import Response, PlainTextResponse
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
    return templates.TemplateResponse(request, "home.html")

@app.get("/about", include_in_schema=False)
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html")

@app.get("/services", include_in_schema=False)
async def services(request: Request):
    return templates.TemplateResponse(request, "services.html")

@app.get("/insurance", include_in_schema=False)
async def insurance(request: Request):
    return templates.TemplateResponse(request, "insurance.html")

@app.get("/new-patients", include_in_schema=False)
@app.get("/new_patients", include_in_schema=False)
async def new_patients(request: Request):
    return templates.TemplateResponse(request, "new_patients.html")

@app.get("/schedule", include_in_schema=False)
async def schedule(request: Request):
    return templates.TemplateResponse(request, "schedule.html")

@app.get("/pay-bill", include_in_schema=False)
async def pay_bill(request: Request):
    return templates.TemplateResponse(request, "pay_bill.html")

@app.get("/contact", include_in_schema=False)
async def contact(request: Request):
    return templates.TemplateResponse(request, "contact.html")

@app.get("/location", include_in_schema=False)
async def location(request: Request):
    return templates.TemplateResponse(request, "location.html")

@app.get("/privacy", include_in_schema=False)
async def privacy(request: Request):
    return templates.TemplateResponse(request, "privacy.html")

@app.get("/accessibility", include_in_schema=False)
async def accessibility(request: Request):
    return templates.TemplateResponse(request, "accessibility.html")

@app.get("/careers", include_in_schema=False)
async def careers(request: Request):
    return templates.TemplateResponse(request, "careers.html")

@app.get("/thanks", include_in_schema=False)
async def thanks(request: Request):
    return templates.TemplateResponse(request, "thanks.html")

@app.get("/financing", include_in_schema=False)
async def financing(request: Request):
    return templates.TemplateResponse(request, "financing.html")

# ── SITEMAP & ROBOTS ─────────────────────────────────────────────────────────
@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap_xml(request: Request):
    base = str(request.base_url).rstrip("/")
    urls = [
        "/", "/about", "/services", "/insurance", "/new-patients", "/schedule", "/pay-bill",
        "/careers", "/location", "/contact", "/privacy", "/accessibility", "/thanks", "/financing",
        "/static/forms/new-patient-packet.pdf",
        "/static/forms/hipaa-notice.pdf",
    ]
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "\n".join([f"<url><loc>{base}{path}</loc></url>" for path in urls]) +
        "\n</urlset>"
    )
    return Response(content=xml, media_type="application/xml")

@app.get("/robots.txt", include_in_schema=False)
async def robots_txt(request: Request):
    base = str(request.base_url).rstrip("/")
    txt = f"""User-agent: *
Allow: /

Sitemap: {base}/sitemap.xml
"""
    return PlainTextResponse(txt)
