from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, utils
from app.dependencies.role import require_super_admin

router = APIRouter(tags=["Create_Admin_or_Student"])

@router.post("/", response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(require_super_admin)
):

    if user.role not in ["admin", "student"]:
        raise HTTPException(detail="Only admin or student allowed")

    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(detail="User already exists")

    new_user = models.User(
        email=user.email,
        password=utils.hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user