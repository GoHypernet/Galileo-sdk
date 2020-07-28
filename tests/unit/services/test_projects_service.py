from datetime import datetime

from galileo_sdk.compat import mock
from galileo_sdk.business.objects.jobs import Job
from galileo_sdk.business.objects.missions import (
    Mission,
    HECRASMission,
    MissionType,
    PythonMission,
)
from galileo_sdk.business.services.missions import MissionsService

BACKEND = "http://BACKEND"
NAME = "test_name"
DESCRIPTION = "description"
PROJECT_ID = "project_id"
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
            "project_id",
            "name",
            "description",
            "source_storage_id",
            "source_path",
            "destination_storage_id",
            "destination_path",
            "user_id",
            datetime.now(),
            "project_type_id",
        )
        for _ in range(5)
    ]

    r = projects_service.list_missions()

    assert len(r) == 5
    assert r[0].mission_id == "project_id"


def test_create_hecras_project():
    projects_service.get_mission_types = mock.MagicMock(
        return_value=[
            MissionType(
                id="hecras_project_type_id",
                name="HECRAS",
                description="description",
                version="version",
            )
        ]
    )
    projects_repo.create_mission.return_value = Mission(
        "project_id",
        NAME,
        DESCRIPTION,
        "source_storage_id",
        "source_path",
        "destination_storage_id",
        "destination_path",
        "user_id",
        datetime.now(),
        "hecras_project_type_id",
    )

    r = projects_service.create_mission(
        HECRASMission(
            name=NAME,
            description=DESCRIPTION,
            version="version",
            source_storage_id="source_storage_id",
            destination_storage_id="destination_storage_id",
            plan="plan",
            input_path="input_path",
            output_path="output_path",
        )
    )

    assert r.name == NAME
    assert r.description == DESCRIPTION
    assert r.project_type_id == "hecras_project_type_id"


def test_create_python_project():
    projects_service.get_mission_types = mock.MagicMock(
        return_value=[
            MissionType(
                id="python_project_type_id",
                name="Python",
                description="description",
                version="version",
            )
        ]
    )
    projects_repo.create_mission.return_value = Mission(
        "project_id",
        NAME,
        DESCRIPTION,
        "source_storage_id",
        "source_path",
        "destination_storage_id",
        "destination_path",
        "user_id",
        datetime.now(),
        "python_project_type_id",
    )

    r = projects_service.create_mission(
        PythonMission(
            name=NAME,
            description=DESCRIPTION,
            version="version",
            source_storage_id="source_storage_id",
            destination_storage_id="destination_storage_id",
            cpu_count=1,
            filename="test.py",
        )
    )

    assert r.name == NAME
    assert r.description == DESCRIPTION
    assert r.project_type_id == "python_project_type_id"


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
    projects_repo.run_job_on_lz.return_value = Job(
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

    r = projects_service.run_job_on_lz(PROJECT_ID, STATION_ID, MACHINE_ID)

    assert r.project_id == "project_id"
    assert r.job_id == "jobid"
