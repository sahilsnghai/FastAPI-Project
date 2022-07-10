from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# SQLALCHEMY_DB_url= 'postgresql://<username>:<password>@<ip_address/hostname/<database_name>'
SQLALCHEMY_DB_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DB_url)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='Myapp', user='postgres', port=7099, password='password12', cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("Database connection was Successfull")
#         break

#     except Exception as error:
#         print("Connecting to Database failed.")
#         print("Error", error)
#         time.sleep(2)
# def find_post(id):
#     for pst in my_posts:
#         if pst['id'] == id:
#             return pst
#     # return "Not Found"


# def find_index(id):
#     for i, pst in enumerate(my_posts):
#         if pst['id'] == id:
#             return i
