from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TableBase(BaseModel):
    number: int
    seats: int

class TableCreate(TableBase):
    pass

class Table(TableBase):
    class Config:
        orm_mode = True

class SeatsUpdate(BaseModel):
    seats: int

class CustomerBase(BaseModel):
    IDCustomer: str
    name: str
    email: str
    tel: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerPydantic(CustomerBase):
    reservations: List['Book'] = []

    class Config:
        orm_mode = True

class CustomerUpdate(BaseModel):
    idCustomer: Optional[str]
    name: Optional[str]
    email: Optional[str]
    tel: Optional[str]

class BookBase(BaseModel):
    table_id: int
    customer_id: int
    time: datetime

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    table: Table  
    customer: CustomerPydantic  

    class Config:
        orm_mode = True