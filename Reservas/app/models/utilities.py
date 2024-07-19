from app.models.pydanticModels import TableCreate, CustomerCreate
from app.models.modelsDB import Table,Customer

def pydanticTableToAlchemy(table:TableCreate):
    return Table(
        number=table.number,
        seats=table.seats,                          
        is_occupied=False
    )


def pydanticCustomerToAlchemy(cust: CustomerCreate):
    return Customer(  
        idcustomer=cust.IDCustomer,
        name=cust.name,
        email=cust.email,
        tel=cust.tel
    )
