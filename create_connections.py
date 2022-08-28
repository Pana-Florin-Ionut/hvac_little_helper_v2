import psycopg2
from config import config

import os
from contextlib import contextmanager
from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool

load_dotenv()
database_url = os.environ.get("DATABASE_URI")
# user = os.environ.get("USER")
# password = os.environ.get("PASSWORD")
# host = os.environ.get("HOST")
# database = os.environ.get("DATABASE")


def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()
        # print(params)
        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # create a cursor

        cursor = conn.cursor()

        # execute a statement
        print("PostgreSQL database version:")
        cursor.execute("SELECT version()")

        # display the PostgreSQL database server version

        db_version = cursor.fetchone()
        print(db_version)

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


# conn = psycopg2.connect(host = 'localhost', database="climacool", user = "postgres", password="admin")


# pool = SimpleConnectionPool(
#     minconn=1, maxconn=10, user=user, password=password, host=host, database=database
# )
pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_url)


@contextmanager
def get_connection():
    """Create a connection with the server
    Yield a connection
    finally put the connection back into pool"""
    connection = pool.getconn()

    try:
        yield connection

    finally:
        pool.putconn(connection)


# if pool:
#     print("Connection pool created successfully")


# ---CURSOR---
@contextmanager
def get_cursor(connection):
    """Yield a cursor for using"""
    with connection:
        with connection.cursor() as cursor:
            yield cursor
