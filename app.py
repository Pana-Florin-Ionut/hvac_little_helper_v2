# from create_connections import get_connection, get_cursor
# from database_model import Database

from flask import (
    Flask,
    flash,
    make_response,
    render_template,
    request,
    redirect,
    session,
    url_for,
)

from flask_forms import (
    CreateOfferForm,
    CreateOfferNameForm,
    FileUploadForm,
    MetalSheetForm,
    CreateMetalSheetForm,
    AddClientsForm,
    AddContactPerson,
    CreateProjectsForm,
    CreateStandardItemsForm,
    InsertProductDimensionForm,
    SuppliersForm,
    ProductsSoldForm,
)

from item_algorithm import GenerateOffer
from app_functions import (
    create_app_folder,
    create_project_folder,
    modify_project_folder_name,
)
import working_databases as database
import psycopg2
from dotenv import load_dotenv
import os
from create_excel import MakeExcel
from create_project_name import create_project_name
from create_pdf import CreatePDFLabels
from werkzeug.utils import secure_filename
from import_excel import Read_Excel
from name_configs import App_name, Os_config, Database_config

load_dotenv()

app = Flask(__name__)

ALLOWED_EXTENSION = {"xlsx", "xls"}

app.secret_key = os.environ.get("APP_SECRET_KEY")

clients_table = Database_config.CLIENTS_TABLE
contact_person_table = Database_config.CONTACT_PERSON_TABLE
projects_table = Database_config.PROJECTS_TABLE
offers_table = Database_config.OFFERS_TABLE
complete_offer_table = Database_config.COMPLETE_OFFER_TABLE
standard_items_table = Database_config.STANDARD_ITEMS_TABLE
suppliers_table = Database_config.SUPPLIERS_TABLE
supplier_sold_items_table = Database_config.SUPPLIER_SOLD_ITEMS_TABLE
create_app_folder()

# database = Database(get_connection, get_cursor)


def create_databases():
    database.create_clients_table(clients_table)
    database.create_contact_person_table(contact_person_table)
    database.create_projects_table(projects_table)
    database.create_offers_table(offers_table)
    database.create_metal_sheet_tables("metal sheet types")
    database.create_standard_items_table(standard_items_table)
    database.create_suppliers_table(suppliers_table)
    database.create_products_sold(supplier_sold_items_table, suppliers_table)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/create_metal_sheet", methods=["GET", "POST"])
def create_metal_sheet():
    form = CreateMetalSheetForm(request.form)
    tables = database.get_selected_table("metal sheet types")
    try:

        if form.validate_on_submit():
            flash("Submit")
            material = form.material.data
            database.insert_metal_sheet_name("metal sheet types", material)
            database.create_metal_sheet_price_table(material)
            tables = database.get_selected_table("metal sheet types")

            return render_template("/create_metal_sheet.html", form=form, tables=tables)

        elif request.method == "GET":
            flash("GET")
            return render_template("/create_metal_sheet.html", form=form, tables=tables)
        else:
            flash("error")
    except TypeError as e:
        print(e)
        return render_template("/create_metal_sheet.html", form=form, tables=tables)
    except psycopg2.errors.UniqueViolation as e:
        print(e)
        flash("Table already exists")
        return render_template("/create_metal_sheet.html", form=form, tables=tables)


@app.route("/metal_sheet/<name>", methods=["GET", "POST"])
def metal_sheet(name):
    form = MetalSheetForm(request.form)
    items = database.get_selected_table(name)
    try:
        if form.validate_on_submit():
            flash("Post")
            thickness = form.thickness.data
            price_per_ton = form.price_per_ton.data
            kg_per_sqm = form.kg_per_sqm.data
            flanges_price = form.flanges_price.data
            corners_price = form.corners_price.data
            database.insert_metal_sheet_price(
                name, thickness, price_per_ton, kg_per_sqm, flanges_price, corners_price
            )
            items = database.get_selected_table(name)

            return render_template(
                "/metal_sheet.html", form=form, items=items, name=name
            )
        elif request.method == "GET":
            flash("GET")
            return render_template(
                "/metal_sheet.html", form=form, items=items, name=name
            )
    except TypeError as e:
        print(e)
        return render_template("/metal_sheet.html", form=form, items=items, name=name)
    except psycopg2.errors.UniqueViolation as e:
        print(e)
        flash("Dimension already exists")
        return render_template("/metal_sheet.html", form=form, items=items, name=name)


@app.route("/metal_sheet_delete")
def metal_sheet_delete():
    try:
        metal_sheet_to_delete = request.args.get("table")
        # print(metal_sheet_to_delete)

        database.clear_metal_sheet_table_row(
            "metal sheet types", "table_name", metal_sheet_to_delete
        )
        database.delete_table(metal_sheet_to_delete)

        return redirect("/create_metal_sheet")
    except psycopg2.errors.UndefinedTable as e:
        print(e)
        flash("Table not found")
        return redirect("/create_metal_sheet")


@app.route("/delete_metal_sheet_thickness")
def delete_metal_sheet_thickness():
    try:
        dimension_to_delete = request.args.get("dimension_to_delete")
        choice = request.args.get("choice")
        table = request.args.get("table")
        name = request.args.get("name")
        database.clear_metal_sheet_table_row(name, choice, dimension_to_delete)
        response = make_response(
            # redirect(f"/metal_sheet?table={table}&name={name}.html")
            redirect(f"/metal_sheet?table={table}&name={name}")
        )
        return response
    except TypeError as e:
        print(f"TypeError - {e}")
        flash(e)
    except Exception as e:
        print(f"Exception: {e}")
        flash(e)


@app.route(
    "/update_metal_sheet_entrys/<table_name>/<dimension_to_update>",
    methods=["GET", "POST"],
)
def update_metal_sheet_entrys(table_name, dimension_to_update):
    form = MetalSheetForm(request.form)
    dimension_to_update = database.read_row(
        table_name, "thickness", dimension_to_update
    )
    items = database.get_selected_table(table_name)

    if request.method != "POST":
        return render_template(
            "/update_metal_sheet_entrys.html",
            form=form,
            items=items,
            dimension_to_update=dimension_to_update,
        )
    try:
        thickness = form.thickness.data
        price_per_ton = form.price_per_ton.data
        kg_per_sqm = form.kg_per_sqm.data
        flanges_price = form.flanges_price.data
        corners_price = form.corners_price.data

        updated_items = {
            "table_name": table_name,
            "choices": "(thickness, price_per_ton, kg_per_sqm, flanges_price, corners_price)",
            "values": (
                thickness,
                price_per_ton,
                kg_per_sqm,
                flanges_price,
                corners_price,
            ),
            "set_item": "thickness",
            "set_item_value": dimension_to_update[0],
        }
        database.update_table(**updated_items)

        items = database.get_selected_table(table_name)

        return redirect(url_for("metal_sheet", name=table_name))
    except TypeError as e:
        print(f"TypeError - {e}")
        flash(e)
    except Exception as e:
        print(f"Exception: {e}")
        flash(e)
    return render_template(
        "/update_metal_sheet_entrys.html",
        form=form,
        items=items,
        dimension_to_update=dimension_to_update,
    )


@app.route("/add_clients", methods=["GET", "POST"])
def add_clients():
    form = AddClientsForm(request.form)
    table_name = clients_table
    database.create_clients_table(table_name)
    table = database.get_selected_table(table_name)
    try:
        if form.validate_on_submit():
            client_name = form.client_name.data
            client_identification = form.client_identification.data
            client_address = form.client_address.data
            client_email = form.client_email.data
            about = form.about.data

            choices = "client_name, client_identification, client_address, client_email, about"
            values = (
                client_name,
                client_identification,
                client_address,
                client_email,
                about,
            )
            database.insert_items(table_name, choices, values)
            table = database.get_selected_table(table_name)

    except Exception as e:
        flash(e)
        print(e)
    return render_template("add_clients.html", form=form, table=table)


@app.route("/delete_clients/<int:idx>", methods=["GET", "POST"])
def delete_clients(idx):
    clients = clients_table
    try:
        projects_to_delete = database.read_table(projects_table, "client_id", idx)
        for project in projects_to_delete:
            project_id = project[0]
            delete_project(project_id)
            offers_to_delete = database.read_table(
                offers_table, "project_id", project_id
            )
            for offer in offers_to_delete:
                database.delete_table(offer[2])
                database.delete_entry(offers_table, "offer_name", offer[2])
            database.delete_entry(projects_table, "id", project_id)
        database.delete_entry(contact_person_table, "client_id", idx)
        database.delete_entry(clients, "id", idx)
    except Exception as e:
        print(e)
        flash(e)
    return redirect("/clients")


# offers_to_delete = database.read_table(offers_table, "project_id", idx)
#     for offer in offers_to_delete:
#         database.delete_table(offer[2])
#     database.delete_entry(offers_table, "project_id", idx)
#     database.delete_entry(projects_table, "id", idx)


@app.route("/update_clients", methods=["GET", "POST"])
def update_clients():
    table_name = clients_table
    idx = request.args.get("id")
    # print(idx)
    client = database.read_row(table_name, "id", idx)
    form = AddClientsForm(request.form)
    try:
        if form.validate_on_submit():
            client_name = form.client_name.data
            client_identification = form.client_identification.data
            client_address = form.client_address.data
            client_email = form.client_email.data
            about = form.about.data
            choices = "(client_name, client_identification, client_address, client_email, about)"
            values = (
                client_name,
                client_identification,
                client_address,
                client_email,
                about,
            )
            set_item = "id"
            set_item_value = idx

            database.update_table(table_name, choices, values, set_item, set_item_value)
            return redirect("/add_clients")
    except psycopg2.errors.UniqueViolation:
        flash("There is allready a client with this name in the database")
    return render_template("/update_clients.html", client=client, form=form)


@app.route("/clients", methods=["GET", "POST"])
def clients():
    table_name = clients_table
    database.create_clients_table(table_name)
    # you can use global variables for this names, in an .env or something like this
    table = database.get_selected_table(table_name)
    return render_template("clients.html", table=table)


@app.route("/client_page", methods=["GET", "POST"])
def client_page():
    table_name = clients_table
    idx = request.args.get("id")
    database.create_contact_person_table("contact_person_table")
    client = database.read_row(table_name, "id", idx)
    persons = database.read_table(contact_person_table, "client_id", idx)
    projects = database.read_table(projects_table, "client_id", idx)
    return render_template(
        "/client_page.html", client=client, persons=persons, projects=projects
    )


@app.route("/add_contact_person", methods=["GET", "POST"])
def add_contact_person():
    form = AddContactPerson(request.form)
    clients_table_name = clients_table
    idx = request.args.get("id")
    client = database.read_row(clients_table_name, "id", idx)
    database.create_contact_person_table(contact_person_table)
    # this should be on separate function that will run once to create all table.
    persons = database.read_table(contact_person_table, "client_id", idx)

    try:
        if form.validate_on_submit():
            person_name = form.person_name.data
            person_phone = form.person_phone.data
            person_email = form.person_email.data
            person_departament = form.departament.data
            # items = {
            #     "table_name":contact_person_table,
            #     "choices":"client_id, person_name, person_phone, person_email, departament",
            #     "values":(idx, person_name, person_phone, person_email, person_departament)
            # }
            choices = "client_id, person_name, person_phone, person_email, departament"
            values = (idx, person_name, person_phone, person_email, person_departament)
            database.insert_items(contact_person_table, choices, values)
            persons = database.read_table(contact_person_table, "client_id", idx)
            return render_template(
                "add_contact_person.html", form=form, client=client, persons=persons
            )
    except psycopg2.errors.UniqueViolation:
        flash("Allready exist a person with this name")

    except Exception as e:
        flash(e)

    return render_template(
        "add_contact_person.html", form=form, client=client, persons=persons
    )


@app.route("/update_contact_person", methods=["GET", "POST"])
def update_contact_person():
    person_id = request.args.get("person_id")
    person = database.read_row(contact_person_table, "id", person_id)
    form = AddContactPerson(request.form)
    try:
        if form.validate_on_submit():
            person_name = form.person_name.data
            person_phone = form.person_phone.data
            person_email = form.person_email.data
            person_departament = form.departament.data
            choices = "(person_name, person_phone, person_email, departament)"
            values = (
                person_name,
                person_phone,
                person_email,
                person_departament,
            )
            database.update_table(
                contact_person_table, choices, values, "id", person_id
            )
            flash("Update Ok")
            person = database.read_row(contact_person_table, "id", person_id)

            return render_template(
                "update_contact_person.html", form=form, person=person
            )
    except Exception as e:
        print(e)
    return render_template("update_contact_person.html", form=form, person=person)


@app.route("/delete_contact_person", methods=["GET", "POST"])
def delete_contact_person():
    table_name = contact_person_table
    idx = request.args.get("id")
    client_id = request.args.get("client_id")
    print(idx)
    try:
        items = {
            "table_name": table_name,
            "choice": "id",
            "value": idx,
        }
        database.delete_entry(**items)
    except Exception as e:
        print(e)
    return make_response(redirect(f"/client_page?id={client_id}"))


@app.route("/projects", methods=["GET", "POST"])
def projects():
    table_name = projects_table
    database.create_projects_table(table_name)
    get_projects_table = database.get_selected_table(table_name)

    return render_template("projects.html", projects=get_projects_table)


@app.route("/create_projects", methods=["GET", "POST"])
def create_projects():
    table_name = projects_table
    form = CreateProjectsForm(request.form)
    # this should be run at the start of application# this should be run at the start of application
    client_id = request.args.get("id")
    client = database.read_row(clients_table, "id", client_id)
    client_name = client[1]
    try:
        if form.validate_on_submit():
            project_name = form.project_name.data
            project_address = form.project_address.data
            about = form.about.data
            items = {
                "table_name": table_name,
                "choices": "(client_id, client_name, project_name, project_address, about)",
                "values": (
                    client_id,
                    client_name,
                    project_name,
                    project_address,
                    about,
                ),
            }
            database.insert_items_kwargs(items)
            project_id = database.read_row(table_name, "project_name", project_name)[0]
            project_folder_name = f"P{project_id} - {project_name}"
            create_project_folder(project_folder_name)
            return redirect("/projects")
    except psycopg2.errors.UniqueViolation:
        flash("This name project is already taken. Please try another project name")
    except Exception as e:
        print(e)
        # flash(e)

    return render_template("/create_projects.html", form=form, client=client)


@app.route("/update_project/<int:idx>", methods=["GET", "POST"])
def update_project(idx):
    project = database.read_row(projects_table, "id", idx)
    project_id = project[0]
    old_project_id = project[0]
    old_project_name = project[3]
    old_project_folder_name = create_project_name(old_project_id, old_project_name)
    # old_project_folder_name = f"P{old_project_id} - {old_project_name}"
    form = CreateProjectsForm(request.form)
    form.project_address.data = project[4]
    form.about.data = project[5]

    try:
        if request.method == "POST":
            table_name = projects_table
            project_name = form.project_name.data
            project_address = form.project_address.data
            about = form.about.data
            items = {
                "table_name": table_name,
                "choices": "(project_name, project_address, about)",
                "values": (
                    project_name,
                    project_address,
                    about,
                ),
                "set_item": "id",
                "set_item_value": idx,
            }

            # new_project_folder_name = f"P{project_id} - {project_name}"
            new_project_folder_name = create_project_name(project_id, project_name)
            project_list = [
                name[3] for name in database.get_selected_table(projects_table)
            ]
            if project_name not in project_list:
                modify_project_folder_name(
                    new_project_folder_name, old_project_folder_name
                )
                database.update_table_kwags(items)
                return redirect("/projects")
            else:
                flash(
                    "This name project is already taken. Please try another project name"
                )

    # except psycopg2.errors.UniqueViolation as e:
    #     flash("This name project is already taken. Please try another project name")
    #     print(e)
    except PermissionError:
        flash("The folder is open, please close it and try again")
        # print(e)
    except Exception as e:
        print(e)
        return render_template("/update_project.html", project=project, form=form)

    return render_template("/update_project.html", project=project, form=form)


@app.route("/delete_project/<int:idx>", methods=["GET", "POST"])
def delete_project(idx):
    offers_to_delete = database.read_table(offers_table, "project_id", idx)
    for offer in offers_to_delete:
        database.delete_table(offer[2])
    database.delete_entry(offers_table, "project_id", idx)
    database.delete_entry(projects_table, "id", idx)

    # This function should delete project files and folders too
    return redirect("/projects")


@app.route("/project_page/<int:idx>", methods=["GET", "POST"])
def project_page(idx):
    try:
        project = database.read_row(projects_table, "id", idx)
        offers = database.read_table(offers_table, "project_id", idx)
        return render_template("/project_page.html", project=project, offers=offers)
    except psycopg2.errors.UndefinedTable:
        return render_template("/project_page.html", project=project)


@app.route("/create_new_offer/<int:idx>", methods=["GET", "POST"])
def create_new_offer(idx):
    """Create a new offer, redirect to offer page"""
    form = CreateOfferNameForm(request.form)
    table_name = offers_table
    project = database.read_row(projects_table, "id", idx)
    try:
        if request.method == "POST":
            project_id = project[0]
            offer_name = form.offer_name.data
            metal_sheet_characteristics = form.metal_sheet_characteristics.data
            database.create_offers_table(offers_table)
            items = {
                "table_name": table_name,
                "choices": "(project_id, offer_name, metal_sheet_characteristics)",
                "values": (project_id, offer_name, metal_sheet_characteristics),
            }

            database.insert_items_kwargs(items)  # insert items in offers table
            # this needs to be fixed
            database.create_offer_new_table(offer_name)
            # database.create_offer_table(offer_name)
            offer_idx = database.read_row(table_name, "offer_name", offer_name)[0]
            return redirect(url_for("offer_page", idx=offer_idx))
    except Exception as e:
        print(f"Exception {e}")
        return render_template("/create_new_offer.html", form=form, project=project)
    return render_template("/create_new_offer.html", form=form, project=project)


@app.route("/update_offer/<offer_name>", methods=["GET", "POST"])
def update_offer(offer_name):
    offer_details = database.read_row2(offers_table, "offer_name", offer_name)
    form = CreateOfferNameForm(request.form)
    try:
        if request.method == "POST":
            project_id = offer_details[1]
            offer_name = form.offer_name.data
            metal_sheet_characteristics = form.metal_sheet_characteristics.data
            database.create_offers_table(offers_table)
            items = {
                "table_name": offers_table,
                "choices": "(project_id, offer_name, metal_sheet_characteristics)",
                "values": (project_id, offer_name, metal_sheet_characteristics),
                "set_item": "id",
                "set_item_value": offer_details[0],
            }
            database.update_table(**items)
            database.alter_table_name(offer_details[2], offer_name)
        else:
            form.offer_name.data = offer_details[2]
            form.metal_sheet_characteristics.data = offer_details[3]
    except Exception as e:
        print(e)
    return render_template("/update_offer.html", form=form, offer_name=offer_name)


@app.route("/delete_offer/<offer_name>", methods=["GET", "POST"])
def delete_offer(offer_name):
    database.delete_entry(offers_table, "offer_name", offer_name)
    database.delete_table(offer_name)
    return redirect("/offers")


@app.route("/offer_page/<int:idx>", methods=["GET", "POST"])
def offer_page(idx):
    """Offer page. Here you can see, add, modify and delete items from it"""
    form = CreateOfferForm()
    offer = database.read_row(offers_table, "id", idx)
    items = database.get_selected_table(offer[2])
    project_id = offer[1]
    project = database.read_row(projects_table, "id", project_id)

    return render_template(
        "/offer_page.html",
        form=form,
        offer=offer,
        project=project,
        items=items,
    )


@app.route("/generate_offer/<offer_name>", methods=["GET", "POST"])
def generate_offer(offer_name):
    offer = database.get_selected_table(offer_name)
    offer_details = database.read_row("offers_table", "offer_name", offer_name)
    g_offer = GenerateOffer(offer, offer_details)
    # g_offer.generate_offer()

    try:
        g_offer.generate_offer()
        offer = database.get_selected_table(offer_name)

    except TypeError as e:
        print(e)
        flash("There is a error in characteristics or an standard item was not found")
        return redirect(url_for("offer_page", idx=offer_details[0]))

    except KeyError as e:
        print(e)
        flash("There is no thickness")
        return redirect(url_for("offer_page", idx=offer_details[0]))
    return redirect(url_for("generated_offer", offer_name=offer_name))


@app.route("/generated_offer/<offer_name>", methods=["GET", "POST"])
def generated_offer(offer_name):
    generated_offer = database.get_selected_table(offer_name)
    offer_details = database.read_row("offers_table", "offer_name", offer_name)

    return render_template(
        "/generated_offer.html",
        generated_offer=generated_offer,
        offer_name=offer_name,
        idx=offer_details[0],
    )


@app.route("/generate_offer_excel/<offer_name>")
def generate_offer_excel(offer_name):
    # print(offer_name)
    try:
        offer = database.get_selected_table(offer_name)
        offer_details = database.read_row2(offers_table, "offer_name", offer_name)
        project_details = database.read_row2(projects_table, "id", offer_details[1])
        project_name = create_project_name(project_details[0], project_details[3])
        excel_offer = MakeExcel(project_name, offer_name, offer)
        excel_offer.create_full_table_excel()
        flash("Excel file exported!")
    except OSError:
        flash("Error: File or folder is opened. Close it and try again")

    return redirect(url_for("generated_offer", offer_name=offer_name))


@app.route("/generate_custom_offer_excel/<offer_name>/<offer_type>")
def generate_custom_offer_excel(offer_name, offer_type):
    # print(offer_name)
    try:
        offer = database.read_table(offer_name, "category", offer_type)
        offer_details = database.read_row2(offers_table, "offer_name", offer_name)
        project_details = database.read_row2(projects_table, "id", offer_details[1])
        project_name = create_project_name(project_details[0], project_details[3])
        # offer_name = f"{offer_name}_{offer_type}"
        excel_offer = MakeExcel(project_name, offer_name, offer, offer_type)
        excel_offer.create_full_table_excel()
        flash(f"{offer_type.capitalize()} Excel file exported!")
    except OSError:
        flash("Error: File or folder is opened. Close it and try again")

    return redirect(request.referrer)


@app.route("/generate_supplier_offer_table/<offer_name>/<offer_type>/<supplier_name>")
def generate_supplier_offer_table(offer_name, supplier_name, offer_type):
    try:
        # offer = database.read_table(offer_name, "category", "bought")
        database.create_temp_table(
            offer_name, supplier_sold_items_table, suppliers_table, supplier_name
        )
        offer = database.get_selected_table("temp_table")
        print(offer)
        offer_details = database.read_row2(offers_table, "offer_name", offer_name)
        project_details = database.read_row2(projects_table, "id", offer_details[1])
        project_name = create_project_name(project_details[0], project_details[3])
        # offer_name = f"{offer_name}_{offer_type}"
        excel_offer = MakeExcel(
            project_name, offer_name, offer, offer_type, supplier_name
        )
        print("creating excel")
        excel_offer.create_excel_table_from_temp()
        print("exporting_excel")
        flash(f"{offer_type.capitalize()} from {supplier_name} Excel file exported!")
    except OSError:
        flash("Error: File or folder is opened. Close it and try again")
    finally:
        database.delete_table("temp_table")

    return redirect(request.referrer)


@app.route("/manufactured_items/<offer_name>", methods=["POST", "GET"])
def manufactured_items(offer_name):
    """Getting manufactured items"""
    offer = database.read_table(offer_name, "category", "manufactured")
    # print(offer)

    return render_template(
        "/manufactured_items.html", offer=offer, offer_name=offer_name
    )


@app.route("/bought_items/<offer_name>", methods=["POST", "GET"])
def bought_items(offer_name):
    """Getting bought items"""
    offer = database.read_table(offer_name, "category", "bought")
    table = database.get_items_supplier(
        offer_name, supplier_sold_items_table, suppliers_table
    )

    return render_template(
        "/bought_items.html", offer=offer, offer_name=offer_name, table=table
    )


@app.route("/bought_items/<offer_name>/<supplier_name>")
def bought_items_supplier(offer_name, supplier_name):
    # print(offer_name)
    # offer = database.read_table(offer_name, "category", "bought")
    table = database.get_items_single_supplier(
        offer_name, supplier_sold_items_table, suppliers_table, supplier_name
    )

    return render_template(
        "bought_items_supplier.html",
        offer_name=offer_name,
        table=table,
        supplier_name=supplier_name,
    )


@app.route("/standard_offer_items/<offer_name>", methods=["GET", "POST"])
def standard_offer_items(offer_name):
    """Displaying standard items"""
    offer = database.read_table(offer_name, "category", "standard")

    return render_template(
        "/standard_offer_items.html", offer=offer, offer_name=offer_name
    )


@app.route("/offers", methods=["GET", "POST"])
def offers():
    """Page with all offers"""
    offers = database.get_selected_table(offers_table)

    return render_template("offers.html", offers=offers)


@app.route("/insert_offer_items/<int:idx>", methods=["POST", "GET"])
def insert_offer_items(idx):
    form = CreateOfferForm()
    offer_detail = database.read_row(offers_table, "id", idx)
    project_id = offer_detail[1]
    offer_name = offer_detail[2]
    offer = database.get_selected_table(offer_name)

    try:
        if request.method == "POST":
            no = form.no.data
            item = form.item.data
            characteristics_A = form.characteristics_A.data
            characteristics_B = form.characteristics_B.data
            characteristics_C = form.characteristics_C.data
            characteristics_D = form.characteristics_D.data
            characteristics_E = form.characteristics_E.data
            characteristics_F = form.characteristics_F.data
            um = form.um.data
            quantity = form.quantity.data
            category = form.category.data
            observations = form.observations.data

            items = {
                "table_name": f'"{offer_name}"',
                "choices": """(id, 
                project_id, 
                item,
                characteristics_A,
                characteristics_B,
                characteristics_C,
                characteristics_D,
                characteristics_E,
                characteristics_F,
                um,
                quantity,
                category,
                observations)""",
                "values": (
                    no,
                    project_id,
                    item,
                    characteristics_A,
                    characteristics_B,
                    characteristics_C,
                    characteristics_D,
                    characteristics_E,
                    characteristics_F,
                    um,
                    quantity,
                    category,
                    observations,
                ),
            }
            database.insert_items_kwargs(items)

        else:
            flash("Else")
            form.no.data = None
            form.item.data = None
            form.characteristics_A.data = None
            form.characteristics_B.data = None
            form.characteristics_C.data = None
            form.characteristics_D.data = None
            form.characteristics_E.data = None
            form.characteristics_F.data = None
            form.um.data = None
            form.quantity.data = None
            form.category.data = None
            form.observations.data = None
        offer = database.get_selected_table(offer_name)

        form.no.data = None
        form.item.data = None
        form.characteristics_A.data = None
        form.characteristics_B.data = None
        form.characteristics_C.data = None
        form.characteristics_D.data = None
        form.characteristics_E.data = None
        form.characteristics_F.data = None
        form.um.data = None
        form.quantity.data = None
        form.category.data = None
        form.observations.data = None

    except psycopg2.errors.UniqueViolation:
        flash("There is an item with same number")

    except Exception as e:
        print(e)

    return render_template(
        "/insert_offer_items.html",
        form=form,
        offer_name=offer_name,
        offer_detail=offer_detail,
        offer=offer,
    )


@app.route("/update_offer_item/<offer_id>/<item_id>", methods=["GET", "POST"])
def update_offer_item(item_id, offer_id):
    form = CreateOfferForm()
    offer_detail = database.read_row2(offers_table, "id", offer_id)
    idx = offer_detail[0]
    offer_name = offer_detail[2]
    item = database.read_row2(offer_name, "id", item_id)
    offer = database.get_selected_table(offer_name)
    # database.pop_item()

    try:
        if request.method == "POST":
            no = form.no.data
            item = form.item.data
            characteristics_A = form.characteristics_A.data
            characteristics_B = form.characteristics_B.data
            characteristics_C = form.characteristics_C.data
            characteristics_D = form.characteristics_D.data
            characteristics_E = form.characteristics_E.data
            characteristics_F = form.characteristics_F.data
            um = form.um.data
            quantity = form.quantity.data
            category = form.category.data
            observations = form.observations.data

            items = {
                "table_name": f'"{offer_name}"',
                "choices": """
                (id, 
                item,
                characteristics_A,
                characteristics_B,
                characteristics_C,
                characteristics_D,
                characteristics_E,
                characteristics_F,
                um,
                quantity,
                category,
                observations)""",
                "values": (
                    no,
                    item,
                    characteristics_A,
                    characteristics_B,
                    characteristics_C,
                    characteristics_D,
                    characteristics_E,
                    characteristics_F,
                    um,
                    quantity,
                    category,
                    observations,
                ),
                "set_item": "id",
                "set_item_value": item_id,
            }
            # database.insert_items_kwargs(items)
            database.update_table(**items)

            return redirect(url_for("insert_offer_items", idx=idx))
        else:
            form.no.data = item[0]
            form.item.data = item[2]
            form.characteristics_A.data = item[3]
            form.characteristics_B.data = item[4]
            form.characteristics_C.data = item[5]
            form.characteristics_D.data = item[6]
            form.characteristics_E.data = item[7]
            form.characteristics_F.data = item[8]
            form.um.data = item[9]
            form.quantity.data = item[10]
            form.category.data = item[11]
            form.observations.data = item[12]
    except Exception as e:
        print(e)
    return render_template(
        "/insert_offer_items.html",
        form=form,
        offer_name=offer_name,
        offer_detail=offer_detail,
        offer=offer,
    )


@app.route("/delete_offer_item/<offer_name>/<item_id>")
def delete_offer_item(item_id, offer_name):
    offer_detail = database.read_row2(offers_table, "offer_name", offer_name)
    idx = offer_detail[0]
    database.delete_entry(offer_name, "id", item_id)
    return redirect(url_for("insert_offer_items", idx=idx))


@app.route("/standard_items", methods=["GET", "POST"])
def standard_items():  # sourcery skip: remove-unnecessary-else
    form = CreateStandardItemsForm(request.form)
    table = database.get_selected_table(standard_items_table)
    try:
        if request.method == "POST":
            item_name = form.item_name.data
            if "/" in item_name:
                flash("You cannot use '/' in item name")
                return render_template("/standard_items.html", form=form, table=table)

            about = form.about.data

            items = {
                "table_name": f'"{standard_items_table}"',
                "choices": "product_name, about",
                "values": (item_name, about),
            }
            database.insert_items(**items)

            database.create_products_table(item_name)
            table = database.get_selected_table(standard_items_table)

            return redirect(url_for("product", product_name=item_name))

    except psycopg2.errors.UniqueViolation:
        flash("There is allready an item with that name")

    return render_template("/standard_items.html", form=form, table=table)


@app.route("/update_standard_item/<item_name>", methods=["GET", "POST"])
def update_standard_item(item_name):
    form = CreateStandardItemsForm(request.form)
    table = database.get_selected_table(standard_items_table)

    try:
        item = database.read_row2(standard_items_table, "product_name", item_name)
        idx = item[0]
        if request.method == "POST":
            item_name = form.item_name.data
            if "/" in item_name:
                flash("You cannot use '/' in item name")
                return render_template("/standard_items.html", form=form, table=table)

            about = form.about.data

            items = {
                "table_name": f'"{standard_items_table}"',
                "choices": "(product_name, about)",
                "values": (item_name, about),
                "set_item": "id",
                "set_item_value": idx,
            }
            database.update_table(**items)
            database.alter_table_name(item[1], item_name)

            database.create_products_table(item_name)
            table = database.get_selected_table(standard_items_table)
            return redirect(url_for("standard_items"))
        else:
            form.item_name.data = item[1]
            form.about.data = item[2]

    except psycopg2.errors.UniqueViolation:
        flash("There is allready an item with that name")

    return render_template("/standard_items.html", form=form, table=table)


@app.route("/delete_standard_item/<int:idx>")
def delete_standard_item(idx):
    item_table = database.read_row2(standard_items_table, "id", idx)
    database.delete_table(item_table[1])
    database.delete_entry(standard_items_table, "id", idx)
    return redirect(url_for("standard_items"))


@app.route("/product/<product_name>", methods=["GET", "POST"])
def product(product_name):
    form = InsertProductDimensionForm(request.form)
    table = database.get_selected_table(product_name)
    try:
        if request.method == "POST":
            dim_A = form.dimension_A.data
            dim_B = float(form.dimension_B.data) if form.dimension_B.data else 0
            dim_C = float(form.dimension_C.data) if form.dimension_C.data else 0
            dim_D = float(form.dimension_D.data) if form.dimension_D.data else 0
            metal_sheet_thickness = form.metal_sheet_thickness.data
            area = float(form.area.data)
            about = form.about.data

            items = {
                "table_name": f'"{product_name}"',
                "choices": "dimension_A, dimension_B, dimension_C, dimension_D, metal_sheet_thickness, area, about",
                "values": (
                    dim_A,
                    dim_B,
                    dim_C,
                    dim_D,
                    metal_sheet_thickness,
                    area,
                    about,
                ),
            }
            database.insert_items(**items)
            table = database.get_selected_table(product_name)
        else:
            form.dimension_A.data = None
            form.dimension_B.data = None
            form.dimension_C.data = None
            form.dimension_D.data = None
            form.metal_sheet_thickness.data = None
            form.area.data = None
            form.about.data = None

    except psycopg2.errors.InvalidTextRepresentation:
        flash("Dimensions are type float")
    except ValueError:
        flash("Dimenions should be numbers or decimal numbers")
    except psycopg2.errors.UniqueViolation:
        flash("Dimensions should be unique")

    form.dimension_A.data = ""
    form.dimension_B.data = ""
    form.dimension_C.data = ""
    form.dimension_D.data = ""
    form.metal_sheet_thickness.data = ""
    form.area.data = ""
    form.about.data = ""

    return render_template(
        "/product.html", product_name=product_name, form=form, table=table
    )


@app.route("/product/update/<product_name>/<int:idx>", methods=["GET", "POST"])
def update_product(product_name, idx):
    form = InsertProductDimensionForm(request.form)
    table = database.get_selected_table(product_name)
    item = database.read_row2(product_name, "id", idx)
    try:
        if request.method == "POST":
            dim_A = form.dimension_A.data
            dim_B = float(form.dimension_B.data) if form.dimension_B.data else 0
            dim_C = float(form.dimension_C.data) if form.dimension_C.data else 0
            dim_D = float(form.dimension_D.data) if form.dimension_D.data else 0
            metal_sheet_thickness = form.metal_sheet_thickness.data
            area = float(form.area.data)
            about = form.about.data

            items = {
                "table_name": f'"{product_name}"',
                "choices": "(dimension_A, dimension_B, dimension_C, dimension_D, metal_sheet_thickness, area, about)",
                "values": (
                    dim_A,
                    dim_B,
                    dim_C,
                    dim_D,
                    metal_sheet_thickness,
                    area,
                    about,
                ),
                "set_item": "id",
                "set_item_value": idx,
            }
            database.update_table(**items)
            table = database.get_selected_table(product_name)
            return redirect(url_for("product", product_name=product_name))
        else:
            form.dimension_A.data = item[1]
            form.dimension_B.data = item[2]
            form.dimension_C.data = item[3]
            form.dimension_D.data = item[4]
            form.metal_sheet_thickness.data = item[5]
            form.area.data = item[6]
            form.about.data = item[7]

    except psycopg2.errors.InvalidTextRepresentation:
        flash("Dimensions are type float")
    except ValueError:
        flash("Dimenions should be numbers or decimal numbers")
    except psycopg2.errors.UniqueViolation:
        flash("Dimensions should be unique")

    return render_template(
        "/product.html", product_name=product_name, form=form, table=table
    )


@app.route("/delete_product/<product_name>/<idx>")
def delete_product(product_name, idx):
    database.delete_entry(product_name, "id", idx)
    return redirect(url_for("product", product_name=product_name))


@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():
    form = SuppliersForm(request.form)
    table = database.get_selected_table(suppliers_table)
    try:
        if request.method == "POST":
            supplier_name = form.supplier_name.data
            supplier_info = form.supplier_info.data
            supplier_address = form.supplier_address.data
            about = form.supplier_about.data

            items = {
                "table_name": suppliers_table,
                "choices": "supplier_name, supplier_info, supplier_address, about",
                "values": (supplier_name, supplier_info, supplier_address, about),
            }
            database.insert_items(**items)
            table = database.get_selected_table(suppliers_table)

        else:
            form.supplier_name.data = ""
            form.supplier_info.data = ""
            form.supplier_address.data = ""
            form.supplier_about.data = ""

    except psycopg2.errors.UniqueViolation:
        flash("There is already an item with that name")
    except Exception as e:
        print(e)

    return render_template("/suppliers.html", table=table, form=form)


@app.route("/supplier/<supplier_name>", methods=["GET", "POST"])
def supplier(supplier_name):
    supplier_details = database.read_row2(
        suppliers_table, "supplier_name", supplier_name
    )
    form = ProductsSoldForm(request.form)
    products_sold = database.read_table(
        supplier_sold_items_table, "supplier_id", supplier_details[0]
    )
    try:
        if request.method == "POST":
            product_sold = form.product_sold.data

            items = {
                "table_name": supplier_sold_items_table,
                "choices": "sold_item, supplier_id",
                "values": (product_sold, supplier_details[0]),
            }
            database.insert_items(**items)

            products_sold = database.read_table(
                supplier_sold_items_table, "supplier_id", supplier_details[0]
            )

            return render_template(
                "/supplier.html",
                form=form,
                supplier_details=supplier_details,
                products_sold=products_sold,
            )

    except psycopg2.errors.UniqueViolation:
        flash("There is already an item with that name")

    except Exception as e:
        flash(e)
        print(e)

    return render_template(
        "/supplier.html",
        form=form,
        supplier_details=supplier_details,
        products_sold=products_sold,
    )


@app.route("/delete_supplier/<supplier_name>")
def delete_supplier(supplier_name):
    supplier = database.read_row2(suppliers_table, "supplier_name", supplier_name)
    # print(supplier)
    try:
        database.delete_entry(supplier_sold_items_table, "supplier_id", supplier[0])
        database.delete_entry(suppliers_table, "supplier_name", supplier_name)
        return redirect(url_for("suppliers"))

    except TypeError as e:
        print(e)

    return redirect(url_for("suppliers"))


@app.route("/create_labels/<offer_name>")
def create_labels(offer_name):
    offer = database.get_labels(offer_name)
    offer_details = database.read_row2(offers_table, "offer_name", offer_name)
    project = database.read_row2(projects_table, "id", offer_details[1])
    project_name = project[3]
    labels = []
    for item in offer:
        for i in range(int(item[2])):
            item_no = f"{item[0]}/{int(i)+1}"
            labels.append((project_name, item_no, item[1], item[3], item[4], item[5]))

    print(labels)

    label_file = CreatePDFLabels(labels, offer_name)
    label_file.create_labels()

    return render_template(
        "/create_labels.html", offer_name=offer_name, project_name=project_name
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSION


@app.route("/upload_excel/<offer_name>", methods=["GET", "POST"])
def upload_excel(offer_name):
    form = FileUploadForm()
    offer_detail = database.read_row(offers_table, "offer_name", offer_name)
    offer_id = offer_detail[0]
    project_id = offer_detail[1]
    if request.method == "POST":
        if "file" not in request.files:
            flash("There was no file")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected ")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("File allowed")
            filename = secure_filename(file.filename)
            offer = Read_Excel(file)
            for item in offer.insert_items():
                database.truncate_table(offer_name)
                no = item[0]
                item_name = item[1]
                ch_A = str(item[2])
                ch_B = str(item[3]) if item[3] else 0
                ch_C = str(item[4]) if item[4] else 0
                ch_D = str(item[5]) if item[5] else 0
                ch_E = str(item[6]) if item[6] else 0
                ch_F = str(item[7]) if item[7] else 0
                um = item[8]
                quantity = item[9]
                category = item[10]
                observations = str(item[11]) if item[11] else 0

                items = {
                    "table_name": f'"{offer_name}"',
                    "choices": """(id, 
                project_id, 
                item,
                characteristics_A,
                characteristics_B,
                characteristics_C,
                characteristics_D,
                characteristics_E,
                characteristics_F,
                um,
                quantity,
                category,
                observations)""",
                    "values": (
                        no,
                        project_id,
                        item_name,
                        ch_A,
                        ch_B,
                        ch_C,
                        ch_D,
                        ch_E,
                        ch_F,
                        um,
                        quantity,
                        category,
                        observations,
                    ),
                }
                database.insert_items_kwargs(items)

            return redirect(url_for("offer_page", idx=offer_id))

    return render_template("upload_excel.html", form=form)


if __name__ == "__main__":
    # this should be created all the tables
    create_databases()
    app.run(debug=True)
