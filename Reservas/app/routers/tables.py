from typing import Union
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.pydanticModels import TableCreate, SeatsUpdate
from app.models.modelsDB import Table
from app.database.connection import get_session
from app.models.utilities import pydanticTableToAlchemy


table = APIRouter()


@table.get("/tables", tags=['Tables'])
def read_tables(session: Session = Depends(get_session)):
    """This function retieves all the tables in the database

    Parameters:
        session (Session, optional): [description]. Defaults to Depends(get_session).

    Returns:
        A dictionary containing list of tables. Each table is represented 
        as a dictionary with colum names as kleys and values.
        If an error occurs during the database operation, a JSON response with
        an error message is returned.
    """
    try:
        result = session.execute(text("SELECT * FROM tables"))
        column_names = [desc[0] for desc in result.cursor.description]

        tables = []
        for row in result:
            table_dict = {column_names[i]
                : value for i, value in enumerate(row)}
            tables.append(table_dict)

        return {"mesas": tables}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()


@table.post("/tables", tags=['Tables'])
def add_table(table_create: TableCreate, session: Session = Depends(get_session)) -> JSONResponse:
    """
    This function adds a new table to the database.

    Parameters:
    table (TableCreate): A Pydantic model representing the table 
    to be added. It contains the table number and seats.
    session (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
    JSONResponse: A JSON response with the following structure:
        - status_code: 201 if the table is successfully added
        , 409 if a table with the same number already exists, or 400 if an error occurs.
        - content: A dictionary containing a message 
        indicating the outcome of the operation. 
        If the table is added, it also includes the table number and seats.
    """
    try:
        new_table = pydanticTableToAlchemy(table_create)
        exist_table = session.query(Table).filter(
            Table.number == new_table.number).first()
        if exist_table:
            return JSONResponse(status_code=409, content={
                "message": "Ya existe una mesa con ese numero"
            })
        session.add(new_table)
        session.commit()
        return JSONResponse(status_code=201, content={"message": "Mesa creada con exito",
                            "table": {"number": new_table.number, "seats": new_table.seats}})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()


@table.get("/tables/{tableNumber}", tags=['Tables'])
def get_single_table(table_number: int, session: Session = Depends(get_session)) -> JSONResponse:
    """
    Retrieves a single table from the database based on the provided table number.

    Parameters:
    table_number (int): The unique identifier of the table to be retrieved.
    session (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
    JSONResponse: A JSON response with the following structure:
        - status_code: 200 if the table is successfully retrieved, 404 if the table is not found.
        - content: A dictionary containing a message indicating the outcome of the operation.
        If the table is retrieved, it also includes the serialized table data.
    """
    try:
        get_table = session.query(Table).filter(
            Table.number == table_number).first()
        if not get_table:
            return JSONResponse(status_code=404, content={
                "message": "No se ha encontrado una mesa con ese numero"
            })
        serialized_table = jsonable_encoder(get_table)
        return JSONResponse(status_code=200, content={
            "message": "Mesa encontrada con exito", "table": serialized_table
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "message": f"Ha ocurrido un error buscando la mesa: {str(e)}"
        })
    finally:
        session.close()


@table.delete("/tables/{tableNumber}", tags=['Tables'])
def delete_table(
    table_number: int, session: Session = Depends(get_session)
    ) -> Response:
    """
    Deletes a table from the database based on the provided table number.

    Parameters:
    tableNumber (int): The unique identifier of the table to be deleted.
    session (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
    Union[JSONResponse, Response]:
        - JSONResponse: A JSON response with the following structure:
            - status_code: 204 if the table is successfully deleted, 404 if the table is not found.
            - content: A dictionary containing a message indicating the outcome of the operation.
        - Response: A response object with a status code of 204 if the table is successfully deleted
    """
    try:
        get_table = session.query(Table).filter(
            Table.number == table_number).first()
        if not get_table:
            return JSONResponse(status_code=404, content={
                "message": "No se ha encontrado una mesa con ese numero"
            })
        session.delete(get_table)
        session.commit()
        return Response(status_code=204)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})


@table.put("/tables/{tableNumber}", tags=['Tables'])
def update_table(
    table_number: int, table_update: SeatsUpdate, session: Session = Depends(get_session)
    ):
    """
    Updates a table in the database based on the provided table number and table update data.

    Parameters:
    table_number (int): The unique identifier of the table to be updated.
    table_update (SeatsUpdate): A Pydantic model representing the fields to be updated.
    session (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
    JSONResponse: A JSON response with the following structure:
        - status_code: 200 if the table is successfully updated, 404 if the table is not found.
        - content: A dictionary containing a message indicating the outcome of the operation.

    Raises:
    Exception: If an error occurs during the database operation.
    """
    try:
        get_table = session.query(Table).filter(
            Table.number == table_number).first()
        if not get_table:
            return JSONResponse(status_code=404, content={
                "message": "No se ha encontrado una mesa con ese numero"
            })
        for key, value in dict(table_update).items():
            setattr(table, key, value)
        session.commit()
        session.refresh(table)
        return JSONResponse(status_code=200, content={
            "message": "Mesa actualizada con exito"
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()


@table.get("/tablesFilter", tags=['Tables'])
def filter_tables(booleanTable: bool, session: Session = Depends(get_session)):
    try:
        result = session.execute(
            text(f"SELECT * FROM tables WHERE is_occupied = {booleanTable}"))
        column_names = [desc[0] for desc in result.cursor.description]

        tables = []

        for row in result:
            table_dict = {column_names[i]
                : value for i, value in enumerate(row)}
            tables.append(table_dict)

        return {"mesas": tables}

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()
