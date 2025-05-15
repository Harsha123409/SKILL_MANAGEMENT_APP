import uuid
from fastapi import FastAPI, Request, Form, Depends, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas
from auth import verify_password, hash_password
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# skill_app/main.py or wherever your app is initialized
import logging
import watchtower

# Create logger
logger = logging.getLogger("skill_app_logger")
logger.setLevel(logging.INFO)

# Add CloudWatch handler
logger.addHandler(watchtower.CloudWatchLogHandler(log_group="SkillAppLogs"))

# Example log
logger.info("Skill app has started and connected to CloudWatch successfully.")


import boto3

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# Send a custom metric
cloudwatch.put_metric_data(
    Namespace='SkillAppMetrics',  # Custom namespace
    MetricData=[  # This should be a list of metric data dictionaries
        {
            'MetricName': 'UserLogins',  # Metric name
            'Value': 1,  # Metric value
            'Dimensions': [{'Name': 'AppName', 'Value': 'skill_app'}]

            'Unit': 'Count'
        },
    ]
)



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# --------------------------------------------------------
# ---------------------------------------------------------
# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




from datetime import datetime  # ✅ Import datetime

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "datetime": datetime  # ✅ Pass datetime to the template
    })


# ----------------------------- 
# Forgot Password Routes 
# -----------------------------

# Step 1: Render Forgot Password form
@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

# Step 2: Handle Forgot Password form submission (sending the email with reset link)
@app.post("/forgot-password")
@app.post("/forgot-password")
async def forgot_password_request(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    email: str = Form(...)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        # Generate reset token and expiration
        reset_token = str(uuid.uuid4())
        expiration_time = datetime.utcnow() + timedelta(hours=1)

        # ✅ Save token to DB
        crud.create_password_reset_token(db, user, reset_token, expiration_time)

        # Build and send reset link
        reset_link = f"http://127.0.0.1:8000/reset-password/{reset_token}"
        background_tasks.add_task(send_password_reset_email, email, reset_link)

        return RedirectResponse(url="/login", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Email not found")

# Step 5: Send password reset email
def send_password_reset_email(email: str, reset_link: str):
    # Set up the server and the message
    sender_email = "jharsha5533@gmail.com"
    sender_password = "sjih qidv nbhn dnlo"
    subject = "Password Reset Request"

    # Create the email content
    body = f"Click the following link to reset your password: {reset_link}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email via SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())

# Step 6: Password reset form (after clicking the link)
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi import Request, Depends

from datetime import datetime
from fastapi import Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

@app.get("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password_form(request: Request, token: str, db: Session = Depends(get_db)):
    reset_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()

    if reset_token and reset_token.expiration_time > datetime.now():
        return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})
    else:
        return templates.TemplateResponse("reset_password.html", {"request": request, "token": token, "msg": "Invalid or expired token"})


@app.post("/reset-password/{token}")
async def reset_password(token: str, new_password: str = Form(...), db: Session = Depends(get_db)):
    # ✅ DO NOT manually recreate db session
    reset_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()

    if not reset_token:
        raise HTTPException(status_code=400, detail="Invalid token.")
    
    if reset_token.expiration_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token has expired.")
    
    user = db.query(models.User).filter(models.User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")

    user.password = hash_password(new_password)
    db.delete(reset_token)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)
from fastapi import Form, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth import verify_password  # Assuming you have the verify_password utility
from fastapi import Request
# -------------------------
# Admin Registration Routes
# -------------------------
@app.get("/admin/register", response_class=HTMLResponse)
def admin_register_form(request: Request):
    return templates.TemplateResponse("admin_register.html", {"request": request})

@app.post("/admin/register")
def admin_register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("admin_register.html", {
            "request": request,
            "msg": "Email already registered"
        })

    hashed_pw = hash_password(password)
    user = models.User(name=name, email=email, password=hashed_pw, role="Admin")
    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(url="/admin/login", status_code=303)

# ----------------------
# Admin Login Routes
# ----------------------
@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_form(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
def admin_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return templates.TemplateResponse("admin_login.html", {
            "request": request,
            "msg": "User not found"
        })

    if user.role != "Admin":
        return templates.TemplateResponse("admin_login.html", {
            "request": request,
            "msg": "Not an admin"
        })

    if not verify_password(password, user.password):
        return templates.TemplateResponse("admin_login.html", {
            "request": request,
            "msg": "Invalid password"
        })

    return RedirectResponse(url=f"/admin/{user.id}", status_code=303)

# ----------------------
# Admin Dashboard Route
# ----------------------
@app.get("/admin/{admin_id}", response_class=HTMLResponse)
def admin_dashboard(request: Request, admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.User).get(admin_id)
    if not admin or admin.role != "Admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    users = db.query(models.User).all()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "admin_id": admin_id,
        "users": users
    })
# Admin Login Route
@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_form(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Find the user with the provided email (checking if it's an admin)
    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify if the user is an admin and check the password
    if user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not an Admin")

    # Verify the password
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Admin is authenticated, redirect to admin dashboard
    return RedirectResponse(url=f"/admin/{user.id}", status_code=302)
# ----------------------------- 
# Employee Registration Routes 
# ----------------------------- 
# -----------------------------
# User Registration Route
# -----------------------------
@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if the email is already registered
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "msg": "Email already registered"
        })

    # Hash the password before saving
    hashed_pw = hash_password(password)
    user = models.User(name=name, email=email, password=hashed_pw, role="User")  # Default role is User
    db.add(user)
    db.commit()
    db.refresh(user)

    # Redirect to the login page after successful registration
    return RedirectResponse(url="/login", status_code=303)
from fastapi import Form, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

@app.post("/reset-password/{token}")
async def reset_password(
    token: str,
    new_password: str = Form(...),
    db: Session = Depends(get_db)  # Use FastAPI's dependency injection properly
):
    # Fetch the token from the database
    reset_token = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token == token
    ).first()

    if not reset_token:
        raise HTTPException(status_code=400, detail="Invalid token.")

    if reset_token.expiration_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token has expired.")

    # Find the associated user
    user = db.query(models.User).filter(models.User.id == reset_token.user_id).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found.")

    # Update and hash the new password
    user.password = hash_password(new_password)

    # Delete token and commit changes
    db.delete(reset_token)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)

# ------------------------ 
# Employee Login Routes 
# ------------------------ 
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email)
    if user and verify_password(password, user.password):
        if user.role == "Manager":
            return RedirectResponse(url=f"/manager/{user.id}", status_code=302)
        elif user.role == "Admin":
            return RedirectResponse(url=f"/admin/{user.id}", status_code=302)
        return RedirectResponse(url=f"/dashboard/{user.id}", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid login"})

# ----------------------------- 
# Admin Dashboard - Manage Users 
# ----------------------------- 
@app.get("/admin/{admin_id}", response_class=HTMLResponse)
def admin_dashboard(request: Request, admin_id: int, db: Session = Depends(get_db)):
    # Only admin should have access to this route
    user = db.query(models.User).get(admin_id)
    if user and user.role != "Admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Not an Admin")
    
    users = db.query(models.User).all()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "admin_id": admin_id,
        "users": users
    })

@app.post("/admin/assign_role")
def assign_role(
    user_id: int = Form(...),
    role: str = Form(...),
    admin_id: int = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    db.commit()
    return RedirectResponse(url=f"/admin/{admin_id}", status_code=302)

# ----------------------------- 
# Employee Dashboard & Skills 
# ----------------------------- 
@app.get("/dashboard/{user_id}", response_class=HTMLResponse)
def dashboard(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/skills/add", response_class=HTMLResponse)
def add_skill_form(request: Request, user_id: int):
    return templates.TemplateResponse("add_skill.html", {"request": request, "user_id": user_id})

@app.post("/skills/add")
def add_skill(
    user_id: int = Form(...),
    name: str = Form(...),
    level: str = Form(...),
    db: Session = Depends(get_db)
):
    skill = schemas.SkillCreate(name=name, level=level)
    crud.add_skill(db, skill, user_id)
    return RedirectResponse(url=f"/dashboard/{user_id}", status_code=302)

@app.post("/skills/delete")
def delete_skill(skill_id: int = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    crud.delete_skill(db, skill_id)
    return RedirectResponse(url=f"/dashboard/{user_id}", status_code=302)

# -----------------------------------
# Manager Dashboard - Review Skills
# -----------------------------------
@app.get("/manager/{manager_id}", response_class=HTMLResponse)
def manager_dashboard(request: Request, manager_id: int, db: Session = Depends(get_db)):
    employees = db.query(models.User).filter(models.User.role == "Employee").all()
    return templates.TemplateResponse("manager_dashboard.html", {
        "request": request,
        "manager_id": manager_id,
        "employees": employees
    })

@app.post("/employee/delete")
def delete_employee(
    employee_id: int = Form(...),
    manager_id: int = Form(...),
    db: Session = Depends(get_db)
):
    crud.delete_user(db, employee_id)
    return RedirectResponse(url=f"/manager/{manager_id}", status_code=302)

@app.post("/skills/approve")
def approve_skill(skill_id: int = Form(...), manager_id: int = Form(...), db: Session = Depends(get_db)):
    crud.approve_skill(db, skill_id)
    return RedirectResponse(url=f"/manager/{manager_id}", status_code=302)

# # ----------------------------- 
# # Project Allocation by Manager
# # ----------------------------- 
@app.get("/projects/allocate", response_class=HTMLResponse)
def project_allocate_form(request: Request, db: Session = Depends(get_db)):
    approved_skills = crud.get_approved_skills(db)  # Fetch approved skills
    users = db.query(models.User).all()  # Fetch all employees (users)
    
    return templates.TemplateResponse("allocate_project.html", {
        "request": request,
        "skills": approved_skills,
        "users": users  # Pass users to the template
    })

from fastapi import Form
from sqlalchemy.orm import Session

@app.post("/projects/allocate")
def assign_project(
    project_name: str = Form(...),
    skill_name: str = Form(...),
    employee_id: int = Form(...),
    db: Session = Depends(get_db)
):
    # Fetch the skill object based on the skill_name
    skill = db.query(models.Skill).filter(models.Skill.name == skill_name).first()

    if skill:
        db_project = models.Project(
            name=project_name,
            skill_id=skill.id,  # Use skill_id instead of skill_name
            employee_id=employee_id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
    else:
        raise HTTPException(status_code=404, detail="Skill not found")

    return RedirectResponse(url="/projects/view", status_code=303)

@app.get("/projects/view", response_class=HTMLResponse)
def view_projects(request: Request, db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    users = db.query(models.User).all()
    user_dict = {user.id: user.name for user in users}

    return templates.TemplateResponse("view_projects.html", {
        "request": request,
        "projects": projects,
        "user_dict": user_dict
    })


# ----------------------------- 
# Export Skills to Excel 
# ----------------------------- 
@app.get("/skills/export", response_class=HTMLResponse)
def export_form(request: Request):
    return templates.TemplateResponse("export.html", {"request": request})

@app.post("/skills/export")
def export_skills_to_excel(approved_only: bool = Form(False), db: Session = Depends(get_db)):
    query = db.query(models.Skill)
    if approved_only:
        query = query.filter(models.Skill.approved == True)
    
    skills = query.all()
    data = [({
        "Employee": s.owner.name,
        "Email": s.owner.email,
        "Skill": s.name,
        "Level": s.level,
        "Approved": s.approved
    }) for s in skills]
    
    df = pd.DataFrame(data)
    file_path = "skills_export.xlsx"
    df.to_excel(file_path, index=False)
    
    return FileResponse(file_path, filename="skills_export.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
