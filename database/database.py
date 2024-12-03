from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'sqlite:///my_database.db'

engine = None
Base = None
session = None

def init_db(uri=DATABASE_URI):
    global engine
    global Base
    global session

    engine = create_engine(uri)
    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    session = Session()

def create_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)