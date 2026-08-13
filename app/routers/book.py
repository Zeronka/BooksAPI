from fastapi import Query, Depends, status, APIRouter

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas import book as book_schemas
from app.service import book as service

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
    db: Session = Depends(get_db)
    ):
    return service.create(book, db)

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
def get_books_by_author(
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
    return service.get_book(book_id, db)

@router.put(
        "/books/{book_id}",
        summary="Update book",
        response_model=book_schemas.BookResponse
        )
def update(
    book_id: int,
    book: book_schemas.BookUpdate,
    db: Session = Depends(get_db)
           ):
    return service.update(book_id, book, db)

@router.delete(
        "/books/{book_id}",
        summary="Delete book",
        status_code=status.HTTP_204_NO_CONTENT
        )
def delete(
    book_id: int,
    db: Session = Depends(get_db)
           ):
    return service.delete(book_id, db)

