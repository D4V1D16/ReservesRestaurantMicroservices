from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse,Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.pydanticModels import BookCreate,BookUpdate
from app.database.connection import get_session
from app.models.modelsDB import Table,Customer,Book
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
def add_book(book_data: BookCreate, session: Session = Depends(get_session)):
    try:
        table_exist = session.query(Table).filter(Table.number == book_data.table_number).first()
        customer_exist = session.query(Customer).filter(Customer.idcustomer == book_data.customer_id).first()
        
        if not table_exist:
            return JSONResponse(status_code=404, content={"message": "No se ha encontrado una mesa con ese número"})
        
        if not customer_exist:
            return JSONResponse(status_code=404, content={"message": "No se ha encontrado un cliente con ese ID"})
        
        book_serialized = pydanticBookToAlchemy(book_data)
        session.add(book_serialized)
        session.commit()
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Se ha creado la reserva con éxito",
                "reserva": {
                    "id": book_serialized.id,
                    "table_number": book_serialized.table_number,
                    "Nombre Cliente": customer_exist.name,
                    "Fecha": book_serialized.time.isoformat()  # Convertir datetime a string
                }
            }
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()

@book.get('/books/{book_id}', tags=['Books'])
def get_single_book(book_id: int, session: Session = Depends(get_session)):
    try:
        get_book = session.query(Book).filter(Book.id == book_id).first()
        if not get_book:
            return JSONResponse(status_code=404, content={"message": "No se ha encontrado una reserva con ese ID"})
        
        book_serialized = jsonable_encoder(get_book)
        return JSONResponse(status_code=200, content={"message": "Reserva encontrada con exito", "reserva": book_serialized})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()

@book.delete('/books/{book_id}', tags=['Books'])
def delete_book(book_id: int, session: Session = Depends(get_session)):
    try:
        get_book = session.query(Book).filter(Book.id == book_id).first()
        if not get_book:
            return JSONResponse(status_code=404, content={"message": "No se ha encontrado una reserva con ese ID"})
        
        session.delete(get_book)
        session.commit()
        return Response(status_code=204)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()

@book.put('/books/{book_id}', tags=['Books'])
def update_book(book_id: int,book_upd:BookUpdate, session: Session = Depends(get_session)):
    try:
        get_book = session.query(Book).filter(Book.id == book_id).first()
        if not get_book:
            return JSONResponse(status_code=404, content={"message": "No se ha encontrado una reserva con ese ID"})
        
        get_customer = session.query(Customer).filter(Customer.idcustomer == book_upd.customer_id).first()
        if not get_customer:
            return JSONResponse(status_code=404, content={"message": "No se ha encontrado un cliente con ese ID"})
        
        get_table = session.query(Table).filter(Table.number == book_upd.table_number).first()
        if not get_table:
            return JSONResponse(status_code=404, content={"message": "No se ha encontrado una mesa con ese número"})
        
        update_data = book_upd.model_dump(exclude_unset=True)

        for key,value in dict(update_data).items():
            setattr(get_book, key, value)
        
        session.commit()
        session.refresh(get_book)
        return JSONResponse(status_code=200, content={"message": "Reserva actualizada con exito"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()
