from fastapi import APIRouter,HTTPException, status, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas import user as user_schemas
from app.service import user as user_service

from app.exceptions import user as user_exceptions

from app.core.security import create_access_token

router = APIRouter(
    tags=["Users"]
)

@router.post(
    "/auth/register",
    response_model=user_schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
    )
def register_user(
        user_data: user_schemas.UserCreate,
        db: Session = Depends(get_db),
):
    try:
        return user_service.register_user(user_data, db)
    except user_exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )
@router.post(
    "/auth/login",
    response_model=user_schemas.Token,
    status_code=status.HTTP_200_OK
    )
def login_user(
        user_data: user_schemas.UserLogin,
        db: Session = Depends(get_db)
):
    try:
        user = user_service.authenticate(user_data.username, user_data.password, db)
        token = create_access_token(data = {"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    except user_exceptions.InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="invalid credential"
        )