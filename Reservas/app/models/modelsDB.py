from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False, unique=True)
    seats = Column(Integer, nullable=False)
    is_occupied = Column(Boolean, nullable=False, default=False)

    reservations = relationship("Book", back_populates="table")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    time = Column(DateTime, nullable=False)

    table = relationship("Table", back_populates="reservations")
    customer = relationship("Customer", back_populates="reservations")

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False,unique=True)
    tel = Column(String(20))

    reservations = relationship("Book", back_populates="customer")