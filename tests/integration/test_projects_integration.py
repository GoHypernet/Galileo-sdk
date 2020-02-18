from src import GalileoSdk

# Must set env variables before running tests
CONFIG = "local"

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
    filename_a = "funny/a.png"
    filename_b = "funny/subfunny/b.jpg"
    filename_c = "funny/a.txt"
    filename_d = "funny/subfunny/b.txt"

    print(project["id"])

    file_a = open(filename_a, "rb").read()
    a_r = galileo.projects.upload_single_file(project["id"], file_a, filename_a[6:])

    file_b = open(filename_b, "rb").read()
    b_r = galileo.projects.upload_single_file(project["id"], file_b, filename_b[6:])

    file_c = open(filename_c, "rb").read()
    c_r = galileo.projects.upload_single_file(project["id"], file_c, filename_c[6:])

    file_d = open(filename_d, "rb").read()
    d_r = galileo.projects.upload_single_file(project["id"], file_d, filename_d[6:])

    assert a_r == True
    assert b_r == True
    assert c_r == True
    assert d_r == True
