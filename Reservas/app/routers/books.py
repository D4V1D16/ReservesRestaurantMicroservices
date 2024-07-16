from fastapi import APIRouter
from sqlalchemy import select
from ..models.pydanticModels import Book

book = APIRouter()

@book.get('/books', tags=['Books'])
def get_books():
    return {"books":"Listado de reservas"}

@book.get('/books/{book_id}', tags=['Books'])
def get_book(book_id: int):
    return {"book_id": book_id, "message":"Reserva"}

@book.post('/books', tags=['Books'])
def add_book(book_data:Book):
    return {"message":"Creando una reserva"}

@book.put('/books/{book_id}', tags=['Books'])
def update_book(book_id: int):
    return {"book_id": book_id, "message":"Actualizando una reserva"}

@book.delete('/books/{book_id}', tags=['Books'])
def delete_book(book_id: int):
    return {"book_id": book_id, "message":"Eliminando una reserva"}

