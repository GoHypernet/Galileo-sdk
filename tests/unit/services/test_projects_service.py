from unittest import mock

from galileo_sdk.business.services.projects import ProjectsService
from galileo_sdk.mock_response import MockResponse

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
    projects_repo.list_projects.return_value = MockResponse(
        {"projects": [{"project": i} for i in range(10)]}, 200
    )

    r = projects_service.list_projects()

    assert len(r["projects"]) == 10
    assert r["projects"][9] == {"project": 9}


def test_create_project():
    projects_repo.create_project.return_value = MockResponse(
        {"project": {"name": NAME, "description": DESCRIPTION,}}, 200
    )

    r = projects_service.create_project(NAME, DESCRIPTION)

    assert r["project"]["name"] == NAME
    assert r["project"]["description"] == DESCRIPTION


def test_upload():
    projects_repo.upload_single_file.return_value = MockResponse(None, 200)
    filename = "test_upload_file.txt"
    dir = "."
    r = projects_service.upload(PROJECT_ID, dir, filename)

    assert r is True


def test_run_job_on_station():
    projects_repo.run_job_on_station.return_value = MockResponse(True, 200)
    r = projects_service.run_job_on_station(PROJECT_ID, STATION_ID)

    assert r == True


def test_run_job_on_machine():
    projects_repo.run_job_on_machine.return_value = MockResponse(True, 200)
    r = projects_service.run_job_on_machine(PROJECT_ID, STATION_ID, MACHINE_ID)

    assert r == True
