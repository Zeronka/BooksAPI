from app.database.database import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, index=True)
    years = Column(Integer, index= True)

    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")