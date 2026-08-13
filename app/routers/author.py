from fastapi import status, Query, APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas import author as author_schemas
from app.service import author as service

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
    db: Session = Depends(get_db)
           ):
    return service.create(author, db)

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
    return service.get_author(author_id, db)

@router.put(
        "/authors/{author_id}",
        summary="Update author",
        response_model=author_schemas.AuthorResponse
            )
def update(
    author_id: int,
    author: author_schemas.AuthorCreate,
    db: Session = Depends(get_db)
    ):
    return service.update(author_id, author, db)

@router.delete(
        "/authors/{author_id}",
        summary="Delete author",
        status_code=status.HTTP_204_NO_CONTENT
               )
def delete(
    author_id: int,
    db: Session = Depends(get_db)
           ):
    return service.delete(author_id, db)