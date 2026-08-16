from app.schemas import user as user_schemas
from sqlalchemy.orm import Session

from app.repository import user as user_repository

from app.exceptions import user as user_exceptions

from app.models.user import User

from app.core.security import verify_password

def register_user(
        user_data: user_schemas.UserCreate,
        db: Session,
) -> User:

    existing_user = user_repository.get_by_username(user_data.username,db)

    if existing_user:
        raise user_exceptions.UserAlreadyExists("User already exists")

    return user_repository.create_user(user_data, db)

def authenticate(
        username: str,
        password: str,
        db: Session
) -> User:

    existing_user = user_repository.get_by_username(username, db)

    if not existing_user:
        raise user_exceptions.InvalidCredentialsError("")

    if not verify_password(password, existing_user.hashed_password):
        raise user_exceptions.InvalidCredentialsError()

    return existing_user