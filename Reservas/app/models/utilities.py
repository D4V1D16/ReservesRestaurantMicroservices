from .pydanticModels import TableCreate,CustomerCreate
from .modelsDB import Table,Customer
def pydanticTableToAlchemy(table:TableCreate):
    return Table(
        number=table.number,
        seats=table.seats,                          
        is_occupied=False
    )


def pydanticCustomerToAlchemy(cust:CustomerCreate):
    return Customer(
        name=cust.name,
        email=cust.email,
        tel=cust.tel
    )



