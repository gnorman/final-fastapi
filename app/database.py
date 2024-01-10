from sqlalchemy import create_engine
# The declarative base function is was deprecated in sqlalcheny 2.0 (sqlalchemy.ext.declarative)>
# It is now sqlalchemy.orm
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
# Note: the module name is psycopg, not psycopg3
#import psycopg
# The way to generate rows as dictionaries in psycopg3 is by passing the dict_row
#from psycopg.rows import dict_row
#import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#while True:

# try:
#     global cur
#     # Connect to an existing database
#     conn = psycopg.connect("dbname= user=postgres password=")
#     # Open a cursor to perform database operations
#     cur = conn.cursor(row_factory=dict_row)
#     print("Database connection was succesfull!")
     
# except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
        