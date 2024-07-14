from fastapi import FastAPI
from app.routers import tables,books

app = FastAPI()



@app.get("/")
def read_root():
    return {"Ping": "Pong"}

app.include_router(tables.table)
app.include_router(books.book)