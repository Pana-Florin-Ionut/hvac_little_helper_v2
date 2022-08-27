import pandas as pd
import working_databases as database
import app_functions


class MakeExcel:
    def __init__(
        self, project_name, offer_name, offer, offer_type=None, supplier_name=None
    ) -> None:
        self.offer = offer
        self.offer_name = offer_name
        self.project_name = project_name
        self.offer_type = offer_type
        self.supplier_name = supplier_name

    def create_full_table_excel(self):
        columns = database.get_columns(self.offer_name)
        columns = [column[0] for column in columns]
        # print(columns)
        path = app_functions.get_project_path(self.project_name)
        # print(f"PATH:   {path}")
        if self.offer_type:
            self.offer_name = f"{self.offer_name}_{self.offer_type}"
        if self.supplier_name:
            self.offer_name = f"{self.offer_name}_{self.supplier_name}"
        print(self.offer_name)
        df = pd.DataFrame(self.offer, columns=columns)
        df.set_index("id", inplace=True)
        print(df)

        df.to_excel(f"{path}//offer//{self.offer_name}.xlsx")

    def create_excel_table_from_temp(self):
        columns = database.get_columns("temp_table")
        print(columns)
        columns = [column[0] for column in columns]
        # print(columns)
        path = app_functions.get_project_path(self.project_name)
        # print(f"PATH:   {path}")
        if self.offer_type:
            self.offer_name = f"{self.offer_name}_{self.offer_type}"
        if self.supplier_name:
            self.offer_name = f"{self.offer_name}_{self.supplier_name}"
        print(self.offer_name)
        df = pd.DataFrame(self.offer, columns=columns)
        df.set_index("id", inplace=True)
        print(df)

        df.to_excel(f"{path}//offer//{self.offer_name}.xlsx")
