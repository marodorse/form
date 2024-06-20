from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import re
import bleach  # Import bleach for HTML sanitization

from database import SessionLocal, init_db, Contact

# Create FastAPI application instance
app = FastAPI()

# Setup Jinja2Templates with templates directory
templates = Jinja2Templates(directory="templates")

# Initialize the database when the application starts
init_db()

# Dependency function to get a database session
def get_db():
    """
    Dependency function to retrieve a SQLAlchemy database session.
    This function ensures the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

HONEYPOT_FIELD = "website"

# Maximum length for input fields
MAX_FIELD_LENGTH = 100

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    """
    GET endpoint to render the HTML form page for submitting contact information.

    Args:
        request (Request): FastAPI Request object.

    Returns:
        TemplateResponse: Rendered form.html template with initial values and no errors.
    """
    return templates.TemplateResponse("form.html", {"request": request, "errors": {}, "first_name": "", "last_name": "", "email": "", "continent": "", "message": "", "gender": "", "subject": ""})

@app.post("/", response_class=HTMLResponse)
async def process_form(
    request: Request,
    first_name: str = Form(..., max_length=MAX_FIELD_LENGTH),  # Required fields + length limitation
    last_name: str = Form(..., max_length=MAX_FIELD_LENGTH),   # Required fields + length limitation
    email: str = Form(..., max_length=MAX_FIELD_LENGTH),       # Required fields + length limitation
    continent: str = Form(..., max_length=MAX_FIELD_LENGTH),   # Required fields + length limitation
    message: str = Form(..., max_length=MAX_FIELD_LENGTH),     # Required fields + length limitation
    gender: str = Form(...),      # Required fields + Dropdown validations
    subject: str = Form("Others"),  # Dropdown validations
    website: str = Form(None),
    db: Session = Depends(get_db)
):
    # Sanitize inputs to remove potentially dangerous characters
    first_name = re.sub(r"[<>]", "", first_name)
    last_name = re.sub(r"[<>]", "", last_name)
    email = re.sub(r"[<>]", "", email)
    continent = re.sub(r"[<>]", "", continent)
    message = re.sub(r"[<>]", "", message)

    # Validate required fields and format
    errors = {}

    if not first_name.strip():
        errors["first_name"] = "First name is required"

    if not last_name.strip():
        errors["last_name"] = "Last name is required"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors["email"] = "Invalid email"

    if not continent.strip():
        errors["continent"] = "Continent is required"

    if not message.strip():
        errors["message"] = "Message is required"

    if gender not in ["P", "O"]:
        errors["gender"] = "Invalid gender"

    if subject not in ["Repair", "Order", "Other"]:
        errors["subject"] = "Invalid subject"

    # Check for honeypot field (website) to detect spam
    if website:
        errors["message"] = "Spam detected"
        return templates.TemplateResponse("errors.html", {"request": request, "errors": errors})

    if errors:
        # Return the form page with validation errors
        return templates.TemplateResponse("form.html", {
            "request": request,
            "errors": errors,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "continent": continent,
            "message": message,
            "gender": gender,
            "subject": subject
        })

    # Save valid form data to the database
    try:
        # Parameterized queries
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            continent=continent,
            message=message,
            gender=gender,
            subject=subject
        )
        db.add(contact)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save contact information.")

    # Redirect to thank_you page with submitted data
    return templates.TemplateResponse("thank_you.html", {
        "request": request,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "continent": continent,
        "message": message,
        "gender": gender,
        "subject": subject
    })

if __name__ == "__main__":
    # Run the FastAPI application using Uvicorn server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
