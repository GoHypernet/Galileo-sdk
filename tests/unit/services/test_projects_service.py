from datetime import datetime

from galileo_sdk.compat import mock
from galileo_sdk.business.objects.jobs import Job
from galileo_sdk.business.objects.missions import Mission
from galileo_sdk.business.services.missions import MissionsService

BACKEND = "http://BACKEND"
NAME = "test_name"
DESCRIPTION = "description"
PROJECT_ID = "mission_id"
STATION_ID = "station_id"
MACHINE_ID = "machine_id"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
projects_repo = mock.Mock()
projects_service = MissionsService(projects_repo)


def test_list_projects():
    projects_repo.list_missions.return_value = [
        Mission(
            "mission_id",
            "name",
            "description",
            "source_storage_id",
            "source_path",
            "destination_storage_id",
            "destination_path",
            "user_id",
            datetime.now(),
            "project_type_id",
        ) for _ in range(5)
    ]

    r = projects_service.list_missions()

    assert len(r) == 5
    assert r[0].mission_id == "mission_id"


def test_upload():
    projects_repo.upload_single_file.return_value = True
    r = projects_service.upload(PROJECT_ID, "python_example")

    assert r is True


def test_run_job_on_station():
    projects_repo.run_job_on_station.return_value = Job(
        "jobid",
        "receiverid",
        "mission_id",
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

    assert r.mission_id == "mission_id"
    assert r.job_id == "jobid"


def test_run_job_on_machine():
    projects_repo.run_job_on_lz.return_value = Job(
        "jobid",
        "receiverid",
        "mission_id",
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

    r = projects_service.run_job_on_lz(PROJECT_ID, STATION_ID, MACHINE_ID)

    assert r.mission_id == "mission_id"
    assert r.job_id == "jobid"


def test_delete_project():
    projects_repo.delete_mission.return_value = True

    # Call
    r = projects_service.delete_mission(PROJECT_ID)

    # Assert
    assert r is True