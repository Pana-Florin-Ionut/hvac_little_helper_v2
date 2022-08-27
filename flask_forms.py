from wtforms import StringField, SubmitField, FloatField, TextAreaField, FileField
from flask_wtf import FlaskForm as Form
from wtforms.validators import DataRequired


class PricesTableForm(Form):
    table = StringField("Table name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ItemPriceForm(Form):
    table = StringField("Table name", validators=[DataRequired()])
    dimension = StringField("Item dimension", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UpdateItemForm(Form):
    table = StringField("Table name", validators=[DataRequired()])
    dimension = StringField("Item dimension", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    surface = StringField("Surface", validators=[DataRequired()])
    submit = SubmitField("Submit")


class InsertItemForm(Form):
    table = StringField("Table name", validators=[DataRequired()])
    dimension = StringField("Item dimension", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    surface = FloatField("Surface", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateOfferForm(Form):
    no = StringField("Nr. Crt.", validators=[DataRequired()])
    item = StringField("Item", validators=[DataRequired()])
    characteristics_A = StringField("Characteristics_A")
    characteristics_B = StringField("Characteristics_B")
    characteristics_C = StringField("Characteristics_C")
    characteristics_D = StringField("Characteristics_D")
    characteristics_E = StringField("Characteristics_E")
    characteristics_F = StringField("Characteristics_F")
    um = StringField("UM", validators=[DataRequired()])
    quantity = StringField("Quantity", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    observations = StringField("Observations")
    submit = SubmitField()


class CreateOfferNameForm(Form):
    offer_name = StringField("Offer Name", validators=[DataRequired()])
    metal_sheet_characteristics = StringField("Metal Sheet Characteristics")
    submit = SubmitField("Submit")


class MetalSheetForm(Form):
    thickness = StringField("Metal Sheet Thickness", validators=[DataRequired()])
    price_per_ton = StringField("Price per Ton", validators=[DataRequired()])
    kg_per_sqm = StringField("Kg per Square meter", validators=[DataRequired()])
    flanges_price = StringField("Flanges price per meter", validators=[DataRequired()])
    corners_price = StringField("Corners price per um", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateMetalSheetForm(Form):
    material = StringField("Metal Sheet Material", validators=[DataRequired()])
    submit = SubmitField("Submit")


class MaterialForm(Form):
    material = StringField("Material dimension", validators=[DataRequired()])
    price = StringField("Price per UM", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddClientsForm(Form):
    client_name = StringField("Client name", validators=[DataRequired()])
    client_identification = StringField("Client identification")
    client_address = StringField("Client address")
    client_email = StringField("Client email")
    about = TextAreaField("About")
    submit = SubmitField("Submit")


class AddContactPerson(Form):
    person_name = StringField("Contact name", validators=[DataRequired()])
    person_phone = StringField("Contact phone")
    person_email = StringField("Contact email")
    departament = StringField("Departament")
    submit = SubmitField("Submit")


class CreateProjectsForm(Form):
    project_name = StringField("Project name", validators=[DataRequired()])
    project_address = TextAreaField("Project address")
    about = TextAreaField("About")
    submit = SubmitField("Submit")


class CreateStandardItemsForm(Form):
    item_name = StringField("Item name", validators=[DataRequired()])
    about = StringField("About")
    submit = SubmitField("Submit")


class InsertProductDimensionForm(Form):
    dimension_A = StringField("Dimension A", validators=[DataRequired()])
    dimension_B = StringField("Dimension B")
    dimension_C = StringField("Dimension C")
    dimension_D = StringField("Dimension D")
    metal_sheet_thickness = StringField(
        "Metal Sheet Thickness", validators=[DataRequired()]
    )
    area = StringField("Area", validators=[DataRequired()])
    about = StringField("About")
    submit = SubmitField("Submit")


class SuppliersForm(Form):
    supplier_name = StringField("Supplier name", validators=[DataRequired()])
    supplier_info = StringField("Supplier Information")
    supplier_address = StringField("Supplier Address")
    supplier_about = StringField("Supplier About")
    submit = SubmitField("Submit")


class ProductsSoldForm(Form):
    product_sold = StringField("Product sold", validators=[DataRequired()])
    submit = SubmitField("Submit")


class FileUploadForm(Form):
    file = FileField("Upload File", validators=[DataRequired()])
    upload = SubmitField("Upload")
