from unittest import result

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, database, models
from app.dependencies.role import require_admin,get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])
@router.post("/create_attendance")
def mark_attendance(
        attendance: schemas.AttendanceCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can mark attendance"
        )

    existing = db.query(models.Attendance).filter(
        models.Attendance.student_id == attendance.student_id,
        models.Attendance.subject_id == attendance.subject_id,
        models.Attendance.date == attendance.date
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this student on this date"
        )

    new_attendance = models.Attendance(
        student_id=attendance.student_id,
        subject_id=attendance.subject_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance
@router.post("/create_subject",response_model=schemas.SubjectOut)
def create_subject(
    subject: schemas.SubjectCreate,
db: Session = Depends(database.get_db),
current_user: models.User = Depends(require_admin)):
    new_subject = models.Subject(
        name=subject.name,
    )
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


@router.post("/create_result")
def add_result(
    result: schemas.ResultCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(require_admin)
):
    new_result = models.Result(
        student_id=result.student_id,
        subject_id=result.subject_id,
        marks=result.marks,
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result


@router.post("/create_holiday")
def create_holiday(
    holiday:schemas.HolidayCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(require_admin)
):
    new_holiday = models.Holiday(
        date=holiday.date,
        reason=holiday.reason,
    )
    db.add(new_holiday)
    db.commit()
    db.refresh(new_holiday)
    return new_holiday