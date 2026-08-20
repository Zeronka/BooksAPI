from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas import user as user_schemas


def create_user(
        user_data: user_schemas.UserCreate,
        db: Session
        ) -> User:

    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = get_password_hash(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_by_username(
        username: str,
        db: Session
) -> User | None:
    return db.query(User).filter(User.username == username).first()

