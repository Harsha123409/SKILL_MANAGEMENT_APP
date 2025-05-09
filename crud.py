# from sqlalchemy.orm import Session
# from models import User, Skill, Project
# from auth import hash_password
# import models  # ✅ This works when running the app directly



# def create_user(db: Session, user):
#     db_user = User(name=user.name, email=user.email,
#                    password=hash_password(user.password), role=user.role)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()
# def delete_user(db: Session, user_id: int):
#     # db.query(models.Skill).filter(models.Skill.owner_id == user_id).delete()
#     db.query(models.Skill).filter(models.Skill.user_id == user_id).delete()

#     db.query(models.Project).filter(models.Project.employee_id == user_id).delete()
#     user = db.query(models.User).get(user_id)
#     if user:
#         db.delete(user)
#         db.commit()


# def add_skill(db: Session, skill, user_id):
#     db_skill = Skill(name=skill.name, level=skill.level, user_id=user_id)
#     db.add(db_skill)
#     db.commit()
#     return db_skill
# def delete_skill(db: Session, skill_id: int):
#     skill = db.query(Skill).get(skill_id)
#     if skill:
#         db.delete(skill)
#         db.commit()

# def approve_skill(db: Session, skill_id):
#     skill = db.query(Skill).get(skill_id)
#     skill.approved = True
#     db.commit()

# def get_approved_skills(db: Session):
#     return db.query(Skill).filter(Skill.approved == True).all()

# # def assign_project(db: Session, project_name, skill_name, employee_id):
# #     db_project = Project(name=project_name, required_skill=skill_name, employee_id=employee_id)
# #     db.add(db_project)
# #     db.commit()
# #     return db_project
# def assign_project(db: Session, project_name: str, skill_name: str, employee_id: int):
#     # Find the project by its name
#     db_project = db.query(Project).filter(Project.name == project_name).first()
    
#     # If the project exists, update the employee_id
#     if db_project:
#         db_project.required_skill = skill_name  # Update the required skill
#         db_project.employee_id = employee_id  # Assign the project to the employee
        
#         db.commit()  # Save the changes
#         db.refresh(db_project)  # Refresh the object to get the updated data
#         return db_project
#     else:
#         return None  # Return None if the project doesn't exist

# ------------------------------------------------------------------------
# from sqlalchemy.orm import Session
# from models import User, Skill, Project, PasswordResetToken
# from auth import hash_password
# from datetime import datetime, timedelta
# import uuid  # For generating a unique token


# def create_user(db: Session, user):
#     db_user = User(name=user.name, email=user.email,
#                    password=hash_password(user.password), role=user.role)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()


# def delete_user(db: Session, user_id: int):
#     # Delete associated skills and projects before deleting user
#     db.query(Skill).filter(Skill.user_id == user_id).delete()
#     db.query(Project).filter(Project.employee_id == user_id).delete()
#     user = db.query(User).get(user_id)
#     if user:
#         db.delete(user)
#         db.commit()


# def add_skill(db: Session, skill, user_id):
#     db_skill = Skill(name=skill.name, level=skill.level, user_id=user_id)
#     db.add(db_skill)
#     db.commit()
#     return db_skill


# def delete_skill(db: Session, skill_id: int):
#     skill = db.query(Skill).get(skill_id)
#     if skill:
#         db.delete(skill)
#         db.commit()


# def approve_skill(db: Session, skill_id):
#     skill = db.query(Skill).get(skill_id)
#     skill.approved = True
#     db.commit()


# def get_approved_skills(db: Session):
#     return db.query(Skill).filter(Skill.approved == True).all()


# def assign_project(db: Session, project_name: str, skill_name: str, employee_id: int):
#     # Find the project by its name
#     db_project = db.query(Project).filter(Project.name == project_name).first()
    
#     # If the project exists, update the employee_id
#     if db_project:
#         db_project.required_skill = skill_name  # Update the required skill
#         db_project.employee_id = employee_id  # Assign the project to the employee
        
#         db.commit()  # Save the changes
#         db.refresh(db_project)  # Refresh the object to get the updated data
#         return db_project
#     else:
#         return None  # Return None if the project doesn't exist


# # -------------- Forgot Password Logic --------------
# def create_password_reset_token(db: Session, user: User):
#     """Creates a password reset token for the user and stores it in the database."""
#     # Generate a unique reset token (you can use a secure method for this)
#     token = str(uuid.uuid4())
    
#     # Set expiration time for the token (e.g., 1 hour)
#     expiration_time = datetime.utcnow() + timedelta(hours=1)
    
#     # Create and store the password reset token in the database
#     reset_token = PasswordResetToken(
#         user_id=user.id,
#         token=token,
#         expiration_time=expiration_time
#     )
    
#     db.add(reset_token)
#     db.commit()
#     db.refresh(reset_token)
    
#     return reset_token


# def get_password_reset_token(db: Session, token: str):
#     """Retrieves a password reset token from the database."""
#     return db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()


# def delete_password_reset_token(db: Session, token: str):
#     """Deletes a password reset token after use or expiration."""
#     reset_token = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
#     if reset_token:
#         db.delete(reset_token)
#         db.commit()


# def reset_password(db: Session, token: str, new_password: str):
#     """Resets the password for a user based on the reset token."""
#     # Find the reset token in the database
#     reset_token = get_password_reset_token(db, token)
    
#     if reset_token and not reset_token.is_expired():
#         # If the token is valid and not expired, update the user's password
#         user = reset_token.user
#         user.password = hash_password(new_password)
#         db.commit()
        
#         # Delete the token after the password has been reset
#         delete_password_reset_token(db, token)
        
#         return True
#     else:
#         # Token is either expired or invalid
#         return False
       

# from sqlalchemy.orm import Session
# from models import User, Skill, Project, PasswordResetToken
# from auth import hash_password
# from datetime import datetime, timedelta
# import uuid  # For generating a unique token


# def create_user(db: Session, user):
#     db_user = User(name=user.name, email=user.email,
#                    password=hash_password(user.password), role=user.role)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()


# def delete_user(db: Session, user_id: int):
#     # Delete associated skills and projects before deleting user
#     db.query(Skill).filter(Skill.user_id == user_id).delete()
#     db.query(Project).filter(Project.employee_id == user_id).delete()
#     user = db.query(User).get(user_id)
#     if user:
#         db.delete(user)
#         db.commit()


# def add_skill(db: Session, skill, user_id):
#     db_skill = Skill(name=skill.name, level=skill.level, user_id=user_id)
#     db.add(db_skill)
#     db.commit()
#     return db_skill


# def delete_skill(db: Session, skill_id: int):
#     skill = db.query(Skill).get(skill_id)
#     if skill:
#         db.delete(skill)
#         db.commit()


# def approve_skill(db: Session, skill_id):
#     skill = db.query(Skill).get(skill_id)
#     skill.approved = True
#     db.commit()


# def get_approved_skills(db: Session):
#     return db.query(Skill).filter(Skill.approved == True).all()


# def assign_project(db: Session, project_name: str, skill_name: str, employee_id: int):
#     # Find the project by its name
#     db_project = db.query(Project).filter(Project.name == project_name).first()
    
#     # If the project exists, update the employee_id
#     if db_project:
#         db_project.required_skill = skill_name  # Update the required skill
#         db_project.employee_id = employee_id  # Assign the project to the employee
        
#         db.commit()  # Save the changes
#         db.refresh(db_project)  # Refresh the object to get the updated data
#         return db_project
#     else:
#         return None  # Return None if the project doesn't exist


# # -------------- Forgot Password Logic --------------
# # Make sure this import is at the top of your crud.py file
# import models
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# import uuid

# def create_password_reset_token(db: Session, user):
#     """Creates a password reset token for the user and stores it in the database."""
#     # Generate a unique reset token
#     token = str(uuid.uuid4())

#     # Set expiration time for the token (e.g., 1 hour from now)
#     expiration_time = datetime.utcnow() + timedelta(hours=1)

#     # Create and store the password reset token in the database
#     reset_token = models.PasswordResetToken(
#         user_id=user.id,
#         token=token,
#         expiration_time=expiration_time
#     )

#     db.add(reset_token)
#     db.commit()
#     db.refresh(reset_token)

#     return reset_token  # Return the reset token object


# def get_password_reset_token(db: Session, token: str):
#     """Retrieves a password reset token from the database."""
#     return db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()


# def delete_password_reset_token(db: Session, token: str):
#     """Deletes a password reset token after use or expiration."""
#     reset_token = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
#     if reset_token:
#         db.delete(reset_token)
#         db.commit()


# def reset_password(db: Session, token: str, new_password: str):
#     """Resets the password for a user based on the reset token."""
#     # Find the reset token in the database
#     reset_token = get_password_reset_token(db, token)
    
#     if reset_token and not reset_token.is_expired():
#         # If the token is valid and not expired, update the user's password
#         user = reset_token.user
#         user.password = hash_password(new_password)
#         db.commit()
        
#         # Delete the token after the password has been reset
#         delete_password_reset_token(db, token)
        
#         return True
#     else:
#         # Token is either expired or invalid
#         return False
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

