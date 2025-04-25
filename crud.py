from sqlalchemy.orm import Session
from models import User, Skill, Project
from auth import hash_password
import models  # ✅ This works when running the app directly



def create_user(db: Session, user):
    db_user = User(name=user.name, email=user.email,
                   password=hash_password(user.password), role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
def delete_user(db: Session, user_id: int):
    # db.query(models.Skill).filter(models.Skill.owner_id == user_id).delete()
    db.query(models.Skill).filter(models.Skill.user_id == user_id).delete()

    db.query(models.Project).filter(models.Project.employee_id == user_id).delete()
    user = db.query(models.User).get(user_id)
    if user:
        db.delete(user)
        db.commit()


def add_skill(db: Session, skill, user_id):
    db_skill = Skill(name=skill.name, level=skill.level, user_id=user_id)
    db.add(db_skill)
    db.commit()
    return db_skill
def delete_skill(db: Session, skill_id: int):
    skill = db.query(Skill).get(skill_id)
    if skill:
        db.delete(skill)
        db.commit()

def approve_skill(db: Session, skill_id):
    skill = db.query(Skill).get(skill_id)
    skill.approved = True
    db.commit()

def get_approved_skills(db: Session):
    return db.query(Skill).filter(Skill.approved == True).all()

def assign_project(db: Session, project_name, skill_name, employee_id):
    db_project = Project(name=project_name, required_skill=skill_name, employee_id=employee_id)
    db.add(db_project)
    db.commit()
    return db_project

