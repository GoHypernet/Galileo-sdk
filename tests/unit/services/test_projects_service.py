from datetime import datetime
from galileo_sdk.compat import mock

from galileo_sdk.business.objects.jobs import Job
from galileo_sdk.business.objects.projects import Project
from galileo_sdk.business.services.projects import ProjectsService

BACKEND = "http://BACKEND"
NAME = "test_name"
DESCRIPTION = "description"
PROJECT_ID = "project_id"
STATION_ID = "station_id"
MACHINE_ID = "machine_id"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
projects_repo = mock.Mock()
projects_service = ProjectsService(projects_repo)


def test_list_projects():
    projects_repo.list_projects.return_value = [
        Project(
            "project_id",
            "name",
            "description",
            "source_storage_id",
            "source_path",
            "destination_storage_id",
            "destination_path",
            "user_id",
            datetime.now(),
        )
        for _ in range(5)
    ]

    r = projects_service.list_projects()

    assert len(r) == 5
    assert r[0].project_id == "project_id"


def test_create_project():
    projects_repo.create_project.return_value = Project(
        "project_id",
        NAME,
        DESCRIPTION,
        "source_storage_id",
        "source_path",
        "destination_storage_id",
        "destination_path",
        "user_id",
        datetime.now(),
    )

    r = projects_service.create_project(NAME, DESCRIPTION)

    assert r.name == NAME
    assert r.description == DESCRIPTION


def test_upload():
    projects_repo.upload_single_file.return_value = True
    r = projects_service.upload(PROJECT_ID, "flatplate")

    assert r is True


def test_run_job_on_station():
    projects_repo.run_job_on_station.return_value = Job(
        "jobid",
        "receiverid",
        "project_id",
        datetime.now(),
        datetime.now(),
        "status",
        "container",
        "name",
        "stationid",
        "userid",
        "state",
        "oaid",
        "pay_status",
        1,
        1,
        True,
        [],
    )
    r = projects_service.run_job_on_station(PROJECT_ID, STATION_ID)

    assert r.project_id == "project_id"
    assert r.job_id == "jobid"


def test_run_job_on_machine():
    projects_repo.run_job_on_machine.return_value = Job(
        "jobid",
        "receiverid",
        "project_id",
        datetime.now(),
        datetime.now(),
        "status",
        "container",
        "name",
        "stationid",
        "userid",
        "state",
        "oaid",
        "pay_status",
        1,
        1,
        True,
        [],
    )

    r = projects_service.run_job_on_machine(PROJECT_ID, STATION_ID, MACHINE_ID)

    assert r.project_id == "project_id"
    assert r.job_id == "jobid"
