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


def query_select_table(table_name):
    query = sql.SQL("SELECT * FROM {table}")
    query = query.format(
        table=sql.Identifier(table_name),
    )
    return query


def query_clear_table(table_name):
    query = sql.SQL("""TRUNCATE {table} RESTART IDENTITY""")
    return query.format(table=sql.Identifier(table_name))


def query_create_metal_sheet_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table} (
            thickness FLOAT PRIMARY KEY NOT NULL,
            price_per_ton FLOAT NOT NULL,
            kg_per_sqm FLOAT NOT NULL,
            price_per_sqm FLOAT GENERATED ALWAYS AS (price_per_ton / 1000 * kg_per_sqm) STORED,
            flanges_price FLOAT,
            corners_price FLOAT)"""
    )
    query = query.format(table=sql.Identifier(table_name))
    return query


def query_create_flanges_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table} (
            dimension FLOAT UNIQUE NOT NULL,
            price FLOAT NOT NULL)"""
    )
    return query.format(table=sql.Identifier(table_name))


def query_insert_into_metal_sheet_price(table_name):
    query = sql.SQL(
        """
    INSERT INTO {table_name} (thickness, price_per_ton, kg_per_sqm, flanges_price, corners_price) VALUES (%s, %s, %s, %s, %s)"""
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_update_into_metal_sheet_price(table_name):
    query = sql.SQL(
        "UPDATE {table} SET price_per_ton = %s, kg_per_sqm=%s, flanges_price=%s, corners_price=%s WHERE thickness = %s"
    )
    return query.format(table=sql.Identifier(table_name))


# Maybe delete this
def query_clear_metal_sheet_table_row(table_name, choice):
    query = sql.SQL("""DELETE FROM {table} WHERE {choice} = %s""")
    return query.format(table=sql.Identifier(table_name), choice=sql.Identifier(choice))


def query_delete_entry(table_name, choice):
    query = sql.SQL("""DELETE FROM {table} WHERE {choice} = %s""")

    return query.format(table=sql.Identifier(table_name), choice=sql.Identifier(choice))


# Maybe switch this with above function and delete this


def query_clear_metal_sheet_row(table_name):
    query = sql.SQL("""DELETE FROM {table} WHERE thickness = %s""")
    return query.format(table=sql.Identifier(table_name))


def query_read_metal_sheet_row(table_name, choice):
    query = sql.SQL("""SELECT * FROM {table} WHERE {choice} = %s""")
    return query.format(table=sql.Identifier(table_name), choice=sql.Identifier(choice))


def query_read_table(table_name, choice, value):
    query = sql.SQL("""SELECT * FROM {table} WHERE {choice} = {value}""")
    return query.format(
        table=sql.Identifier(table_name),
        choice=sql.Identifier(choice),
        value=sql.Literal(value),
    )


def query_create_metal_sheet_tables(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table} (
        idx SERIAL PRIMARY KEY, 
        table_name VARCHAR(255) UNIQUE)"""
    )
    return query.format(table=sql.Identifier(table_name))


def query_insert_metal_sheet_name(table_name):
    query = sql.SQL("""INSERT INTO {table} (table_name) VALUES (%s)""")
    return query.format(table=sql.Identifier(table_name))


def query_delete_table(table_name):
    query = sql.SQL("DROP TABLE IF EXISTS {table} CASCADE")
    return query.format(table=sql.Identifier(table_name))


def query_insert_items(table_name):
    query = sql.SQL("""INSERT INTO {table} (dimension, price) VALUES (%s, %s)""")
    return query.format(table=sql.Identifier(table_name))


def query_create_clients_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table} (
        id SERIAL PRIMARY KEY UNIQUE,
        client_name VARCHAR(255) NOT NULL UNIQUE,
        client_identification VARCHAR(255), 
        client_address TEXT, 
        client_email VARCHAR(255),
        about TEXT)"""
    )
    return query.format(table=sql.Identifier(table_name))


def query_insert_values(table_name, choices, values):

    return sql.SQL(f"INSERT INTO {table_name} ({choices}) VALUES {values}")


def query_update_clients_table(table_name):
    query = sql.SQL(
        "UPDATE {table_name} SET client_name = %s, client_identification = %s, client_address = %s, client_email = %s WHERE id = %s "
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_update_table(table_name, choices, values, set_item, set_item_value):
    # print(
    #     (
    #         f"UPDATE {table_name} SET {choices}={values} WHERE {set_item} = {set_item_value} "
    #     )
    # )
    return sql.SQL(
        f"UPDATE {table_name} SET {choices}={values} WHERE {set_item} = {set_item_value} "
    )


def query_insert_items_kwargs(table_name, choices, values):
    return sql.SQL(f"INSERT INTO {table_name} {choices} VALUES {values}")


def query_insert_items_kwargs_return_id(table_name, choices, values):
    return sql.SQL(f"INSERT INTO {table_name} {choices} VALUES {values} returning id")


def query_create_contact_person_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL, client_id INTEGER, person_name VARCHAR(255),
        person_phone VARCHAR(255),
        person_email VARCHAR(255),
        departament VARCHAR(255),
        FOREIGN KEY(client_id) REFERENCES clients (id))
    """
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_create_projects_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        client_id INTEGER, 
        client_name VARCHAR(255),
        project_name VARCHAR(255) UNIQUE,
        project_address TEXT,
        about TEXT,
        date_created TIMESTAMP NOT NULL DEFAULT NOW(),
        FOREIGN KEY(client_id) REFERENCES clients(id))"""
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_create_offers_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        project_id INTEGER, 
        offer_name VARCHAR(255) UNIQUE,
        metal_sheet_characteristics VARCHAR(255),
        date_created TIMESTAMP NOT NULL DEFAULT NOW(),
        FOREIGN KEY(project_id) REFERENCES projects_table(id))"""
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_offer_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
        id FLOAT PRIMARY KEY, 
        project_id INTEGER,
        item VARCHAR(255), 
        characteristics_A VARCHAR(255), 
        characteristics_B VARCHAR(255), 
        characteristics_C VARCHAR(255), 
        characteristics_D VARCHAR(255), 
        characteristics_E VARCHAR(255), 
        characteristics_F VARCHAR(255),
        um VARCHAR(255), 
        quantity FLOAT, 
        category VARCHAR(255),
        observations VARCHAR(500),
        FOREIGN KEY (project_id) REFERENCES projects_table(id))
        """
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_standard_products(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        product_name VARCHAR(255) UNIQUE,
        about VARCHAR(500))"""
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_create_products_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        dimension_A FLOAT NOT NULL,
        dimension_B FLOAT,
        dimension_C FLOAT,
        dimension_D FLOAT,
        metal_sheet_thickness FLOAT,
        area FLOAT,
        about VARCHAR(255),
        UNIQUE (dimension_A, dimension_B, dimension_C, dimension_D))"""
    )

    return query.format(table_name=sql.Identifier(table_name))


def query_get_standard_item(product_type, dimensions):
    query = f'SELECT * FROM "{product_type}"'
    # print(dimensions)
    dims = ["a", "b", "c", "d"]
    for i, value in enumerate(dimensions):
        if i == 0:
            query += f" WHERE dimension_a = '{dimensions[0]}'"
        elif value:
            query += f" AND dimension_{dims[i]} = "
            query += f"'{value}'"
    # print(query)
    return query


def query_create_offer_new_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
            id FLOAT PRIMARY KEY UNIQUE NOT NULL,
            project_id INTEGER,
            item VARCHAR(255), 
            characteristics_A VARCHAR(255), 
            characteristics_B VARCHAR(255), 
            characteristics_C VARCHAR(255), 
            characteristics_D VARCHAR(255), 
            characteristics_E VARCHAR(255), 
            characteristics_F VARCHAR(255),
            um VARCHAR(255), 
            quantity FLOAT, 
            category VARCHAR(255),
            observations VARCHAR(500),
            product_type VARCHAR(255),
            characteristics VARCHAR(255),
            thickness FLOAT,
            area FLOAT,
            flanges FLOAT,
            corners FLOAT,
            price_per_sqm FLOAT,
            flanges_price FLOAT,
            corners_price FLOAT,
            price_per_um FLOAT,
            total_price FLOAT GENERATED ALWAYS AS (quantity * price_per_um) STORED,
            label_A VARCHAR(255),
            label_B VARCHAR(255),
            label_C VARCHAR(255),
            FOREIGN KEY (project_id) REFERENCES projects_table(id))
            """
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_read_row(table_name, choice, value):
    query = sql.SQL("""SELECT * FROM {table} WHERE {choice} = {value} """)
    return query.format(
        table=sql.Identifier(table_name),
        choice=sql.Identifier(choice),
        value=sql.Literal(value),
    )


def query_alter_table_name(table_name, new_name):
    query = sql.SQL("""ALTER TABLE {table_name} RENAME TO {new_name}""")
    return query.format(
        table_name=sql.Identifier(table_name), new_name=sql.Identifier(new_name)
    )


def query_create_suppliers_table(table_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        supplier_name VARCHAR(255) UNIQUE,
        supplier_info VARCHAR(255),
        supplier_address VARCHAR(255),
        about VARCHAR(500)
        )"""
    )
    return query.format(table_name=sql.Identifier(table_name))


def query_create_products_sold(table_name, suppliers_table):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            sold_item VARCHAR(255),
            supplier_id INTEGER,
            UNIQUE (sold_item, supplier_id),
            FOREIGN KEY (supplier_id) REFERENCES {suppliers_table}(id))"""
    )
    return query.format(
        table_name=sql.Identifier(table_name),
        suppliers_table=sql.Identifier(suppliers_table),
    )


def query_create_bought_offer_table(table_name, supplier_name):
    query = sql.SQL(
        """CREATE TABLE IF NOT EXISTS {table_name}_{supplier_name} 
        id INTEGER PRIMARY KEY,
        item_name VARCHAR(255),
        characteristics VARCHAR(500),
        um VARCHAR(255),
        quantity FLOAT,
        obs VARCHAR(500)
        """
    )
    return query.format(
        table_name=sql.Identifier(table_name),
        supplier_name=sql.Identifier(supplier_name),
    )


def query_get_items_supplier(offer_name, supplier_items_table, suppliers_table):
    # print(offer_name)
    query = sql.SQL(
        """SELECT table_1.id, table_1.product_type, table_1.characteristics, table_1.um, table_1.quantity, table_2.supplier_id, table_3.supplier_name FROM {offer_name} as table_1
JOIN {supplier_items_table} as table_2 on item = sold_item 
JOIN {suppliers_table} as table_3 on table_2.supplier_id = table_3.id 
WHERE table_1.category='bought' 
ORDER BY table_3.supplier_name"""
    )
    return query.format(
        offer_name=sql.Identifier(offer_name),
        supplier_items_table=sql.Identifier(supplier_items_table),
        suppliers_table=sql.Identifier(suppliers_table),
    )


def query_get_single_supplier_items(
    offer_name, supplier_items_table, suppliers_table, supplier_name
):

    query = sql.SQL(
        """SELECT table_1.id, table_1.product_type, table_1.characteristics, table_1.um, table_1.quantity, table_2.supplier_id, table_3.supplier_name FROM {offer_name} as table_1 
JOIN {supplier_items_table} as table_2 on item = sold_item 
JOIN {suppliers_table} as table_3 on table_2.supplier_id = table_3.id  
WHERE table_3.supplier_name = {supplier_name} AND table_1.category='bought'"""
    )

    return query.format(
        offer_name=sql.Identifier(offer_name),
        supplier_items_table=sql.Identifier(supplier_items_table),
        suppliers_table=sql.Identifier(suppliers_table),
        supplier_name=sql.Literal(supplier_name),
    )


def query_get_columns(table_name):
    query = sql.SQL(
        """SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = {table_name} ORDER BY ordinal_position"""
    )
    return query.format(table_name=sql.Literal(table_name))


def query_create_temp_table(
    offer_name, supplier_items_table, suppliers_table, supplier_name
):
    # print(offer_name)
    query = sql.SQL(
        """SELECT table_1.id, table_1.product_type, table_1.characteristics, table_1.um, table_1.quantity, table_2.supplier_id, table_3.supplier_name INTO temp_table FROM {offer_name} as table_1 
JOIN {supplier_items_table} as table_2 on item = sold_item 
JOIN {suppliers_table} as table_3 on table_2.supplier_id = table_3.id  
WHERE table_3.supplier_name = {supplier_name} AND table_1.category='bought';
"""
    )
    query = query.format(
        offer_name=sql.Identifier(offer_name),
        supplier_items_table=sql.Identifier(supplier_items_table),
        suppliers_table=sql.Identifier(suppliers_table),
        supplier_name=sql.Literal(supplier_name),
    )

    print(query)
    return query


def query_get_labels(offer_name):
    query = sql.SQL(
        """
    SELECT id, product_type, quantity, label_A, label_B, label_C FROM {offer_name} WHERE category = 'manufactured' OR category = 'standard' """
    )
    query = query.format(offer_name=sql.Identifier(offer_name))
    return query


def query_truncate_table(table_name):
    query = sql.SQL(
        """
                    TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"""
    )
    return query.format(table_name=sql.Identifier(table_name))


# CRUD operations


def clear_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_clear_table(table_name))


def create_metal_sheet_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_metal_sheet_table(table_name))


def insert_into_metal_sheet_price(
    connection,
    table_name,
    thickness,
    price_per_ton,
    kg_per_sqm,
    flanges_price,
    corners_price,
):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_insert_into_metal_sheet_price(table_name),
            [thickness, price_per_ton, kg_per_sqm, flanges_price, corners_price],
        )


def update_into_metal_sheet_price(
    connection, table_name, thickness, price_per_ton, kg_per_sqm
):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_update_into_metal_sheet_price(table_name),
            [
                price_per_ton,
                kg_per_sqm,
                thickness,
            ],
        )


def clear_metal_sheet_row(connection, table_name, thickness):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_clear_metal_sheet_row(table_name),
            [
                thickness,
            ],
        )


def create_metal_sheet_tables(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_metal_sheet_tables(table_name))


def insert_metal_sheet_name(connection, table_name, sheet_name):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_insert_metal_sheet_name(table_name),
            [
                sheet_name,
            ],
        )


def clear_metal_sheet_table_row(connection, table_name, choice, dimension):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_clear_metal_sheet_table_row(table_name, choice),
            [
                dimension,
            ],
        )


def delete_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_delete_table(table_name))


def insert_items(connection, table_name, dimension, price):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_insert_items(table_name),
            [dimension, price],
        )


def create_flanges_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_flanges_table(table_name))


def delete_entry(connection, table_name, choice, value):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_delete_entry(table_name, choice),
            [
                value,
            ],
        )


def create_clients_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_clients_table(table_name))


def insert_values(connection, table_name, choices, values):
    with get_cursor(connection) as cursor:
        cursor.execute(query_insert_values(table_name, choices, values))


def update_clients_table(
    connection,
    table_name,
    client_id,
    client_name,
    client_identification,
    client_address,
    client_email,
):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_update_clients_table(table_name),
            [
                client_name,
                client_identification,
                client_address,
                client_email,
                client_id,
            ],
        )


def update_table(connection, table_name, choices, values, set_item, set_item_value):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_update_table(table_name, choices, values, set_item, set_item_value)
        )


def create_contact_person_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_contact_person_table(table_name))


def read_table(connection, table_name, choice, value):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_read_table(table_name, choice),
            [
                value,
            ],
        )


def create_projects_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_projects_table(table_name))


def insert_items_kwargs(connection, table_name, choices, values):
    with get_cursor(connection) as cursor:
        cursor.execute(query_insert_items_kwargs(table_name, choices, values))


def create_offers_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_offers_table(table_name))


def create_offer_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_offer_table(table_name))


def create_standard_items_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_standard_products(table_name))


def create_products_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_products_table(table_name))


def create_offer_new_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_offer_new_table(table_name))


def alter_table_name(connection, table_name, new_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_alter_table_name(table_name, new_name))


def create_suppliers_table(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_suppliers_table(table_name))


def create_products_sold(connection, table_name, supplier_table):
    with get_cursor(connection) as cursor:
        cursor.execute(query_create_products_sold(table_name, supplier_table))


def get_items_supplier(connection, offer_name, supplier_table):
    with get_cursor(connection) as cursor:
        cursor.execute(query_get_items_supplier(offer_name, supplier_table))


def get_columns(connection, table_name):
    with get_cursor(connection) as cursor:
        cursor.execute(query_get_columns(table_name))


def create_temp_table(
    connection, offer_name, supplier_items_table, suppliers_table, supplier_name
):
    with get_cursor(connection) as cursor:
        cursor.execute(
            query_create_temp_table(
                offer_name, supplier_items_table, suppliers_table, supplier_name
            )
        )
        # return cursor.fetchall()


def truncate_table(connection, table_name):
    with get_cursor(connection) as cursor:
        query_truncate_table(table_name)
