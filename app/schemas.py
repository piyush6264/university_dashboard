from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None
    role: str | None = None

class SubjectCreate(BaseModel):
    name: str

class SubjectOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    student_id: int
    subject_id: int
    date: date
    status: str  # present / absent

class AttendanceOut(BaseModel):
    id: int
    student_id: int
    subject_id: int
    date: date
    status: str

    class Config:
        from_attributes = True

class ResultCreate(BaseModel):
    student_id: int
    subject_id: int
    marks: int

class ResultOut(BaseModel):
    id: int
    student_id: int
    subject_id: int
    marks: int

    class Config:
        from_attributes = True

class HolidayCreate(BaseModel):
    date: date
    reason: str

class HolidayOut(BaseModel):
    id: int
    date: date
    reason: str

    class Config:
        from_attributes = True