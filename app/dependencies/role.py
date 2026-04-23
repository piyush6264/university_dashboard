from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import oauth2, database, models

def get_current_user(
    token: str = Depends(oauth2.oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials"
    )

    token_data = oauth2.verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if not user:
        raise credentials_exception

    return user


def require_super_admin(current_user = Depends(get_current_user)):
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Admin allowed"
        )
    return current_user

def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin allowed"
        )
    return current_user