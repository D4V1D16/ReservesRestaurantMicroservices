from fastapi import APIRouter

table = APIRouter()

@table.get("/tables")
async def read_tables() -> dict[str, str]:

    return {"tables": "Lista de mesas que estan disponibles"}


