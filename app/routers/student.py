from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import database, models, schemas
from app.dependencies.role import get_current_user

router = APIRouter(prefix="/student", tags=["Student"])

from typing import Optional

@router.get("/student/subjects", response_model=list[schemas.SubjectOut])
def get_subjects(
        student_id: Optional[int] = None,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):

    if current_user.role not in ["student", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    # Student gets own subjects automatically
    if current_user.role == "student":
        target_id = current_user.id

    # Admin can fetch any student's subjects
    else:
        if not student_id:
            raise HTTPException(
                status_code=400,
                detail="Admin must provide student_id parameter"
            )

        target_id = student_id

    subjects = db.query(models.Subject).join(
        models.SubjectAllocation,
        models.Subject.id == models.SubjectAllocation.subject_id
    ).filter(
        models.SubjectAllocation.student_id == target_id
    ).all()

    return subjects

@router.get("/student/attendance", response_model=list[schemas.AttendanceOut])
def get_attendance(
    student_id: Optional[int] = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")

    if current_user.role == "student":
        target_id = current_user.id
    else:
        if not student_id:
            raise HTTPException(
                status_code=400,
                detail="Admin must provide student_id to view attendance"
            )
        target_id = student_id

    attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == target_id
    ).all()

    return attendance


@router.get("/student/results", response_model=list[schemas.ResultOut])
def get_results(
    student_id: Optional[int] = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Students and Admins only"
        )

    if current_user.role == "student":
        target_id = current_user.id
    else:
        if not student_id:
            raise HTTPException(
                status_code=400,
                detail="Admin must provide a student_id to view results"
            )
        target_id = student_id

    results = db.query(models.Result).filter(
        models.Result.student_id == target_id
    ).all()

    return results

