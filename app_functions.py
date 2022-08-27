import contextlib
from dotenv import load_dotenv
import os
import platform
# from create_project_name import create_project_name

load_dotenv()


app_name = os.environ.get("APP_NAME")


def parent_directory():
    if platform.system() == "Windows":
        parent_directory = os.environ.get("WINDOWS_PARENT_DIRECTORY")
    else:
        parent_directory = os.environ.get("UBUNTU_PARENT_DIRECTORY")

    return os.path.expandvars(parent_directory)


def get_app_path():
    return os.path.join(parent_directory(), app_name)


def create_app_folder():
    with contextlib.suppress(FileExistsError):
        app_path = os.path.join(parent_directory(), app_name)
        os.mkdir(app_path)
        return f"{app_path}"


def get_project_path(project_name):
    app_path = os.path.join(parent_directory(), app_name)
    project_directory = project_name
    return os.path.join(app_path, project_directory)


def create_project_folder(project_name):
    project_path = get_project_path(project_name)
    folders = ["offer", "sent", "drawings"]
    with contextlib.suppress(FileExistsError):
        os.mkdir(project_path)
    for item in folders:
        folder_path = os.path.join(project_path, item)
        with contextlib.suppress(FileExistsError):
            os.mkdir(folder_path)


def modify_project_folder_name(project_name, old_project_name):

    old_project_path = get_project_path(old_project_name)
    # print(old_project_path)
    new_project_path = get_project_path(project_name)
    # print(new_project_path)
    os.rename(old_project_path, new_project_path)


# create_app_folder()
# print(create_app_folder())
# create_project_folder("new_project")

# print(create_project_folder("new_project3"))
# print(get_app_path())
# print(get_project_path("bought offer test"))
# print(check_folder_open("New project 2"))
