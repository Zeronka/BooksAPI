from fastapi import Query, Depends, status, APIRouter, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.core.deps import get_current_user
from app.models.user import User

from app.schemas import book as book_schemas
from app.service import book as service

from app.exceptions.book import BookNotFoundError, BookInvalidYearsError, BookAlreadyExistsError
from app.exceptions.author import AuthorNotFoundError

router = APIRouter(
    tags=["Books"]
)

@router.post(
        "/books",
        summary= "Create book",
        response_model=book_schemas.BookResponse,
        status_code=status.HTTP_201_CREATED
        )
def create(
    book: book_schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    try:
        return service.create(book, db)
    except BookAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Book already exists"
        )
    except BookInvalidYearsError:
        raise HTTPException(
            status_code=400,
            detail="Invalid years"
        )
    except AuthorNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

@router.get(
        "/books",
        summary= "Get all books",
        response_model=list[book_schemas.BookListResponse],
        )
def get_books(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of books returned"),
    db: Session = Depends(get_db)
    ):
    return service.get_books(skip, limit, db)

@router.get(
        "/books/search_by_title",
        summary="Get book by title",
        response_model=list[book_schemas.BookListResponse]
        )
def search_by_title(title: str, db: Session = Depends(get_db)):
    return service.search_by_title(title, db)

@router.get(
        "/books/by-author/{author_id}",
        summary="Get books by author",
        response_model=list[book_schemas.BookListResponse]
        )
def get_books_by_author_id(
    author_id: int,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of books returned"),
    db: Session = Depends(get_db)
    ):
    return service.get_by_author_id(author_id, skip, limit, db)

@router.get(
        "/books/{book_id}",
        summary="Get one book",
        response_model=book_schemas.BookResponse
        )
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
    ):
    try:
        return service.get_book(book_id, db)
    except BookNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

@router.put(
        "/books/{book_id}",
        summary="Update book",
        response_model=book_schemas.BookResponse
        )
def update(
    book_id: int,
    book: book_schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
           ):
    try:
        return service.update(book_id, book, db)
    except BookNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

@router.delete(
        "/books/{book_id}",
        summary="Delete book",
        status_code=status.HTTP_204_NO_CONTENT
        )
def delete(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
           ):

    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    
    try:
        return service.delete(book_id, db)
    except BookNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

