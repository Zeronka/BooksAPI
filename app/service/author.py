from sqlalchemy.orm import Session

from app.exceptions import author as author_exceptions
from app.repository import author as author_repository
from app.repository import book as book_repository
from app.schemas import author as author_schemas


def create(
        author_data: author_schemas.AuthorCreate,
        db: Session
):
    existing_author = author_repository.get_by_name(author_data.name, db)

    if existing_author:
        raise author_exceptions.AuthorAlreadyExistsError("Author already exists")

    return author_repository.create(author_data, db)

def get_authors(skip: int, limit: int, db: Session):
    return author_repository.get_authors(skip, limit, db)

def get_author(
        author_id: int,
        db: Session
        ):

    existing_author = author_repository.get_by_id(author_id, db)

    if not existing_author:
        raise author_exceptions.AuthorNotFoundError("Author not found")

    return existing_author

def update(
        author_id: int,
        author: author_schemas.AuthorUpdate,
        db: Session
):
    existing_author = author_repository.get_by_id(author_id, db)

    if not existing_author:
        raise author_exceptions.AuthorNotFoundError("Author not found")

    author_with_same_name = author_repository.get_by_name(author.name, db)

    if(
        author_with_same_name
        and existing_author.id != author_with_same_name.id
    ): 
        raise author_exceptions.AuthorAlreadyExistsError("Author already exists")
                
    return author_repository.update(existing_author,author,db)

def delete(
    author_id: int,
    db: Session
):
    author = author_repository.get_by_id(author_id, db)

    if not author:
        raise author_exceptions.AuthorNotFoundError("Author not found")

    existing_book = book_repository.author_has_books(author_id, db)

    if existing_book:
        raise author_exceptions.AuthorHasBooksError("Author has books")

    return author_repository.delete(author, db)