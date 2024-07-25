from fastapi import APIRouter,Depends,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.pydanticModels import CustomerCreate,CustomerUpdate
from app.models.modelsDB import Customer
from app.models.utilities import pydanticCustomerToAlchemy
from app.database.connection import get_session

customer = APIRouter()


@customer.get("/customers", tags=['Customer'])
def read_customers(session : Session = Depends(get_session)) -> dict:
    """
    Retrieve all customers from the database.

    Parameters:
    session (Session): A database session object provided by FastAPI Depends.

    Returns:
    dict: A dictionary containing a list of customers.
    """
    try:
        result = session.execute(text("SELECT * FROM customers"))
        column_names = [desc[0] for desc in result.cursor.description]

        customers = []
        for row in result:
            customer_dict = {column_names[i]: value for i, value in enumerate(row)}
            customers.append(customer_dict)

        return {"customers":customers}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()


@customer.post("/customers", tags=['Customer'])
def add_customer(new_customer: CustomerCreate, session: Session = Depends(get_session)) -> JSONResponse:
    """
    Add a new customer to the database.

    Parameters:
    customer (CustomerCreate): A Pydantic model representing the new customer.
    session (Session): A database session object provided by FastAPI Depends.

    Returns:
    JSONResponse: A JSON response with a success message and the created customer.
    """
    try:
        customer_serialized = pydanticCustomerToAlchemy(new_customer)
        exist_customer = session.query(Customer).filter(Customer.idcustomer == customer_serialized.idcustomer).first()

        if exist_customer:
            return JSONResponse(status_code=409, content={
                "message":"Ya existe un cliente con ese ID"
                })
        
        session.add(customer)
        session.commit()
        return JSONResponse(status_code=201, 
                            content={"message":"Cliente creado con exito",
                            "customer":{
                                "idCustomer":customer_serialized.idcustomer,
                                "name":customer_serialized.name,
                                "email":customer_serialized.email,
                                "tel":customer_serialized.tel
                                }})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Ha ocurrido un error: {str(e)}"})
    
    finally:
        session.close()


@customer.get("/customers/{idCustomer}", tags=['Customer'])
def get_single_client(idCustomer:str,session:Session = Depends(get_session)) -> JSONResponse:
    """
    Retrieve a single customer from the database by their ID.

    Parameters:
    idCustomer (str): The ID of the customer to retrieve.
    session (Session): A database session object provided by FastAPI Depends.

    Returns:
    JSONResponse: A JSON response with a success message and the retrieved customer.
    """
    try:
        customer = session.query(Customer).filter(Customer.idcustomer == idCustomer).first()
        if not customer:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado un cliente con ese ID"})
        customerSerialized = jsonable_encoder(customer)
        return JSONResponse(status_code=200, content={"message":"Cliente encontrado con exito","customer":customerSerialized})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()


@customer.delete("/customers/{idCustomer}", tags=['Customer'])
def delete_customer(idCustomer: str, session: Session = Depends(get_session)) -> Union[Response, JSONResponse]:
    """
    Delete a customer from the database by their ID.

    Parameters:
    idCustomer (str): The ID of the customer to delete.
    session (Session): A database session object provided by FastAPI Depends.

    Returns:
    Union[Response, JSONResponse]: A FastAPI Response object with a status code of 204 if successful, or a JSON response with an error message.
    """
    try:
        customer = session.query(Customer).filter(Customer.idcustomer == idCustomer).first()
        if not customer:
            return JSONResponse(status_code=404, content={"message": "No se ha encontrado un cliente con ese ID"})
        session.delete(customer)
        session.commit()
        return Response(status_code=204)
    except Exception as e:
        error_message = {"message": f"Ha ocurrido un error: {str(e)}"}
        return JSONResponse(status_code=500, content=error_message)
    finally:
        session.close()


@customer.put("/customers/{idCustomer}", tags=['Customer'])
def update_customer(idCustomer:str, customer_upd:CustomerUpdate,session : Session = Depends(get_session)) -> JSONResponse:
    """
    Update an existing customer in the database.

    Parameters:
    idCustomer (str): The ID of the customer to update.
    customer_upd (CustomerUpdate): A Pydantic model representing the updated customer.
    session (Session): A database session object provided by FastAPI Depends.

    Returns:
    JSONResponse: A JSON response with a success message.
    """
    try:
        customer = session.query(Customer).filter(Customer.idcustomer == idCustomer).first()
        if not customer:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado un cliente con ese ID"})
        for key,value in dict(customer_upd).items():
            setattr(customer, key, value)

        session.commit()
        session.refresh(customer)
        return JSONResponse(status_code=200, content={"message": "Cliente actualizado con exito"})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()