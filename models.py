from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default='Employee')
    skills = relationship("Skill", back_populates="owner")

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    level = Column(String)
    approved = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="skills")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    required_skill = Column(String)
    employee_id = Column(Integer, ForeignKey('users.id'))
