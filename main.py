from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine, Base
from pydantic import BaseModel 
from models import Book
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

class BookRequest(BaseModel):
    title: str
    author: str
    cover: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.get("/books/{id}")
def get_book_by_id(id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).get(id)
    if db_book:
        return db_book
    raise HTTPException(status_code=404, detail=f"Book with id {id} not found")

@app.post("/create-book")
def create_book(book: BookRequest, db: Session = Depends(get_db)):
    title = book.title
    author = book.author
    cover = book.cover
    db_book = Book(title=title, author=author, cover=cover)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/update-book/{id}")
def update_book(id: int, book: BookRequest, db: Session = Depends(get_db)):
    db_book = db.query(Book).get(id)
    if db_book:
        db_book.title = book.title
        db_book.author = book.author
        db_book.cover = book.cover
        db.commit()
        db.refresh(db_book)
        return db_book
    return HTTPException(status_code=404, detail=f"Book with id {id} not found")
    

@app.delete("/delete-book/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).get(id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return {"message": f"Book with id {id} successfully deleted"}
    raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
