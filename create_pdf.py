from fpdf import FPDF

# import working_databases as database

width = 195 / 2  # Half of width of A4
height = 270 / 9  # 9 Rows in one A4


# data = database.get_selected_table("excel test offer")


# data = [
#     (
#         "Spital Hunedoara",
#         "1/1",
#         "Tubulatura rectangulara",
#         "500x300",
#         "L1230",
#         "Some text",
#     ),
#     (
#         "Spital Hunedoara",
#         "1/2",
#         "Tubulatura rectangulara",
#         "500x300",
#         "L1230",
#         "Some text",
#     ),
#     ("Spital Hunedoara", "1/3", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/4", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/5", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/6", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/7", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/8", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/9", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/10", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     (
#         "Spital Hunedoara",
#         "1/11",
#         "Tubulatura rectangulara",
#         "500x300",
#         "L1230",
#         "Some text",
#     ),
#     (
#         "Spital Hunedoara",
#         "1/12",
#         "Tubulatura rectangulara",
#         "500x300",
#         "L1230",
#         "Some text",
#     ),
#     (
#         "Spital Hunedoara",
#         "1/13",
#         "Tubulatura rectangulara",
#         "500x300",
#         "L1230",
#         "Some text",
#     ),
#     ("Spital Hunedoara", "1/14", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/15", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/16", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/17", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/18", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/19", "Tubulatura rectangulara", "500x300", "L1230", ""),
#     ("Spital Hunedoara", "1/20", "Tubulatura rectangulara", "500x300", "L1230", ""),
# ]


class CustomPDF(FPDF):
    def create_cell(
        self,
        x,
        y,
        client_name,
        item_no,
        item_name,
        item_ch1=False,
        item_ch2=False,
        item_ch3=False,
    ):
        self.cell(width, height, border=1, align="C")
        self.text(x + 60, y + 15, client_name)
        self.image("Climacool LOGO.jpg", x=x + 11, y=y + 11, w=49, h=10)
        self.text(x + 15, y + 30, item_no)
        self.text(x + 60, y + 20, item_name)
        if item_ch1 and item_ch2 and item_ch3:
            self.text(x + 40, y + 26, item_ch1)
            self.text(x + 40, y + 32, item_ch2)
            self.text(x + 40, y + 38, item_ch3)

        elif item_ch1 and item_ch2:
            self.text(x + 40, y + 27, item_ch1)
            self.text(x + 40, y + 35, item_ch2)
        elif item_ch1:
            self.text(x + 40, y + 30, item_ch1)


class CreatePDFLabels(CustomPDF):
    def __init__(self, offer, offer_name) -> None:
        super().__init__()
        self.offer = offer
        self.offer_name = offer_name

    def create_labels(self):
        custom_PDF = CustomPDF("P", "mm", "A4")
        custom_PDF.set_font("times", "", 12)
        custom_PDF.t_margin = 10
        for i in range(len(self.offer)):

            if i == 0 or i % 16 == 0:
                custom_PDF.add_page()
                current_y = 10
            if i % 2 == 0:
                project_name = self.offer[i][0]
                item_no = self.offer[i][1]
                item_name = self.offer[i][2]
                item_ch1 = None or self.offer[i][3]
                item_ch2 = None or self.offer[i][4]
                item_ch3 = None or self.offer[i][5]

                custom_PDF.create_cell(
                    0,
                    current_y - 10,
                    project_name,
                    item_no,
                    item_name,
                    item_ch1,
                    item_ch2,
                    item_ch3,
                )

                try:
                    project_name = self.offer[i + 1][0]
                    item_no = self.offer[i + 1][1]
                    item_name = self.offer[i + 1][2]
                    item_ch1 = None or self.offer[i + 1][3]
                    item_ch2 = None or self.offer[i + 1][4]
                    item_ch3 = None or self.offer[i + 1][5]

                    custom_PDF.create_cell(
                        100,
                        current_y - 10,
                        project_name,
                        item_no,
                        item_name,
                        item_ch1,
                        item_ch2,
                        item_ch3,
                    )
                    current_y = current_y + 30
                    custom_PDF.set_y(current_y)
                except Exception as e:
                    print(e)

        print("Creating Label Excel")
        custom_PDF.output(f"{self.offer_name}_labels.pdf")


# labels = CreatePDFLabels(data)
# labels.create_labels()
