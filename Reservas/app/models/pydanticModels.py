from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional


class TableBase(BaseModel):
    number: int
    seats: int


class TableCreate(TableBase):
    pass

class Table(TableBase):
    class Config:
        orm_mode = True

class SeatsUpdate(BaseModel):
    seats : int

        
class CustomerBase(BaseModel):
    name: str
    email: str
    tel: str = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):

    reservations: List['Book'] = []

    class Config:
        orm_mode: True

class BookBase(BaseModel):
    table_id: int
    customer_id: int
    time: datetime

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    table: Table  
    customer: Customer  

    class Config:
        orm_mode: True