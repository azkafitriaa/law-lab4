from sqlalchemy import Column, Integer, String, Text

from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    cover = Column(Text)