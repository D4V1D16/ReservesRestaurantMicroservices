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
def add_customer(customer: CustomerCreate, session: Session = Depends(get_session)):
    try:
        customer = pydanticCustomerToAlchemy(customer)
        existCustomer = session.query(Customer).filter(Customer.idcustomer == customer.idcustomer).first()
        if existCustomer:
            return JSONResponse(status_code=409, content={"message":"Ya existe un cliente con ese ID"})
        session.add(customer)
        session.commit()
        return JSONResponse(status_code=201, 
                            content={"message":"Cliente creado con exito",
                            "customer":{"idCustomer":customer.idcustomer,"name":customer.name,"email":customer.email,"tel":customer.tel}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()


@customer.get("/customers/{idCustomer}", tags=['Customer'])
def get_single_client(idCustomer:str,session:Session = Depends(get_session)):
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
    return {"customers": "Obteniendo un solo Cliente"}

@customer.delete("/customers/{idCustomer}", tags=['Customer'])
def delete_customer(idCustomer: str, session: Session = Depends(get_session)):
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
def update_customer(idCustomer:str, customer_upd:CustomerUpdate,session : Session = Depends(get_session)):
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
        print(e)
        #return JSONResponse(status_code=500, content={"message": f"Ha ocurrido un error: {str(e)}"})
    finally:
        session.close()
