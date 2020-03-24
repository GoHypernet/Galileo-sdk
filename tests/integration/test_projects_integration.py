from galileo_sdk import GalileoSdk
from galileo_sdk.business.objects.jobs import Job
from galileo_sdk.business.objects.projects import Project

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)


def test_create_project():
    project = galileo.projects.create_project("test_project", "description")

    assert project.name == "test_project"
    assert project.description == "description"


def test_list_projects():
    project_list = galileo.projects.list_projects()

    assert project_list[0].creation_timestamp is not None
    assert project_list[0].source_path is not None


def test_upload_file():
    project = galileo.projects.create_project("project", "upload single file")
    response = galileo.projects.upload(project.project_id, "flatplate")

    assert response == True
    assert project is not None


def test_create_and_run():
    stations_list = galileo.stations.list_stations()
    job = galileo.projects.create_project_and_run_job(
        "sdk_project", "flatplate", stations_list[0].stationid
    )

    assert job is not None
    assert isinstance(job, Job)


def test_create_and_upload():
    project = galileo.projects.create_and_upload_project("sdk_project2", "flatplate")

    assert project is not None
    assert isinstance(project, Project)


galileo.disconnect()
