from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from datetime import datetime
import os, logging

# ── ENV & LOGGING ────────────────────────────────────────────────────────────
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "YOUR_SENDGRID_KEY_HERE")
MAIL_TO          = os.getenv("MAIL_TO", "duncanfamilydentistry@gmail.com")
MAIL_FROM        = os.getenv("MAIL_FROM", "noreply@duncanfamilydentistry.com")

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# ── FASTAPI / JINJA SETUP ────────────────────────────────────────────────────
app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["now"] = datetime.now     # enables {{ now().year }}

# ── DATA MODELS ──────────────────────────────────────────────────────────────
class ContactPayload(BaseModel):
    name: str
    phone: str
    email: EmailStr
    preferred_date: str | None = None
    message: str | None = None

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
@app.get("/new_patients", include_in_schema=False)   # handles dash & underscore
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

# ── API ROUTE ────────────────────────────────────────────────────────────────
@app.post("/api/contact", response_class=JSONResponse, include_in_schema=False)
async def submit_contact(payload: ContactPayload):
    """Send contact form via SendGrid or just log during dev."""
    logging.info("Contact form: %s", payload.dict())

    # Dev / no-email fallback
    if SENDGRID_API_KEY == "YOUR_SENDGRID_KEY_HERE":
        return {"success": True, "message": "Thank you! We will contact you soon."}

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        body = "\n".join([
            f"New inquiry from {payload.name}",
            f"Phone: {payload.phone}",
            f"Email: {payload.email}",
            f"Preferred Date: {payload.preferred_date or 'N/A'}",
            "",
            payload.message or "(no message)"
        ])

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(Mail(from_email=MAIL_FROM,
                     to_emails=MAIL_TO,
                     subject="Website Contact",
                     plain_text_content=body))

        return {"success": True, "message": "Thank you! We will contact you soon."}

    except Exception as exc:
        logging.error("SendGrid error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False,
                     "message": "There was an error sending your message."}
        )
