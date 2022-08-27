from create_connections import get_connection
import create_databases as database

# Working with tables


def create_metal_sheet_price_table(table_name):
    with get_connection() as connection:
        database.create_metal_sheet_table(connection, table_name)


def insert_metal_sheet(table_name, thickness, price_per_ton, kg_per_sqm, price_per_sqm):
    with get_connection() as connection:
        database.insert_metal_sheet(
            connection, table_name, thickness, price_per_ton, kg_per_sqm, price_per_sqm
        )


def create_item_table(table_name):
    with get_connection() as connection:
        database.create_item_table(connection, table_name)


def create_offer_table(table_name):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(database.query_create_offer_table(table_name))


def get_selected_table(table_name):
    """Return a table"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(database.query_select_table(table_name))
            return cursor.fetchall()


def create_new_table(table_name):
    with get_connection() as connection:
        database.create_table(connection, table_name)


def insert_items_manufacturing(
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
    with get_connection() as connection:
        database.insert_items_into_offer(
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
        )


# def insert_items_manufacturing(
#     table_name, area, metal_sheet_price, manufacturing_price, additional_price
# ):
#     with get_connection() as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 (database.query_insert_items(table_name)),
#                 [area, metal_sheet_price, manufacturing_price, additional_price],
#             )


# def insert_into_offer(
#     table_name,
#     item,
#     characteristics_A,
#     characteristics_B,
#     characteristics_C,
#     characteristics_D,
#     characteristics_E,
#     characteristics_F,
#     characteristics_G,
#     characteristics_H,
#     isolation,
#     um,
#     quantity,
# ):
#     with get_connection() as connection:
#         database.insert_items_into_offer(
#             connection,
#             table_name,
#             item,
#             characteristics_A,
#             characteristics_B,
#             characteristics_C,
#             characteristics_D,
#             characteristics_E,
#             characteristics_F,
#             characteristics_G,
#             characteristics_H,
#             isolation,
#             um,
#             quantity,
#         )


# create_metal_sheet_price_table("zn160") #ok
