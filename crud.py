from sqlalchemy.orm import Session
import models
from datetime import datetime
import uuid
from auth import hash_password

# -------------------------
# User CRUD Operations
# -------------------------

def create_user(db: Session, user):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user_role(db: Session, user_id: int, role: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.role = role
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).get(user_id)
    if user:
        db.delete(user)
        db.commit()

# -------------------------
# Skill CRUD Operations
# -------------------------

def add_skill(db: Session, skill, user_id: int):
    db_skill = models.Skill(
        name=skill.name,
        level=skill.level,
        user_id=user_id
    )
    db.add(db_skill)
    db.commit()
    return db_skill

def get_skill_by_id(db: Session, skill_id: int):
    return db.query(models.Skill).filter(models.Skill.id == skill_id).first()

def get_skills_by_user_id(db: Session, user_id: int):
    return db.query(models.Skill).filter(models.Skill.user_id == user_id).all()

def delete_skill(db: Session, skill_id: int):
    skill = db.query(models.Skill).get(skill_id)
    if skill:
        db.delete(skill)
        db.commit()

def approve_skill(db: Session, skill_id: int):
    skill = db.query(models.Skill).get(skill_id)
    if skill:
        skill.approved = True
        db.commit()

def get_approved_skills(db: Session):
    return db.query(models.Skill).filter(models.Skill.approved == True).all()

# -------------------------
# Project CRUD Operations
# -------------------------

def assign_project(db: Session, project_name: str, skill_name: str, employee_id: int):
    db_project = models.Project(
        name=project_name,
        skill_name=skill_name,
        employee_id=employee_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project_by_id(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects_by_employee_id(db: Session, employee_id: int):
    return db.query(models.Project).filter(models.Project.employee_id == employee_id).all()

def get_projects_by_skill(db: Session, skill_name: str):
    return db.query(models.Project).filter(models.Project.skill_name == skill_name).all()

# -------------------------
# Password Reset Token Operations
# -------------------------

def create_password_reset_token(db: Session, user, reset_token: str, expiration_time: datetime):
    reset_token_obj = models.PasswordResetToken(
        user_id=user.id,
        token=reset_token,
        expiration_time=expiration_time
    )
    db.add(reset_token_obj)
    db.commit()
    db.refresh(reset_token_obj)
    return reset_token_obj

def get_password_reset_token(db: Session, token: str):
    return db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()

def delete_password_reset_token(db: Session, token: str):
    reset_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()
    if reset_token:
        db.delete(reset_token)
        db.commit()

def is_token_expired(expiration_time: datetime):
    return expiration_time < datetime.utcnow()

# -------------------------
# Helper Methods
# -------------------------

def hash_password(password: str):
    # This should implement password hashing logic (e.g., using bcrypt or similar).
    # Example:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

