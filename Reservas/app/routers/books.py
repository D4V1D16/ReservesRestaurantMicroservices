from fastapi import APIRouter

book = APIRouter()

@book.get('/books')
def get_books():
    return {"books":"Listado de reservas"}

@book.get('/books/{book_id}')
def get_book(book_id: int):
    return {"book_id": book_id, "message":"Reserva"}

@book.post('/books')
def add_book(book_data):
    return {"message":"Creando una reserva"}

@book.put('/books/{book_id}')
def update_book(book_id: int, book_data):
    return {"book_id": book_id, "message":"Actualizando una reserva"}

@book.delete('/books/{book_id}')
def delete_book(book_id: int):
    return {"book_id": book_id, "message":"Eliminando una reserva"}

