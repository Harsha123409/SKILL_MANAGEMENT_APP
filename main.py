from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas
from auth import verify_password
import pandas as pd

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Employee Registration Routes
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
    role: str = Form("Employee"),
    db: Session = Depends(get_db)
):
    user = schemas.UserCreate(name=name, email=email, password=password, role=role)
    crud.create_user(db, user)
    return RedirectResponse(url="/login", status_code=302)


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
        return RedirectResponse(url=f"/dashboard/{user.id}", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid login"})


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


# -----------------------------
# Project Allocation by Manager
# -----------------------------
@app.get("/projects/allocate", response_class=HTMLResponse)
def project_allocate_form(request: Request, db: Session = Depends(get_db)):
    approved_skills = crud.get_approved_skills(db)
    return templates.TemplateResponse("allocate_project.html", {
        "request": request,
        "skills": approved_skills
    })

@app.post("/projects/allocate")
def assign_project(
    project_name: str = Form(...),
    skill_name: str = Form(...),
    employee_id: int = Form(...),
    db: Session = Depends(get_db)
):
    crud.assign_project(db, project_name, skill_name, employee_id)
    return RedirectResponse(url="/projects/allocate", status_code=302)
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
    data = [{
        "Employee": s.owner.name,
        "Email": s.owner.email,
        "Skill": s.name,
        "Level": s.level,
        "Approved": s.approved
    } for s in skills]
    
    df = pd.DataFrame(data)
    file_path = "skills_export.xlsx"
    df.to_excel(file_path, index=False)
    
    return FileResponse(file_path, filename="skills_export.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
