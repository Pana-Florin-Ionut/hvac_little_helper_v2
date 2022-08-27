import pandas as pd


class Read_Excel:
    def __init__(self, file):
        self.file = file

    def _get_items(self):
        return pd.read_excel(self.file)

    def insert_items(self):
        return self._get_items().values.tolist()


# new_excel = Read_Excel("flask_app/excel_test.xlsx", "offer_name")
# # print(new_excel.insert_items())
# for item in new_excel.insert_items():
#     print(item)
