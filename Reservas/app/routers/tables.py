from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.pydanticModels import TableCreate
from ..models.modelsDB import Table
from ..database.connection import get_session
from ..models.utilities import pydanticToAlchemy

table = APIRouter()

@table.get("/tables", tags = ['Tables'])
def read_tables(session : Session = Depends(get_session)):
    try:
        result = session.execute(text("SELECT * FROM tables"))
        column_names = [desc[0] for desc in result.cursor.description]

        tables = []
        for row in result:
            table_dict = {column_names[i]: value for i, value in enumerate(row)}
            tables.append(table_dict)

        return {"mesas":tables}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()


@table.post("/tables", tags = ['Tables'])
def add_table(table : TableCreate,session : Session = Depends(get_session)):
    try:
        table = pydanticToAlchemy(table)
        existTable = session.query(Table).filter(Table.number == table.number).first()
        if existTable:
            return JSONResponse(status_code=400, content={"message":"Ya existe una mesa con ese numero"})
        session.add(table)
        session.commit()
        return JSONResponse(status_code=201, 
                            content={"message":"Mesa creada con exito",
                            "table":{"number":table.number,"seats":table.seats}})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message":f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()

@table.get("/tables/{id}", tags = ['Tables'])
def get_single_table(id : int, session : Session = Depends(get_session)):
    try:
        table = session.query(Table).filter(Table.number == id).first()
        if not table:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado una mesa con ese numero"})
        tableSerialized = jsonable_encoder(table)
        return JSONResponse(status_code=200, content={"message":"Mesa encontrada con exito","table":tableSerialized})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Ha ocurrido un error buscando la mesa: {str(e)}"})

@table.delete("/tables/{id}", tags = ['Tables'])
def delete_table(id : int, session : Session = Depends(get_session)):
    try:
        table = session.query(Table).filter(Table.number == id).first()
        if not table:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado una mesa con ese numero"})
        d = Table.delete
        session.delete(table)
        session.commit()
        return JSONResponse(status_code=200, content={"message":"Mesa borrada con exito"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Ha ocurrido un error: {str(e)}"})

@table.put("/tables/{id}", tags = ['Tables'])
def update_table(id : int):
    return {"message":"Actualizando una mesa"}

