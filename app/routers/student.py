from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import database, models, schemas
from app.dependencies.role import get_current_user

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/student/subjects", response_model=list[schemas.SubjectOut])
def get_subjects(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    subjects = db.query(models.Subject).all()
    return subjects

@router.get("/student/attendance", response_model=list[schemas.AttendanceOut])
def get_attendance(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == current_user.id
    ).all()

    return attendance

@router.get("/student/results", response_model=list[schemas.ResultOut])
def get_results(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    results = db.query(models.Result).filter(
        models.Result.student_id == current_user.id
    ).all()

    return results

