from contextlib import contextmanager
from psycopg2 import sql




class Database:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def execute(self, func):
        with self.connection() as connection:
            with self.cursor(connection) as cursor:
                cursor.execute(func)

    def execute_returnint(self, func):
        with self.connection() as connection:
            with self.cursor(connection) as cursor:
                cursor.execute(func)
                return cursor.fetchall()

    def execute_wrapper(func):
        def wrapper(self, *args, **kwargs):
            with self.connection() as connection:
                with self.cursor(connection) as cursor:
                    return cursor.execute(func(self, *args, **kwargs))

        return wrapper

    def execute_returning_all(func):
        def wrapper(self, *args, **kwargs):
            with self.connection() as connection:
                with self.cursor(connection) as cursor:
                    cursor.execute(func(self, *args, **kwargs))
                    return cursor.fetchall()

        return wrapper

    def execute_returning_first(func):
        def wrapper(self, *args, **kwargs):
            with self.connection() as connection:
                with self.cursor(connection) as cursor:
                    cursor.execute(func(self, *args, **kwargs))
                    return cursor.fetchone()

        return wrapper

    @execute_wrapper
    def insert_new_data(self, table_name, columns, values):
        return sql.SQL(f"INSERT INTO {table_name} {columns} VALUES {values}")

    def make_table(self, table_name, columns):
        return sql.SQL(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

    def insert_data(self, table_name, columns, values):
        print(columns, values)
        return sql.SQL(f"INSERT INTO {table_name} {columns} VALUES {values}")

    def delete_data(self, table_name, choices, values):
        return sql.SQL(f"DELETE FROM {table_name} WHERE {choices} = {values}")

    def see_table(self, table_name):
        return sql.SQL(f"SELECT * FROM {table_name}")

    def see_row(self, table_name, choice, value):
        return sql.SQL(f"SELECT * FROM {table_name} WHERE {choice} = {value}")

    @execute_returning_all
    def see_table2(self, table_name):
        return sql.SQL(f"SELECT * FROM {table_name}")

    @execute_returning_first
    def see_row2(self, table_name, choice, value):
        return sql.SQL(f"SELECT * FROM {table_name} WHERE {choice} = {value}")

    @execute_returning_all
    def insert_returning_id(self, table_name, choices, values, returning):
        """Requiers: table_name(str), choices(str(touple)), values(str(touple)), returning(str)
        ex: 'table_name'"""
        return sql.SQL(
            f"INSERT INTO {table_name} {choices} VALUES {values} RETURNING {returning}"
        )

