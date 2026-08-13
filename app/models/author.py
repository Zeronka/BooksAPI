from app.database.database import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)

    books = relationship("Book", back_populates="author")