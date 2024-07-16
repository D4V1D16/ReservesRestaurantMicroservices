from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import modelsDB
engine = create_engine('postgresql://postgres:abc123@localhost:5432/booksdb')

modelsDB.Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    try:
        session = SessionLocal()
        return session
    except Exception as e:
        print(f"Error al crear la sesión con la base de datos: {e}")
        return None

def migration () :
    try:
        modelsDB.Base.metadata.create_all(bind=engine) 
        print("RAW INFO: MIGRATION COMPLETED") 
        return True
    except Exception as e:
        print(f"Error al migrar la base de datos: {e}")
        return False


migration()