from fastapi import APIRouter, Depends
from app.dependencies.role import get_current_user

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/subjects")
def get_subjects(user = Depends(get_current_user)):
    return {"subjects": ["Math", "Science"]}

@router.get("/attendance")
def get_attendance(user = Depends(get_current_user)):
    return {"attendance": "75%"}

@router.get("/result")
def get_result(user = Depends(get_current_user)):
    return {"marks": 85}