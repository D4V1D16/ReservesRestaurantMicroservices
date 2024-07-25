from app.models.pydanticModels import TableCreate, CustomerCreate,BookCreate
from app.models.modelsDB import Table,Customer,Book

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


def pydanticBookToAlchemy(book : BookCreate):
    return Book(
        table_number=book.table_id,
        customer_id=book.customer_id,
        time=book.time  
    )