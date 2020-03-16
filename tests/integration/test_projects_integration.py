from galileo_sdk import GalileoSdk

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)


def test_create_project():
    project = galileo.projects.create_project("test_project", "description")

    assert project["project"]["name"] == "test_project"
    assert project["project"]["description"] == "description"


def test_list_projects():
    project_list = galileo.projects.list_projects()

    assert "creation_timestamp" in project_list["projects"][0]
    assert "source_path" in project_list["projects"][0]


def test_upload_file():
    project = galileo.projects.create_project("project", "upload single file")
    project = project["project"]
    response = galileo.projects.upload(project["id"], "funny", "funny")

    assert response == True


galileo.disconnect()
