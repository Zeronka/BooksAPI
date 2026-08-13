from sqlalchemy.orm import Session

from app.models.author import Author

from app.schemas import author as author_schemas


def create(
        author: author_schemas.AuthorCreate,
        db: Session
):
    new_author = Author(
        name = author.name
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author

def get_authors(skip: int, limit: int, db: Session):
    return db.query(Author).offset(skip).limit(limit).all()

def get_by_name(
        author: author_schemas.AuthorBase,
        db: Session
):
    return db.query(Author).filter(Author.name == author).first()

def get_by_id(
        author_id: int,
        db: Session
):
    return db.query(Author).filter(Author.id == author_id).first()

def update(
        existing_author: Author,
        author: author_schemas.AuthorUpdate,
        db: Session
):

    existing_author.name = author.name

    db.commit()
    db.refresh(existing_author)

    return existing_author

def delete(
        author: Author,
        db: Session
):

    db.delete(author)
    db.commit()