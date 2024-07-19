from fastapi import FastAPI
from app.routers import tables,books,customer



app = FastAPI(
    title="Reservas de Mesas",
    description="API para reservar mesas en un restaurante",
    version="1.0",
    openapi_tags=[
        {"name": "Tables", "description": "API para administrar mesas"},
        {"name": "Books", "description": "API para administrar reservas"},
        {"name": "Customer", "description": "API para administrar clientes"}
    ]
)





app.include_router(tables.table)
app.include_router(books.book)
app.include_router(customer.customer)