from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.pydanticModels import CustomerCreate,Customer,CustomerUpdate
from ..models.utilities import pydanticCustomerToAlchemy
from ..database.connection import get_session

customer = APIRouter()


@customer.get("/customers", tags=['Customer'])
def read_customers(session : Session = Depends(get_session)):
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
def add_customer(customer : CustomerCreate,session : Session = Depends(get_session)):
    try:
        customer_obj = pydanticCustomerToAlchemy(customer)
        existCustomer = session.query(Customer).filter(Customer.id == customer_obj)
        if existCustomer:
            return JSONResponse(status_code=409, content={"message":"Ya existe un cliente con ese ID"})
        session.add(customer_obj)
        session.commit()
        return JSONResponse(status_code=201, 
                            content={
                                "message":"Cliente creado con exito",
                                "cliente":customer_obj.id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()


@customer.get("/customers/{id}", tags=['Customer'])
def get_single_client(id:int,session:Session = Depends(get_session)):
    try:
        customer = session.query(Customer).filter(Customer.id == id).first()
        if not customer:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado un cliente con ese ID"})
        customerSerialized = jsonable_encoder(customer)
        return JSONResponse(status_code=200, content={"message":"Cliente encontrado con exito","customer":customerSerialized})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()
    return {"customers": "Obteniendo un solo Cliente"}

@customer.delete("/customers/{id}", tags=['Customer'])
def add_customer(id:int,session:Session = Depends(get_session)):
    try:
        customer = session.query(Customer).filter(Customer.id == id).first()
        if not customer:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado un cliente con ese ID"})
        session.delete(customer)
        session.commit()
        return JSONResponse(status_code=204, content={"message":"Cliente eliminado con exito"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()

@customer.put("/customers/{id}", tags=['Customer'])
def update_customer(id:int, customer_upd:CustomerUpdate,session : Session = Depends(get_session)):
    try:
        customer = session.query(Customer).filter(Customer.id == id).first()
        if not customer:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado un cliente con ese ID"})
        for key,value in dict(customer_upd):
            setattr(customer, key, value)

        session.commit()
        session.refresh(customer)
        return JSONResponse(status_code=200, content={"message": "Cliente actualizado con exito"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()
