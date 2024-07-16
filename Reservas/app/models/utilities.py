from .pydanticModels import TableCreate
from .modelsDB import Table
def pydanticToAlchemy(table:TableCreate):
    return Table(
        number=table.number,
        seats=table.seats,
        is_occupied=False
    )


