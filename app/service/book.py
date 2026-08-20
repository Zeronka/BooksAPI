from sqlalchemy.orm import Session

from app.exceptions import author as author_exceptions
from app.exceptions import book as book_exceptions
from app.repository import author as author_repository
from app.repository import book as book_repository
from app.schemas import book as book_schemas


def search_by_title(title: str, db: Session):
    book = book_repository.search_by_title(title, db)

    return book

def get_by_author_id(author_id: int, skip, limit, db: Session):

    book = book_repository.get_by_author_id(author_id, skip, limit, db)

    return book

def create(
        book_data: book_schemas.BookCreate,
        db: Session
                ):

    book = book_repository.get_by_title(book_data.title, db)
    

    if book:
        raise book_exceptions.BookAlreadyExistsError("Book already exists")
    
    if book_data.years > 2026 or book_data.years < 1:
        raise book_exceptions.BookInvalidYearsError("Invalid years")
    
    author = author_repository.get_by_id(book_data.author_id, db)
    
    if not author:
        raise author_exceptions.AuthorNotFoundError("Author not found")
    

    return book_repository.create(book_data, db)

def get_books(
        skip: int,
        limit: int,
        db: Session
):
    return book_repository.get_all(skip, limit, db)

def get_book(
        book_id: int,
        db: Session
):
    existing_book = book_repository.get_by_id(book_id, db)

    if not existing_book:
        raise book_exceptions.BookNotFoundError("Book not found")

    return existing_book

    
def update(
        book_id: int,
        book: book_schemas.BookUpdate,
        db: Session
):
    existing_book = book_repository.get_by_id(book_id, db)

    if not existing_book:
        raise book_exceptions.BookNotFoundError("Book not found")

    return book_repository.update(existing_book, book, db)

def delete(
        book_id: int,
        db: Session
):
    book = book_repository.get_by_id(book_id, db)

    if not book:
        raise book_exceptions.BookNotFoundError("Book not found")

    return book_repository.delete(book, db)