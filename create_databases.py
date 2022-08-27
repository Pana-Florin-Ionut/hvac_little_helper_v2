from contextlib import contextmanager
from psycopg2 import sql


# ---CURSOR---


@contextmanager
def get_cursor(connection):
    """Yield a cursor for using"""
    with connection:
        with connection.cursor() as cursor:
            yield cursor


# CREATING CUSTOM QUERIES


def query_create_metal_sheet_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table} (
            thickness FLOAT PRIMARY KEY NOT NULL,
            price_per_ton FLOAT NOT NULL,
            kg_per_sqm FLOAT NOT NULL,
            price_per_sqm FLOAT GENERATED ALWAYS AS (price_per_ton / kg_per_sqm) STORED)"""
    )
    query = query.format(table=sql.Identifier(table_name))
    return query


def query_insert_metal_sheet(table_name):
    query = sql.SQL(
        """INSERT INTO {table} VALUES (%s, %s, %s)
    """
    )
    query = query.format(table=sql.Identifier(table_name))


def query_create_offer_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table} (
        id SERIAL PRIMARY KEY, 
        item VARCHAR(100), 
        characteristics_A FLOAT, 
        characteristics_B FLOAT, 
        characteristics_C FLOAT, 
        characteristics_D FLOAT, 
        characteristics_E FLOAT, 
        characteristics_F FLOAT, 
        characteristics_G FLOAT, 
        characteristics_H FLOAT, 
        isolation BOOLEAN, 
        um VARCHAR(20), 
        quantity FLOAT 
       )"""
    )
    query = query.format(table=sql.Identifier(table_name))
    return query


def query_create_item_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table} (
        id SERIAL PRIMARY KEY, 
        item VARCHAR(100), 
        characteristics_A FLOAT, 
        characteristics_B FLOAT, 
        characteristics_C FLOAT, 
        characteristics_D FLOAT, 
        characteristics_E FLOAT, 
        characteristics_F FLOAT, 
        characteristics_G FLOAT, 
        characteristics_H FLOAT, 
        isolation BOOLEAN, 
        um VARCHAR(20), 
        quantity FLOAT 
       )"""
    )

    query = query.format(
        table=sql.Identifier(table_name),
    )
    return query


def query_select_table(table_name):
    query = sql.SQL("SELECT * FROM {table};")
    query = query.format(
        table=sql.Identifier(table_name),
    )
    return query


def query_insert_items(table_name):
    return sql.SQL("INSERT INTO {table} values (%s, %s, %s, %s)").format(
        table=sql.Identifier(table_name)
    )


# CRUD functions


def get_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_select_table(table_name))
        return cursor.fetchall()


def create_metal_sheet_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_metal_sheet_table(table_name))


def insert_metal_sheet(
    connection, table_name, thickness, price_per_ton, kg_per_sqm, price_per_sqm
):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_insert_metal_sheet(
                table_name, thickness, price_per_ton, kg_per_sqm, price_per_sqm
            )
        )


def create_item_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_item_table(table_name))


def insert_items_into_offer(
    connection,
    table_name,
    item,
    characteristics_A,
    characteristics_B,
    characteristics_C,
    characteristics_D,
    characteristics_E,
    characteristics_F,
    characteristics_G,
    characteristics_H,
    isolation,
    um,
    quantity,
):
    with get_cursor(connection) as cursor:
        cursor.execute(
            sql.SQL(
                """INSERT INTO {table_name}(
                    item,
                    characteristics_A,
                    characteristics_B,
                    characteristics_C,
                    characteristics_D,
                    characteristics_E,
                    characteristics_F,
                    characteristics_G,
                    characteristics_H,
                    isolation,
                    um,
                    quantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
            ).format(table_name=sql.Identifier(table_name)),
            [
                item,
                characteristics_A,
                characteristics_B,
                characteristics_C,
                characteristics_D,
                characteristics_E,
                characteristics_F,
                characteristics_G,
                characteristics_H,
                isolation,
                um,
                quantity,
            ],
        )
