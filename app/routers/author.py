from fastapi import status, Query, APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.core.deps import get_current_user

from app.models.user import User

from app.schemas import author as author_schemas
from app.service import author as service

from app.exceptions.author import AuthorNotFoundError, AuthorHasBooksError, AuthorAlreadyExistsError

router = APIRouter(
    tags=["Authors"]
)

@router.post(
        "/authors",
        summary="Create author",
        response_model=author_schemas.AuthorResponse,
        status_code=status.HTTP_201_CREATED
            )
def create(
    author: author_schemas.AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
           ):
    try:
        return service.create(author, db)
    except AuthorAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Author already exists"
        )

@router.get(
        "/authors",
        summary="Get all authors",
        response_model=list[author_schemas.AuthorListResponse]
            )
def get_authors(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of authors returned"),
    db: Session = Depends(get_db)
    ):
    return service.get_authors(skip, limit, db)

@router.get(
        "/authors/{author_id}",
        summary="Get one author",
        response_model=author_schemas.AuthorResponse
            )
def get_author(
    author_id: int,
    db: Session = Depends(get_db)
            ):
    try:
        return service.get_author(author_id, db)
    except AuthorNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

@router.put(
        "/authors/{author_id}",
        summary="Update author",
        response_model=author_schemas.AuthorResponse
            )
def update(
    author_id: int,
    author: author_schemas.AuthorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    try:
        return service.update(author_id, author, db)
    except AuthorNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
            )
    except AuthorAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Author already exists"
            )

@router.delete(
        "/authors/{author_id}",
        summary="Delete author",
        status_code=status.HTTP_204_NO_CONTENT
               )
def delete(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
           ):

    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    
    try:
        return service.delete(author_id, db)
    except AuthorNotFoundError:
        raise HTTPException(status_code=404, detail="Author not found")
    except AuthorHasBooksError:
        raise HTTPException(status_code=409, detail="Author has books")