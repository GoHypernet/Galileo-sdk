from galileo_sdk.compat import mock
from galileo_sdk.business.objects import Job
from galileo_sdk.business.objects.jobs import EJobStatus
from galileo_sdk.business.objects.missions import CreateMissionRequest
from galileo_sdk.business.utils.generate_query_str import generate_query_str
from galileo_sdk.data.repositories.missions import MissionsRepository
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
PROJECT_ID = "mission_id"
STATION_ID = "station_id"
LZ_ID = "lz_id"
CPU_COUNT = "1"
MEMORY_AMOUNT = "1048"
GPU_COUNT = "0"
QUERY_STR = generate_query_str(
    {"ids": ["id"], "names": ["name"], "user_ids": [
        "user_id"], "page": 1, "items": 25, }
)
TIMESTAMP = 1584946381
UNIVERSE_ID = "universe_id"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
settings_repo.get_settings().universe = UNIVERSE_ID
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
projects_repo = MissionsRepository(settings_repo, auth_provider, NAMESPACE)


def mocked_requests_get(*args, **kwargs):
    if args[0] == "{backend}{namespace}/projects?{query}".format(
        backend=BACKEND, namespace=NAMESPACE, query=QUERY_STR
    ):
        return MockResponse(
            {
                "projects": [
                    {
                        "id": "id",
                        "name": "name",
                        "description": "description",
                        "source_storage_id": "source_storage_id",
                        "source_path": "source_path",
                        "destination_storage_id": "destination_storage_id",
                        "destination_path": "destination_path",
                        "user_id": "user_id",
                        "creation_timestamp": "creation_timestamp",
                        "mission_type_id": "mission_type_id",
                        "project_type_id": "project_type_id",
                    }
                ]
            },
            200,
        )

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    if args[0] == "{backend}{namespace}/projects".format(
        backend=BACKEND, namespace=NAMESPACE, query=QUERY_STR
    ):
        return MockResponse(
            {
                "project": {
                    "id": "id",
                    "name": "name",
                    "description": "description",
                    "source_storage_id": "source_storage_id",
                    "source_path": "source_path",
                    "destination_storage_id": "destination_storage_id",
                    "destination_path": "destination_path",
                    "user_id": "user_id",
                    "creation_timestamp": "creation_timestamp",
                    "mission_type_id": "mission_type_id",
                }
            },
            200,
        )
    elif args[0] == "{backend}{namespace}/projects/{project_id}/files".format(
        backend=BACKEND, namespace=NAMESPACE, project_id=PROJECT_ID
    ):
        return MockResponse(True, 200)
    elif args[0] == "{backend}{namespace}/projects/{project_id}/jobs".format(
        backend=BACKEND, namespace=NAMESPACE, project_id=PROJECT_ID
    ):
        return MockResponse(
            {
                "job": {
                    "jobid": "jobid",
                    "receiverid": "receiverid",
                    "mission_id": "mission_id",
                    "time_created": TIMESTAMP,
                    "last_updated": TIMESTAMP,
                    "status": "uploaded",
                    "cpu_count": 1,
                    "gpu_count": 0,
                    "memory_amount": 0,
                    "enable_tunnel": False,
                    "tunnel_port": 8080,
                    "tunnel_url": "https://example.com",
                    "name": "name",
                    "stationid": "stationid",
                    "userid": "userid",
                    "state": "state",
                    "pay_status": "pay_status",
                    "pay_interval": 1,
                    "total_runtime": 10000,
                    "archived": False,
                    "container": "container",
                    "oaid": "oaid",
                    "status_history": [{"timestamp": TIMESTAMP, "status": "uploaded"}],
                }
            },
            200,
        )

    return MockResponse(None, 404)

def mocked_requests_delete(*args, **kwargs):
    if args[0] == "{backend}{namespace}/projects/{id}".format(
        backend=BACKEND, namespace=NAMESPACE, id=PROJECT_ID
    ):
        return MockResponse(True, 200)

    return MockResponse(None, 404)

@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_list_projects(mocked_requests):
    r = projects_repo.list_missions(QUERY_STR)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/projects?{query}".format(
            backend=BACKEND, namespace=NAMESPACE, query=QUERY_STR
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
        },
        json=None,
    )

    assert len(r) == 1
    assert r[0].mission_id == "id"
    assert r[0].user_id == "user_id"
    assert r[0].name == "name"


@mock.patch("galileo_sdk.compat.requests.post", side_effect=mocked_requests_post)
def tests_create_project(mocked_requests):
    r = projects_repo.create_mission(
        CreateMissionRequest(
            name="name",
            description="description",
            mission_type_id="mission_type_id",
            source_storage_id="source_storage_id",
            destination_storage_id="destination_storage_id",
        )
    )

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/projects".format(
            backend=BACKEND, namespace=NAMESPACE),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
        },
        json={
            "name": "name",
            "description": "description",
            "source_storage_id": "source_storage_id",
            "destination_storage_id": "destination_storage_id",
            "mission_type_id": "mission_type_id",
            "public": False,
            "source_path": None,
            "destination_path": None,
        },
    )

    assert r.mission_id == "id"
    assert r.name == "name"
    assert r.description == "description"


@mock.patch("galileo_sdk.compat.requests.post", side_effect=mocked_requests_post)
def tests_upload_file(mocked_requests):
    open("test_upload_file.txt", "wb")
    filename = "test_upload_file.txt"
    file = {"upload_file": open(filename, "rb")}
    r = projects_repo.upload_single_file(PROJECT_ID, file, filename)

    assert r is True


@mock.patch("galileo_sdk.compat.requests.post", side_effect=mocked_requests_post)
def test_run_job_on_station(mocked_requests):
    r = projects_repo.run_job_on_station(
        PROJECT_ID, STATION_ID, CPU_COUNT, MEMORY_AMOUNT, GPU_COUNT)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/projects/{project_id}/jobs".format(
            backend=BACKEND, namespace=NAMESPACE, project_id=PROJECT_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
        },
        json={
            "station_id": STATION_ID,
            "cpu_count": CPU_COUNT,
            "memory_amount": MEMORY_AMOUNT,
            "gpu_count": GPU_COUNT
        }
    )

    assert isinstance(r, Job)


@mock.patch("galileo_sdk.compat.requests.post", side_effect=mocked_requests_post)
def test_run_job_on_machine(mocked_requests):
    r = projects_repo.run_job_on_lz(
        PROJECT_ID, STATION_ID, LZ_ID, CPU_COUNT, MEMORY_AMOUNT, GPU_COUNT)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/projects/{project_id}/jobs".format(
            backend=BACKEND, namespace=NAMESPACE, project_id=PROJECT_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
        },
        json={
            "station_id": STATION_ID,
            "machine_id": LZ_ID,
            "cpu_count": CPU_COUNT,
            "memory_amount": MEMORY_AMOUNT,
            "gpu_count": GPU_COUNT
        }
    )

    assert isinstance(r, Job)
    assert r.mission_id == "mission_id"
    assert r.job_id == "jobid"
    assert len(r.status_history) == 1
    assert r.status_history[0].status == EJobStatus.uploaded

@mock.patch("galileo_sdk.compat.requests.delete", side_effect=mocked_requests_delete)
def test_delete_project(mocked_requests):
    # Call
    r = projects_repo.delete_mission(PROJECT_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/projects/{project_id}".format(
            backend=BACKEND, namespace=NAMESPACE, project_id=PROJECT_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
        },
        json=None,
    )

    # Assert
    assert r is True