from unittest import result

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, database, models
from app.dependencies.role import require_admin, get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/create_attendance")
def mark_attendance(
        attendance: schemas.AttendanceCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(require_admin)
):
    role_check = db.query(models.User).filter(models.User.id == attendance.student_id, models.User.role == 'student').first()
    if not role_check:
        raise HTTPException(status_code=400, detail=" This student id is not matched with student role! Check Again.")

    existing = db.query(models.Attendance).filter(
        models.Attendance.student_id == attendance.student_id,
        models.Attendance.subject_id == attendance.subject_id,
        models.Attendance.date == attendance.date
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this student on this date for this subject"
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


@router.post("/create_subject")
def create_subject(
    subject: schemas.SubjectCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(require_admin)
):

    # Check duplicate subject
    existing_subject = db.query(models.Subject).filter(
        models.Subject.name == subject.name
    ).first()

    if existing_subject:
        raise HTTPException(
            status_code=400,
            detail="Subject already exists"
        )

    new_subject = models.Subject(
        name=subject.name
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject

@router.post("/allocate_subject")
def allocate_subject(
    allocation: schemas.SubjectAllocationCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(require_admin)
):

    # Check student exists
    student = db.query(models.User).filter(
        models.User.id == allocation.student_id,
        models.User.role == "student"
    ).first()

    if not student:
        raise HTTPException(
            status_code=400,
            detail="Invalid student id"
        )

    # Check subject exists
    subject = db.query(models.Subject).filter(
        models.Subject.id == allocation.subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=400,
            detail="Invalid subject id"
        )

    # Prevent duplicate allocation
    existing = db.query(models.SubjectAllocation).filter(
        models.SubjectAllocation.student_id == allocation.student_id,
        models.SubjectAllocation.subject_id == allocation.subject_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Subject already allocated to this student"
        )

    new_allocation = models.SubjectAllocation(
        student_id=allocation.student_id,
        subject_id=allocation.subject_id
    )

    db.add(new_allocation)
    db.commit()
    db.refresh(new_allocation)

    return new_allocation

@router.post("/create_result")
def add_result(result: schemas.ResultCreate, db: Session = Depends(database.get_db),
               current_user: models.User = Depends(require_admin)):

    role_check = db.query(models.User).filter(models.User.id == result.student_id, models.User.role == 'student').first()
    if not role_check:
        raise HTTPException(status_code=400, detail=" This student id is not matched with student role! Check Again.")


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
        holiday: schemas.HolidayCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(require_admin)
):

    existing_holiday = db.query(models.Holiday).filter(models.Holiday.date == holiday.date).first()
    if existing_holiday:
        raise HTTPException(status_code=400, detail="Holiday already exists")
    new_holiday = models.Holiday(
        date=holiday.date,
        reason=holiday.reason,
    )
    db.add(new_holiday)
    db.commit()
    db.refresh(new_holiday)
    return new_holiday
