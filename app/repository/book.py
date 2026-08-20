from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas import book as book_schemas


def author_has_books(
        author_id: int,
        db: Session
        ):

    return db.query(Book).filter(Book.author_id == author_id).first()

def search_by_title(title: str, db: Session):
    return db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

def get_by_author_id(author_id: int, skip, limit, db: Session):
    return db.query(Book).filter(Book.author_id == author_id).offset(skip).limit(limit).all()


def create(
        book: book_schemas.BookCreate,
        db: Session
        ):

    new_book = Book(
        title = book.title,
        years = book.years,
        author_id = book.author_id
    )
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

def get_by_id(book_id: int, db: Session):
    return db.query(Book).filter(Book.id == book_id).first()

def get_by_title(title: str, db: Session):
    return db.query(Book).filter(Book.title == title).first()

def get_all(
        skip: int,
        limit: int,
        db: Session
        ):
    return db.query(Book).offset(skip).limit(limit).all()

def update(
        existing_book: Book,
        book: book_schemas.BookUpdate,
        db: Session
):
    
    existing_book.title = book.title
    existing_book.years = book.years

    db.commit()
    db.refresh(existing_book)

    return existing_book

def delete(
        book: Book,
        db: Session
):

    db.delete(book)
    db.commit()