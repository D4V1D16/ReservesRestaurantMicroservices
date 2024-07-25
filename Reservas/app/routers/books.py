from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from app.models.pydanticModels import Book,BookCreate
from app.database.connection import get_session
from app.models.modelsDB import Table,Customer
from app.models.utilities import pydanticBookToAlchemy

book = APIRouter()

@book.get('/books', tags=['Books'])
def get_books(session : Session = Depends(get_session)):
    try:
        result = session.execute(text("SELECT * FROM books"))
        column_names = [desc[0] for desc in result.cursor.description]

        books = []

        for row in result:
            table_dict = {column_names[i]: value for i, value in enumerate(row)}
            books.append(table_dict)

        return {"books":books}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()

@book.post('/books', tags=['Books'])
def add_book(book_data:BookCreate,session : Session = Depends(get_session)):
    try:
        table_exist = session.query(Table).filter(Table.number == book_data.table_number).first()
        customer_exist = session.query(Customer).filter(Customer.idcustomer == book_data.customer_id).first()
        if not table_exist:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado una mesa con ese numero"})
        if not customer_exist:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado un cliente con ese ID"})
        book = pydanticBookToAlchemy(book_data)
        session.add(book)
        session.commit()
        return JSONResponse(status_code=201,
                            content={"message":"Se ha creado la reserva con exito",
                                     "reserva":{"id":book.id,"table_number":book.table_number,"Nombre Cliente":customer_exist.name,"Fecha":book.time}}) 
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()

@book.put('/books/{book_id}', tags=['Books'])
def update_book(book_id: int):
    return {"book_id": book_id, "message":"Actualizando una reserva"}

@book.delete('/books/{book_id}', tags=['Books'])
def delete_book(book_id: int):
    return {"book_id": book_id, "message":"Eliminando una reserva"}

