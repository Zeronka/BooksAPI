from pydantic import BaseModel
from app.schemas.author import AuthorResponse

class BookBase(BaseModel):
    title: str
    years: int
    author_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    author: AuthorResponse

class BookListResponse(BaseModel):
    id: int
    title: str