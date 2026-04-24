from fastapi import FastAPI

from app.config import settings
from app.database import engine, Base
from app.routers import user, auth, student,admin
from app.database import SessionLocal
from app import models
from app.utils import hash_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title="University Dashboard")
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)

app.include_router(student.router)



def create_super_admin():
    db = SessionLocal()

    existing = db.query(models.User).filter(models.User.role == "super_admin").first()

    if not existing:
        super_admin = models.User(
            email= settings.super_admin_email,
            password=hash_password(settings.super_admin_password),
            role="super_admin"
        )
        db.add(super_admin)
        db.commit()
        print(" Super Admin Created")
    else:
        print(" Super Admin already exists")

    db.close()

create_super_admin()