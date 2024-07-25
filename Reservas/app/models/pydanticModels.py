from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class TableBase(BaseModel):
    number: int
    seats: int

class TableCreate(TableBase):
    pass

class PydanticTable(TableBase):
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
    reservations: List['PydanticBook'] = []

    class Config:
        orm_mode = True

class CustomerUpdate(BaseModel):
    idCustomer: Optional[str]
    name: Optional[str]
    email: Optional[str]
    tel: Optional[str]

class BookBase(BaseModel):
    table_number: int
    customer_id: str
    time: datetime

class BookCreate(BookBase):
    pass

class PydanticBook(BookBase):
    id: int
    table: PydanticTable  
    customer: CustomerPydantic  


class BookUpdate(BaseModel):
    table_number: Optional[int] = None
    customer_id: Optional[str] = None
    time: Optional[datetime] = None


    class Config:
        orm_mode = True