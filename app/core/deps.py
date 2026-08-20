from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.database import get_db
from app.repository.user import get_by_username

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_schema),
):
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_by_username(payload["sub"], db)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user