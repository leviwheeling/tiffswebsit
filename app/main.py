from fastapi import FastAPI, Request, Form, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from datetime import datetime
import os
import logging

# -----------------------------------------------------------------------------
# Environment & Logging
# -----------------------------------------------------------------------------
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "YOUR_SENDGRID_KEY_HERE")
MAIL_TO = os.getenv("MAIL_TO", "duncanfamilydentistry@gmail.com")
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@duncanfamilydentistry.com")

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# -----------------------------------------------------------------------------
# FastAPI app & Jinja environment
# -----------------------------------------------------------------------------
app = FastAPI(title="Duncan Family Dentistry", docs_url=None, redoc_url=None)

# Serve CSS/JS/images/PDFs from one origin
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
# Make `now()` available in all templates so {{ now().year }} works
templates.env.globals["now"] = datetime.now

# -----------------------------------------------------------------------------
# Pydantic schema for contact form
# -----------------------------------------------------------------------------
class ContactPayload(BaseModel):
    name: str
    phone: str
    email: EmailStr
    preferred_date: str | None = None
    message: str | None = None

# -----------------------------------------------------------------------------
# Page routes
# -----------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/contact", include_in_schema=False)
async def contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

# Shallow stubs for the rest so nav links don’t 404
for _p in ["about", "services", "new_patients", "gallery", "testimonials", "privacy"]:
    route = f"/{_p}"

    @app.get(route, include_in_schema=False)  # type: ignore
    async def _page(request: Request, _tpl=_p):  # capture value via default arg
        return templates.TemplateResponse(f"{_tpl}.html", {"request": request})

# -----------------------------------------------------------------------------
# API route – contact form to SendGrid (or console in dev)
# -----------------------------------------------------------------------------
@app.post("/api/contact", response_class=JSONResponse, include_in_schema=False)
async def submit_contact(payload: ContactPayload):
    """Handle contact form submission"""
    logging.info("Contact form received: %s", payload.dict())

    if SENDGRID_API_KEY == "YOUR_SENDGRID_KEY_HERE":
        logging.warning("SendGrid key missing – message logged but not emailed.")
        return {"success": True, "message": "Thank you! We will contact you soon."}

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        content = [
            f"New patient inquiry from {payload.name}",
            f"Phone: {payload.phone}",
            f"Email: {payload.email}",
            f"Preferred Date: {payload.preferred_date or 'N/A'}",
            "", payload.message or "(no message)"
        ]
        email = Mail(
            from_email=MAIL_FROM,
            to_emails=MAIL_TO,
            subject="Website Contact Form Submission",
            plain_text_content="\n".join(content)
        )
        sg.send(email)
        return {"success": True, "message": "Thank you! We will contact you soon."}
    except Exception as exc:
        logging.error("SendGrid error: %s", exc)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"success": False, "message": "There was an error sending your message."})
