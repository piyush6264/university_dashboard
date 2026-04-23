from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    date = Column(Date)
    status = Column(String)  # present / absent

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    marks = Column(Integer)


class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    reason = Column(String)