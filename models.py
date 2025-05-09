# # # from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
# # # from sqlalchemy.orm import relationship
# # # from database import Base

# # # class User(Base):
# # #     __tablename__ = 'users' 
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String)
# # #     email = Column(String, unique=True, index=True)
# # #     password = Column(String)
# # #     role = Column(String, default='Employee')
# # #     skills = relationship("Skill", back_populates="owner")

# # # class Skill(Base):
# # #     __tablename__ = 'skills'
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String)
# # #     level = Column(String)
# # #     approved = Column(Boolean, default=False)
# # #     user_id = Column(Integer, ForeignKey('users.id'))
# # #     owner = relationship("User", back_populates="skills")

# # # class Project(Base):
# # #     __tablename__ = 'projects'
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String)
# # #     required_skill = Column(String)
# # #     employee_id = Column(Integer, ForeignKey('users.id'))
# # # from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
# # # from sqlalchemy.orm import relationship
# # # from database import Base

# # # class User(Base):
# # #     __tablename__ = 'users'
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String)
# # #     email = Column(String, unique=True, index=True)
# # #     password = Column(String)
# # #     role = Column(String, default='Employee')

# # #     # This line is the relationship for User to Skill
# # #     skills = relationship("Skill", back_populates="owner")

# # #     # This line is the reverse relationship for User to Project
# # #     projects = relationship("Project", back_populates="employee")

# # # class Skill(Base):
# # #     __tablename__ = 'skills'
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String)
# # #     level = Column(String)
# # #     approved = Column(Boolean, default=False)
# # #     user_id = Column(Integer, ForeignKey('users.id'))

# # #     # Relationship for Skill to User
# # #     owner = relationship("User", back_populates="skills")

# # # class Project(Base):
# # #     __tablename__ = 'projects'
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String)
# # #     required_skill = Column(String)
# # #     employee_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to the 'users' table

# # #     # Relationship to the User (Employee) model
# # #     employee = relationship("User", back_populates="projects")



# # from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
# # from sqlalchemy.orm import relationship
# # from database import Base

# # class User(Base):
# #     __tablename__ = 'users'
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String)
# #     email = Column(String, unique=True, index=True)
# #     password = Column(String)
# #     role = Column(String, default='Employee')

# #     # This line is the relationship for User to Skill
# #     skills = relationship("Skill", back_populates="owner")

# #     # This line is the reverse relationship for User to Project
# #     projects = relationship("Project", back_populates="employee")

# # class Skill(Base):
# #     __tablename__ = 'skills'
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String)
# #     level = Column(String)
# #     approved = Column(Boolean, default=False)
# #     user_id = Column(Integer, ForeignKey('users.id'))

# #     # Relationship for Skill to User
# #     owner = relationship("User", back_populates="skills")

# # class Project(Base):
# #     __tablename__ = 'projects'
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String)
# #     skill_id = Column(Integer, ForeignKey('skills.id'))  # Foreign key to Skill
# #     employee_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User (Employee)

# #     # Relationships
# #     skill = relationship("Skill", backref="projects")  # Link to Skill table
# #     employee = relationship("User", back_populates="projects")
# from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
# from sqlalchemy.orm import relationship
# from database import Base
# from datetime import datetime, timedelta


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)
#     role = Column(String, default='Employee')

#     # Relationships
#     skills = relationship("Skill", back_populates="owner")
#     projects = relationship("Project", back_populates="employee")
#     password_reset_tokens = relationship("PasswordResetToken", back_populates="user")


# class Skill(Base):
#     __tablename__ = 'skills'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     level = Column(String)
#     approved = Column(Boolean, default=False)
#     user_id = Column(Integer, ForeignKey('users.id'))

#     # Relationship for Skill to User
#     owner = relationship("User", back_populates="skills")


# class Project(Base):
#     __tablename__ = 'projects'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     skill_id = Column(Integer, ForeignKey('skills.id'))  # Foreign key to Skill
#     employee_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User (Employee)

#     # Relationships
#     skill = relationship("Skill", backref="projects")  # Link to Skill table
#     employee = relationship("User", back_populates="projects")


# # New model for Password Reset Tokens
# class PasswordResetToken(Base):
#     __tablename__ = 'password_reset_tokens'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     token = Column(String, unique=True, index=True)
#     expiration_time = Column(DateTime, nullable=False)

#     # Relationships
#     user = relationship("User", back_populates="password_reset_tokens")
    
#     # Method to check if the token is expired
#     def is_expired(self):
#         return self.expiration_time < datetime.utcnow()

#     # Method to generate a reset token (you can implement your token generation logic here)
#     @staticmethod
#     def generate_token():
#         # This should generate a unique token. You can use any method, for example, UUID or any secure random string generator
#         import uuid
#         return str(uuid.uuid4())
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta
import secrets


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default='Employee')

    # Relationships
    skills = relationship("Skill", back_populates="owner")
    projects = relationship("Project", back_populates="employee")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    level = Column(String)
    approved = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationship for Skill to User
    owner = relationship("User", back_populates="skills")


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    skill_id = Column(Integer, ForeignKey('skills.id'))  # Foreign key to Skill
    employee_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User (Employee)

    # Relationships
    skill = relationship("Skill", backref="projects")  # Link to Skill table
    employee = relationship("User", back_populates="projects")


# New model for Password Reset Tokens
class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    token = Column(String, unique=True, index=True)
    expiration_time = Column(DateTime, nullable=False)

    # Relationships
    user = relationship("User", back_populates="password_reset_tokens")
    
    # Method to check if the token is expired
    def is_expired(self):
        return self.expiration_time < datetime.utcnow()

    # Method to generate a reset token (more secure using secrets module)
    @staticmethod
    def generate_token():
        # Generate a secure random token using secrets module for cryptographic strength
        return secrets.token_urlsafe(64)  # 64 is the number of bytes for the token, resulting in a 88-character token
