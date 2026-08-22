from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

#model
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

#schemas
class BookRequest(BaseModel):
    id: Optional[int] = Field(title="ID is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1980, lt=2031)

    class Config:
        schema_extra = {
        "json_schema_extra": {
            "example": {
                "title": "A New Book",
                "author": "codingwithroby",
                "description": "A New Description of a Book",
                "rating": 5,
                "published_date": 2029
            }
        }
    }








BOOKS = [
    Book(1, "Computer Science Pro", "Codingwithrody", "A very nice book", 5, 2016),
    Book(2, "Be fast with FastAPI", "Codingwithrody", "A great book", 5, 1998),
    Book(3, "Muster Endpoints", "Codingwithrody", "A awesome book", 5, 2010),
    Book(4, "HP1", "Author 1", "Book description", 2, 2010),
    Book(5, "HP2", "Author 2", "Book description", 3, 1990),
    Book(6, "HP3", "Author 3", "Book description", 1, 1990)
]

#routers
@app.get("/books")
async def read_all_books():
    return BOOKS

#get book id
@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book

#get book rating
@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book_rating == book.rating:
            books_to_return.append(book)
    return books_to_return




#exercises :Add a new field to Book and BookRequest called published_date: int (for example, published_date: int = 2012).
# So, this book as published on the year of 2012.

#Enhance each Book to now have a published_date



@app.get("/books/publish/")
async def read_book_by_published_date(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return





@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))



def find_book_id(book: BOOKS):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break





