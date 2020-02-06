from src import GalileoSdk

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)


def test_create_project():
    project = galileo.projects.create_project("test_project", "description")

    assert project["project"]["name"] == "test_project"
    assert project["project"]["description"] == "description"


def test_list_projects():
    project_list = galileo.projects.list_projects()
    project_list["projects"].sort(key=lambda project: project["creation_timestamp"])

    assert project_list["projects"][-1]["name"] == "test_project"
    assert project_list["projects"][-1]["description"] == "description"


def test_upload_file():
    project = galileo.projects.create_project("project", "upload single file")
    project = project["project"]
    open("test_upload_file.txt", "wb")

    print(project["id"])

    file = {"upload_file": open("test_upload_file.txt", "rb")}
    galileo.projects.upload_single_file(project["id"], file)
