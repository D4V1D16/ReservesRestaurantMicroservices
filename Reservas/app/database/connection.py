from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from ..models import modelsDB
engine = create_engine('postgresql://admin:abc123@localhost:6000/booksdb')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
modelsDB.Base.metadata.create_all(bind=engine)

