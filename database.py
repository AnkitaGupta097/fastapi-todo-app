from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from typing_extensions import Annotated

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5433/todos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
   session = SessionLocal()
   try:
       yield session
   finally:
       session.close()    

db_dependency = Annotated[Session, Depends(get_db_session)]
       