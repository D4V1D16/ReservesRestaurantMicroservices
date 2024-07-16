from fastapi import APIRouter
from ..models.pydanticModels import Customer

customer = APIRouter()


@customer.get("/customers", tags=['Customer'])
def read_customers():
    return {"customers": "Obteniendo Clientes"}

@customer.post("/customers", tags=['Customer'])
def add_customer(cust:Customer):
    return {"customers": "Creando Clientes"}

@customer.post("/customers/{id}", tags=['Customer'])
def get_single_client(id:int):
    return {"customers": "Obteniendo un solo Cliente"}

@customer.delete("/customers/{id}", tags=['Customer'])
def add_customer(id:int):
    return {"customers": "Creando Clientes"}

@customer.put("/customers/{id}", tags=['Customer'])
def update_customer(id:int, cust:Customer):
    return {"customers": "Actualizando Clientes"}