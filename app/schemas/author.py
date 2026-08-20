from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int

class AuthorListResponse(BaseModel):
    id: int
    name: str
