from create_connections import get_connection
import create_databases2 as database

# Working with tables


def get_selected_table(table_name):
    """Return a table"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(database.query_select_table(table_name))
            return cursor.fetchall()


def create_metal_sheet_price_table(table_name):
    with get_connection() as connection:
        database.create_metal_sheet_table(connection, table_name)


def insert_metal_sheet_price(
    table_name, thickness, price_per_ton, kg_per_sqm, flanges_price, corners_price
):
    with get_connection() as connection:
        database.insert_into_metal_sheet_price(
            connection,
            table_name,
            thickness,
            price_per_ton,
            kg_per_sqm,
            flanges_price,
            corners_price,
        )


def update_metal_sheet_price(table_name, thickness, price_per_ton, kg_per_sqm):
    with get_connection() as connection:
        database.update_into_metal_sheet_price(
            connection, table_name, thickness, price_per_ton, kg_per_sqm
        )


def clear_metal_sheet_entry(table_name, thickness):
    with get_connection() as connection:
        database.clear_metal_sheet_row(connection, table_name, thickness)


def clear_metal_sheet_table_row(table_name, choice, dimension):
    with get_connection() as connection:
        database.clear_metal_sheet_table_row(connection, table_name, choice, dimension)


def clear_table(table_name):
    with get_connection() as connection:
        database.clear_table(connection, table_name)


def read_row(table_name, choice, value):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                database.query_read_metal_sheet_row(table_name, choice),
                [
                    value,
                ],
            )
            return cursor.fetchone()


def read_row2(table_name, choice, value):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            # print(database.query_read_row(table_name, choice, value))
            cursor.execute(database.query_read_row(table_name, choice, value))
            return cursor.fetchone()


def get_standard_item(product_type, dimensions):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(database.query_get_standard_item(product_type, dimensions))
            return cursor.fetchone()


def create_metal_sheet_tables(table_name):
    with get_connection() as connection:
        database.create_metal_sheet_tables(connection, table_name)


def insert_metal_sheet_name(table_name, sheet_name):
    with get_connection() as connection:
        database.insert_metal_sheet_name(connection, table_name, sheet_name)


def delete_table(table_name):
    with get_connection() as connection:
        database.delete_table(connection, table_name)


def insert_all_items(args):
    with get_connection() as connection:
        database.insert_items(connection, **args)


def create_flanges_table(table_name):
    with get_connection() as connection:
        database.create_flanges_table(connection, table_name)


def delete_entry(table_name, choice, value):
    """DELETE FROM {table} WHERE {choice} = %s CASCADE
    table_name - table to delete item,
    choice - WHERE cause name,
    value - WHERE cause value"""
    with get_connection() as connection:
        database.delete_entry(connection, table_name, choice, value)


def create_clients_table(table_name):
    with get_connection() as connection:
        database.create_clients_table(connection, table_name)


def insert_items(table_name, choices, values):
    with get_connection() as connection:
        database.insert_values(connection, table_name, choices, values)


def update_clients_table(
    table_name,
    client_id,
    client_name,
    client_identification,
    client_address,
    client_email,
):
    with get_connection() as connection:
        database.update_clients_table(
            connection,
            table_name,
            client_id,
            client_name,
            client_identification,
            client_address,
            client_email,
        )


def update_table(table_name, choices, values, set_item, set_item_value):
    with get_connection() as connection:
        database.update_table(
            connection, table_name, choices, values, set_item, set_item_value
        )


def update_table_kwags(items):
    with get_connection() as connection:
        database.update_table(connection, **items)


def create_contact_person_table(table_name):
    with get_connection() as connection:
        database.create_contact_person_table(connection, table_name)


def read_table(table_name, choice, value):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(database.query_read_table(table_name, choice, value))
            return cursor.fetchall()


def create_projects_table(table_name):
    with get_connection() as connection:
        database.create_projects_table(connection, table_name)


def insert_items_kwargs(items):
    with get_connection() as connection:
        database.insert_items_kwargs(connection, **items)


def create_offers_table(table_name):
    with get_connection() as connection:
        database.create_offers_table(connection, table_name)


def create_offer_table(table_name):
    with get_connection() as connection:
        database.create_offer_table(connection, table_name)


def create_standard_items_table(table_name):
    with get_connection() as connection:
        database.create_standard_items_table(connection, table_name)


def execute(query):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            cursor.fetchall()


def execute2(query):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)


def create_products_table(table_name):
    with get_connection() as connection:
        database.create_products_table(connection, table_name)


def create_offer_new_table(table_name):
    with get_connection() as connection:
        database.create_offer_new_table(connection, table_name)


def alter_table_name(table_name, new_name):
    with get_connection() as connection:
        database.alter_table_name(connection, table_name, new_name)


def create_suppliers_table(table_name):
    with get_connection() as connection:
        database.create_suppliers_table(connection, table_name)


def create_products_sold(table_name, supplier_table):
    with get_connection() as connection:
        database.create_products_sold(connection, table_name, supplier_table)


def get_items_supplier(offer_name, supplier_items_table, suppliers_table):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                database.query_get_items_supplier(
                    offer_name, supplier_items_table, suppliers_table
                )
            )
            # print(f"Multiple items -------{cursor.fetchall()}")

            return cursor.fetchall()


def get_items_single_supplier(
    offer_name, supplier_items_table, suppliers_table, supplier_name
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                database.query_get_single_supplier_items(
                    offer_name, supplier_items_table, suppliers_table, supplier_name
                )
            )
            # print(f"Single item -------{cursor.fetchall()}")
            return cursor.fetchall()


def get_columns(table_name):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(database.query_get_columns(table_name))
            return cursor.fetchall()


# print(get_columns("test offer 3"))


def create_temp_table(offer_name, supplier_items_table, suppliers_table, supplier_name):
    with get_connection() as connection:
        database.create_temp_table(
            connection, offer_name, supplier_items_table, suppliers_table, supplier_name
        )


def get_labels(offer_name):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(database.query_get_labels(offer_name))
            return cursor.fetchall()


def truncate_table(table_name):
    with get_connection() as connection:
        database.truncate_table(connection, table_name)
