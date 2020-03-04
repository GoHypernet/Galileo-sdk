from unittest import mock

from galileo_sdk.business.utils.generate_query_str import generate_query_str
from galileo_sdk.data.repositories.projects import ProjectsRepository
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
PROJECT_ID = "project_id"
STATION_ID = "station_id"
MACHINE_ID = "machine_id"
QUERY_STR = generate_query_str(
    {
        "ids": ["ids"],
        "names": ["names"],
        "user_ids": ["user_ids"],
        "page": 1,
        "items": 25,
    }
)

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
projects_repo = ProjectsRepository(settings_repo, auth_provider)


def mocked_requests_get(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/projects?{QUERY_STR}":
        return MockResponse({"projects": [{"project": i} for i in range(10)]}, 200)

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/projects":
        return MockResponse(
            {
                "project": {
                    "name": kwargs["json"]["name"],
                    "description": kwargs["json"]["description"],
                }
            },
            200,
        )
    elif args[0] == f"{BACKEND}{NAMESPACE}/projects/{PROJECT_ID}/files":
        return MockResponse(None, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/projects/{PROJECT_ID}/jobs":
        return MockResponse(True, 200)

    return MockResponse(None, 404)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_list_projects(mocked_requests):
    r = projects_repo.list_projects(QUERY_STR)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/projects?{QUERY_STR}",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    assert len(r["projects"]) == 10
    assert r["projects"][9] == {"project": 9}


@mock.patch("requests.post", side_effect=mocked_requests_post)
def tests_create_project(mocked_requests):
    r = projects_repo.create_project("name", "description")
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/projects",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json={"name": "name", "description": "description"},
    )

    assert r["project"]["name"] == "name"
    assert r["project"]["description"] == "description"


@mock.patch("requests.post", side_effect=mocked_requests_post)
def tests_upload_file(mocked_requests):
    open("test_upload_file.txt", "wb")
    filename = "test_upload_file.txt"
    file = {"upload_file": open(filename, "rb")}
    r = projects_repo.upload_single_file(PROJECT_ID, file, filename)

    # Act
    # mocked_requests.assert_called_once_with(
    #     f"{BACKEND}{NAMESPACE}/projects/{PROJECT_ID}/files",
    #     headers={
    #         'Authorization': 'Bearer ACCESS_TOKEN',
    #         'filename': 'test_upload_file.txt',
    #         'Content-Type': 'application/octet-stream'
    #     },
    #     json=None,
    #     data={'upload_file': open(filename, "rb")},
    # )

    assert r.json() is None
    assert r.status_code == 200


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_run_job_on_station(mocked_requests):
    r = projects_repo.run_job_on_station(PROJECT_ID, STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/projects/{PROJECT_ID}/jobs",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json={"station_id": STATION_ID},
    )

    assert r.json() == True
    assert r.status_code == 200


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_run_job_on_machine(mocked_requests):
    r = projects_repo.run_job_on_machine(PROJECT_ID, STATION_ID, MACHINE_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/projects/{PROJECT_ID}/jobs",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json={"station_id": STATION_ID, "machine_id": MACHINE_ID},
    )

    assert r.json() == True
    assert r.status_code == 200
