# from fastapi import APIRouter, Depends
# from app.dependencies.role import require_admin
#
# router = APIRouter(prefix="/attendance", tags=["Attendance"])
#
# @router.post("/")
# def mark_attendance(
#     student_id: int,
#     subject: str,
#     status: str,
#     user = Depends(require_admin)
# ):
#     return {
#         "message": "Attendance marked",
#         "student_id": student_id,
#         "subject": subject,
#         "status": status
#     }