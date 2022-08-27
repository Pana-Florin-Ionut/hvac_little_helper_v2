import working_databases as database
from offer_object import Object
from dotenv import load_dotenv
import items_config
import os
import manufactured_model, standard_model

load_dotenv()

standard_items_table = os.environ.get("STANDARD_ITEMS_TABLE")
manufactured_items_table = os.environ.get("MANUFACTURED_ITEMS_TABLE")
# bought = os.environ.get("BOUGHT")
offers_table = os.environ.get("OFFERS_TABLE")
projects_table = os.environ.get("PROJECTS_TABLE")


manufactured_item_list_values = list(items_config.manufactured.values())
manufactured_item_list_keys = list(items_config.manufactured)
standard_item_list_values = list(items_config.standard.values())
standard_item_list_keys = list(items_config.standard)


def standard_items():
    return [item[1] for item in database.get_selected_table(standard_items_table)]


def manufactured_items():
    return [item[1] for item in database.get_selected_table(manufactured_items_table)]


def clear_tables(table_name):
    """Delete old tables"""
    database.delete_table(table_name)


class GenerateOffer:
    def __init__(self, offer, offer_details) -> None:
        self.offer = offer
        self.offer_details = offer_details
        self.offer_name = self.offer_details[2]
        self.offer_metal_sheet_ch = self.offer_details[3]

    def generate_offer(self):
        """Generate offer"""
        print("generating offer")

        # sorting items
        for item in self.offer:
            # print(item)

            if "manufactured" in item[11].lower():
                if item[2].lower() in list(items_config.manufactured.values()):
                    values = self.manufactured(item)
                    insert_manufactured_items = {
                        "table_name": f'"{self.offer_name}"',
                        "choices": "(product_type, characteristics, thickness, area, flanges, corners, price_per_sqm, flanges_price, corners_price, price_per_um, label_A, label_B, label_C)",
                        "values": (
                            values["product_type"],
                            values["characteristics"],
                            values["thickness"],
                            values["area"],
                            values["flanges"],
                            values["corners"],
                            values["price_per_sqm"],
                            values["flanges_price"],
                            values["corners_price"],
                            values["price_per_um"],
                            values["label_A"],
                            values["label_B"],
                            values["label_C"],
                        ),
                        "set_item": "id",
                        "set_item_value": values["id"],
                    }

                    database.update_table(**insert_manufactured_items)

            elif "standard" in item[11].lower():
                if item[2].lower() in list(items_config.standard.values()):
                    values = self.standard(item)
                    # print(values)
                    insert_standard_items = {
                        "table_name": f'"{self.offer_name}"',
                        "choices": "(product_type, characteristics, thickness, area, price_per_sqm, price_per_um, label_A, label_B, label_C)",
                        "values": (
                            values["product_type"],
                            values["characteristics"],
                            values["standard_thickness"],
                            values["standard_area"],
                            values["price_per_sqm"],
                            values["price_per_um"],
                            values["label_A"],
                            values["label_B"],
                            values["label_C"],
                        ),
                        "set_item": "id",
                        "set_item_value": values["id"],
                    }
                    database.update_table(**insert_standard_items)

            elif "bought" in item[11].lower():
                values = self.bought(item)

                insert_bought_items = {
                    "table_name": f'"{self.offer_name}"',
                    "choices": "(product_type, characteristics)",
                    "values": (values["product_type"], values["characteristics"]),
                    "set_item": "id",
                    "set_item_value": values["id"],
                }

                database.update_table(**insert_bought_items)
            else:
                continue

    def manufactured(self, item):
        # print("manufactured")
        name_index = manufactured_item_list_values.index(item[2].lower())
        new_item = getattr(manufactured_model, manufactured_item_list_keys[name_index])(
            item
        )

        thickness = round(new_item.item_thickness(), 2)
        thickness_characteristics = database.read_row2(
            self.offer_metal_sheet_ch, "thickness", thickness
        )
        price_per_um = round(
            (
                new_item.area() * thickness_characteristics[3]
                + new_item.flange() * thickness_characteristics[4]
                + new_item.corners() * thickness_characteristics[5]
            ),
            2,
        )

        idx = new_item.item_id()
        product_type = new_item.item_name()
        characteristics = new_item.characteristics()
        thickness = thickness
        area = new_item.area()
        flanges = new_item.flange()
        corners = new_item.corners()
        price_per_sqm = round(thickness_characteristics[3], 2)
        flanges_price = round(thickness_characteristics[4], 2)
        corners_price = round(thickness_characteristics[5], 2)
        price_per_um = price_per_um
        label_A = new_item.label_field_A()
        label_B = new_item.label_field_B()
        label_C = new_item.label_field_C()

        return {
            "id": idx,
            "product_type": product_type,
            "characteristics": characteristics,
            "thickness": thickness,
            "area": area,
            "flanges": flanges,
            "corners": corners,
            "price_per_sqm": price_per_sqm,
            "flanges_price": flanges_price,
            "corners_price": corners_price,
            "price_per_um": price_per_um,
            "label_A": label_A,
            "label_B": label_B,
            "label_C": label_C,
        }

    def standard(self, item):
        # print("standard")
        name_index = standard_item_list_values.index(item[2].lower())
        new_item = getattr(standard_model, standard_item_list_keys[name_index])(item)
        idx = new_item.item_id()
        # print(f"idx: {idx}")
        product_type = new_item.item_name()
        characteristics = new_item.name_characteristics()
        item_dimensions = new_item.item_dimensions()
        standard_item = database.get_standard_item(product_type, item_dimensions)
        standard_thickness = standard_item[5]
        standard_area = standard_item[6]
        thickness_characteristics = database.read_row2(
            self.offer_metal_sheet_ch, "thickness", standard_thickness
        )
        price_per_sqm = round(thickness_characteristics[3], 2)
        price_per_um = round(standard_area * price_per_sqm, 2)
        price_per_um = price_per_um
        label_A = new_item.label_field_A()
        label_B = new_item.label_field_B()
        label_C = new_item.label_field_C()

        return {
            "id": idx,
            "product_type": product_type,
            "characteristics": characteristics,
            "standard_thickness": standard_thickness,
            "standard_area": standard_area,
            "price_per_sqm": price_per_sqm,
            "price_per_um": price_per_um,
            "label_A": label_A,
            "label_B": label_B,
            "label_C": label_C,
        }

    def bought(self, item):

        if item[2].lower() in list(items_config.standard.values()):
            return self.standard(item)
        elif item[2].lower() in list(items_config.manufactured.values()):
            return self.manufactured(item)
        else:
            item = Object(item)
            idx = item.item_id()
            product_type = item.name()
            characteristics = " ".join(map(str, item.characteristics()))
            return {
                "id": idx,
                "product_type": product_type,
                "characteristics": characteristics,
            }

    def generate_labels_from_excel(self):
        print(self.offer_details)

    def get_offer_labels(self):
        pass


# offer_name = "excel test offer"
# offer = database.get_selected_table(offer_name)
# offer_details = database.read_row("offers_table", "offer_name", offer_name)
# generated_offer = GenerateOffer(offer, offer_details)
# project = database.read_row2(projects_table, "id", offer_details[1])
# print(project)
# generated_offer.generate_labels_from_excel()
# # generated_offer.generate_offer()
